from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_UP, SDLK_DOWN

import game_framework
from state_machine import StateMachine
import config

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
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

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

        self.player.frame = 0  # 프레임 초기화
        self.player.frame_time = get_time()  # 진입 시 시간 기록

    def exit(self, e):
        pass

    def do(self):
        # 현재 시간 확인
        current_time = get_time()
        # 설정된 간격이 지났을 때만 프레임 변경
        if current_time - self.player.frame_time >= self.player.frame_interval:
            self.player.frame = (self.player.frame + 1) % 4
            self.player.frame_time = current_time  # 시간 업데이트
            if self.player.frame == 0:  # 한 사이클이 끝났을 때
                self.player.state_machine.cur_state = self.player.IDLE


    def draw(self):
        # 공격 애니메이션 그리기
        if self.attack_dir == 1:  # Up
            self.player.UpAttackFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)
        elif self.attack_dir == 2:  # Down
            self.player.DownAttackFRAME[self.player.frame].clip_draw(0,0,self.player.width,self.player.height,self.player.x,self.player.y,self.player.size,self.player.size)
        elif self.attack_dir == 3:  # Left
            pass
        elif self.attack_dir == 4:  # Right
            pass


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
    def __init__(self):
        # 플레이어 좌표
        self.x, self.y = 640, 440
        self.prev_x, self.prev_y = self.x, self.y
        self.width, self.height = 16, 16
        self.UD_dir = 0
        self.RL_dir = 0
        self.face_dir = 2 # 1: 정면(Up) 2: 후면(Down) 3: 좌측 4: 우측 (초기값 후면으로 변경)
        self.speed = 2
        self.frame = 0
        self.size = 50

        # 애니메이션 타이밍 변수 추가
        self.frame_time = 0
        self.frame_interval = 0.2  # 0.2초마다 프레임 변경

        # 이미지 파일 경로 수정
        base_path = 'resource/LinkFrame/'
        # 각 방향 프레임 개수 (필요에 맞게 수정)
        up_count = 2
        down_count = 2
        lr_count = 2
        attack_count = 4

        self.UPFRAME = [load_image(f'{base_path}Link{i + 5}.png') for i in range(up_count)]
        self.DOWNFRAME = [load_image(f'{base_path}Link{i + 1}.png') for i in range(down_count)]
        self.LRFRAME = [load_image(f'{base_path}Link{i + 3}.png') for i in range(lr_count)]

        self.UpAttackFRAME = [load_image(f'{base_path}LinkUpAck{i + 1}.png') for i in range(attack_count)]
        self.DownAttackFRAME = [load_image(f'{base_path}LinkDownAck{i + 1}.png') for i in range(attack_count)]

        self.IDLE = Idle(self)
        self.UPDOWN = UpDown(self)
        self.RIGHTLEFT = RightLeft(self)
        self.ATTACK = Attack(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    up_down: self.UPDOWN,
                    down_down: self.UPDOWN,
                    right_down: self.RIGHTLEFT,
                    left_down: self.RIGHTLEFT,
                    attack: self.ATTACK
                },
                self.UPDOWN: {
                    up_up: self.IDLE,
                    down_up: self.IDLE,
                    right_down: self.RIGHTLEFT,
                    left_down: self.RIGHTLEFT,
                    # 같은 상태 내에서 방향 변경을 위해 추가
                    up_down: self.UPDOWN,
                    down_down: self.UPDOWN,
                    attack: self.ATTACK
                },
                self.RIGHTLEFT: {
                    right_up: self.IDLE,
                    left_up: self.IDLE,
                    up_down: self.UPDOWN,
                    down_down: self.UPDOWN,
                    # 같은 상태 내에서 방향 변경을 위해 추가
                    right_down: self.RIGHTLEFT,
                    left_down: self.RIGHTLEFT,
                    attack: self.ATTACK
                },
                self.ATTACK : {

                }
            }
        )

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def update(self):
        self.prev_x, self.prev_y = self.x, self.y
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        """플레이어의 충돌 박스(Bounding Box) 반환"""
        half_col_size = 25  # 충돌 박스 크기 조절 (size 50의 절반이 25이므로)

        return (
            self.x - half_col_size,  # left
            self.y - half_col_size,  # bottom
            self.x + half_col_size,  # right
            self.y + half_col_size  # top
        )

    def handle_collision(self,group, other):
        if group == 'player:obstacle':
            # update에서 저장해둔 '이전 위치'로 되돌아감
            self.x = self.prev_x
            self.y = self.prev_y
