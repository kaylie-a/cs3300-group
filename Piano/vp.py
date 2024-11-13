import keyboard
import time
import pygame
from pygame import mixer
from mingus.midi import fluidsynth
from mingus.containers.note import Note 
from sys import exit
from tkinter import filedialog

# Constants
SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Colors
WHITE       = (255, 255, 255)
WHITE_PRESS = (200, 200, 200)
BLACK       = (0, 0, 0)
BLACK_PRESS = (75, 75, 75)
LIGHT_GRAY  = (100, 100, 100)
KEY_BORDER  = (200, 200, 200)

pygame.init()
mixer.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
digipiano_icon = pygame.image.load("icons\DigiPianoTestIcon.png")
pygame.display.set_icon(digipiano_icon)
pygame.display.set_caption('DigiPiano')
screen.fill(LIGHT_GRAY)
clock = pygame.time.Clock()
total_keys = []
pygame.display.flip()

# Keybinds for 5 octaves --------------------------------------------------------------------------------------
'''        C        C#    D     D#    E     F     F#    G     G#    A     A#     B '''				# Keybinds for piano
OCT_5 = [ "esc",   "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11",				# Octave 1
		  "1",     "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "-",   "=", 				# Octave 2
	      "q",     "w",  "e",  "r",  "t",  "y",  "u",  "i",  "o",  "p",  "[",   "]", 				# Octave 3
	      "a",     "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l",  ";",  "'",   "enter", 			# Octave 4
		  "shift", "z",  "x",  "c",  "v",  "b",  "n",  "m",  ",",  ".",  "/",   "right shift" ]		# Octave 5
'''TOTAL_KEYS_5    = 35			# Total white keys
SEMITONE_5      = 24			# Pitch shift
X_OFFSET_5      = 155
Y_OFFSET_FPM_5  = 480			# Center
Y_OFFSET_LM_5   = 860			# Bottom
WHITE_KEY_WIDTH_5  = 45
WHITE_KEY_HEIGHT_5 = 200
BLACK_KEY_WIDTH_5  = 27
BLACK_KEY_HEIGHT_5 = 125'''

# Hands for 2 octaves -----------------------------------------------------------------------------------------
'''         C    C#   D    D#   E    F    F#   G    G#   A    A#   B '''							# Keybinds for piano
L_HAND = [ "q", "2", "w", "3", "e", "r", "5", "t", "6", "y", "7", "u" ]								# Left octave
R_HAND = [ "b", "h", "n", "j", "m", ",", "l", ".", ";", "/", "'", "right shift" ]					# Right octave
TOTAL_KEYS_2    = 7				# Total white keys
SEMITONE_2      = 36			# Pitch shift
X_OFFSET_2      = 500
Y_OFFSET_2      = 480			# Center (2 octaves not used for LM, no bottom)
WHITE_KEY_WIDTH_2  = 60
WHITE_KEY_HEIGHT_2 = 250
BLACK_KEY_WIDTH_2  = 37
BLACK_KEY_HEIGHT_2 = 160

# Indicates which are black keys (True) -----------------------------------------------------------------------
BLACKS = [ False, True, False, True, False, False, True, False, True, False, True, False ]

# White key positions - up to 5 octaves
W_POSITION = [ 0,  2,  4,  5,  7,  9,  11, 
			   12, 14, 16, 17, 19, 21, 23, 
			   24, 26, 28, 29, 31, 33, 35, 
			   36, 38, 40, 41, 43, 45, 47, 
			   48, 50, 52, 53, 55, 57, 59 ]

# Black key positions
# -1: no black keys on E and B
B_POSITION = [ 1,  3,  -1, 6,  8,  10, -1, 
			   13, 15, -1, 18, 20, 22, -1, 
			   25, 27, -1, 30, 32, 34, -1, 
			   37, 39, -1, 42, 44, 46, -1, 
			   49, 51, -1, 54, 56, 58, -1 ]

# -------------------------------------------------------------------------------------------------------------

# pygame.Rect( x_pos, y_pos, rect_width, rect_height )	==>	anchor point is top left
# Left side menu
freeplay_button = pygame.Rect(10, 10, 50, 50)
learning_button = pygame.Rect(10, 70, 50, 50)
note_label_toggle = pygame.Rect(10, 130, 50, 50)
keybind_toggle = pygame.Rect(10, 190, 50, 50)
transpose_up = pygame.Rect(10, 250, 50, 50)
transpose_down = pygame.Rect(10, 310, 50, 50)
inc_piano_vol = pygame.Rect(10, 370, 50, 50)
low_piano_vol = pygame.Rect(10, 430, 50, 50)
info_button = pygame.Rect(10, 490, 50, 50)

# Right side menu
file_button = pygame.Rect(1490, 10, 50, 50)
song_title_button = pygame.Rect(1550, 10, 360, 50)
play_button = pygame.Rect(1860, 70, 50, 50)
pause_button = pygame.Rect(1860, 130, 50, 50)
slow_button = pygame.Rect(1860, 190, 50, 50)
fast_button = pygame.Rect(1860, 250, 50, 50)
metronome_button = pygame.Rect(1860, 310, 50, 50)
inc_song_vol = pygame.Rect(1860, 370, 50, 50)
low_song_vol = pygame.Rect(1860, 430, 50, 50)

welcome_screen = pygame.Rect(660, 390, 600, 300)

class Piano:
	def __init__(self, soundfont_path, transpose=0):
		self.transposition = transpose
		self.soundfont_path = soundfont_path
		self.order = []
		self.pressed_array = []
		self.semitone = 24
		self.channel = 0
		self.volume_value = 128
		self.sustain = False
		self.mode = False			# Freeplay Mode: False, Learning Mode: True

		self.total_key_num = 0
		self.x_offset      = 0
		self.y_offset      = 0
		self.white_key_width  = 0
		self.white_key_height = 0
		self.black_key_width  = 0
		self.black_key_height = 0

		self.filename = " "
		self.song_title = "Select MIDI file..."

		# Initialize and run piano
		self.init()
		self.play_piano()

	def init(self):
		fluidsynth.init(self.soundfont_path)
		keyboard.hook(self.key)

		if self.sustain:
			fluidsynth.control_change(0, 64, 127)
			fluidsynth.control_change(0, 91, 127)
			print("Sustain: ON")
		else:
			fluidsynth.control_change(0, 64, 0)
			fluidsynth.control_change(0, 91, 0)
			print("Sustain: OFF")

		# Startup sound: Plays note in each octave
		for octave in range(9):
			fluidsynth.play_Note(Note("C", octave))
			time.sleep(0.1)

	# Piano reacts on keyboard press based on the order of keybinds
	def key(self, callback):
		# Keyboard event DOWN: play note and store that the key is pressed
		# Keyboard event UP:   Set the key to released
		try:
			index = self.order.index(callback.name)
			# DOWN event
			
			if callback.event_type == 'down': 
				# If key is not pressed
				if self.pressed_array[index] is False: 
					# Transpose the note index to start at lower octave
					n = Note().from_int(index + self.semitone + self.transposition) 
					fluidsynth.play_Note(n) 				# Play note
					self.pressed_array[index] = True 		# The key is now pressed
					self.press_key(index)					# Update GUI
					print(f"{callback.name} => {n}")
			# UP event
			else: 
				self.pressed_array[index] = False 			# Key is released
				self.release_key(index)						# Update GUI

		except Exception as e:
			print(e)

	# Updates GUI, shows on piano when a key is pressed
	def press_key(self, index):
		# White key
		if BLACKS[index % 12] == False:
			i = W_POSITION.index(index)
			total_keys[index] = pygame.draw.rect(screen, WHITE_PRESS, (self.x_offset + i * self.white_key_width, 
															  		   self.y_offset, 
																	   self.white_key_width, 
																	   self.white_key_height))
			self.draw_black_keys()
			pygame.display.update()
		# Black key
		else:
			i = B_POSITION.index(index)
			total_keys[index] = pygame.draw.rect(screen, BLACK_PRESS, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
															  		   self.y_offset, 
																	   self.black_key_width, 
																	   self.black_key_height))
			pygame.display.update()

	# Updates GUI, shows on piano when a key is released
	def release_key(self, index):
		# White key
		if BLACKS[index % 12] == False:
			i = W_POSITION.index(index)
			total_keys[index] = pygame.draw.rect(screen, WHITE, (self.x_offset + i * self.white_key_width, 
																 self.y_offset, 
																 self.white_key_width, 
																 self.white_key_height))
			self.draw_piano()
			pygame.display.update()
		# Black key
		else:
			i = B_POSITION.index(index)
			total_keys[index] = pygame.draw.rect(screen, BLACK, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
																 self.y_offset, 
																 self.black_key_width, 
																 self.black_key_height))
			self.draw_piano()
			pygame.display.update()

	# Draw the keys
	def draw_piano(self):
    	# Draw white keys and border
		for i in range(self.total_key_num):
			key = pygame.draw.rect(screen, WHITE, (self.x_offset + i * self.white_key_width, 
										  		   self.y_offset, 
												   self.white_key_width, 
												   self.white_key_height))
			pygame.draw.rect(screen, KEY_BORDER, (self.x_offset + i * self.white_key_width, 
										 		  self.y_offset, 
												  self.white_key_width, 
												  self.white_key_height), 1)
			total_keys.append(key)

		self.draw_black_keys()
		pygame.display.flip()

	# Separate function for only black keys - highlight on white keys doesn't cover black keys
	def draw_black_keys(self):
		skip_count = 0

    	# Draw black keys in the appropriate positions
		for i in range(self.total_key_num):
			# Skip keys for E and B
			if skip_count != 2 and skip_count != 6:
				pygame.draw.rect(screen, BLACK, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
									 			 self.y_offset, 
												 self.black_key_width, 
												 self.black_key_height))

			skip_count += 1

    	    # Reset count on last key in octave
			if skip_count == 7:
				skip_count = 0

	def menu_freeplay(self):		# implement 2 octave and 5 octave
		self.total_key_num = 35
		self.order    = OCT_5
		self.semitone = 24
		self.x_offset = 155
		self.y_offset = 480
		self.white_key_width  = 45
		self.white_key_height = 200
		self.black_key_width  = 27
		self.black_key_height = 125
		self.pressed_array = [False]*len(self.order)
		self.mode = False
		screen.fill(LIGHT_GRAY)
		self.draw_piano()

	def menu_learning(self):
		self.total_key_num = 35
		self.order    = OCT_5
		self.semitone = 24
		self.x_offset = 155
		self.y_offset = 860
		self.white_key_width  = 45
		self.white_key_height = 200
		self.black_key_width  = 27
		self.black_key_height = 125
		self.pressed_array = [False]*len(self.order)
		self.mode = True
		screen.fill(LIGHT_GRAY)
		self.draw_piano()

	# Draws menu buttons
	def draw_menu(self):
		pygame.draw.rect(screen, (238, 137, 147), note_label_toggle)
		pygame.draw.rect(screen, (220, 87, 154), keybind_toggle)
		pygame.draw.rect(screen, (145, 0, 255), freeplay_button)
		pygame.draw.rect(screen, (240, 137, 247), learning_button)
		pygame.draw.rect(screen, (106, 185, 114), transpose_up)
		pygame.draw.rect(screen, (106, 185, 114), transpose_down)
		pygame.draw.rect(screen, (131, 177, 191), inc_piano_vol)
		pygame.draw.rect(screen, (131, 177, 191), low_piano_vol)
		pygame.draw.rect(screen, (124, 47, 129), info_button)

		if self.mode == True:
			pygame.draw.rect(screen, (255, 255, 255), file_button)
			pygame.draw.rect(screen, (255, 255, 255), song_title_button)
			pygame.draw.rect(screen, (255, 255, 0), play_button)
			pygame.draw.rect(screen, (255, 111, 0), pause_button)
			pygame.draw.rect(screen, (0, 0, 255), slow_button)
			pygame.draw.rect(screen, (255, 0, 0), fast_button)
			pygame.draw.rect(screen, (0, 255, 255), metronome_button)
			pygame.draw.rect(screen, (131, 145, 191), inc_song_vol)
			pygame.draw.rect(screen, (131, 145, 191), low_song_vol)
			screen.blit(pygame.font.SysFont("Calibri", 20).render(self.song_title, True, BLACK), (1560, 25))
		# implement button text/icon images

	# Run pygame and piano interface
	def play_piano(self):
		run = True
		start = False
		paused = False
		song_volume = 2

		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()
					exit()
				
				# 3 states: MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION
				# event.button == 1: left mouse button
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = event.pos

					# Left side menu --------------------------------------------------------------------------------------------------------

					# Check which button is pressed
					if note_label_toggle.collidepoint(mouse_pos):
						pass

					elif keybind_toggle.collidepoint(mouse_pos):
						pass
					
					elif freeplay_button.collidepoint(mouse_pos):
						self.menu_freeplay()
						start = True
						mixer.music.stop()

					elif learning_button.collidepoint(mouse_pos):
						self.menu_learning()
						start = True

					elif file_button.collidepoint(mouse_pos):
						# Open file select
						self.filename = filedialog.askopenfilename(initialdir="C:/", title="Select file:")
						
						# Remove path, extension name, and capitalize
						self.song_title = self.filename.split("/")[-1]
						self.song_title = self.song_title.split(".")[0]
						self.song_title = self.song_title.replace("-", " ").replace("_", " ")
						self.song_title = self.song_title.title()

					elif transpose_up.collidepoint(mouse_pos):
						self.semitone += 1

					elif transpose_down.collidepoint(mouse_pos):
						self.semitone -= 1

					elif inc_piano_vol.collidepoint(mouse_pos):
						pass

					elif low_piano_vol.collidepoint(mouse_pos):
						pass

					elif info_button.collidepoint(mouse_pos):
						pass

					# Right side menu -------------------------------------------------------------------------------------------------------

					elif play_button.collidepoint(mouse_pos):
						try:
							mixer.music.load(self.filename)
							mixer.music.set_volume(song_volume)
							if paused == False:
								mixer.music.play()
							else:
								print("unpause")				# TODO
								mixer.music.unpause()
						except Exception as e:
							print(e)
							self.song_title = "No MIDI file found!"
					elif pause_button.collidepoint(mouse_pos):
						try:
							mixer.music.pause()
							paused = True	
						except Exception as e:
							print(e)
					elif slow_button.collidepoint(mouse_pos):
						pass
					elif fast_button.collidepoint(mouse_pos):
						pass
					elif metronome_button.collidepoint(mouse_pos):
						pass
					elif inc_song_vol.collidepoint(mouse_pos):
						song_volume += 0.2
						mixer.music.set_volume(song_volume)
					elif low_song_vol.collidepoint(mouse_pos):
						song_volume -= 0.2
						mixer.music.set_volume(song_volume)

			if start == False:
				pygame.draw.rect(screen, WHITE, welcome_screen)
			
			# Update the screen
			self.draw_menu()
			pygame.display.update()
			clock.tick(FPS)
	
	@property
	def volume(self):
		return self.volume_value

	@volume.setter
	def volume(self, value):
		self.volume_value = value
		fluidsynth.main_volume(self.channel, value)

