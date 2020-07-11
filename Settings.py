"""
    Settings
"""
# Main Settings
project_title = "Traveler of Elrualia"
screen_size = WIDTH, HEIGHT = 1280, 720
FPS = 60

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
# Characters settings / 0: bottom, 1: left, 2: right, 3: top
GAME_DICT = {"background_image": "background_battle.png", "background_color": LIGHTBLUE,
             "platform_size": [950, 270],
             "hp_font": None, "hp_color": WHITE, "hp_size": 25,
             "grid_size": [4, 4], "grid_dt": [120, 70],
             "pos": {"player": [220, 360], "enemy": [0, 0],
                     "player_name": [0, 0], "enemy_name": [0, 0], "enemy_name_dt": [0, 0],
                     "player_level": [0, 0], "player_exp": [0, 0], "player_mana": [0, 0],
                     "next_spell": [0, 0], "current_spell": [0, 0], "current_attack": [0, 0],
                     "stage": [0, 0], "time": [0, 0], "option": [0, 0], "fps": [0, 0]},
             "color": {"health": GREEN, "mana": LIGHTSKYBLUE, "spell": [RED, BLUE, GREEN]},
             "font": None}



CHARACTER_DICT = {"layer": 3,
                  "player": {"name": "Player", "pos": [220, 320], "grid_pos": [0, 0], "range": [], "move": True,
                             "image": "character_SecretHideout_Gunner_Blue_Idle_960x192_192x192.png", "side": 0, "center": True, "bobbing": False, "flip": False,
                             "table": True, "reverse": False, "size": [192, 192], "animation_time": 0.150, "animation_loop": False, "impact": False,
                             "hp_offset": [0, 55],
                             "spell_offset": [0, -48], "cast_offset": [102, 0],
                             "debug_color": BLUE, "debug_pos": [168, 333], "debug_dt": [104, 54],
                             "move_speed": [1.25 * GAME_DICT["platform_size"][0], 2.5 * GAME_DICT["platform_size"][1]],
                             "level": 1, "max_health": 100, "health": 100, "max_mana": 5, "mana": 3.75,
                             "attack_rate": 225},
                  "enemy": {"name": "Enemy", "pos": [700, 320], "grid_pos": [0, 0], "range": [], "move": True,
                            "hp_offset": [0, 55],
                            "debug_color": RED, "debug_pos": [648, 333], "debug_dt": [104, 54],
                            "image": "character_SecretHideout_Gunner_Red_Idle_960x192_192x192.png", "side": 0, "center": True, "bobbing": False, "flip": True,
                            "table": True, "reverse": False, "size": [192, 192], "animation_time": 0.150, "animation_loop": False, "impact": False,
                            "move_speed": [1.25 * GAME_DICT["platform_size"][0], 2.5 * GAME_DICT["platform_size"][1]],
                            "level": 1, "max_health": 100, "health": 100, "max_mana": 6, "mana": 4.50,
                            "move_frequency": 1000}}

SPELL_DICT = {"layer": 2,
              "energy_ball": {"pos": [220, 360], "range": 8 * [[1, 0]], "move": True,
                              "image": "effect_pimen_EnergyBall_128x128.png", "center": True, "bobbing": False, "flip": False, "impact": True,
                              "table": True, "reverse": False, "size": [128, 128], "side": 0, "animation_time": 0.025, "animation_loop": False,
                              "move_speed": [2 * GAME_DICT["platform_size"][0], 4 * GAME_DICT["platform_size"][1]], "debug_move_speed": [250, 250],
                              "damage": 10},
              "energy_ball_impact": {"pos": [0, 0], "range": [0, 0], "move": False,
                                     "image": "effect_pimen_EnergyBall_Impact_128x128.png", "center": True, "bobbing": False, "flip": False, "impact": False,
                                     "table": True, "reverse": True, "size": [128, 128], "side": 0, "animation_time": 0.025, "animation_loop": True},

              "thunder": {"pos": [220, 360], "range": [3, 0], "move": False,
                          "image": "effect_pimen_Thunder_64x256.png", "center": True, "bobbing": False, "flip": False, "impact": False,
                          "table": True, "reverse": False, "size": [64, 256], "side": 0, "animation_time": 0.025, "animation_loop": True,
                          "damage": 50}
              }