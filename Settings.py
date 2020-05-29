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

ORANGE = 255, 120, 30

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

HEALTH_COLOR = GREEN
ARMOR_COLOR = ORANGE
MANA_COLOR = LIGHTBLUE

PLAYER_HEALTH_X = 83
PLAYER_HEALTH_Y = 23
PLAYER_HEALTH_WIDTH = 254
PLAYER_HEALTH_HEIGHT = 34

PLAYER_ARMOR_X = 83
PLAYER_ARMOR_Y = 63
PLAYER_ARMOR_WIDTH = 254
PLAYER_ARMOR_HEIGHT = 34

PLAYER_MANA_X = 553
PLAYER_MANA_Y = 653
MANA_X_DT = 40
MANA_WIDTH = 34
MANA_HEIGHT = 34

# Background settings
BACKGROUND_COLOR = LIGHTBLUE
BACKGROUND_BATTLE_IMG = "background_battle.png"

# Items
ITEM_IMAGES = {"health": ["item_beyonderboy_heart_edited.png"],
               "mana": ["item_raventale_gem_2_blue_42x42.png"],
               "shield": ["item_alex_s_assets_shield_2_32x32.png"],
               "clock": ["item_nyknck_sandclock_1_58x58.png", "item_nyknck_sandclock_2_58x58.png",
                         "item_nyknck_sandclock_3_58x58.png", "item_nyknck_sandclock_4_58x58.png",
                         "item_nyknck_sandclock_5_58x58.png"]}

SPELL_IMAGES = {"sword_1": ["item_alex_s_assets_sword_1_48x48.png"],
               "sword_2": ["item_alex_s_assets_sword_2_48x48.png"],
               "sword_3": ["item_alex_s_assets_sword_3_48x48.png"],
               "armor_1": ["item_alex_s_assets_armor_1_48x48.png"],
               "armor_2": ["item_alex_s_assets_armor_3_48x48.png"],
               "armor_3": ["item_alex_s_assets_armor_4_48x48.png"]}