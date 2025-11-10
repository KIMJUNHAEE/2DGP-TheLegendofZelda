# 상단 체력, 미니맵, 아이템들이 표시되는 화면

from pico2d import *
import game_framework
import game_world
import play_mode
from Player import player

class TopScreen:

    def __init__(self, player_obj):
        self.player = player_obj
        self.image = load_image(f'/resource/TopScreen.png')
        self.x = 0
        self.y = 880

    def draw(self):
        self.image.clip_draw(0, 0, 256, 56, self.x, self.y, 1280, 1020)