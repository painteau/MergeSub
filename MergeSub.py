from srtmerge import srtmerge
import os
import glob
from pathlib import Path
import logging
import time
from logging.handlers import RotatingFileHandler

# LOGGER SETUP

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
 # création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

# VARIABLES

clear = lambda: os.system('clear')
path_dir = r'/mnt/user/mount_rclone/GdriveMedia/movies' # without ending slash please



clear()
logging.info('Start of script.')
for source_name in glob.glob(path_dir + "/**/*.fr.srt" ,  recursive = True):
	logging.info('-------------------------------------------------------------------------------------------')
	path, fullname = os.path.split(source_name)
	logging.info('' + fullname)
	basename, ext = os.path.splitext(fullname)
	filename, ext = os.path.splitext(basename)
	ko_file = Path(f"{path}/{filename}.ko.srt")
	yo_file = Path(f"{path}/{filename}.yo.srt")
	if ko_file.is_file():
		logging.info('Korean subtitles exists for this file.')
		if yo_file.is_file():
			logging.info('Yoruba subtitles already exists, skipping file')
		else:
			logging.info("Yoruba subtitles doesn't exist.... yet !")
			logging.info('Trying to merge FR and KO files...')
			try:
				srtmerge([f"{path}/{filename}.ko.srt", f"{path}/{filename}.fr.srt"], f"{path}/{filename}.yo.srt")
				logging.info("Merging to " + f"{path}/{filename}.yo.srt" + " was succesfull !")
				break
			except:
				logging.warning('Oops ! Merging was unsuccesfull for ' + f'{path}/{filename}' + ' ! Check the subtitles file for unsupported lines !')	
	else:
		logging.info("Unfortunately, we could not find Korean subtitles for this file :( !")

logging.info('End of script.')
time.sleep(3) 