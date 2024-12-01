import pygame
import const


pygame.init()

SCREEN_WIDTH  = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT*0.93])

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


# Class for piano key press or release
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
          
          
# -------------------------------------------------------------------------------------------------------------


# pygame.Rect( x_pos, y_pos, rect_width, rect_height )	==>	anchor point is top left
# Left side menu -------------------------------------------------------------------------------------------------------------
image = pygame.image.load("icons/fpm-icon.png").convert_alpha()
freeplay_button = pygame.Rect(10, 10, 70, 70)
freeplay_icon = Button(10, 10, image, const.SCALE)

image = pygame.image.load("icons/lm-icon.png").convert_alpha()
learning_button = pygame.Rect(10, 90, 70, 70)
learning_icon = Button(10, 90, image, const.SCALE)

image = pygame.image.load("icons/keybind-toggle-icon.png").convert_alpha()
keybind_toggle = pygame.Rect(10, 170, 70, 70)
keybind_icon = Button(10, 170, image, const.SCALE)

image = pygame.image.load("icons/note-toggle-icon.png").convert_alpha()
note_toggle = pygame.Rect(10, 250, 70, 70)
note_icon = Button(10, 250, image, const.SCALE)

image = pygame.image.load("icons/transpose-up-icon.png").convert_alpha()
transpose_up = pygame.Rect(10, 330, 70, 70)
transpose_up_icon = Button(10, 330, image, const.SCALE)

image = pygame.image.load("icons/transpose-down-icon.png").convert_alpha()
transpose_down = pygame.Rect(10, 410, 70, 70)
transpose_down_icon = Button(10, 410, image, const.SCALE)

image = pygame.image.load("icons/info-icon.png").convert_alpha()
info_button = pygame.Rect(10, 490, 70, 70)
info_icon = Button(10, 490, image, const.SCALE)

image = pygame.image.load("icons/info-tab.png").convert_alpha()
info_tab = Button((SCREEN_WIDTH / 2) - 450, (SCREEN_HEIGHT / 2) - 500, image, 0.8)

# Background Image
image = pygame.image.load("icons/image-icon.png").convert_alpha()
background_button = pygame.Rect(10, 570, 70, 70)
background_icon = Button(10, 570, image, const.SCALE)


# Right side menu ------------------------------------------------------------------------------------------------------------
image = pygame.image.load("icons/file-icon.png").convert_alpha()
file_button = pygame.Rect(SCREEN_WIDTH - 475, 10, 70, 70)
file_icon = Button(SCREEN_WIDTH - 475, 10, image, const.SCALE)

song_title_button = pygame.Rect(SCREEN_WIDTH - 390, 10, 380, 70)

image = pygame.image.load("icons/play-icon.png").convert_alpha()
play_button = pygame.Rect(SCREEN_WIDTH - 80, 90, 70, 70)
play_icon = Button(SCREEN_WIDTH - 80, 90, image, const.SCALE)

image = pygame.image.load("icons/pause-icon.png").convert_alpha()
pause_button = pygame.Rect(SCREEN_WIDTH - 80, 170, 70, 70)
pause_icon = Button(SCREEN_WIDTH - 80, 170, image, const.SCALE)

image = pygame.image.load("icons/volume-up-icon.png").convert_alpha()
inc_vol = pygame.Rect(SCREEN_WIDTH - 80, 250, 70, 70)
inc_vol_icon = Button(SCREEN_WIDTH - 80, 250, image, const.SCALE)

image = pygame.image.load("icons/volume-down-icon.png").convert_alpha()
low_vol = pygame.Rect(SCREEN_WIDTH - 80, 330, 70, 70)
low_vol_icon = Button(SCREEN_WIDTH - 80, 330, image, const.SCALE)

# Load Staff Image In - temp
image = pygame.image.load("icons/staffIMG.jpg").convert_alpha()
staff_image = Button(200, 0, image, SCREEN_WIDTH/1920 - 0.1)

image = pygame.image.load("icons/welcome-screen.png").convert_alpha()
welcome_screen = Button((SCREEN_WIDTH / 2) - 400, (SCREEN_HEIGHT / 2) - 250, image, 0.65)


# Testing ---------------------------------------------------------------------------------------------------------------------
image = pygame.image.load("icons/test-icon.png").convert_alpha()
test_keys_button = pygame.Rect(10, SCREEN_HEIGHT*0.95 - 160, 70, 70)
test_keys_icon = Button(10, SCREEN_HEIGHT*0.95 - 160, image, const.SCALE)

image = pygame.image.load("icons/DigiPiano-icon.png").convert_alpha()
test_songs_button = pygame.Rect(10, SCREEN_HEIGHT*0.95 - 240, 70, 70)
test_songs_icon = Button(10, SCREEN_HEIGHT*0.95 - 240, image, const.SCALE)
