import keyboard
import time
from mingus.midi import fluidsynth
from mingus.containers.note import Note 

import pygame
from sys import exit

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
X_OFFSET = 100
Y_OFFSET = 480
WHITE_KEY_WIDTH = 35
WHITE_KEY_HEIGHT = 180
BLACK_KEY_WIDTH = 22
BLACK_KEY_HEIGHT = 120
TOTAL_KEYS = 84
TOTAL_WHITE_BLACK = 49
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
KEY_BORDER = (200, 200, 200)

# temp colors
GREEN = (150, 225, 125)

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(GRAY)
clock = pygame.time.Clock()

total_keys = []
white_keys = []

# Keybinds for 7 octaves
order = [ "`", "~", "1", "!", "2", "3", "#",  "4", "$", "5",  "%", "6",					# Ocatve 1
		  "7", "&", "8", "*", "9", "0", ")",  "-", "_", "=",  "+", "backspace",			# Ocatve 2
		  "q", "Q", "w", "W", "e", "r", "R",  "t", "T", "y",  "Y", "u",					# Ocatve 3
		  "i", "I", "o", "O", "p", "[", "{",  "]", "}", "\\", "|", "enter",				# Ocatve 4
		  "a", "A", "s", "S", "d", "f", "F",  "g", "G", "h",  "H", "j",					# Ocatve 5
		  "k", "K", "l", "L", ";", "'", "\"", ",", "<", ".",  ">", "/", 				# Ocatve 6
		  "z", "Z", "x", "X", "c", "v", "V",  "b", "B", "n",  "N", "m"	]				# Ocatve 7		

# Indicates which are black keys (True)
blacks = [ False, True, False, True, False, False, True, False, True, False, True, False, 
		   False, True, False, True, False, False, True, False, True, False, True, False, 
		   False, True, False, True, False, False, True, False, True, False, True, False, 
		   False, True, False, True, False, False, True, False, True, False, True, False, 
		   False, True, False, True, False, False, True, False, True, False, True, False, 
		   False, True, False, True, False, False, True, False, True, False, True, False, 
		   False, True, False, True, False, False, True, False, True, False, True, False, ]

w_position = [ 0,  2,  4,  5,  7,  9,  11, 
			   12, 14, 16, 17, 19, 21, 23, 
			   24, 26, 28, 29, 31, 33, 35, 
			   36, 38, 40, 41, 43, 45, 47, 
			   48, 50, 52, 53, 55, 57, 59, 
			   60, 62, 64, 65, 67, 69, 71, 
			   72, 74, 76, 77, 79, 81, 83 ]

b_position = [ 1,  3,  -1, 6,  8,  10, -1, 
			   13, 15, -1, 18, 20, 22, -1, 
			   25, 27, -1, 30, 32, 34, -1, 
			   37, 39, -1, 42, 44, 46, -1, 
			   49, 51, -1, 54, 56, 58, -1, 
			   61, 63, -1, 66, 68, 70, -1, 
			   73, 75, -1, 78, 80, 82, -1 ]

class Piano:
	def __init__(self, soundfont_path, transpose=0, sustain=False):
		self.transposition = transpose
		self.soundfont_path = soundfont_path
		self.order = order
		self.channel = 0
		self.volume_value = 128
		self.pressed_array = [False]*len(order) 	# Store if a key is pressed to prevent key repetition
		self.sustain = sustain

		self.init()
		self.draw_piano()
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

	def key(self, callback):
		# Keyboard event DOWN: play note and store that the key is pressed
		# Keyboard event UP:   Set the key to released
		try:
			index = self.order.index(callback.name)
			# DOWN event
			if callback.event_type == 'down': 
				# If key is not pressed
				if self.pressed_array[index] is False: 
					# Transpose the note index by 12 semitones - starts at lower octave
					n = Note().from_int(index + 12 + self.transposition) 
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

	def press_key(self, index):
		# White key
		if blacks[index] == False:
			i = w_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, GREEN, (X_OFFSET + i * WHITE_KEY_WIDTH, Y_OFFSET, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT))
			self.draw_black_keys()
			pygame.display.update()
		# Black key
		else:
			i = b_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, GREEN, (X_OFFSET + i * WHITE_KEY_WIDTH + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2, Y_OFFSET, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT))
			pygame.display.update()

	def release_key(self, index):
		# White key
		if blacks[index] == False:
			i = w_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, WHITE, (X_OFFSET + i * WHITE_KEY_WIDTH, Y_OFFSET, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT))
			self.draw_piano()
			pygame.display.update()
		# Black key
		else:
			i = b_position.index(index)
			total_keys[index] = pygame.draw.rect(screen, BLACK, (X_OFFSET + i * WHITE_KEY_WIDTH + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2, Y_OFFSET, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT))
			self.draw_piano()
			pygame.display.update()

	# Draw the keys
	def draw_piano(self):
    	# Draw white keys and border
		for i in range(TOTAL_WHITE_BLACK):
			key = pygame.draw.rect(screen, WHITE, (X_OFFSET + i * WHITE_KEY_WIDTH, Y_OFFSET, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT))
			pygame.draw.rect(screen, KEY_BORDER, (X_OFFSET + i * WHITE_KEY_WIDTH, Y_OFFSET, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT), 1)
			
			if blacks[i] == False:
				white_keys.append(i)
			total_keys.append(key)

		self.draw_black_keys()
		pygame.display.flip()

	# Separate function for only black keys - highlight on white keys doesn't cover black keys
	def draw_black_keys(self):
		skip_count = 0

    	# Draw black keys in the appropriate positions
		for i in range(TOTAL_WHITE_BLACK):
			# Skip keys for E and B
			if skip_count != 2 and skip_count != 6:
				pygame.draw.rect(screen, BLACK, (X_OFFSET + i * WHITE_KEY_WIDTH + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2, Y_OFFSET, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT))
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

		# Update the screen
		self.draw_piano()
		pygame.display.update()
		clock.tick(FPS)

	@property
	def volume(self):
		return self.volume_value

	@volume.setter
	def volume(self, value):
		self.volume_value = value
		fluidsynth.main_volume(self.channel, value)

