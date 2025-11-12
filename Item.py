#아이템
from pico2d import *
import config
import game_world

class Item:
    def __init__(self, x, y, item_type, player=None):
        self.item_type = item_type
        self.x = x
        self.y = y
        self.player = player
        self.should_remove = False  # 제거 플래그 추가
        self.remove_time = 0  # 제거 시간 추가

        if self.item_type == 'sword':
            base_path = 'resource/Items/'
            self.image = load_image(f'{base_path}sword.png')

    def update(self):
        if self.should_remove and get_time() >= self.remove_time:
            game_world.remove_object(self)
            game_world.remove_collision_object(self)


    def draw(self):
        if self.item_type == 'sword':
            self.image.clip_draw(0, 0, 7, 16, self.x, self.y, 24, 50)

        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.item_type == 'sword':
            return self.x - 12, self.y - 25, self.x + 12, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:item' and not self.should_remove:
            self.remove_time = get_time() + 2.0  # 2초 후 제거
            self.should_remove = True
            self.x = self.player.x - 20
            self.y = self.player.y + 45


