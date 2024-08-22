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

path_dir = r'/mnt/user/media/test/'  # Path without ending slash

clear_console()
logging.info('Start of script.')

for source_name in glob.glob(os.path.join(path_dir, "**", "*.srt"), recursive=True):
    logging.info('-------------------------------------------------------------------------------------------')
    path, fullname = os.path.split(source_name)
    logging.info(fullname)
    basename, ext = os.path.splitext(fullname)
    filename, ext = os.path.splitext(basename)
    
    # Détermination du fichier source (soit .srt soit .en.srt)
    if fullname.endswith(".en.srt"):
        primary_srt = Path(source_name)
        logging.info("Found English subtitles (.en.srt).")
    elif fullname.endswith(".srt") and not fullname.endswith(".en.srt") and not fullname.endswith(".ko.srt") and not fullname.endswith(".yo.srt"):
        primary_srt = Path(source_name)
        logging.info("Found primary subtitles (.srt).")
    else:
        continue  # Si ce n'est ni .srt ni .en.srt, on passe au fichier suivant

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
