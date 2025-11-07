from pico2d import open_canvas, delay, close_canvas
import game_framework

import play_mode as start_mode

game_weight = 1280
game_height = 880

open_canvas(game_weight, game_height)
game_framework.run(start_mode)
close_canvas()


