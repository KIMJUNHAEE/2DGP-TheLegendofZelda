from pico2d import *
import game_world
import MD
import config
import random
import game_framework
import math

class MonsterDead:
    def __init__(self, x, y, Monster):
        self.x, self.y = x, y
        self.name = Monster.name
        self.frame_index = 0
        self.frame_time = get_time()
        self.frame_interval = 0.2  # 각 프레임 간격 (초)

        base_path = 'resource/Enemies/'
        if self.name == 'Octorok':
            self.width = MD.OctorokWidth
            self.height = MD.OctorokHeight
            self.size = MD.OctorokSize
            self.frames = [load_image(f'{base_path}MDead{i + 1}.png') for i in range(4)]
        elif self.name == 'Tektite':
            self.width = MD.TektiteWidth
            self.height = MD.TektiteHeight
            self.size = MD.TektiteSize
            self.frames = [load_image(f'{base_path}MDead{i + 1}.png') for i in range(4)]

    def update(self):
        current_time = get_time()
        if current_time - self.frame_time >= self.frame_interval:
            self.frame_index += 1
            self.frame_time = current_time

        if self.frame_index >= len(self.frames):
            game_world.remove_object(self)
            return

    def get_bb(self):
        half_size = self.size // 2
        return (self.x - half_size, self.y - half_size,
                self.x + half_size, self.y + half_size)

    def draw(self):
        if self.frame_index < len(self.frames):
            self.frames[self.frame_index].clip_draw(0, 0, 16, 16, self.x, self.y, self.size, self.size)



class Arrow:
    def __init__(self, x, y, Monster):
        self.x, self.y = x, y
        self.name = Monster.name
        self.size = 0
        self.direction = Monster.direction  # 1: up, 2: down, 3: left, 4: right
        self.frame_index = 0
        self.speed = 0
        self.range = 0
        self.damage = Monster.damage

        base_path = 'resource/Enemies/'
        if self.name == 'Octorok':
            self.image = load_image(f'{base_path}BulletOctorok.png')
            self.size = MD.OctorokAckSize
            self.speed = MD.OctorokAckSpeed
            self.range = MD.OctorokAckRange

    def update(self):
        if self.name == 'Octorok':
            distance = self.speed * game_framework.frame_time

            # 화면 경계 체크 및 제거
            half_size = self.size // 2
            if (self.x - half_size < 0 or self.x + half_size > 1280 or
                    self.y - half_size < 0 or self.y + half_size > 880):
                game_world.remove_object(self)
                game_world.remove_collision_object(self)
                return

            self.range -= distance
            if self.range <= 0:
                game_world.remove_object(self)
                game_world.remove_collision_object(self)
                return

            if self.direction == 1:  # up
                self.y += distance
            elif self.direction == 2:  # down
                self.y -= distance
            elif self.direction == 3:  # left
                self.x -= distance
            elif self.direction == 4:  # right
                self.x += distance


    def draw(self):
        if self.name == 'Octorok':
            self.image.clip_draw(0, 0, 8, 10, self.x, self.y, self.size, self.size)

        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        half_size = self.size // 2
        return (self.x - half_size, self.y - half_size,
                self.x + half_size, self.y + half_size)

    def handle_collision(self, group, other):
        if group in ['arrow:obstacle', 'player:arrow']:
            game_world.remove_object(self)
            game_world.remove_collision_object(self)


class Monster:
    def __init__(self, x, y, name, map_num=None, monster_index=None):
        self.name = name
        self.x, self.y = x, y
        self.damage = 0
        self.map_num = map_num  # 몬스터가 속한 맵 번호
        self.monster_index = monster_index  # 몬스터의 인덱스
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
        self.is_dead = False  # 죽음 상태 플래그 추가

        self.last_attack_time = 0  # 마지막 화살 발사 시간
        self.attack_interval = 0  # 화살 발사 간격 (몬스터별로 다름)

        # 이동 관련 변수 추가
        self.speed = 0  # 이동 속도
        self.move_time = get_time()
        self.direction_change_interval = 1.0  # 2초마다 방향 변경

        base_path = 'resource/Enemies/'
        if self.name == 'Octorok':
            self.hp = MD.OctorokHp
            self.width = MD.OctorokWidth
            self.height = MD.OctorokHeight
            self.size = MD.OctorokSize
            self.speed = MD.OctorokSpeed
            self.attack_interval = MD.OctorokAckInterval
            self.damage = MD.OctorokDamage
            self.LRframes = [load_image(f'{base_path}OctorokLR{i + 1}.png') for i in range(MD.OctorokFrame_count)]
            self.UDframes = [load_image(f'{base_path}OctorokUD{i + 1}.png') for i in range(MD.OctorokFrame_count)]

        elif self.name == 'Tektite':
            self.hp = MD.TektiteHp
            self.width = MD.TektiteWidth
            self.height = MD.TektiteHeight
            self.size = MD.TektiteSize
            self.speed = MD.TektiteSpeed
            self.damage = MD.TektiteDamage
            self.LRframes = [load_image(f'{base_path}Tektite{i + 1}.png') for i in range(MD.TektiteFrame_count)]
            # 점프 관련 변수 추가
            self.jump_start_time = get_time()
            self.jump_duration = 1.0
            self.base_y = self.y
            self.jump_height = 50
            self.jump_direction = random.choice([1, 2, 3, 4])



    def get_bb(self):
        half_size = self.size // 2
        return (self.x - half_size, self.y - half_size,
                self.x + half_size, self.y + half_size)

    def update(self):
        if self.hp <= 0:
            # 처치될 때 MapManager에 기록
            if hasattr(self, 'map_num') and hasattr(self, 'monster_index'):
                import play_mode
                if hasattr(play_mode, 'map_manager_obj'):
                    play_mode.map_manager_obj.add_defeated_monster(self.map_num, self.monster_index)

            game_world.remove_object(self)
            game_world.remove_collision_object(self)
            return

        self.prev_x, self.prev_y = self.x, self.y
        # 애니메이션 프레임 업데이트
        current_time = get_time()

        # 화살 발사 로직
        if self.name == 'Octorok' and current_time - self.last_attack_time >= self.attack_interval:
            self.shoot_arrow()
            self.last_attack_time = current_time

        if self.name == 'Octorok':
            # 방향 변경 로직
            if current_time - self.move_time >= self.direction_change_interval:
                self.direction = random.randint(1, 4)  # 1~4 랜덤 방향
                self.move_time = current_time

            # 이동 로직
            if self.direction == 1:  # up
                self.y += self.speed * game_framework.frame_time
            elif self.direction == 2:  # down
                self.y -= self.speed * game_framework.frame_time
            elif self.direction == 3:  # left
                self.x -= self.speed * game_framework.frame_time
            elif self.direction == 4:  # right
                self.x += self.speed * game_framework.frame_time

            # 화면 경계 제한 (1280x880 범위)
            half_size = self.size // 2
            if self.x - half_size < 0:
                self.x = half_size
                self.direction = 4  # 오른쪽으로 방향 변경
            elif self.x + half_size > 1280:
                self.x = 1280 - half_size
                self.direction = 3  # 왼쪽으로 방향 변경

            if self.y - half_size < 0:
                self.y = half_size
                self.direction = 1  # 위쪽으로 방향 변경
            elif self.y + half_size > 880:
                self.y = 880 - half_size
                self.direction = 2  # 아래쪽으로 방향 변경

            if current_time - self.frame_time >= self.frame_interval:
                if self.name == 'Octorok':
                    if self.direction == 1 or self.direction == 2:
                        self.frame_index = (self.frame_index + 1) % len(self.UDframes)
                        self.frame_time = current_time
                    elif self.direction == 3 or self.direction == 4:
                        self.frame_index = (self.frame_index + 1) % len(self.LRframes)
                        self.frame_time = current_time
        elif self.name == 'Tektite':
            # 점프 관련 변수 초기화 (생성자에서 추가 필요)
            if not hasattr(self, 'jump_start_time'):
                self.jump_start_time = current_time
                self.jump_duration = 1.0  # 점프 지속 시간
                self.base_y = self.y  # 기본 Y 좌표
                self.jump_height = 50  # 점프 높이
                self.jump_direction = random.choice([1, 2, 3, 4])  # 점프 방향

            # 점프 진행률 계산 (0~1)
            jump_progress = (current_time - self.jump_start_time) / self.jump_duration

            if jump_progress >= 1.0:  # 점프 완료
                self.y = self.base_y
                # 새로운 점프 시작
                self.jump_start_time = current_time
                self.base_y = self.y
                self.jump_direction = random.choice([1, 2, 3, 4])
                jump_progress = 0

            # 사인파를 이용한 수직 이동 (포물선 궤적)
            self.y = self.base_y + self.jump_height * math.sin(jump_progress * math.pi)

            # 수평 이동
            distance = self.speed * game_framework.frame_time
            if self.jump_direction == 1:  # up
                self.base_y += distance
            elif self.jump_direction == 2:  # down
                self.base_y -= distance
            elif self.jump_direction == 3:  # left
                self.x -= distance
            elif self.jump_direction == 4:  # right
                self.x += distance

            # 화면 경계 처리
            half_size = self.size // 2
            if self.x - half_size < 0 or self.x + half_size > 1280:
                self.jump_direction = random.choice([1, 2])
            if self.base_y - half_size < 0 or self.base_y + half_size > 880:
                self.jump_direction = random.choice([3, 4])

            # 프레임 애니메이션
            if current_time - self.frame_time >= self.frame_interval:
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

        elif self.name == 'Tektite':
            self.LRframes[self.frame_index].clip_draw(0, 0, self.width, self.height, self.x, self.y, self.size, self.size)

        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'monster:obstacle':
            self.x = self.prev_x
            self.y = self.prev_y
            self.direction = random.randint(1, 4)
            self.move_time = get_time()  # 방향 변경 시간 리셋

        elif group == 'attack_range:monster':
            if not self.is_dead:  # 아직 죽지 않았을 때만 데미지 처리
                self.hp -= other.damage
                if self.hp <= 0:
                    self.is_dead = True  # 죽음 상태로 변경
                    monsterdead = MonsterDead(self.x, self.y, self)
                    game_world.add_object(monsterdead, 1)

    def shoot_arrow(self):
        # 현재 방향으로 화살 생성
        arrow = Arrow(self.x, self.y, self)
        game_world.add_object(arrow, 1)
        game_world.add_collision_pair('player:arrow', None, arrow)
        game_world.add_collision_pair('arrow:obstacle', arrow, None)
        game_world.add_collision_pair('player:arrow', None, arrow)