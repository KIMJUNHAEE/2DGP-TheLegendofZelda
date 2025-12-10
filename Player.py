from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_UP, SDLK_DOWN

import game_framework
from state_machine import StateMachine
import config
import game_world




# player의 Run Speed 계산
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

#화면 크기
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 880

# 이벤트 체크 함수
# 상하좌우 이동
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def attack(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE and config.get_sword

def get_item_event(e):
    return e[0] == 'GET_ITEM'

def hurt_event(e):
    return e[0] == 'HURT'

class Hurt:
    def __init__(self, player):
        self.player = player
        self.start_time = 0
        self.duration = 0.5  # 1초간 밀려남
        self.knockback_speed = 800  # 밀려나는 속도
        self.hurt_direction = 0  # 밀려나는 방향

    def enter(self, e):
        self.start_time = get_time()
        self.player.frame = 0
        self.player.frame_time = get_time()
        self.player.Hurt = True

    def exit(self, e):
        self.player.Hurt = False
        config.cant_control = False


    def do(self):
        current_time = get_time()

        # 애니메이션 프레임 업데이트
        if current_time - self.player.frame_time >= 0.1:
            self.player.frame = (self.player.frame + 1) % 4
            self.player.frame_time = current_time

        # 밀려나는 이동 처리
        elapsed_time = current_time - self.start_time
        if elapsed_time < self.duration:
            # 시간이 지날수록 속도 감소 (감속 효과)
            speed_factor = max(0, 1 - elapsed_time / self.duration)
            move_speed = self.knockback_speed * speed_factor * game_framework.frame_time

            if self.hurt_direction == 1:  # Up으로 밀려남
                self.player.y += move_speed
            elif self.hurt_direction == 2:  # Down으로 밀려남
                self.player.y -= move_speed
            elif self.hurt_direction == 3:  # Left로 밀려남
                self.player.x -= move_speed
            elif self.hurt_direction == 4:  # Right로 밀려남
                self.player.x += move_speed
        else:
            # 1초가 지나면 Idle 상태로 복귀하고 모든 상태 초기화
            self.player.state_machine.cur_state = self.player.IDLE
            self.player.Hurt = False
            config.cant_control = False

    def draw(self):
        # 피격 애니메이션 그리기 (깜빡임 효과 제거)
        if self.player.face_dir == 1:  # Up
            self.player.LinkUpHurtFrames1[self.player.frame].clip_draw(0, 0, 16, 16, self.player.x, self.player.y,
                                                                       self.player.size, self.player.size)
        elif self.player.face_dir == 2:  # Down
            self.player.LinkDownHurtFrames1[self.player.frame].clip_draw(0, 0, 16, 16, self.player.x, self.player.y,
                                                                         self.player.size, self.player.size)
        elif self.player.face_dir == 3:  # Left
            self.player.LinkLRHurtFrames1[self.player.frame].clip_composite_draw(0, 0, 16, 16, 0, 'h',
                                                                                 self.player.x, self.player.y,
                                                                                 self.player.size, self.player.size)
        elif self.player.face_dir == 4:  # Right
            self.player.LinkLRHurtFrames1[self.player.frame].clip_draw(0, 0, 16, 16, self.player.x, self.player.y,
                                                                       self.player.size, self.player.size)

class GetItem:
    def __init__(self, player):
        self.player = player
        self.frame = 0
        self.start_time = 0
        self.duration = 2.0
        self.animation_complete = False  # 애니메이션 완료 플래그 추가

    def enter(self, e):
        self.frame = 0
        self.start_time = get_time()
        self.player.frame_time = get_time()
        self.animation_complete = False

    def exit(self, e):
        pass

    def do(self):
        current_time = get_time()

        # 애니메이션이 완료되지 않았을 때만 프레임 업데이트
        if not self.animation_complete and current_time - self.player.frame_time >= self.player.frame_interval:
            self.frame += 1
            self.player.frame_time = current_time

            # 프레임이 2에 도달하면 애니메이션 완료
            if self.frame >= 2:
                self.frame = 1  # 마지막 프레임 고정
                self.animation_complete = True

        # 2초가 지났는지 확인
        if current_time - self.start_time >= self.duration:
            self.player.state_machine.cur_state = self.player.IDLE

    def draw(self):
        self.player.GetItemFRAME[self.frame].clip_draw(0,0,16,16,self.player.x,self.player.y,self.player.size,self.player.size)
        if config.Show_BB:
            draw_rectangle(*self.player.get_bb())

class AttackRange:
    def __init__(self, player_x, player_y, attack_dir, damage):
        if attack_dir == 1:  # Up
            self.x = player_x
            self.y = player_y + 40
        elif attack_dir == 2:  # Down
            self.x = player_x
            self.y = player_y - 40
        elif attack_dir == 3:  # Left
            self.x = player_x - 40
            self.y = player_y
        elif attack_dir == 4:  # Right
            self.x = player_x + 40
            self.y = player_y

        self.x1 = self.x - 15
        self.y1 = self.y - 15
        self.x2 = self.x + 15
        self.y2 = self.y + 15
        self.damage = damage

    def draw(self):
        if config.Show_BB:
            draw_rectangle(self.x1, self.y1, self.x2, self.y2)

    def update(self):
        pass

    def get_bb(self):
        return self.x1, self.y1, self.x2, self.y2

    def handle_collision(self,group, other):
        if group == 'attack_range:monster':
            game_world.remove_object(self)
            game_world.remove_collision_object(self)

class Attack:
    def __init__(self, player):
        self.player = player
        self.attack_dir = 0

    def enter(self, e):
        if attack(e):
            if self.player.face_dir == 1:
                self.attack_dir = 1
            elif self.player.face_dir == 2:
                self.attack_dir = 2
            elif self.player.face_dir == 3:
                self.attack_dir = 3
            elif self.player.face_dir == 4:
                self.attack_dir = 4
        global attack_range
        attack_range = AttackRange(self.player.x, self.player.y, self.attack_dir, self.player.damage)
        game_world.add_object(attack_range, 1)
        for obj in game_world.world[1]:  # 몬스터들이 1번 레이어에 있음
            if hasattr(obj, 'name') or obj.__class__.__name__ == 'Ganon':
                game_world.add_collision_pair('attack_range:monster', attack_range, obj)

        self.player.frame = 0  # 프레임 초기화
        self.player.frame_time = get_time()  # 진입 시 시간 기록

    def exit(self, e):
        pass

    def do(self):
        self.player.attack_sound.play()

        # 현재 시간 확인
        current_time = get_time()
        # 설정된 간격이 지났을 때만 프레임 변경
        if current_time - self.player.frame_time >= self.player.Attack_frame_interval:
            self.player.frame = (self.player.frame + 1) % 4
            self.player.frame_time = current_time  # 시간 업데이트
            if self.player.frame == 0:  # 한 사이클이 끝났을 때
                self.player.state_machine.cur_state = self.player.IDLE
                game_world.remove_object(attack_range)
                game_world.remove_collision_object(attack_range)

    def draw(self):
        # 공격 애니메이션 그리기
        if self.attack_dir == 1:  # Up
            self.player.UpAttackFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)
            self.player.swordX = self.player.x
            self.player.swordY = self.player.y + 40
            self.player.UpSwordFRAME[self.player.frame - 1].clip_draw(0,0,8,12,self.player.swordX,self.player.swordY,30,30)
        elif self.attack_dir == 2:  # Down
            self.player.DownAttackFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)
            self.player.swordX = self.player.x + 3
            self.player.swordY = self.player.y - 40
            self.player.DownSwordFRAME[self.player.frame - 1].clip_draw(0,0,8,11,self.player.swordX,self.player.swordY,30,30)
        elif self.attack_dir == 3:  # Left
            self.player.LRAttackFRAME[self.player.frame].clip_composite_draw(0,0,self.player.width,self.player.height,0,'h',self.player.x,self.player.y,self.player.size,self.player.size)
            self.player.swordX = self.player.x - 40
            self.player.swordY = self.player.y - 1
            self.player.LRSwordFRAME[self.player.frame - 1].clip_composite_draw(0,0,11,16,0,'h',self.player.swordX,self.player.swordY,30,30)
        elif self.attack_dir == 4:  # Right
            self.player.LRAttackFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)
            self.player.swordX = self.player.x + 40
            self.player.swordY = self.player.y - 1
            self.player.LRSwordFRAME[self.player.frame - 1].clip_draw(0,0,11,16,self.player.swordX,self.player.swordY,30,30)


class RightLeft:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e):
            self.player.RL_dir = 1
            self.player.face_dir = 4
        elif left_down(e):
            self.player.RL_dir = -1
            self.player.face_dir = 3

        self.player.frame = 0  # 프레임 초기화
        self.player.frame_time = get_time()  # 진입 시 시간 기록

    def exit(self, e):
        pass

    def do(self):
        # 현재 시간 확인
        current_time = get_time()
        # 설정된 간격이 지났을 때만 프레임 변경
        if current_time - self.player.frame_time >= self.player.frame_interval:
            self.player.frame = (self.player.frame + 1) % 2
            self.player.frame_time = current_time  # 시간 업데이트

        # 새로운 위치 계산
        new_x = self.player.x + self.player.speed * self.player.RL_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.player.x = new_x

    def draw(self):
        # 좌우 이동 시 같은 LRFRAME 사용, 방향에 따라 flip 가능
        if self.player.RL_dir == 1:  # right
            self.player.LRFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)
        else:  # RL_dir == -1: # left
            self.player.LRFRAME[self.player.frame].clip_composite_draw(0,0,self.player.width,self.player.height,0,'h',self.player.x,self.player.y,self.player.size,self.player.size)

class UpDown:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if up_down(e):
            self.player.UD_dir = 1
            self.player.face_dir = 1
        elif down_down(e):
            self.player.UD_dir = -1
            self.player.face_dir = 2

        self.player.frame = 0 # 프레임 초기화
        self.player.frame_time = get_time()  # 진입 시 시간 기록

    def exit(self, e):
        pass

    def do(self):
        # 현재 시간 확인
        current_time = get_time()
        # 설정된 간격이 지났을 때만 프레임 변경
        if current_time - self.player.frame_time >= self.player.frame_interval:
            self.player.frame = (self.player.frame + 1) % 2
            self.player.frame_time = current_time  # 시간 업데이트

        # 새로운 위치 계산
        new_y = self.player.y + self.player.speed * self.player.UD_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.player.y = new_y

    def draw(self):
        if self.player.UD_dir == 1: # up
            self.player.UPFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)
        else: # UD_dir == -1: # down
            self.player.DOWNFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self,e):
        pass

    def exit(self,e):
        pass

    def do(self):
        pass

    def draw(self):
        # Idle 상태일 때 face_dir에 따라 마지막으로 바라보던 방향의 이미지를 그림
        # UPFRAME과 DOWNFRAME의 방향이 반대인 것 같아 수정했습니다.
        if self.player.face_dir == 1: # 정면 (Up)
            self.player.UPFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x, self.player.y,self.player.size,self.player.size)
        elif self.player.face_dir == 2: # 후면 (Down)
            self.player.DOWNFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x, self.player.y,self.player.size,self.player.size)
        elif self.player.face_dir == 3: # 좌측
            self.player.LRFRAME[self.player.frame].clip_composite_draw(0,0,self.player.width,self.player.height,0,'h',self.player.x, self.player.y,self.player.size,self.player.size)
        elif self.player.face_dir == 4: # 우측
            self.player.LRFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x, self.player.y,self.player.size,self.player.size)


class player:
    # music
    get_item_sound = None
    attack_sound = None
    hurt_sound = None

    def __init__(self):
        # 플레이어 좌표
        self.x, self.y = 640, 440
        self.hp = 10
        self.MaxHp = 32 # Max = 32
        self.prev_x, self.prev_y = self.x, self.y
        self.width, self.height = 16, 16
        self.UD_dir = 0
        self.RL_dir = 0
        self.face_dir = 2 # / 1: Up / 2: Down / 3: Left / 4: Right
        self.speed = 2
        self.frame = 0
        self.size = 50
        self.swordX = 0
        self.swordY = 0
        self.damage = 1

        self.God = False
        self.god_start_time = 0  # 무적 시작 시간 추가
        self.GodTime = 3.0  # 무적 지속 시간 (1초)

        self.HurtTime = 1.0
        self.Hurt = False

        # 애니메이션 타이밍 변수 추가
        self.frame_time = 0
        self.frame_interval = 0.2  # 0.2초마다 프레임 변경
        self.Attack_frame_interval = 0.12  # 공격 애니메이션 프레임 변경 간격

        # 이미지 파일 경로 수정
        base_path = 'resource/LinkFrame/'
        base_path2 = 'resource/Items/'
        # 각 방향 프레임 개수 (필요에 맞게 수정)
        up_count = 2
        down_count = 2
        lr_count = 2
        attack_count = 4
        get_Item_count = 2

        player.get_item_sound = load_wav('sound/BG/SmallItemGet.mp3')
        player.attack_sound = load_wav('sound/LOZ_Complete_201609/LOZ_Sword_Slash.wav')
        player.attack_sound.set_volume(32)
        player.hurt_sound = load_wav('sound/LOZ_Complete_201609/LOZ_Link_Hurt.wav')

        self.UPFRAME = [load_image(f'{base_path}Link{i + 5}.png') for i in range(up_count)]
        self.DOWNFRAME = [load_image(f'{base_path}Link{i + 1}.png') for i in range(down_count)]
        self.LRFRAME = [load_image(f'{base_path}Link{i + 3}.png') for i in range(lr_count)]

        self.UpAttackFRAME = [load_image(f'{base_path}LinkUpAck{i + 1}.png') for i in range(attack_count)]
        self.DownAttackFRAME = [load_image(f'{base_path}LinkDownAck{i + 1}.png') for i in range(attack_count)]
        self.LRAttackFRAME = [load_image(f'{base_path}LinkLRAck{i + 1}.png') for i in range(attack_count)]
        self.UpSwordFRAME = [load_image(f'{base_path}UpSword{i + 1}.png') for i in range(attack_count - 1)]
        self.DownSwordFRAME = [load_image(f'{base_path}DownSword{i + 1}.png') for i in range(attack_count - 1)]
        self.LRSwordFRAME = [load_image(f'{base_path}LRSword{i + 1}.png') for i in range(attack_count - 1)]
        self.GetItemFRAME = [load_image(f'{base_path2}GetItem{i + 1}.png') for i in range(get_Item_count)]

        self.LinkDownHurtFrames1 = [load_image(f'{base_path}LinkDownHurt{i + 1}.png') for i in range(4)]
        self.LinkUpHurtFrames1 = [load_image(f'{base_path}LinkUpHurt{i + 1}.png') for i in range(4)]
        self.LinkLRHurtFrames1 = [load_image(f'{base_path}LinkLRHurt{i + 1}.png') for i in range(4)]
        self.LinkDownHurtFrames2 = [load_image(f'{base_path}LinkDownHurt{i + 5}.png') for i in range(4)]
        self.LinkUpHurtFrames2 = [load_image(f'{base_path}LinkUpHurt{i + 5}.png') for i in range(4)]
        self.LinkLRHurtFrames2 = [load_image(f'{base_path}LinkLRHurt{i + 5}.png') for i in range(4)]

        self.IDLE = Idle(self)
        self.UPDOWN = UpDown(self)
        self.RIGHTLEFT = RightLeft(self)
        self.ATTACK = Attack(self)
        self.GetItem = GetItem(self)
        self.HURT = Hurt(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    up_down: self.UPDOWN,
                    down_down: self.UPDOWN,
                    right_down: self.RIGHTLEFT,
                    left_down: self.RIGHTLEFT,
                    attack: self.ATTACK,
                    get_item_event: self.GetItem,
                    hurt_event: self.HURT
                },
                self.UPDOWN: {
                    up_up: self.IDLE,
                    down_up: self.IDLE,
                    right_down: self.RIGHTLEFT,
                    left_down: self.RIGHTLEFT,
                    up_down: self.UPDOWN,
                    down_down: self.UPDOWN,
                    attack: self.ATTACK,
                    get_item_event: self.GetItem,
                    hurt_event: self.HURT
                },
                self.RIGHTLEFT: {
                    right_up: self.IDLE,
                    left_up: self.IDLE,
                    up_down: self.UPDOWN,
                    down_down: self.UPDOWN,
                    right_down: self.RIGHTLEFT,
                    left_down: self.RIGHTLEFT,
                    attack: self.ATTACK,
                    get_item_event: self.GetItem,
                    hurt_event: self.HURT
                },
                self.ATTACK: {
                    get_item_event: self.GetItem,
                    hurt_event: self.HURT
                },
                self.GetItem: {
                    hurt_event: self.HURT
                },
                self.HURT: {
                }
            }
        )

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def update(self):
        self.prev_x, self.prev_y = self.x, self.y
        self.state_machine.update()

        # 무적 시간 체크
        if self.God:
            current_time = get_time()
            if current_time - self.god_start_time >= self.GodTime:
                self.God = False


    def draw(self):
        self.state_machine.draw()
        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        half_col_size = 25  # 충돌 박스 크기 조절 (size 50의 절반이 25이므로)
        return (
            self.x - half_col_size,  # left
            self.y - half_col_size,  # bottom
            self.x + half_col_size,  # right
            self.y + half_col_size  # top
        )

    def handle_collision(self,group, other):
        global get_item_sound
        if group == 'player:obstacle':
            self.x = self.prev_x
            self.y = self.prev_y
        elif group == 'player:door':
            self.door_collision = True
        elif group == 'player:item':
            if not other.should_remove:
                if other.item_type == 'sword':
                    config.get_sword = True
                else:
                    print(f"아이템 획득: {other.item_type}")
                get_item_event = ('GET_ITEM', None)
                player.get_item_sound.play()
                self.state_machine.handle_state_event(get_item_event)

        elif group == 'player:monster':
            if not self.God:
                self.hurt_sound.play()
                self.hp -= other.damage
                self.God = True
                self.god_start_time = get_time()
                config.cant_control = True

                dx = self.x - other.x
                dy = self.y - other.y

                if abs(dx) > abs(dy):
                    # 좌우 방향으로 밀려남
                    self.HURT.hurt_direction = 4 if dx > 0 else 3
                else:
                    # 상하 방향으로 밀려남
                    self.HURT.hurt_direction = 1 if dy > 0 else 2

                hurt_event_tuple = ('HURT', None)
                self.state_machine.handle_state_event(hurt_event_tuple)

                print(f"플레이어가 몬스터에게 {other.damage}의 피해를 입었습니다. 남은 체력: {self.hp}")

        elif group == 'player:arrow':
            if not self.God:
                self.hp -= other.damage
                self.God = True
                config.cant_control = True

                dx = self.x - other.x
                dy = self.y - other.y

                if abs(dx) > abs(dy):
                    # 좌우 방향으로 밀려남
                    self.HURT.hurt_direction = 4 if dx > 0 else 3
                else:
                    # 상하 방향으로 밀려남
                    self.HURT.hurt_direction = 1 if dy > 0 else 2

                hurt_event_tuple = ('HURT', None)
                self.state_machine.handle_state_event(hurt_event_tuple)

                print(f"플레이어가 화살에게 {other.damage}의 피해를 입었습니다. 남은 체력: {self.hp}")
        elif group == 'player:zelda':
            self.x, self.y = 700, 490