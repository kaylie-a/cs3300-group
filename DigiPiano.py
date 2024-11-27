import keyboard
import time
import pygame
from pygame import mixer
from mingus.midi import fluidsynth
from mingus.containers.note import Note 
from sys import exit
from tkinter import filedialog

import const
import buttons

mixer.init()
pygame.init()
pygame.font.init()

SCREEN_WIDTH  = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

font = pygame.font.match_font("Calibri")
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT*0.95])
screen.fill(const.LIGHT_GRAY)

digipiano_icon = pygame.image.load("icons\DigiPiano-icon.png")
pygame.display.set_icon(digipiano_icon)
pygame.display.set_caption('DigiPiano')

clock = pygame.time.Clock()
pygame.display.flip()


# -------------------------------------------------------------------------------------------------------------


class Piano:
	def __init__(self, soundfont_path, transpose):
		self.transposition = transpose
		self.soundfont_path = soundfont_path
		self.order = []
		self.pressed_array = []
		self.semitone = 24
		self.channel = 0
		self.volume_value = 128
		self.mode = False			# Freeplay Mode: False, Learning Mode: True
		self.start = False

		self.total_key_num = 0
		self.x_offset      = 0
		self.y_offset      = 0
		self.white_key_width  = 0
		self.white_key_height = 0
		self.black_key_width  = 0
		self.black_key_height = 0

		self.background_image = "None"
		self.midi_filename = " "
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
		if const.BLACKS[index % 12] == False:
			i = const.W_POSITION.index(index)
			const.total_keys[index] = pygame.draw.rect(screen, const.WHITE_PRESS, (self.x_offset + i * self.white_key_width + 1, 	# Printing doesn't overlap border
															  		   self.y_offset + 2 * self.white_key_height // 3, 
																	   self.white_key_width - 2, 
																	   self.white_key_height // 3))
			
			#self.draw_black_keys()
		# Black key
		else:
			i = const.B_POSITION.index(index)
			const.total_keys[index] = pygame.draw.rect(screen, const.BLACK_PRESS, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
															  		   self.y_offset, 
																	   self.black_key_width, 
																	   self.black_key_height))
			
		pygame.display.update()


	# Updates GUI, shows on piano when a key is released
	def release_key(self, index):
		# White key
		if const.BLACKS[index % 12] == False:
			i = const.W_POSITION.index(index)
			const.total_keys[index] = pygame.draw.rect(screen, const.WHITE, (self.x_offset + i * self.white_key_width + 1, 
																 self.y_offset + 2 * self.white_key_height // 3, 
																 self.white_key_width - 2, 
																 self.white_key_height // 3))
		# Black key
		else:
			i = const.B_POSITION.index(index)
			const.total_keys[index] = pygame.draw.rect(screen, const.BLACK, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
																 self.y_offset, 
																 self.black_key_width, 
																 self.black_key_height))
		
		#TODO -- draw other keyboard on top with 0 transparency, on keypress set key to 255 transparency and then back to 0 on release
		const.total_keys[index].update()


	# Draw keys on piano
	def draw_keys(self):
    	# Draw white keys and border
		skip_count = 0

		# Draw white keys
		for i in range(self.total_key_num):
			key = pygame.draw.rect(screen, const.WHITE, (self.x_offset + i * self.white_key_width, 
										  		   self.y_offset, 
												   self.white_key_width, 
												   self.white_key_height))
			pygame.draw.rect(screen, const.KEY_BORDER, (self.x_offset + i * self.white_key_width, 
										 		  self.y_offset, 
												  self.white_key_width, 
												  self.white_key_height), 1)
			const.total_keys.append(key)
   
			if self.keybind_toggle_on == 0 or self.note_toggle_on == 0:
				self.draw_labels(i,False)
    
		# Draw black keys
		for i in range(self.total_key_num):
			if skip_count not in [2, 6]:
				pygame.draw.rect(screen, const.BLACK, (self.x_offset + i * self.white_key_width + self.white_key_width - self.black_key_width // 2, 
									 			 self.y_offset, 
												 self.black_key_width, 
												 self.black_key_height))
												 

			if self.keybind_toggle_on == 0 or self.note_toggle_on == 0:
				self.draw_labels(i,True)
    
			skip_count += 1
			
    	    # Reset count on last key in octave for black keys
			if skip_count == 7:
				skip_count = 0

		#self.draw_black_keys()
		pygame.display.flip()


	# Separate function for drawing black keys - highlight on white keys doesn't cover black keys
	'''
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
 	'''
			

	# Draw keybind and note labels on piano
	def draw_labels(self, i, black_key):

		if self.keybind_toggle:
			# Label black keys: 5 black keys per octave
			if black_key == True:
				label = pygame.font.Font(font,16).render(const.black_order[i], True, const.BLACK, const.LIGHT_GRAY).convert_alpha()
				label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width, 
													(self.y_offset + self.black_key_height - 150)))
				screen.blit(label, label_rect)

			# Label white keys: 7 white keys per octave
			else: 
				label = pygame.font.Font(font,16).render(const.white_order[i], True, const.WHITE, const.LIGHT_GRAY).convert_alpha()
				label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width // 2, 
												(self.y_offset + self.white_key_height - 210)))
				screen.blit(label, label_rect)

		if self.note_toggle:
			# Label black keys: 5 black keys per octave
			if black_key == True:
				label = pygame.font.Font(font,16).render(const.black_notes_full[i], True, const.BLACK, const.LIGHT_GRAY).convert_alpha()
				label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width, 
													(self.y_offset + self.black_key_height + 110)))
				screen.blit(label, label_rect)

			# Label white keys: 7 white keys per octave
			else:
				label = pygame.font.Font(font,16).render(const.white_notes_full[i], True, const.WHITE, const.LIGHT_GRAY).convert_alpha()
				label_rect = label.get_rect(center=((self.x_offset + i * self.white_key_width) + self.white_key_width // 2, 
												(self.y_offset + self.white_key_height + 15)))
				screen.blit(label, label_rect)


	# Initializes piano in Freeplay mode
	def menu_freeplay(self):
		self.total_key_num 	= 35
		self.order    		= const.order
		self.semitone 		= 24
		self.x_offset 		= 235
		self.y_offset 		= (SCREEN_HEIGHT / 2) - 120
		self.white_key_width  = 45
		self.white_key_height = 200
		self.black_key_width  = 27
		self.black_key_height = 125
		self.pressed_array = [False]*len(self.order)
		self.mode = False
		self.start = True
		self.info_tab_on = False

		self.keybind_toggle_on = 0	
		self.note_toggle_on = 0

		if (self.background_image == "None"):
			screen.fill(const.LIGHT_GRAY)
		else:
			screen.blit(self.background_image, (0, 0))

		self.draw_keys()

	
	# Initializes piano in Learning mode
	def menu_learning(self):
		self.total_key_num = 35
		self.order    = const.order
		self.semitone = 24
		self.x_offset = 235
		self.y_offset = SCREEN_HEIGHT - 340
		self.white_key_width  = 45
		self.white_key_height = 200
		self.black_key_width  = 27
		self.black_key_height = 125
		self.pressed_array = [False]*len(self.order)
		self.mode = True
		self.start = True
		self.info_tab_on = False

		self.keybind_toggle_on = 0
		self.note_toggle_on = 0

		if (self.background_image == "None"):
			screen.fill(const.LIGHT_GRAY)
		else:
			screen.blit(self.background_image, (0, 0))

		self.draw_keys()
		

	# Draws menu buttons
	def draw_menu(self):
		# Draw left side buttons
		pygame.draw.rect(screen, const.BLACK, buttons.keybind_toggle)
		pygame.draw.rect(screen, const.BLACK, buttons.note_toggle)		
		pygame.draw.rect(screen, const.BLACK, buttons.freeplay_button)
		pygame.draw.rect(screen, const.BLACK, buttons.learning_button)
		pygame.draw.rect(screen, const.BLACK, buttons.transpose_up)
		pygame.draw.rect(screen, const.BLACK, buttons.transpose_down)
		pygame.draw.rect(screen, const.BLACK, buttons.info_button)
		pygame.draw.rect(screen, const.BLACK, buttons.background_button)

		# Draw left side icons
		buttons.keybind_icon.draw()
		buttons.note_icon.draw()
		buttons.freeplay_icon.draw()
		buttons.learning_icon.draw()
		buttons.transpose_up_icon.draw()
		buttons.transpose_down_icon.draw()
		buttons.info_icon.draw()
		buttons.background_icon.draw()

		# Test button shows up after piano is drawn once
		if self.start == True:
			pygame.draw.rect(screen, const.BLACK, buttons.test_keys_button)
			buttons.test_keys_icon.draw()

		# Learning mode buttons
		if self.mode == True:
			if self.info_tab_on == False:
				buttons.staff_image.draw()

			# Draw right side buttons
			pygame.draw.rect(screen, const.BLACK, buttons.file_button)
			pygame.draw.rect(screen, const.WHITE, buttons.song_title_button)
			pygame.draw.rect(screen, const.BLACK, buttons.play_button)
			pygame.draw.rect(screen, const.BLACK, buttons.pause_button)
			pygame.draw.rect(screen, const.BLACK, buttons.inc_vol)
			pygame.draw.rect(screen, const.BLACK, buttons.low_vol)
			
			# Draw right side icons
			buttons.file_icon.draw()
			buttons.play_icon.draw()
			buttons.pause_icon.draw()
			buttons.inc_vol_icon.draw()
			buttons.low_vol_icon.draw()
			screen.blit(pygame.font.SysFont("Calibri", 20).render(self.song_title, True, const.BLACK), (SCREEN_WIDTH - 360, 35))		


	# Testing ------------------------------------------------------------------------------------------------------------------------------------

	# Tests if MIDI file is valid
	def test_MIDI(self, filename):

		# Separate file extension name
		file_type = filename.split("/")
		file_type = file_type[len(file_type) - 1]
		file_type = file_type.split(".")[1]
		
		# Valid MIDI file
		if file_type == "mid":
			self.midi_filename = filename

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
		callback = buttons.Callback()

		self.menu_freeplay()

		for i in const.order:
			callback.name = i

			callback.event_type = "down"
			self.key(callback)

			pygame.time.wait(100)

			callback.event_type = "up"
			self.key(callback)


	# -------------------------------------------------------------------------------------------------------------


	# Run pygame and piano interface
	def play_piano(self):
		run = True
		song_volume = 2

		buttons.welcome_screen.draw()

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

					if buttons.freeplay_button.collidepoint(mouse_pos):
						
						'''
						Draw freeplay mode 
						Stop MIDI music playback when exiting
						Piano and some button functionalities enabled after starting piano
						Reset showing info tab
						'''
						self.menu_freeplay()
						mixer.music.stop()

					if buttons.learning_button.collidepoint(mouse_pos):
						
						self.menu_learning()

					elif buttons.keybind_toggle.collidepoint(mouse_pos):
						
						# Button functions after piano is drawn
						if self.start == True:
							# Toggle
							self.keybind_toggle = (not self.keybind_toggle)

							if (self.background_image == "None"):
								screen.fill(const.LIGHT_GRAY)
							else:
								screen.blit(self.background_image, (0, 0))

							self.draw_keys()
       
							if self.keybind_toggle == True:
								self.draw_labels
        

							'''
							self.keybind_toggle = (not self.keybind_toggle)
							self.draw_keys()

							if self.keybind_toggle == True:
								self.keybind_toggle_on += 1
							else:
								screen.fill(LIGHT_GRAY)
								self.draw_keys()
								self.keybind_toggle_on = 0

								if self.note_toggle == True:
									self.draw_keys()
       						'''

					elif buttons.note_toggle.collidepoint(mouse_pos):
						
						# Button functions after piano is drawn
						if self.start == True:
							# Toggle
							self.note_toggle = (not self.note_toggle)
							self.draw_keys()

							if self.note_toggle == True:
								self.note_toggle_on += 1
							else:
								if (self.background_image == "None"):
									screen.fill(const.LIGHT_GRAY)
								else:
									screen.blit(self.background_image, (0, 0))

								self.draw_keys()
								self.note_toggle_on = 0

								if self.keybind_toggle == True:
									self.draw_keys()

					elif buttons.file_button.collidepoint(mouse_pos):

						# Open file select
						try:
							filename = filedialog.askopenfilename(initialdir="/songs", title="Select file:", filetypes=[("MIDI files", "*.mid")])
							self.test_MIDI(filename)
						except Exception as e:
							print(e)

					elif buttons.transpose_up.collidepoint(mouse_pos):

						if self.start == True:
							self.semitone += 1

					elif buttons.transpose_down.collidepoint(mouse_pos):

						if self.start == True:
							self.semitone -= 1

					elif buttons.info_button.collidepoint(mouse_pos):

						self.info_tab_on = (not self.info_tab_on)

						if self.info_tab_on == True:
							buttons.info_tab.draw()
						else:
							if (self.background_image == "None"):
								screen.fill(const.LIGHT_GRAY)
							else:
								screen.blit(self.background_image, (0, 0))

							if self.start == False:
								buttons.welcome_screen.draw()
							else:
								self.draw_keys()

					# Custom background image --------------------------------------------------------------- TODO

					elif buttons.background_button.collidepoint(mouse_pos):

						try:
							
							background_filename = filedialog.askopenfilename(
								initialdir="/images",
								title="Select file:",
								filetypes=[("JPG or PNG files", "*.jpg;*.png")]
							)

							self.background_image = pygame.image.load(background_filename)
							self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

							screen.blit(self.background_image, (0, 0))
							pygame.display.flip()

							#self.draw_black_keys()
							#self.draw_white_keys()
							self.draw_keys()
							self.draw_labels()
							#self.play_piano()
							#self.draw_menu

						except Exception as e:
							print(f"Error: {e}")

	

					# Right side menu -------------------------------------------------------------------------------------------------------

					elif buttons.play_button.collidepoint(mouse_pos):

						try:
							mixer.music.load(self.midi_filename)
							mixer.music.set_volume(song_volume)
							mixer.music.play()
								
						except Exception as e:
							print(e)
							self.song_title = "No MIDI file found!"

					elif buttons.pause_button.collidepoint(mouse_pos):

						try:
							mixer.music.pause()
							paused = True

						except Exception as e:
							print(e)

					elif buttons.inc_vol.collidepoint(mouse_pos):

						song_volume += 0.2
						mixer.music.set_volume(song_volume)

					elif buttons.low_vol.collidepoint(mouse_pos):

						song_volume -= 0.2
						mixer.music.set_volume(song_volume)

					# Test buttons ------------------------------------------------------------------------------------------------------------

					elif buttons.test_keys_button.collidepoint(mouse_pos):

						mixer.music.stop()
						self.test_keys()
						self.start = True
						self.info_tab_on = False
					
			# Update the screen
			self.draw_menu()
			pygame.display.update()
			clock.tick(const.FPS)
