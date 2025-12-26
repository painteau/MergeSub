"""
MergeSub - Automatic Subtitle Merger
Merges Korean subtitles with primary subtitles to create bilingual subtitle files.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from logging.handlers import RotatingFileHandler
from srtmerge import srtmerge


class SubtitleMerger:
    """Handles the merging of subtitle files for video content."""

    def __init__(self, config_path: str = "config.json"):
        """Initialize the SubtitleMerger with configuration.

        Args:
            config_path: Path to the JSON configuration file
        """
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.stats = {"processed": 0, "merged": 0, "skipped": 0, "errors": 0}

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file.

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid
        """
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with config_file.open('r', encoding='utf-8') as f:
            return json.load(f)

    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration.

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        logger.handlers.clear()

        # Formatter
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.config.get('log_file', 'activity.log'),
            mode='a',
            maxBytes=self.config.get('log_max_size', 1000000),
            backupCount=self.config.get('log_backup_count', 1),
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def _validate_media_directory(self) -> Path:
        """Validate and return the media directory path.

        Returns:
            Validated Path object

        Raises:
            ValueError: If directory doesn't exist or is not accessible
        """
        media_dir = Path(self.config['media_directory'])

        if not media_dir.exists():
            raise ValueError(f"Media directory does not exist: {media_dir}")

        if not media_dir.is_dir():
            raise ValueError(f"Media path is not a directory: {media_dir}")

        self.logger.debug(f"Validated media directory: {media_dir}")
        return media_dir

    def _find_video_files(self, media_dir: Path) -> List[Path]:
        """Find all video files in the media directory.

        Args:
            media_dir: Root directory to search

        Returns:
            List of video file paths
        """
        video_files = []
        extensions = self.config.get('video_extensions', ['.mp4', '.mkv', '.avi', '.mov'])

        self.logger.info(f"Searching for video files in: {media_dir}")

        # Single recursive search for all extensions
        for ext in extensions:
            # Search for both lowercase and uppercase extensions
            for variant in [ext, ext.upper()]:
                pattern = f"**/*{variant}"
                found_files = list(media_dir.glob(pattern))
                video_files.extend(found_files)
                self.logger.debug(f"Found {len(found_files)} files matching {pattern}")

        # Remove duplicates (in case of case-insensitive filesystems)
        video_files = list(set(video_files))

        self.logger.info(f"Total video files found: {len(video_files)}")
        return sorted(video_files)

    def _find_primary_subtitle(self, video_path: Path) -> Optional[Path]:
        """Find the primary subtitle file for a video.

        Priority: .srt > .en.srt > .fr.srt

        Args:
            video_path: Path to the video file

        Returns:
            Path to primary subtitle file, or None if not found
        """
        base_name = video_path.stem
        parent_dir = video_path.parent

        excluded_patterns = self.config.get('excluded_subtitle_patterns', [])
        priorities = self.config.get('subtitle_priorities', ['.srt', '.en.srt', '.fr.srt'])

        for priority_ext in priorities:
            subtitle_path = parent_dir / f"{base_name}{priority_ext}"

            # For generic .srt, ensure it's not a language-specific subtitle
            if priority_ext == '.srt':
                # Check if the base name already ends with a language code
                is_excluded = any(
                    base_name.endswith(pattern.replace('.srt', ''))
                    for pattern in excluded_patterns
                )
                if is_excluded:
                    continue

            if subtitle_path.exists() and subtitle_path.is_file():
                self.logger.debug(f"Found primary subtitle: {subtitle_path.name}")
                return subtitle_path

        return None

    def _merge_subtitles(self, korean_sub: Path, primary_sub: Path, output_sub: Path) -> bool:
        """Merge two subtitle files into one.

        Args:
            korean_sub: Path to Korean subtitle file
            primary_sub: Path to primary subtitle file
            output_sub: Path for output merged subtitle

        Returns:
            True if merge was successful, False otherwise
        """
        try:
            self.logger.info(f"Merging: {primary_sub.name} + {korean_sub.name} → {output_sub.name}")
            srtmerge([str(korean_sub), str(primary_sub)], str(output_sub))
            self.logger.info(f"✓ Successfully created: {output_sub.name}")
            return True
        except Exception as e:
            self.logger.error(f"✗ Merge failed for {output_sub.name}: {e}")
            return False

    def _process_video_file(self, video_path: Path) -> None:
        """Process a single video file for subtitle merging.

        Args:
            video_path: Path to the video file
        """
        self.logger.info("=" * 90)
        self.logger.info(f"Processing: {video_path.name}")
        self.stats["processed"] += 1

        # Find primary subtitle
        primary_subtitle = self._find_primary_subtitle(video_path)

        if not primary_subtitle:
            self.logger.info("No suitable primary subtitles found, skipping.")
            self.stats["skipped"] += 1
            return

        self.logger.info(f"Primary subtitle: {primary_subtitle.name}")

        # Check for Korean subtitle
        base_name = video_path.stem
        parent_dir = video_path.parent

        korean_ext = self.config.get('korean_subtitle_extension', '.ko.srt')
        output_ext = self.config.get('output_subtitle_extension', '.yo.srt')

        korean_subtitle = parent_dir / f"{base_name}{korean_ext}"
        output_subtitle = parent_dir / f"{base_name}{output_ext}"

        if not korean_subtitle.exists():
            self.logger.info("No Korean subtitles found for this video.")
            self.stats["skipped"] += 1
            return

        self.logger.info(f"Korean subtitle: {korean_subtitle.name}")

        # Check if output already exists
        if output_subtitle.exists():
            self.logger.info("Output subtitle already exists, skipping merge.")
            self.stats["skipped"] += 1
            return

        # Perform merge
        if self._merge_subtitles(korean_subtitle, primary_subtitle, output_subtitle):
            self.stats["merged"] += 1
        else:
            self.stats["errors"] += 1

    def run(self) -> None:
        """Main execution method to process all video files."""
        self.logger.info("🚀 MergeSub - Starting subtitle merger")

        try:
            # Validate media directory
            media_dir = self._validate_media_directory()

            # Find all video files
            video_files = self._find_video_files(media_dir)

            if not video_files:
                self.logger.warning("No video files found in the specified directory.")
                return

            # Process each video file
            for video_file in video_files:
                try:
                    self._process_video_file(video_file)
                except Exception as e:
                    self.logger.error(f"Error processing {video_file.name}: {e}")
                    self.stats["errors"] += 1

            # Print summary
            self._print_summary()

        except Exception as e:
            self.logger.critical(f"Fatal error: {e}")
            sys.exit(1)

        self.logger.info("✓ MergeSub completed")

    def _print_summary(self) -> None:
        """Print execution summary statistics."""
        self.logger.info("=" * 90)
        self.logger.info("📊 SUMMARY")
        self.logger.info(f"  Videos processed: {self.stats['processed']}")
        self.logger.info(f"  Subtitles merged: {self.stats['merged']}")
        self.logger.info(f"  Files skipped: {self.stats['skipped']}")
        self.logger.info(f"  Errors: {self.stats['errors']}")
        self.logger.info("=" * 90)


def main():
    """Entry point for the script."""
    try:
        merger = SubtitleMerger()
        merger.run()
    except KeyboardInterrupt:
        print("\n\n⚠ Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
