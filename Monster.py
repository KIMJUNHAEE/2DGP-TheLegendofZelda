from pico2d import *
import game_world
import MD
import config

class Monster:
    def __init__(self, x, y, name):
        self.name = name
        self.x, self.y = x, y
        self.prev_x, self.prev_y = self.x, self.y
        self.hp = 0
        self.frame_index = 0
        self.frame_time = get_time()  # 초기화 시점 기록
        self.frame_interval = 0.5
        self.width = 0
        self.height = 0
        self.size = 0
        self.direction = 4 # 1 : up 2 : down 3 : left 4 : right
        self.LRframes = []
        self.UDframes = []

        base_path = 'resource/Enemies/'
        if self.name == 'Octorok':
            self.hp = MD.OctorokHp
            self.width = MD.OctorokWidth
            self.height = MD.OctorokHeight
            self.size = MD.OctorokSize
            self.LRframes = [load_image(f'{base_path}OctorokLR{i + 1}.png') for i in range(MD.OctorokFrame_count)]
            self.UDframes = [load_image(f'{base_path}OctorokUD{i + 1}.png') for i in range(MD.OctorokFrame_count)]

    def get_bb(self):
        half_size = self.size // 2
        return (self.x - half_size, self.y - half_size,
                self.x + half_size, self.y + half_size)

    def update(self):
        if self.hp <= 0:
            game_world.remove_object(self)
            game_world.remove_collision_object(self)
            return
        # 애니메이션 프레임 업데이트
        current_time = get_time()
        if current_time - self.frame_time >= self.frame_interval:
            if self.name == 'Octorok':
                if self.direction == 1 or self.direction == 2:
                    self.frame_index = (self.frame_index + 1) % len(self.UDframes)
                    self.frame_time = current_time
                elif self.direction == 3 or self.direction == 4:
                    self.frame_index = (self.frame_index + 1) % len(self.LRframes)
                    self.frame_time = current_time

    def draw(self):
        if self.name == 'Octorok':
            if self.direction == 1:
                self.UDframes[self.frame_index].clip_composite_draw(0, 0, self.width, self.height, 0, 'v', self.x, self.y, self.size, self.size)
            elif self.direction == 2:
                self.UDframes[self.frame_index].clip_draw(0, 0, self.width, self.height, self.x, self.y, self.size, self.size)
            elif self.direction == 3:
                self.LRframes[self.frame_index].clip_draw(0, 0, self.width, self.height, self.x, self.y, self.size,self.size)
            elif self.direction == 4:
                self.LRframes[self.frame_index].clip_composite_draw(0, 0, self.width, self.height, 0, 'h', self.x, self.y, self.size, self.size)

        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'monster:obstacle':
            self.x = self.prev_x
            self.y = self.prev_y

        elif group == 'attack_range:monster':
            self.hp -= other.damage
