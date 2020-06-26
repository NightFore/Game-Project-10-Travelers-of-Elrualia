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
LAYER_CURSOR = 4

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

# Characters settings / 0: bottom, 1: left, 2: right, 3: top
UI_DICT = {"grid_size": [4, 4],
           "health": GREEN, "armor": ORANGE, "mana": LIGHTSKYBLUE,
           "spell_color": [RED, BLUE, GREEN], "spell_color_pos": [203, 643, 54, 54], "spell_color_dt": [60, 0],
           "spell_size": 38, "spell_dt": 95, "spell_side_dt": 190,
           "status_font": None, "status_size": 50, "status_color": BLACK, "status_enemy_pos": [960, 670]}



GAME_DICT = {"grid_size": [4, 4], "grid_dt": [120, 70],
             "pos": {"player": [220, 360], "enemy": [0, 0],
                     "player_name": [0, 0], "enemy_name": [0, 0], "enemy_name_dt": [0, 0],
                     "player_level": [0, 0], "player_exp": [0, 0], "player_mana": [0, 0],
                     "next_spell": [0, 0], "current_spell": [0, 0], "current_attack": [0, 0],
                     "stage": [0, 0], "time": [0, 0], "option": [0, 0], "fps": [0, 0]},
             "color": {"health": GREEN, "mana": LIGHTSKYBLUE, "spell": [RED, BLUE, GREEN]},
             "font": None
             }

CHARACTER_DICT = {"layer": 2,
                  "player": {"name": "Player", "pos": [208, 332], "grid_pos": [0, 0],
                             "image": "character_oco_Knight_Idle_strip_noBKG_256x256.png", "side": 0, "center": True, "bobbing": False,
                             "table": True, "size": [256, 256], "animation_time": 0.075, "speed": [625, 625],
                             "level": 1, "max_health": 100, "health": 100, "max_mana": 5, "mana": 3.75,
                             "attack_rate": 225},
                  "skeleton": {"name": "Skeleton", "pos": [700, 360], "grid_pos": [0, 0],
                               "image": "character_pipoya_enemy_04_1.png", "side": 1, "center": True, "bobbing": False,
                               "table": True, "size": [32, 32], "animation_time": 0.075, "speed": [625, 625],
                               "level": 1, "max_health": 100, "health": 100, "max_mana": 6, "mana": 4.50,
                               "move_frequency": 1000}}

SPELL_DICT = {"layer": 3, "offset": [0, -40], "cast_offset": [40, 0],
              "energy_ball": {"image": "effect_pimen_EnergyBall.png", "side": 0, "center": True, "bobbing": False,
                              "table": True, "size": [128, 128], "animation_time": 0.100, "movespeed": [800, 800],
                              "damage": 10, "range": 8 * [[1, 0]]}}


PLAYER_DICT = {"name": "Player", "center": True, "bobbing": False,
               "image": "character_oco_Knight_Idle_strip_noBKG_256x256.png", "table": True, "tile_dt": [256, 256], "default_side": 0,
               "pos": [208, 332], "pos_dt": [120, 70], "grid_pos": [0, 0],
               "max_health": 100, "health": 100, "health_rect": [83, 23, 254, 34],
               "max_armor": 50, "armor": 25, "armor_rect": [83, 63, 254, 34],
               "max_mana": 5, "mana": 3.75, "mana_rect": [553, 653, 34, 34], "mana_dt": [40, 0],
               "spell_range_dt": 95,
               "current_spell_pos": [230, 670], "current_spell_dt": [60, 0],
               "waiting_spell_pos": [70, 730], "waiting_spell_dt": [0, -60],
               "next_spell_pos": [130, 670], "passive_spell_pos": [410, 670]}

ENEMY_DICT = {"skeleton": {"image": "character_pipoya_enemy_04_1.png", "icon": "character_pipoya_enemy_04_1_icon_64x64.png",
                           "grid_pos": [0, 0], "max_health": 100, "health": 100, "max_mana": 6, "mana": 4.50, "move_frequency": 1000},
              "table": True, "tile_dt": [32, 32], "center": True, "bobbing": False,
              "pos": [735, 260], "pos_dt": [95, 95], "icon_pos": [1200, 660],
              "health_rect": [1203, 223, 34, 394], "mana_rect": [1163, 583, 34, 34], "mana_dt": [0, -40]}

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

SPELL_OLD1 = {"sword_1": {"image": "item_alex_s_assets_sword_1_48x48.png", "type": 1, "damage": 20, "range": [[1, 1, 1]]},
              "sword_2": {"image": "item_alex_s_assets_sword_2_48x48.png", "type": 1, "damage": 30, "range": [[1, 1, 1], [1]]},
              "sword_3": {"image": "item_alex_s_assets_sword_3_48x48.png", "type": 1, "damage": 50, "range": [[1, 1, 1], [1, 1, 1]]},
              "spear_1": {"image": "item_alex_s_assets_spear_1_48x48.png", "type": 1, "damage": 15, "range": [[1], [1]]},
              "spear_2": {"image": "item_alex_s_assets_spear_3_48x48.png", "type": 1, "damage": 30, "range": [[1], [1], [1]]},
              "spear_3": {"image": "item_alex_s_assets_spear_4_48x48.png", "type": 1, "damage": 45, "range": [[1, 1, 1], [1], [1]]},
              "armor_1": {"image": "item_alex_s_assets_armor_1_48x48.png", "type": 0},
              "armor_2": {"image": "item_alex_s_assets_armor_3_48x48.png", "type": 0},
              "armor_3": {"image": "item_alex_s_assets_armor_4_48x48.png", "type": 0}}

PASSIVE_DICT = {"atk_crystal": {"image": "item_raventale_variables_1_necklace_withruby_45x45.png"},
                "def_crystal": {"image": "item_raventale_variables_1_necklace_withamethyst_45x45.png"},
                "mana_crystal": {"image": "item_raventale_variables_1_necklace_withtopaz_45x45.png"}}
