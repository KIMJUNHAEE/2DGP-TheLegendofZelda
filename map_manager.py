# map_manager.py
import game_world
from pico2d import draw_rectangle

# 장애물 객체 클래스
# game_world의 충돌 시스템은 '객체'를 기반으로 동작하므로,
# 단순한 사각형 좌표가 아닌 '객체'로 만들어 등록해야 합니다.

class Obstacle:
    def __init__(self, rect):
        # rect는 (x1, y1, x2, y2) 형태
        self.rect = rect

    def get_bb(self):
        # (left, bottom, right, top) 반환
        return self.rect[0], self.rect[1], self.rect[2], self.rect[3]

    def handle_collision(self, group, other):
        # 장애물은 충돌 시 아무것도 할 필요가 없습니다.
        pass

    def update(self):
        pass  # 장애물은 업데이트할 내용이 없습니다.

    def draw(self):
        draw_rectangle(*self.get_bb())
        # (디버깅용: from pico2d import draw_rectangle
        #  draw_rectangle(*self.get_bb()))


class MapManager:
    def __init__(self):
        self.map_data = {}
        self.current_map_num = 120  # over_world.py의 start_num과 일치
        self.current_obstacles = []  # 현재 맵의 장애물 객체 리스트
        self.load_map_data()

    def load_map_data(self):
        # over_world.py의 주석과 변수를 기반으로 맵 데이터 정의
        # 맵 1칸당 월드 좌표계 오프셋: (dx=257, dy=177)
        # 맵 스크린 좌표계 크기: (0, 0) ~ (1280, 880)

        # 시작 맵 (120) - 젤다 시작 동굴 화면
        self.map_data[120] = {
            'cam_x': 1800, 'cam_y': 182,  # OverWorld 카메라 좌표
            'transitions': {  # 이웃 맵 번호
                'left': 119, 'right': 121, 'up': 104, 'down': None
            },
            'obstacles': [  # (x1, y1, x2, y2) - 스크린 좌표 기준
                # 맵 경계 (길이 있는 곳 제외)
                (0, 0, 1280, 170),  # 하단 경계
                (404, 724, 558, 880),  # 상단문 좌측
                (720, 482, 1280, 880),  # 상단문 우측
                (0, 0, 150, 400),  # 좌측 경계
                (1120, 150, 1280, 410)


                # 내부 장애물 (예시: 시작 지점의 바위와 물)
                # (200, 200, 400, 400), # 예시 돌
                # (600, 300, 700, 500)  # 예시 물
            ]
        }

        # 우측 맵 (121)
        self.map_data[121] = {
            'cam_x': 1800 + 257, 'cam_y': 182,
            'transitions': {
                'left': 120, 'right': None, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 0, 1280, 100),  # 하단
                (0, 880 - 100, 1280, 880),  # 상단
                (1180, 100, 1280, 880),  # 우측 (1180으로 수정)
                (0, 100, 100, 340),  # 좌측 하단
                (0, 540, 100, 880),  # 좌측 상단 (가운데 길)
            ]
        }

        # 상단 맵 (104)
        self.map_data[104] = {
            'cam_x': 1800, 'cam_y': 182 + 177,
            'transitions': {
                'left': None, 'right': None, 'up': None, 'down': 120
            },
            'obstacles': [
                (0, 0, 540, 100),  # 하단 좌측
                (740, 0, 1280, 100),  # 하단 우측 (가운데 길)
                (0, 880 - 100, 1280, 880),  # 상단
                (0, 100, 100, 880),  # 좌측
                (1180, 100, 1280, 880),  # 우측
            ]
        }

        # TODO: 여기에 다른 맵(105, 119 등)의 데이터도 추가해야 합니다.

    def load_obstacles(self, map_num, player):
        """현재 맵의 장애물을 game_world와 충돌 시스템에 등록"""

        # 1. 이전 맵의 장애물들을 game_world와 collision_pairs에서 제거
        for o in self.current_obstacles:
            game_world.remove_object(o)
            game_world.remove_collision_object(o)  # game_world.py에 정의된 함수
        self.current_obstacles.clear()

        # 2. 새 맵의 장애물 목록을 가져옴
        obstacle_rects = self.get_obstacles(map_num)
        if not obstacle_rects:
            return

        # 3. 새 장애물 객체를 생성하여 game_world와 collision_pairs에 추가
        for rect in obstacle_rects:
            obstacle_obj = Obstacle(rect)
            self.current_obstacles.append(obstacle_obj)
            game_world.add_object(obstacle_obj, 0)  # 0번 레이어(배경)에 추가
            # 'player:obstacle' 그룹으로 플레이어와 장애물을 충돌 등록
            game_world.add_collision_pair('player:obstacle', player, obstacle_obj)

    def get_obstacles(self, map_num):
        """현재 맵의 장애물 사각형 리스트 반환"""
        if map_num in self.map_data:
            return self.map_data[map_num]['obstacles']
        return []  # 맵 데이터가 없으면 빈 리스트 반환

    def get_transition(self, map_num, direction):
        """지정된 방향의 다음 맵 번호 반환"""
        if map_num in self.map_data:
            return self.map_data[map_num]['transitions'].get(direction)
        return None

    def get_camera_pos(self, map_num):
        """지정된 맵의 카메라 좌표 (cam_x, cam_y) 반환"""
        if map_num in self.map_data:
            data = self.map_data[map_num]
            return data['cam_x'], data['cam_y']
        return None, None  # 데이터가 없으면 None 반환