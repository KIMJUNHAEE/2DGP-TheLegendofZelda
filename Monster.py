from pico2d import *
import game_world
import MD

class Monster:
    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        self.hp = 0
        self.frame = 0
        self.width = 0
        self.height = 0
        self.size = 0
        self.direction = 0

        base_path = 'resource/Enemies/'
        if self.name == 'Octorok':
            self.hp = MD.OctorokHp
            self.width = MD.OctorokWidth
            self.height = MD.OctorokHeight
            self.size = MD.OckorokSize
            self.frame = [load_image(f'{base_path}Octorok{i + 1}.png') for i in range(MD.OctorokFrame_count)]

    def get_bb(self):
        half_width = self.image.w // 2
        half_height = self.image.h // 2
        return (self.x - half_width, self.y - half_height,
                self.x + half_width, self.y + half_height)

    def handle_collision(self, group, other):
        pass

    def update(self):
        pass

    def draw(self):
        self.frame.clip_draw(0, 0, self.width, self.height, self.x, self.y, self.size, self.size)