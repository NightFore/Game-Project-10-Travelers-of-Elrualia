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
LAYER_CHARACTERS = 2
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
LIGHTSKYBLUE = 135, 206, 250

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
ENEMY_IMG = "Icon_Wolf.png"

GRID_DT = 95
GRID_SIDE_DT = 190


COLOR_DICT = {"health": GREEN, "armor": ORANGE, "mana": LIGHTSKYBLUE, "spell": [RED, BLUE, GREEN]}
HEALTH_COLOR = GREEN
ARMOR_COLOR = ORANGE
MANA_COLOR = LIGHTSKYBLUE
COLOR_SPELL = [RED, BLUE, GREEN]

PLAYER_DICT = {"image": "character_pipoya_male_01_2.png",
               "pos": [260, 260], "pos_dt": [95, 95],
               "health_rect": [83, 23, 254, 34],
               "armor_rect": [83, 63, 254, 34],
               "mana_rect": [553, 653, 34, 34], "mana_dt": [40, 0],
               "current_spell_pos": [230, 670], "current_spell_dt": [60, 0],
               "waiting_spell_pos": [70, 730], "waiting_spell_dt": [0, -60],
               "next_spell_pos": [130, 670],
               "passive_spell_pos": [410, 670],
               "spell_range_dt": 95}

ENEMY_DICT = {"character_pos": [1200, 660], "character_dt": [95, 95],
              "health_pos": [1203, 223], "health_dt": [34, 394],
              "mana_pos": [1163, 583], "mana_dt": [40, 40]}
ENEMY_X = 1200
ENEMY_Y = 660
ENEMY_HEALTH_X = 1203
ENEMY_HEALTH_Y = 223
ENEMY_HEALTH_WIDTH = 34
ENEMY_HEALTH_HEIGHT = 394
ENEMY_MANA_X = 1163
ENEMY_MANA_Y = 583

SPELL_DT = 95

MANA_X_DT = 40
MANA_Y_DT = -40
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

SPELL_DICT = {"sword_1": {"image": "item_alex_s_assets_sword_1_48x48.png", "type": 1, "damage": 20, "range": [[0, 1, 0]]},
              "sword_2": {"image": "item_alex_s_assets_sword_2_48x48.png", "type": 1, "damage": 30, "range": [[1, 1, 1]]},
              "sword_3": {"image": "item_alex_s_assets_sword_3_48x48.png", "type": 1, "damage": 50, "range": [[1, 1, 1], [0, 1, 0]]},
              "spear_1": {"image": "item_alex_s_assets_spear_1_48x48.png", "type": 1, "damage": 15, "range": [[0, 1, 0], [0, 1, 0]]},
              "spear_2": {"image": "item_alex_s_assets_spear_3_48x48.png", "type": 1, "damage": 30, "range": [[0, 1, 0], [0, 1, 0], [0, 1, 0]]},
              "spear_3": {"image": "item_alex_s_assets_spear_4_48x48.png", "type": 1, "damage": 45, "range": [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]]},
              "armor_1": {"image": "item_alex_s_assets_armor_1_48x48.png", "type": 0},
              "armor_2": {"image": "item_alex_s_assets_armor_3_48x48.png", "type": 0},
              "armor_3": {"image": "item_alex_s_assets_armor_4_48x48.png", "type": 0}}

PASSIVE_DICT = {"atk_crystal": {"image": "item_raventale_variables_1_necklace_withruby_45x45.png"},
                "def_crystal": {"image": "item_raventale_variables_1_necklace_withamethyst_45x45.png"},
                "mana_crystal": {"image": "item_raventale_variables_1_necklace_withtopaz_45x45.png"}}
