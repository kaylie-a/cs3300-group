import time
import os
import configparser
import DigiPiano

# Modify path to load fluid synth
app_path = os.getcwd()+r'\fluidsynth'
print(app_path)
if os.environ["PATH"][-1] == '.':
	os.environ["PATH"] = os.environ["PATH"][:-1]
os.environ["PATH"] += ';'+app_path
print(os.environ["PATH"])

config = configparser.ConfigParser()
config.read('settings.ini')

soundfont_path = config['PIANO']['instrument']
transposition = int(config['PIANO']['transposition'])
volume = int(config['PIANO']['volume'])

b1 = DigiPiano.Piano(soundfont_path, transpose=transposition)
b1.volume = volume
while True:
	time.sleep(5)