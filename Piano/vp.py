import keyboard
import time
from mingus.midi import fluidsynth
from mingus.containers.note import Note 

# Keybinds for 7 octaves
order = [ "`", "~", "1", "!", "2", "3", "#",  "4", "$", "5",  "%", "6",					# Ocatve 1
		  "7", "&", "8", "*", "9", "0", ")",  "-", "_", "=",  "+", "backspace",			# Ocatve 2
		  "q", "Q", "w", "W", "e", "r", "R",  "t", "T", "y",  "Y", "u",					# Ocatve 3
		  "i", "I", "o", "O", "p", "[", "{",  "]", "}", "\\", "|", "enter",				# Ocatve 4
		  "a", "A", "s", "S", "d", "f", "F",  "g", "G", "h",  "H", "j",					# Ocatve 5
		  "k", "K", "l", "L", ";", "'", "\"", ",", "<", ".",  ">", "/", 				# Ocatve 6
		  "z", "Z", "x", "X", "c", "v", "V",  "b", "B", "n",  "N", "m",					# Ocatve 7
		  "M" ]																			# C8

class Piano:
	def __init__(self, soundfont_path, transpose=0, sustain=False):
		self.transposition = transpose
		self.soundfont_path = soundfont_path
		self.order = order
		self.channel = 0
		self.volume_value = 128
		self.pressed_array = [False]*len(order) # Store if a key is pressed to prevent key repetition
		self.sustain = sustain

		self.init()

	def init(self):
		fluidsynth.init(self.soundfont_path)
		keyboard.hook(self.key)

		if self.sustain:
			fluidsynth.control_change(0, 64, 127)
			fluidsynth.control_change(0, 91, 127)
			print("Sustain ON!")
		else:
			fluidsynth.control_change(0, 64, 0)
			fluidsynth.control_change(0, 91, 0)
			print("Sustain OFF!")
		# Startup sound: Plays note in each octave
		for octave in range(9):
			fluidsynth.play_Note(Note("C", octave))
			time.sleep(0.1)

		# Start GUI - TODO

	def key(self, callback):
		'''
		If keyboard event is DOWN, play the note and store that the key
		is pressed in the pressed_array. Upon a key UP event, set the key
		to released in the pressed_array to allow future notes.
		'''
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
					print(f"{callback.name} => {n}")
			# UP event
			else: 
				self.pressed_array[index] = False 			# Key is released, allow notes

		except Exception as e:
			print(e)

	@property
	def volume(self):
		return self.volume_value

	@volume.setter
	def volume(self, value):
		self.volume_value = value
		fluidsynth.main_volume(self.channel, value)