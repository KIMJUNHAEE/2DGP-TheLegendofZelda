from pico2d import *

import random
import math
import game_framework
import game_world
import config
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class GaonoArrow:
    image = None
    def load_images(self):
        base_path = 'resource/Enemies/'
        if GaonoArrow.image == None:
            GaonoArrow.image = [load_image(f'{base_path}GanonArrow{i + 1}.png') for i in range(4)]

    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.tx = target_x
        self.ty = target_y
        self.frame_count = 0
        self.frame_time = 0
        self.frame_interval = 0.1  # 0.1초마다 프레임 변경
        self.size = 40

        # 방향 계산
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.dx = dx / distance
            self.dy = dy / distance
        else:
            self.dx = self.dy = 0

        self.speed = 300  # 화살 속도
        self.load_images()

    def update(self):

        # 현재 시간 확인
        current_time = get_time()
        # 설정된 간격이 지났을 때만 프레임 변경
        if current_time - self.frame_time >= self.frame_interval:
            self.frame_count = (self.frame_count + 1) % 4
            self.frame_time = current_time  # 시간 업데이트
        self.x += self.dx * self.speed * game_framework.frame_time
        self.y += self.dy * self.speed * game_framework.frame_time

        # 화면 밖으로 나가면 제거
        if self.x < 0 or self.x > 1280 or self.y < 0 or self.y > 880:
            game_world.remove_object(self)

    def draw(self):
        if GaonoArrow.image:
            GaonoArrow.image[self.frame_count].clip_draw(0, 0, 8, 12, self.x, self.y, self.size, self.size)

        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        self.half_size = self.size / 2
        return self.x -  self.half_size, self.y -  self.half_size, self.x +  self.half_size, self.y +  self.half_size

    def handle_collision(self, group, other):
        if group == 'player:ganon_arrow':
            game_world.remove_object(self)
        elif group == 'obstacle:ganon_arrow':
            game_world.remove_object(self)


animation_names = ['Idle', 'Hit', 'Stun', 'Attack', 'Dead']


class Ganon:
    IdleImage = None
    HitImage = None
    StunImage = None
    AttackImage = None

    def load_images(self):
        base_path = 'resource/Enemies/'
        if Ganon.IdleImage == None:
            Ganon.IdleImage = load_image(f'{base_path}GanonIdle.png')
        if Ganon.HitImage == None:
            Ganon.HitImage = load_image(f'{base_path}GanonHit.png')
        if Ganon.StunImage == None:
            Ganon.StunImage = load_image(f'{base_path}GanonStun.png')
        if Ganon.AttackImage == None:
            Ganon.AttackImage = [load_image(f'{base_path}GanonAttack{i + 1}.png') for i in range(3)]

    def __init__(self):
        self.x, self.y = 640, 512
        self.nx, self.ny = 640, 512
        self.load_images()
        self.frame_size = 32
        self.state = 'Idle'

        # 투명화 관련 변수
        self.alpha = False
        self.alpha_timer = 0.0

        # 행동 카운트 (1초마다 1번씩, 총 5번 행동하기 위함)
        self.move_count = 0

        self.hp = 10
        self.StunHp = 3

        self.is_invulnerable = False
        self.invulnerable_start_time = 0
        self.invulnerable_duration = 1.0  # 1초간 무적

        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.alpha_mode()
        self.bt.run()

        if self.is_invulnerable:
            current_time = get_time()
            if current_time - self.invulnerable_start_time >= self.invulnerable_duration:
                self.is_invulnerable = False
                print("가논의 무적 상태가 해제되었습니다.")  # 디버깅용

        if self.hp <= 0:
            self.state = 'Dead'


    def draw(self):
        if not self.alpha:  # 투명화 상태가 아닐 때만 그리기
            if self.state == 'Idle':
                Ganon.IdleImage.clip_draw(0, 0, self.frame_size, self.frame_size, self.x, self.y, 100, 100)
            elif self.state == 'Hit':
                Ganon.HitImage.clip_draw(0, 0, self.frame_size, self.frame_size, self.x, self.y, 100, 100)
            elif self.state == 'Stun':
                Ganon.StunImage.clip_draw(0, 0, self.frame_size, self.frame_size, self.x, self.y, 100, 100)
            elif self.state == 'Attack':
                Ganon.IdleImage.clip_draw(0, 0, self.frame_size, self.frame_size, self.x, self.y, 100, 100)

        if config.Show_BB:
            draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'attack_range:monster':
            # 무적상태가 아닐 때만 피해를 받음
            if not self.is_invulnerable:
                self.hp -= other.damage

                # 무적상태 시작
                self.is_invulnerable = True
                self.invulnerable_start_time = get_time()

                print(f"가논이 {other.damage}의 피해를 입었습니다. 남은 체력: {self.hp}")

                if self.hp <= 0:
                    print("가논이 처치되었습니다!")
                    game_world.remove_object(self)
            else:
                print("가논이 무적상태입니다!")

    def alpha_mode(self):
        self.alpha_timer += game_framework.frame_time

        if self.alpha:
            # 투명 상태: 5.0초 유지
            if self.alpha_timer >= 5.0:
                self.alpha = False
                self.alpha_timer = 0.0
                self.move_count = 0  # 카운트 초기화
        else:
            # 보이는 상태: 1.5초 유지 (스턴 아닐 때만)
            if self.state != 'Stun' and self.alpha_timer >= 1.5:
                self.alpha = True
                self.alpha_timer = 0.0
                self.move_count = 0  # 카운트 초기화

    def is_alpha(self):
        if self.alpha:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def check_move_timing(self):
        # 5초 동안 5번 행동 (0초, 1초, 2초, 3초, 4초 시점)
        # 현재 시간이 (행동횟수 * 1.0초)를 넘겼으면 행동할 차례
        if self.move_count < 5 and self.alpha_timer >= self.move_count * 1.0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def set_random_location(self):
        self.nx = random.randint(100, 1280 - 100)
        self.ny = random.randint(100, 880 - 100)
        return BehaviorTree.SUCCESS

    def move_to(self):
        # 순간이동
        self.x = self.nx
        self.y = self.ny
        return BehaviorTree.SUCCESS

    def shoot_arrow(self):
        # 플레이어 위치 가져오기 (circular import 방지를 위해 내부 import)
        import play_mode
        if play_mode.player_obj:
            tx, ty = play_mode.player_obj.x, play_mode.player_obj.y
            arrow = GaonoArrow(self.x, self.y, tx, ty)
            game_world.add_object(arrow, 1)
            game_world.add_collision_pair('player:ganon_arrow', play_mode.player_obj, arrow)
            # 필요시 장애물 충돌 추가
            # game_world.add_collision_pair('obstacle:ganon_arrow', None, arrow)

        self.state = 'Attack'
        self.move_count += 1  # 화살까지 쏘면 행동 1회 완료로 처리
        return BehaviorTree.SUCCESS

    def is_StunHP(self):
        if self.hp <= self.StunHp:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Stun_state(self):
        self.state = 'Stun'
        self.alpha = False
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # 1. 투명화 공격 사이클 (타이밍 체크 -> 위치 설정 -> 이동 -> 발사)
        c_timing = Condition('이동 타이밍인가', self.check_move_timing)
        a_set_loc = Action('랜덤 위치 설정', self.set_random_location)
        a_move = Action('순간이동', self.move_to)
        a_shoot = Action('화살 발사', self.shoot_arrow)

        # 타이밍이 맞을 때만 이 시퀀스가 끝까지 실행됨
        attack_step = Sequence('공격 단계', c_timing, a_set_loc, a_move, a_shoot)

        # 2. 투명화 패턴 전체 구조
        c_alpha = Condition('투명화 상태인가', self.is_alpha)
        # 투명 상태면 attack_step을 계속 시도 (타이밍 맞을 때만 실행됨)
        alpha_sequence = Sequence('투명화 패턴', c_alpha, attack_step)

        # 3. 스턴 패턴
        c_stun_check = Condition('스턴 체력인가', self.is_StunHP)
        a_stun_effect = Action('스턴 상태', self.Stun_state)
        stun_sequence = Sequence('스턴 패턴', c_stun_check, a_stun_effect)

        # 4. 루트
        root = Selector('가논 행동', stun_sequence, alpha_sequence)

        self.bt = BehaviorTree(root)