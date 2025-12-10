from pico2d import open_canvas, delay, close_canvas
import game_framework

import title_mode as start_mode

# 게임 화면 크기 설정
# 플레이 화면 1280 x 880
# 상단 화면 1280 x 140
game_weight = 1280
game_height = 1020

open_canvas(game_weight, game_height)
game_framework.run(start_mode)
close_canvas()


