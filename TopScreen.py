# 상단 체력, 미니맵, 아이템들이 표시되는 화면

from pico2d import *
import game_framework
import game_world

# 상단 화면 1280 x 140
class TopScreen:

    def __init__(self, player_obj):
        self.player = player_obj
        base_path = 'resource/'
        self.image = load_image(f'{base_path}TopScreen.png')
        self.x = 640
        self.y = 950

    def draw(self):
        self.image.clip_draw(0, 0, 256, 56, self.x, self.y, 1280, 140)

    def update(self):
        pass