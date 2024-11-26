import keyboard
import time
import pygame
from pygame import mixer
from mingus.midi import fluidsynth
from mingus.containers.note import Note 
from sys import exit
from tkinter import filedialog



FPS = 60

# Colors
WHITE       = (255, 255, 255)
WHITE_PRESS = (220, 220, 220)
BLACK       = (0, 0, 0)
BLACK_PRESS = (75, 75, 75)
LIGHT_GRAY  = (150, 150, 150)
KEY_BORDER  = (200, 200, 200)
# Test color
GREEN       = (0, 255, 0)

mixer.init()
pygame.init()
pygame.font.init()

# Constants
SCREEN_WIDTH  = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
SCALE = 0.12

font = pygame.font.match_font("Calibri")
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT*0.93])
screen.fill(LIGHT_GRAY)

digipiano_icon = pygame.image.load("icons\DigiPiano-icon.png")
pygame.display.set_icon(digipiano_icon)
pygame.display.set_caption('DigiPiano')

total_keys = []
clock = pygame.time.Clock()
pygame.display.flip()

# Names for note label printing
white_notes_full = [ "C1", "D1", "E1", "F1", "G1", "A1", "B1",
					 "C2", "D2", "E2", "F2", "G2", "A2", "B2",
					 "C3", "D3", "E3", "F3", "G3", "A3", "B3",
					 "C4", "D4", "E4", "F4", "G4", "A4", "B4",
					 "C5", "D5", "E5", "F5", "G5", "A5", "B5" ]

black_notes_full = [ "C#1", "D#1", " ",  "F#1", "G#1", "A#1", " ",
					 "C#2", "D#2", " ",  "F#2", "G#2", "A#2", " ",
					 "C#3", "D#3", " ",  "F#3", "G#3", "A#3", " ",
					 "C#4", "D#4", " ",  "F#4", "G#4", "A#4", " ",
					 "C#5", "D#5", " ",  "F#5", "G#5", "A#5", " " ]

# Names for keybind label printing
white_order = [ "esc", "f2", "f4", "f5", "f7", "f9", "f11",
			    "1",   "3",  "5",  "6",  "8",  "0",  "=",
				"q",   "e",  "t",  "y",  "i",  "p",  "]",
				"a",   "d",  "g",  "h",  "k",  ";",  "ret",
				"sh",  "x",  "v",  "b",  "m",  ".",  "rsh" ]

black_order = [ "f1", "f3", " ", "f6", "f8", "f10", " ",
			    "2",  "4",  " ", "7",  "9",  "-",  " ",
				"w",  "r",  " ", "u",  "o",  "[",  " ",
				"s",  "f",  " ", "j",  "l",  "'",  " ",
				"z",  "c",  " ", "n",  ",",  "/",  " " ]

# Keybinds for 5 octaves --------------------------------------------------------------------------------------
'''        C        C#    D     D#    E     F     F#    G     G#    A     A#     B '''				# Keybinds for piano
order = [ "esc",   "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11",				# Octave 1
		  "1",     "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "0",  "-",   "=", 				# Octave 2
	      "q",     "w",  "e",  "r",  "t",  "y",  "u",  "i",  "o",  "p",  "[",   "]", 				# Octave 3
	      "a",     "s",  "d",  "f",  "g",  "h",  "j",  "k",  "l",  ";",  "'",   "enter", 			# Octave 4
		  "shift", "z",  "x",  "c",  "v",  "b",  "n",  "m",  ",",  ".",  "/",   "right shift" ]		# Octave 5

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

# Class for printing images to scale for buttons
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int (width * scale), int (height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))


class Callback():
	def __init__(self):
		self.name = ""
		self.event_type = "down"

	def name(self):
		return self.name

	def event_type(self):
		return self.event_type
	
	def set_name(self, name):
		self.name = name

	def set_event_type(self, event_type):
		self.event_type = event_type


# pygame.Rect( x_pos, y_pos, rect_width, rect_height )	==>	anchor point is top left
# Left side menu -------------------------------------------------------------------------------------------------------------
image = pygame.image.load("icons/fpm-icon.png").convert_alpha()
freeplay_button = pygame.Rect(10, 10, 70, 70)
freeplay_icon = Button(10, 10, image, SCALE)

image = pygame.image.load("icons/lm-icon.png").convert_alpha()
learning_button = pygame.Rect(10, 90, 70, 70)
learning_icon = Button(10, 90, image, SCALE)

image = pygame.image.load("icons/keybind-toggle-icon.png").convert_alpha()
keybind_toggle = pygame.Rect(10, 170, 70, 70)
keybind_icon = Button(10, 170, image, SCALE)

image = pygame.image.load("icons/note-toggle-icon.png").convert_alpha()
note_toggle = pygame.Rect(10, 250, 70, 70)
note_icon = Button(10, 250, image, SCALE)

image = pygame.image.load("icons/transpose-up-icon.png").convert_alpha()
transpose_up = pygame.Rect(10, 330, 70, 70)
transpose_up_icon = Button(10, 330, image, SCALE)

image = pygame.image.load("icons/transpose-down-icon.png").convert_alpha()
transpose_down = pygame.Rect(10, 410, 70, 70)
transpose_down_icon = Button(10, 410, image, SCALE)

image = pygame.image.load("icons/info-icon.png").convert_alpha()
info_button = pygame.Rect(10, 490, 70, 70)
info_icon = Button(10, 490, image, SCALE)

image = pygame.image.load("icons/info-tab.png").convert_alpha()
info_tab = Button((SCREEN_WIDTH / 2) - 450, (SCREEN_HEIGHT / 2) - 500, image, 0.8)


# Right side menu ------------------------------------------------------------------------------------------------------------
image = pygame.image.load("icons/file-icon.png").convert_alpha()
file_button = pygame.Rect(SCREEN_WIDTH - 475, 10, 70, 70)
file_icon = Button(SCREEN_WIDTH - 475, 10, image, SCALE)

song_title_button = pygame.Rect(SCREEN_WIDTH - 390, 10, 380, 70)

image = pygame.image.load("icons/play-icon.png").convert_alpha()
play_button = pygame.Rect(SCREEN_WIDTH - 80, 90, 70, 70)
play_icon = Button(SCREEN_WIDTH - 80, 90, image, SCALE)

image = pygame.image.load("icons/pause-icon.png").convert_alpha()
pause_button = pygame.Rect(SCREEN_WIDTH - 80, 170, 70, 70)
pause_icon = Button(SCREEN_WIDTH - 80, 170, image, SCALE)

image = pygame.image.load("icons/volume-up-icon.png").convert_alpha()
inc_vol = pygame.Rect(SCREEN_WIDTH - 80, 250, 70, 70)
inc_vol_icon = Button(SCREEN_WIDTH - 80, 250, image, SCALE)

image = pygame.image.load("icons/volume-down-icon.png").convert_alpha()
low_vol = pygame.Rect(SCREEN_WIDTH - 80, 330, 70, 70)
low_vol_icon = Button(SCREEN_WIDTH - 80, 330, image, SCALE)

#Background Image **need to figure out
image = pygame.image.load("icons/background-icon.png").convert_alpha()
background_button = pygame.Rect(SCREEN_WIDTH - 80, 420, 70, 70)
background_icon = Button(SCREEN_WIDTH - 80, 420, image, SCALE)

# Load Staff Image In - temp
image = pygame.image.load("icons/staffIMG.jpg").convert_alpha()
staff_image = Button(200, 0, image, SCREEN_WIDTH/1920 - 0.1)

image = pygame.image.load("icons/welcome-screen.png").convert_alpha()
welcome_screen = Button((SCREEN_WIDTH / 2) - 400, (SCREEN_HEIGHT / 2) - 250, image, 0.65)


# Testing ---------------------------------------------------------------------------------------------------------------------
image = pygame.image.load("icons/test-icon.png").convert_alpha()
test_keys_button = pygame.Rect(10, SCREEN_HEIGHT - 160, 70, 70)
test_keys_icon = Button(10, SCREEN_HEIGHT - 160, image, SCALE)


class Piano:
	def __init__(self, soundfont_path, transpose=0):
		self.transposition = transpose
		self.soundfont_path = soundfont_path
		self.order = []
		self.pressed_array = []
		self.semitone = 24
		self.channel = 0
		self.volume_value = 128
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

		self.keybind_toggle = False
		self.keybind_toggle_on = 0
		self.note_toggle = False
		self.note_toggle_on = 0
		self.info_tab_on = False
		
		# Initialize and run piano
		self.init()
		self.play_piano()


	def init(self):
		fluidsynth.init(self.soundfont_path)
		keyboard.hook(self.key)

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
				if self.pressed_array[index] is False and self.info_tab_on == False: 
					# Transpose the note index to start at lower octave
					n = Note().from_int(index + self.semitone + self.transposition) 
					fluidsynth.play_Note(n) 					# Play note
					self.pressed_array[index] = True 			# The key is now pressed
					self.press_key(index)						# Update GUI

					print(f"{callback.name} => {n}")
			# UP event
			else: 
				if self.info_tab_on == False:
					self.pressed_array[index] = False 			# Key is released
					self.release_key(index)						# Update GUI

		except Exception as e:
			print(e)


	# Updates GUI, shows on piano when a key is pressed
	def press_key(self, index):
		# White key
		if BLACKS[index % 12] == False:
			i = W_POSITION.index(index)
			total_keys[index] = pygame.draw.rect(screen, WHITE_PRESS, (self.x_offset + i * self.white_key_width + 1, 	# Printing doesn't overlap border
															  		   self.y_offset, 
																	   self.white_key_width - 2, 
																	   self.white_key_height))			
			self.draw_black_keys()
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
		# Black key
		else:
			i = B_POSITION.index(index)
			total_keys[index] = pygame.draw.rect(screen, BLACK, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
																 self.y_offset, 
																 self.black_key_width, 
																 self.black_key_height))
		
		self.draw_white_keys()
		pygame.display.update()


	# Draw white keys on piano
	def draw_white_keys(self):
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

			if self.keybind_toggle_on == 0 or self.note_toggle_on == 0 :
				self.draw_labels(i, False)

		self.draw_black_keys()
		pygame.display.flip()


	# Separate function for drawing black keys - highlight on white keys doesn't cover black keys
	def draw_black_keys(self):
		skip_count = 0

    	# Draw black keys in the appropriate positions
		for i in range(self.total_key_num):
			# Skip keys for E and B
			if skip_count not in [2, 6]:
				pygame.draw.rect(screen, BLACK, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
									 			 self.y_offset, 
												 self.black_key_width, 
												 self.black_key_height))
												 
			if self.keybind_toggle_on == 0 or self.note_toggle_on == 0 :
				self.draw_labels(i, True)

			skip_count += 1

    	    # Reset count on last key in octave
			if skip_count == 7:
				skip_count = 0
			

	# Draw keybind and note labels on piano
	def draw_labels(self, i, black_key):
		if self.keybind_toggle:
			# Label white keys: 7 white keys per octave
			label = pygame.font.Font(font,16).render(white_order[i], True, WHITE)
			label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width // 2, 
												(self.y_offset + self.white_key_height - 210)))
			screen.blit(label, label_rect)

			# Label black keys: 5 black keys per octave
			if black_key == True:
				label = pygame.font.Font(font,16).render(black_order[i], True, BLACK)
				label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width, 
													(self.y_offset + self.black_key_height - 150)))
				screen.blit(label, label_rect)

		if self.note_toggle:
			label = pygame.font.Font(font,16).render(white_notes_full[i], True, WHITE)
			label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width // 2, 
												(self.y_offset + self.white_key_height + 15)))
			screen.blit(label, label_rect)

			# Label black keys: 5 black keys per octave
			if black_key == True:
				label = pygame.font.Font(font,16).render(black_notes_full[i], True, BLACK)
				label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width, 
													(self.y_offset + self.black_key_height + 110)))
				screen.blit(label, label_rect)


	# Initializes piano in Freeplay mode
	def menu_freeplay(self):
		self.total_key_num 	= 35
		self.order    		= order
		self.semitone 		= 24
		self.x_offset 		= 235
		self.y_offset 		= (SCREEN_HEIGHT / 2) - 120
		self.white_key_width  = 45
		self.white_key_height = 200
		self.black_key_width  = 27
		self.black_key_height = 125
		self.pressed_array = [False]*len(self.order)
		self.mode = False

		self.keybind_toggle = False		# Need to reset, otherwise breaks piano speed/visual
		self.keybind_toggle_on = 0
		self.note_toggle = False		
		self.note_toggle_on = 0

		screen.fill(LIGHT_GRAY)
		self.draw_white_keys()

	
	# Initializes piano in Learning mode
	def menu_learning(self):
		self.total_key_num = 35
		self.order    = order
		self.semitone = 24
		self.x_offset = 235
		self.y_offset = SCREEN_HEIGHT - 340
		self.white_key_width  = 45
		self.white_key_height = 200
		self.black_key_width  = 27
		self.black_key_height = 125
		self.pressed_array = [False]*len(self.order)
		self.mode = True

		self.keybind_toggle = False		# Need to reset, otherwise breaks piano speed/visual
		self.keybind_toggle_on = 0
		self.note_toggle = False		
		self.note_toggle_on = 0

		screen.fill(LIGHT_GRAY)
		self.draw_white_keys()
		

	# Draws menu buttons
	def draw_menu(self):
		# Draw left side buttons
		pygame.draw.rect(screen, BLACK, keybind_toggle)
		pygame.draw.rect(screen, BLACK, note_toggle)		
		pygame.draw.rect(screen, BLACK, freeplay_button)
		pygame.draw.rect(screen, BLACK, learning_button)
		pygame.draw.rect(screen, BLACK, transpose_up)
		pygame.draw.rect(screen, BLACK, transpose_down)
		pygame.draw.rect(screen, BLACK, info_button)

		# Draw left side icons
		keybind_icon.draw()
		note_icon.draw()
		freeplay_icon.draw()
		learning_icon.draw()
		transpose_up_icon.draw()
		transpose_down_icon.draw()
		info_icon.draw()

		# Learning mode buttons
		if self.mode == True:
			if self.info_tab_on == False:
				staff_image.draw()

			# Draw right side buttons
			pygame.draw.rect(screen, BLACK, file_button)
			pygame.draw.rect(screen, WHITE, song_title_button)
			pygame.draw.rect(screen, BLACK, play_button)
			pygame.draw.rect(screen, BLACK, pause_button)
			pygame.draw.rect(screen, BLACK, inc_vol)
			pygame.draw.rect(screen, BLACK, low_vol)

			#Background button/icons **testing will clean up later
			pygame.draw.rect(screen, BLACK, background_button)

			
			# Draw right side icons
			file_icon.draw()
			play_icon.draw()
			pause_icon.draw()
			inc_vol_icon.draw()
			low_vol_icon.draw()
			screen.blit(pygame.font.SysFont("Calibri", 20).render(self.song_title, True, BLACK), (SCREEN_WIDTH - 360, 35))

			#Background button/icons **testing will clean up later
			background_icon.draw()

		# Testing buttons
		pygame.draw.rect(screen, BLACK, test_keys_button)
		test_keys_icon.draw()


	# Run pygame and piano interface
	def play_piano(self):
		run = True
		start = False
		song_volume = 2

		welcome_screen.draw()

		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()
					exit()
				
				# 3 states: MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION
				# event.button == 1: left mouse button
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					
					# Check which button is pressed
					# Left side menu --------------------------------------------------------------------------------------------------------
					mouse_pos = event.pos

					if freeplay_button.collidepoint(mouse_pos):
						
						'''
						Draw freeplay mode 
						Stop MIDI music playback when exiting
						Piano and some button functionalities enabled after starting piano
						Reset showing info tab
						'''
						self.menu_freeplay()
						mixer.music.stop()
						start = True
						self.info_tab_on = False

					if learning_button.collidepoint(mouse_pos):
						
						self.menu_learning()
						start = True
						self.info_tab_on = False

					elif keybind_toggle.collidepoint(mouse_pos):
						
						# Button functions after piano is drawn
						if start == True:
							# Toggle
							self.keybind_toggle = (not self.keybind_toggle)
							self.draw_white_keys()

							if self.keybind_toggle == True:
								self.keybind_toggle_on += 1
							else:
								screen.fill(LIGHT_GRAY)
								self.draw_white_keys()
								self.keybind_toggle_on = 0

								if self.note_toggle == True:
									self.draw_white_keys()

					elif note_toggle.collidepoint(mouse_pos):
						
						# Button functions after piano is drawn
						if start == True:
							# Toggle
							self.note_toggle = (not self.note_toggle)
							self.draw_white_keys()

							if self.note_toggle == True:
								self.note_toggle_on += 1
							else:
								screen.fill(LIGHT_GRAY)
								self.draw_white_keys()
								self.note_toggle_on = 0

								if self.keybind_toggle == True:
									self.draw_white_keys()

					elif file_button.collidepoint(mouse_pos):

						# Open file select
						try:
							filename = filedialog.askopenfilename(initialdir="/songs", title="Select file:", filetypes=[("MIDI files", "*.mid")])
							self.test_MIDI(filename)
						except Exception as e:
							print(e)

					elif transpose_up.collidepoint(mouse_pos):
						if start == True:
							self.semitone += 1

					elif transpose_down.collidepoint(mouse_pos):
						if start == True:
							self.semitone -= 1

					elif info_button.collidepoint(mouse_pos):
						self.info_tab_on = (not self.info_tab_on)

						if self.info_tab_on == True:
							info_tab.draw()
						else:
							screen.fill(LIGHT_GRAY)

							if start == False:
								welcome_screen.draw()
							else:
								self.draw_white_keys()

	

					# Right side menu -------------------------------------------------------------------------------------------------------

					elif play_button.collidepoint(mouse_pos):

						try:
							mixer.music.load(self.filename)
							mixer.music.set_volume(song_volume)
							mixer.music.play()
								
						except Exception as e:
							print(e)
							self.song_title = "No MIDI file found!"

					elif pause_button.collidepoint(mouse_pos):

						try:
							mixer.music.pause()
							paused = True

						except Exception as e:
							print(e)

					elif inc_vol.collidepoint(mouse_pos):

						song_volume += 0.2
						mixer.music.set_volume(song_volume)

					elif low_vol.collidepoint(mouse_pos):

						song_volume -= 0.2
						mixer.music.set_volume(song_volume)



					# Test buttons ------------------------------------------------------------------------------------------------------------

					elif test_keys_button.collidepoint(mouse_pos):
						mixer.music.stop()
						start = True
						self.info_tab_on = False
						self.test_keys()
					
					# Custom background image --------------------------------------------------------------- IN PROGRESS

					elif background_button.collidepoint(mouse_pos):

						try:
							
							filenameofbackgroundimage = filedialog.askopenfilename(
								initialdir="/images",
								title="Select file:",
								filetypes=[("JPG or PNG files", "*.jpg;*.png")]
							)

							background_image = pygame.image.load(filenameofbackgroundimage)

							background_image = pygame.transform.scale(background_image, (SCREEN_HEIGHT, SCREEN_WIDTH))

							screen.blit(background_image)

							pygame.display.flip()

						except Exception as e:
							print(f"Error: {e}")

			# Update the screen
			self.draw_menu()
			pygame.display.update()
			clock.tick(FPS)


	# Tests if MIDI file is valid
	def test_MIDI(self, filename):

		# Separate file extension name
		file_type = filename.split("/")
		file_type = file_type[len(file_type) - 1]
		file_type = file_type.split(".")[1]
		
		# Valid MIDI file
		if file_type == "mid":
			self.filename = filename

			# Remove path, extension name, and capitalize
			song_title = filename.split("/")[-1].split(".")[0]
			song_title = song_title.replace("-", " ").replace("_", " ")
			self.song_title = song_title.title()

			print("Valid file type!")
		# Invalid file
		else:
			self.song_title = "Invalid file type!"
			print("Invalid file type!")


	# Tests each piano key for correct audio, press, and release visual
	def test_keys(self):
		callback = Callback()

		self.menu_freeplay()

		for i in order:
			callback.name = i

			callback.event_type = "down"
			self.key(callback)

			pygame.time.wait(100)

			callback.event_type = "up"
			self.key(callback)

