# 동굴
from pico2d import load_image

class Cave:
    def __init__(self, player=None):
        base_path = 'resource/Maps/'
        self.image = load_image(f'{base_path}cave.png')
        self.player = player

        self.screen_width = 1280
        self.screen_height = 880
        self.map_width = 256
        self.map_height = 176

    def draw(self):
        self.image.clip_draw(0, 0, 256, 176, self.screen_width // 2, self.screen_height // 2, self.screen_width, self.screen_height)

    def update(self):
        pass