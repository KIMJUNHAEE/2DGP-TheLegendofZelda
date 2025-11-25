# 상단 체력, 미니맵, 아이템들이 표시되는 화면
from pico2d import *

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

        current_hp = self.player.hp
        max_heart = (self.player.MaxHp + 1) // 2 # 올림으로 계산

        for i in range(max_heart):
            row = i // 8
            col = i % 8

            heart_x = 896 + (col * 40)
            heart_y = 910 + (row * 20)


            heart_hp = current_hp - (i * 2)

            if heart_hp >= 2:
                TopScreen.FullHeart.clip_draw(0, 0, 16, 16, heart_x, heart_y,40,20)
            elif heart_hp == 1:
                TopScreen.HalfHeart.clip_draw(0, 0, 16, 16, heart_x, heart_y,40,20)
            else:
                TopScreen.EmptyHeart.clip_draw(0, 0, 16, 16, heart_x, heart_y,40,20)


    def update(self):
        pass