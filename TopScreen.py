# 상단 체력, 미니맵, 아이템들이 표시되는 화면
from pico2d import *

from play_mode import player_obj


# 상단 화면 1280 x 140
class TopScreen:
    image = None
    EmptyHeart = None
    HalfHeart = None
    FullHeart = None

    def __init__(self, player_obj):
        self.player = player_obj
        base_path = 'resource/'

        if TopScreen.image == None:
             TopScreen.image = load_image(f'{base_path}TopScreen.png')
        if TopScreen.EmptyHeart == None:
             TopScreen.EmptyHeart = load_image(f'{base_path}EmptyHeart.png')
        if TopScreen.HalfHeart == None:
            TopScreen.HalfHeart = load_image(f'{base_path}HalfHeart.png')
        if TopScreen.FullHeart == None:
            TopScreen.FullHeart = load_image(f'{base_path}FullHeart.png')

        self.x = 640
        self.y = 950

    def draw(self):
        TopScreen.image.clip_draw(0, 0, 256, 56, self.x, self.y, 1280, 140)

        if player_obj.


    def update(self):
        pass