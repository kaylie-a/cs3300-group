# Constants
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

SCALE = 0.12

total_keys = []

# Names for note label printing
white_notes_full = [ "C1", "D1", "E1", "F1", "G1", "A1", "B1",
					 "C2", "D2", "E2", "F2", "G2", "A2", "B2",
					 "C3", "D3", "E3", "F3", "G3", "A3", "B3",
					 "C4", "D4", "E4", "F4", "G4", "A4", "B4",
					 "C5", "D5", "E5", "F5", "G5", "A5", "B5" ]

black_notes_full = [ "C#1", "D#1", "",  "F#1", "G#1", "A#1", "",
					 "C#2", "D#2", "",  "F#2", "G#2", "A#2", "",
					 "C#3", "D#3", "",  "F#3", "G#3", "A#3", "",
					 "C#4", "D#4", "",  "F#4", "G#4", "A#4", "",
					 "C#5", "D#5", "",  "F#5", "G#5", "A#5", "" ]

# Names for keybind label printing
white_order = [ "esc", "f2", "f4", "f5", "f7", "f9", "f11",
			    "1",   "3",  "5",  "6",  "8",  "0",  "=",
				"q",   "e",  "t",  "y",  "i",  "p",  "]",
				"a",   "d",  "g",  "h",  "k",  ";",  "ret",
				"sh",  "x",  "v",  "b",  "m",  ".",  "rsh" ]

black_order = [ "f1", "f3", "", "f6", "f8", "f10", "",
			    "2",  "4",  "", "7",  "9",  "-",  "",
				"w",  "r",  "", "u",  "o",  "[",  "",
				"s",  "f",  "", "j",  "l",  "'",  "",
				"z",  "c",  "", "n",  ",",  "/",  "" ]

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