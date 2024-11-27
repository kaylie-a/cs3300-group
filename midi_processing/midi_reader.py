import pygame
import mido
from pygame.locals import *
import sys

# Initialize Pygame
pygame.init()

# Constants for window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NOTE_RADIUS = 7
STAFF_WIDTH = 700
STAFF_HEIGHT = 400
STAVE_OFFSET_Y = 100
LINE_HEIGHT = 10  # Space between the staff lines

# Dictionary to map MIDI note numbers to note names without octave
NOTE_NAMES = {
    60: "C", 61: "C#", 62: "D", 63: "D#", 64: "E", 65: "F", 66: "F#", 67: "G", 68: "G#", 69: "A",
    70: "A#", 71: "B", 72: "C", 73: "C#", 74: "D", 75: "D#", 76: "E", 77: "F", 78: "F#", 79: "G",
    80: "G#", 81: "A", 82: "A#", 83: "B", 84: "C", 85: "C#", 86: "D", 87: "D#", 88: "E", 89: "F",
    90: "F#", 91: "G", 92: "G#", 93: "A", 94: "A#", 95: "B", 96: "C", 97: "C#", 98: "D", 99: "D#",
    100: "E", 101: "F", 102: "F#", 103: "G", 104: "G#", 105: "A", 106: "A#", 107: "B", 108: "C"
}

# Adjusted relative position on the staff for notes from F (bottom-most) to E (top-most)
BASE_NOTE_POSITIONS = {
    'F': -1.6, 'F#': -1.6, 'G': -1.1, 'G#': -1.1, 'A': -0.6, 'A#': -0.6, 'B': -0.1,
    'C': 0.4, 'C#': 0.4, 'D': 0.9, 'D#': 0.9, 'E': 1.4
}

# Initialize the MIDI file reader
def read_midi(file_path):
    midi = mido.MidiFile(file_path)
    notes_pressed = set()

    for msg in midi.play():
        if msg.type == 'note_on' and msg.velocity > 0:
            note_name = NOTE_NAMES.get(msg.note, 'Unknown')
            print(f"Note {note_name} pressed")
            notes_pressed.add(note_name)
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            note_name = NOTE_NAMES.get(msg.note, 'Unknown')
            notes_pressed.discard(note_name)

        screen.fill((255, 255, 255))
        draw_treble_clef(notes_pressed)
        pygame.display.update()

def draw_treble_clef(notes_pressed):
    # Draw the staff lines
    for i in range(5):
        pygame.draw.line(screen, (0, 0, 0), (50, STAVE_OFFSET_Y + i * LINE_HEIGHT), (STAFF_WIDTH, STAVE_OFFSET_Y + i * LINE_HEIGHT), 2)

    draw_notes(notes_pressed)

def get_note_y_position(note):
    base_position = BASE_NOTE_POSITIONS[note]  # Use note name without octave
    return STAVE_OFFSET_Y + (2 - base_position) * LINE_HEIGHT

def draw_notes(notes_pressed):
    offset_x = 130  # Shifted further left to start closer to the clef
    font = pygame.font.Font(None, 33)  
    for note, y_offset in BASE_NOTE_POSITIONS.items():
   
        x = offset_x + list(BASE_NOTE_POSITIONS.keys()).index(note) * 40
        y = get_note_y_position(note)
        
        color = (160, 0, 255) if note in notes_pressed else (0, 0, 0)

        pygame.draw.circle(screen, color, (x, y), NOTE_RADIUS)

        text = font.render(note, True, (0, 0, 0))
        screen.blit(text, (x - 10, y - NOTE_RADIUS - 20))

if __name__ == "__main__":
    midi_file = r'C:\GitHub\cs3300-group\songs\Fur-Elise-1.mid'             # This path will be different depending on computer directory and name
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Treble Clef MIDI Visualization")
    
    read_midi(midi_file)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
