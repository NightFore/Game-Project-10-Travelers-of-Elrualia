"""
    Settings
"""
# Main Settings
project_title = "Traveler of Elrualia"
screen_size = WIDTH, HEIGHT = 1280, 720
FPS = 60

# Map Settings
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Layer Settings
LAYER_ITEMS = 1
LAYER_PLAYER = 2
LAYER_CURSOR = 3

"""
    Colors
"""
BLACK = 0, 0, 0
WHITE = 255, 255, 255

RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

YELLOW = 255, 255, 0
MAGENTA = 255, 0, 255
CYAN = 0, 255, 255

LIGHTGREY = 100, 100, 100
LIGHTBLUE = 90, 135, 180

"""
    Game Settings
"""
# Cursor settings
CURSOR_WIDTH = 40
CURSOR_HEIGHT = 40
CURSOR_COLOR = BLUE

# Characters settings
PLAYER_IMG = "Sprite_iris.png"
PLAYER_IMG_2 = "character_pipoya_male_01_2.png"
PLAYER_X = 255
PLAYER_Y = 260
PLAYER_X_DT = 95
PLAYER_Y_DT = 95

# Background settings
BACKGROUND_COLOR = LIGHTBLUE
BACKGROUND_BATTLE_IMG = "Background_battle.png"

# Items
ITEM_IMAGES = {"health": ["item_beyonderboy_heart.png"],
               "mana": ["item_raventale_gem_2_blue.png"],
               "armor": ["item_alex_s_assets_shield_2.png"],
               "clock": ["item_nyknck_sandclock_1.png", "item_nyknck_sandclock_2.png", "item_nyknck_sandclock_3.png",
                         "item_nyknck_sandclock_4.png", "item_nyknck_sandclock_5.png"]}