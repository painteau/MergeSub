import os
import glob
from pathlib import Path
import logging
import time
from logging.handlers import RotatingFileHandler
from srtmerge import srtmerge

# LOGGER SETUP

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# VARIABLES

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

path_dir = r'\\192.168.1.100\media\Movies'  # Path without ending slash

clear_console()
logging.info('Start of script.')

# Extensions vidéo à rechercher
video_extensions = ('*.mp4', '*.mkv', '*.avi', '*.mov')

# Recherche de tous les fichiers vidéo dans le répertoire spécifié
for extension in video_extensions:
    for video_file in glob.glob(os.path.join(path_dir, "**", extension), recursive=True):
        logging.info('-------------------------------------------------------------------------------------------')
        path, fullname = os.path.split(video_file)
        logging.info(f'Processing video file: {fullname}')
        basename, ext = os.path.splitext(fullname)
        filename, ext = os.path.splitext(basename)
        
        # Priorité de sélection : .srt > .en.srt > .fr.srt
        generic_file = Path(f"{path}/{filename}.srt")
        en_file = Path(f"{path}/{filename}.en.srt")
        fr_file = Path(f"{path}/{filename}.fr.srt")
        
        if generic_file.is_file() and not fullname.endswith(".en.srt") and not fullname.endswith(".fr.srt") and not fullname.endswith(".ko.srt") and not fullname.endswith(".yo.srt"):
            primary_srt = generic_file
            logging.info("Found primary subtitles (.srt).")
        elif en_file.is_file():
            primary_srt = en_file
            logging.info("Found English subtitles (.en.srt).")
        elif fr_file.is_file():
            primary_srt = fr_file
            logging.info("Found French subtitles (.fr.srt).")
        else:
            logging.info("No suitable subtitles found for this video, skipping.")
            continue  # Aucun fichier de sous-titres approprié trouvé, on passe à la vidéo suivante

        ko_file = Path(f"{path}/{filename}.ko.srt")
        yo_file = Path(f"{path}/{filename}.yo.srt")
        
        if ko_file.is_file():
            logging.info('Korean subtitles exist for this file.')
            
            if yo_file.is_file():
                logging.info('Yoruba subtitles already exist, skipping file.')
            else:
                logging.info("Yoruba subtitles do not exist... yet!")
                logging.info('Attempting to merge primary and Korean subtitles...')
                
                try:
                    srtmerge([str(ko_file), str(primary_srt)], str(yo_file))
                    logging.info(f"Merging to {yo_file} was successful!")
                except Exception as e:
                    logging.warning(f"Oops! Merging was unsuccessful for {filename}! Error: {e}")
        else:
            logging.info("Unfortunately, we could not find Korean subtitles for this file :( !")

logging.info('End of script.')
time.sleep(3)
