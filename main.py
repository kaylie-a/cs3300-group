import time
import os
import configparser
import DigiPiano

# Add fluidsynth path to environment variables
app_path = os.getcwd()+r'\fluidsynth'

if os.environ["PATH"][-1] == '.':
	os.environ["PATH"] = os.environ["PATH"][:-1]

os.environ["PATH"] += ';'+app_path

# Set initial settings from file
config = configparser.ConfigParser()
config.read("settings.ini")

soundfont_path = config["PIANO"]["instrument"]
transposition = int(config["PIANO"]["transposition"])
volume = int(config["PIANO"]["volume"])

piano = DigiPiano.Piano(soundfont_path, transpose = transposition)
piano.volume = volume

while True:
	time.sleep(5)