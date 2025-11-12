# npc

from pico2d import *
import game_world

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

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25
