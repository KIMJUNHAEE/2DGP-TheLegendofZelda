# npc
from pico2d import *
import config

class OldManNPC:
    def __init__(self, x, y):
        base_path = 'resource/NPCs/'
        self.image = load_image(f'{base_path}oldman.png')
        self.x = x
        self.y = y
        self.frame = 0

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 16, 16, self.x, self.y,50,50)
        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

class FireNPC:
    def __init__(self, x, y):
        base_path = 'resource/NPCs/'
        self.image = [load_image(f'{base_path}fire{i + 1}.png') for i in range(2)]
        self.x = x
        self.y = y
        self.frame = 0
        self.frame_time = get_time()  # 초기화 시점 기록
        self.frame_interval = 0.1

    def update(self):

        current_time = get_time()
        if current_time - self.frame_time >= self.frame_interval:
            self.frame = (self.frame + 1) % 2
            self.frame_time = current_time


    def draw(self):
        self.image[int(self.frame)].clip_draw(0, 0, 16, 16, self.x, self.y,50,50)
        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25