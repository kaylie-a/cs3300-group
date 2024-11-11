import keyboard
import time
from mingus.midi import fluidsynth
from mingus.containers.note import Note 

import pygame
from sys import exit

# Constants
SCREEN_WIDTH     = 1920
SCREEN_HEIGHT    = 1080
FPS = 60

# Colors
WHITE       = (255, 255, 255)
WHITE_PRESS = (200, 200, 200)
BLACK       = (0, 0, 0)
BLACK_PRESS = (75, 75, 75)
LIGHT_GRAY  = (100, 100, 100)
KEY_BORDER  = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(LIGHT_GRAY)
clock = pygame.time.Clock()
total_keys = []

# Keybinds for 5 octaves --------------------------------------------------------------------------------------
'''        C        C#    D     D#    E     F     F#    G     G#    A     A#     B '''				# Keybinds for piano
oct_5 = [ "esc",   "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11",				# Octave 1
		  "1",     "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "-",   "=", 				# Octave 2
	      "q",     "w",  "e",  "r",  "t",  "y",  "u",  "i",  "o",  "p",  "[",   "]", 				# Octave 3
	      "a",     "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l",  ";",  "'",   "enter", 			# Octave 4
		  "shift", "z",  "x",  "c",  "v",  "b",  "n",  "m",  ",",  ".",  "/",   "right shift" ]		# Octave 5
SEMITONE_5      = 24			# Pitch shift
TOTAL_KEYS_5    = 35			# Total white keys
X_OFFSET_5      = 155
Y_OFFSET_FPM_5  = 480			# Center
Y_OFFSET_LM_5   = 860			# Bottom
WHITE_KEY_WIDTH_5  = 45
WHITE_KEY_HEIGHT_5 = 200
BLACK_KEY_WIDTH_5  = 27
BLACK_KEY_HEIGHT_5 = 125

# Hands for 2 octaves -----------------------------------------------------------------------------------------
'''         C    C#   D    D#   E    F    F#   G    G#   A    A#   B '''							# Keybinds for piano
l_hand = [ "q", "2", "w", "3", "e", "r", "5", "t", "6", "y", "7", "u" ]								# Left octave
r_hand = [ "b", "h", "n", "j", "m", ",", "l", ".", ";", "/", "'", "right shift" ]					# Right octave
SEMITONE_2      = 36			# Pitch shift
TOTAL_KEYS_2    = 7				# Total white keys
X_OFFSET_2      = 500
Y_OFFSET_2      = 480			# Center (2 octaves not used for LM, no bottom)
WHITE_KEY_WIDTH_2  = 60
WHITE_KEY_HEIGHT_2 = 250
BLACK_KEY_WIDTH_2  = 37
BLACK_KEY_HEIGHT_2 = 160

# Indicates which are black keys (True) -----------------------------------------------------------------------
blacks = [ False, True, False, True, False, False, True, False, True, False, True, False ]

# White key positions
w_position = [ 0,  2,  4,  5,  7,  9,  11, 
			   12, 14, 16, 17, 19, 21, 23, 
			   24, 26, 28, 29, 31, 33, 35, 
			   36, 38, 40, 41, 43, 45, 47, 
			   48, 50, 52, 53, 55, 57, 59 ]

# Black key positions
b_position = [ 1,  3,  -1, 6,  8,  10, -1, 
			   13, 15, -1, 18, 20, 22, -1, 
			   25, 27, -1, 30, 32, 34, -1, 
			   37, 39, -1, 42, 44, 46, -1, 
			   49, 51, -1, 54, 56, 58, -1 ]

# -------------------------------------------------------------------------------------------------------------

# temp
order = l_hand
semitone = SEMITONE_2
total_key_num = TOTAL_KEYS_2
x_offset = X_OFFSET_2
y_offset_fpm = Y_OFFSET_2
#y_offset_lm = Y_OFFSET_LM_2
white_key_width  = WHITE_KEY_WIDTH_2
white_key_height = WHITE_KEY_HEIGHT_2
black_key_width  = BLACK_KEY_WIDTH_2
black_key_height = BLACK_KEY_HEIGHT_2

button = pygame.Rect(100, 100, 50, 50)


class Piano:
	def __init__(self, soundfont_path, transpose=0, sustain=False):
		self.transposition = transpose
		self.soundfont_path = soundfont_path
		self.order = order
		self.channel = 0
		self.volume_value = 128
		self.pressed_array = [False]*len(order) 	# Store if a key is pressed to prevent key repetition
		self.sustain = sustain

		# Initialize and begin playing piano
		self.init()
		self.draw_piano()
		self.play_piano()
		# draw menu

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
					n = Note().from_int(index + semitone + self.transposition) 
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
		if blacks[index % 12] == False:
			i = w_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, WHITE_PRESS, (x_offset + i * white_key_width, y_offset_fpm, white_key_width, white_key_height))
			self.draw_black_keys()
			pygame.display.update()
		# Black key
		else:
			i = b_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, BLACK_PRESS, (x_offset + i * white_key_width + white_key_width - black_key_width // 2, y_offset_fpm, black_key_width, black_key_height))
			pygame.display.update()

	# Updates GUI, shows on piano when a key is released
	def release_key(self, index):
		# White key
		if blacks[index % 12] == False:
			i = w_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, WHITE, (x_offset + i * white_key_width, y_offset_fpm, white_key_width, white_key_height))
			self.draw_piano()
			pygame.display.update()
		# Black key
		else:
			i = b_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, BLACK, (x_offset + i * white_key_width + white_key_width - black_key_width // 2, y_offset_fpm, black_key_width, black_key_height))
			self.draw_piano()
			pygame.display.update()

	# Draw the keys
	def draw_piano(self):
    	# Draw white keys and border
		for i in range(total_key_num):
			key = pygame.draw.rect(screen, WHITE, (x_offset + i * white_key_width, y_offset_fpm, white_key_width, white_key_height))
			pygame.draw.rect(screen, KEY_BORDER, (x_offset + i * white_key_width, y_offset_fpm, white_key_width, white_key_height), 1)
			total_keys.append(key)

		self.draw_black_keys()
		pygame.display.flip()

	# Separate function for only black keys - highlight on white keys doesn't cover black keys
	def draw_black_keys(self):
		skip_count = 0

    	# Draw black keys in the appropriate positions
		for i in range(total_key_num):
			# Skip keys for E and B
			if skip_count != 2 and skip_count != 6:
				pygame.draw.rect(screen, BLACK, (x_offset + i * white_key_width + white_key_width - black_key_width // 2, y_offset_fpm, black_key_width, black_key_height))
				#total_keys[i] = key

			skip_count += 1

    	    # Reset count on last key in octave
			if skip_count == 7:
				skip_count = 0

	def play_piano(self):
		run = True
		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()
					exit()
				
				# 3 states: MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION
				# event.button == 1: 'left' mouse button
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = event.pos

					if button.collidepoint(mouse_pos):
						screen.fill((75, 75, 75))
						print("Button clicked")

		# Update the screen
		#screen.fill(LIGHT_GRAY)
		self.draw_piano()
		pygame.draw.rect(screen, (255, 0, 0), button)
		pygame.display.update()
		clock.tick(FPS)

	#def draw_menu(self):
	@property
	def volume(self):
		return self.volume_value

	@volume.setter
	def volume(self, value):
		self.volume_value = value
		fluidsynth.main_volume(self.channel, value)

