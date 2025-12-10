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
        self.monster = Monster
        self.name = Monster.name
        self.frame_index = 0
        self.frame_time = get_time()
        self.frame_interval = 0.2  # 각 프레임 간격 (초)
        self.SC = 1

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
        if self.SC == 1:
            self.monster.Die_sound.play()
            self.SC += 1
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

    def handle_collision(self, group, other):
        # 죽은 몬스터는 충돌 처리를 하지 않음
        pass



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
                game_world.remove_collision_object(self)  # 주석 해제
                return

            if self.direction == 1:  # up
                self.y += distance
            elif self.direction == 2:  # down
                self.y -= distance
            elif self.direction == 3:  # left
                self.x -= distance
            elif self.direction == 4:  # right
                self.x += distance

            # 사거리 감소 (이동 후에 처리)
            self.range -= distance
            if self.range <= 0:
                game_world.remove_object(self)
                game_world.remove_collision_object(self)  # 주석 해제
                return

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
            # 이미 제거 중인지 확인
            if self in game_world.world[1]:  # 화살이 아직 존재하는지 확인
                game_world.remove_object(self)
                game_world.remove_collision_object(self)


class Monster:
    LRframes = None
    UDframes = None
    TektiteFrames = None

    Die_sound = None


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
        self.is_dead = False  # 죽음 상태 플래그 추가

        self.last_attack_time = 0  # 마지막 화살 발사 시간
        self.attack_interval = 0  # 화살 발사 간격 (몬스터별로 다름)

        # 이동 관련 변수 추가
        self.speed = 0  # 이동 속도
        self.move_time = get_time()
        self.direction_change_interval = 1.0  # 2초마다 방향 변경

        self.Die_sound = load_wav('sound/LOZ_Complete_201609/LOZ_Enemy_Die.wav')

        base_path = 'resource/Enemies/'
        # 몬스터 등장 이펙트
        self.AppearCount = 3
        self.Appear = True
        self.AppearFrame = [load_image(f'{base_path}MonsterAppear{i + 1}.png') for i in range(self.AppearCount)]

        if self.name == 'Octorok':
            self.hp = MD.OctorokHp
            self.width = MD.OctorokWidth
            self.height = MD.OctorokHeight
            self.size = MD.OctorokSize
            self.speed = MD.OctorokSpeed
            self.attack_interval = MD.OctorokAckInterval
            self.damage = MD.OctorokDamage
            if Monster.LRframes is None:
                Monster.LRframes = [load_image(f'{base_path}OctorokLR{i + 1}.png') for i in range(MD.OctorokFrame_count)]
            if Monster.UDframes is None:
                Monster.UDframes = [load_image(f'{base_path}OctorokUD{i + 1}.png') for i in range(MD.OctorokFrame_count)]


        elif self.name == 'Tektite':
            self.hp = MD.TektiteHp
            self.width = MD.TektiteWidth
            self.height = MD.TektiteHeight
            self.size = MD.TektiteSize
            self.speed = MD.TektiteSpeed
            self.damage = MD.TektiteDamage
            if Monster.TektiteFrames is None:
                Monster.TektiteFrames = [load_image(f'{base_path}Tektite{i + 1}.png') for i in range(MD.TektiteFrame_count)]



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

        if self.Appear:
            current_time = get_time()
            if current_time - self.frame_time >= 0.2:
                self.frame_index += 1
                self.frame_time = current_time

            if self.frame_index >= self.AppearCount:
                self.Appear = False
                self.frame_index = 0  # 애니메이션 프레임 초기화

                if self.name == 'Tektite':
                    # 점프 관련 변수들 초기화
                    self.jump_start_time = get_time()
                    self.jump_duration = 1.0  # 점프 지속 시간
                    self.rest_duration = 1.5  # 휴식 시간
                    self.is_jumping = True  # 점프 중인지 휴식 중인지 구분
                    self.start_pos = (self.x, self.y)

                    # 첫 번째 목표 위치 설정
                    target_x = self.x + random.randint(-150, 150)
                    target_y = self.y + random.randint(-150, 150)

                    # 화면 경계 제한
                    half_size = self.size // 2
                    target_x = max(half_size, min(1280 - half_size, target_x))
                    target_y = max(half_size, min(880 - half_size, target_y))

                    self.target_pos = (target_x, target_y)
            return  # 등장 애니메이션이 끝날 때까지 업데이트 중지

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
                if self.direction == 1 or self.direction == 2:
                    self.frame_index = (self.frame_index + 1) % len(self.UDframes)
                    self.frame_time = current_time
                elif self.direction == 3 or self.direction == 4:
                    self.frame_index = (self.frame_index + 1) % len(self.LRframes)
                    self.frame_time = current_time


        elif self.name == 'Tektite':
            if self.is_jumping:  # 점프 중
                jump_progress = (current_time - self.jump_start_time) / self.jump_duration

                if jump_progress >= 1.0:  # 점프 완료
                    self.x, self.y = self.target_pos
                    self.is_jumping = False  # 휴식 모드
                    self.jump_start_time = current_time  # 휴식 시작 시간 기록

                else:
                    # 점프 중 - 곡선 이동
                    t = jump_progress
                    x1, y1 = self.start_pos
                    x2, y2 = self.target_pos

                    # 선형 보간으로 기본 위치 계산
                    self.x = (1 - t) * x1 + t * x2
                    base_y = (1 - t) * y1 + t * y2

                    # 아치 효과 추가
                    arch_height = 60 * math.sin(t * math.pi)
                    self.y = base_y + arch_height

                    # 화면 경계 제한 (아치 효과 적용 후)
                    half_size = self.size // 2
                    self.y = max(half_size, min(880 - half_size, self.y))

            else:  # 점프 후 휴식
                rest_progress = (current_time - self.jump_start_time) / self.rest_duration

                if rest_progress >= 1.0:  # 휴식 완료
                    # 새로운 점프 준비
                    self.is_jumping = True
                    self.jump_start_time = current_time
                    self.start_pos = (self.x, self.y)

                    # 새로운 목표 위치 설정
                    target_x = self.x + random.randint(-150, 150)
                    target_y = self.y + random.randint(-150, 150)

                    # 화면 경계 제한
                    half_size = self.size // 2
                    target_x = max(half_size, min(1280 - half_size, target_x))
                    target_y = max(half_size, min(880 - half_size, target_y))

                    self.target_pos = (target_x, target_y)

            # 프레임 애니메이션 (점프 중일 때만)
            if self.is_jumping and current_time - self.frame_time >= 0.2:
                self.frame_index = (self.frame_index + 1) % len(self.TektiteFrames)
                self.frame_time = current_time
            elif not self.is_jumping and current_time - self.frame_time >= 0.8:  # 휴식 중에는 느리게
                self.frame_index = (self.frame_index + 1) % len(self.TektiteFrames)
                self.frame_time = current_time


    def draw(self):

        if self.Appear:
            self.AppearFrame[self.frame_index].clip_draw(0, 0, 16, 16, self.x, self.y, self.size, self.size)
            return

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
            self.TektiteFrames[self.frame_index].clip_draw(0, 0, self.width, self.height, self.x, self.y, self.size, self.size)

        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'monster:obstacle':
            #if not self.name == 'Tektite':
                self.x = self.prev_x
                self.y = self.prev_y
                self.direction = random.randint(1, 4)
                self.move_time = get_time()  # 방향 변경 시간 리셋


        elif group == 'attack_range:monster':
            if not self.is_dead:  # 아직 죽지 않았을 때만 데미지 처리
                self.hp -= other.damage
                if self.hp <= 0:
                    self.is_dead = True  # 죽음 상태로 변경
                    config.score += 1  # 몬스터 처치 시 점수 1점 증가
                    print(f"{self.name} 몬스터가 처치되었습니다! 현재 점수: {config.score}")
                    monsterdead = MonsterDead(self.x, self.y, self)
                    game_world.add_object(monsterdead, 1)

    def shoot_arrow(self):
        # 현재 방향으로 화살 생성
        arrow = Arrow(self.x, self.y, self)
        game_world.add_object(arrow, 1)
        game_world.add_collision_pair('player:arrow', None, arrow)
        game_world.add_collision_pair('arrow:obstacle', arrow, None)
