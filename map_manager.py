# map_manager.py
import game_world
from pico2d import draw_rectangle
import config
from Monster import Monster
from NPC import OldManNPC, FireNPC
from Item import Item

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
        if config.Show_BB:
            draw_rectangle(*self.get_bb())
        elif config.Show_BB == False:
            pass
        # (디버깅용: from pico2d import draw_rectangle
        #  draw_rectangle(*self.get_bb()))

class MapManager:
    def __init__(self):
        self.map_data = {}
        self.current_map_num = 120  # over_world.py의 start_num과 일치
        self.current_obstacles = [] # 현재 맵의 장애물 객체 리스트
        self.current_monsters = []
        self.current_doors = []
        self.current_npcs = []
        self.current_items = []
        self.load_map_data()

    def load_map_data(self):
        # over_world.py의 주석과 변수를 기반으로 맵 데이터 정의
        # 맵 1칸당 월드 좌표계 오프셋: (dx=257, dy=177)
        # 맵 스크린 좌표계 크기: (0, 0) ~ (1280, 880)

        self.map_data[103] = {
            'cam_x': 1800 - 257, 'cam_y': 182 + 177,
            'transitions': {
                'left': 102, 'right': 104, 'up': None, 'down': 119
            },
            'obstacles': [
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        # 상단 맵 (104)
        self.map_data[104] = {
            'cam_x': 1800, 'cam_y': 182 + 177,
            'transitions': {
                'left': 103, 'right': 105, 'up': None, 'down': 120
            },
            'obstacles': [
                (0, 0, 563, 158),
                (720, 0, 874, 245),
                (874, 0, 1280, 156),
                (1121, 156, 1201, 242),
                (1201, 242, 1280, 321),
                (0, 158, 80, 318),
                (80, 158, 158, 237),

                (240, 243, 318, 320),
                (399, 242, 479, 319),
                (399, 404, 479, 476),
                (238, 404, 319, 478),
                (239, 566, 318, 640),
                (397, 562, 482, 639),
                (960, 242, 1037, 308),
                (957, 400, 1040, 475),
                (962, 565, 1039, 638),

                (0, 567, 76, 879),
                (76, 654, 156, 878),
                (160, 722, 1280, 880),
                (719, 649, 880, 721),
                (1121, 643, 1199, 722),
                (1199, 565, 1280, 720)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[105] = {
            'cam_x': 1800 + 257, 'cam_y': 182 + 177,
            'transitions': {
                'left': 104, 'right': 106, 'up': 89, 'down': 121
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[106] = {
            'cam_x': 2314, 'cam_y': 359,
            'transitions': {
                'left': 105, 'right': 107, 'up': None, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[107] = {
            'cam_x': 2571, 'cam_y': 359,
            'transitions': {
                'left': 106, 'right': 108, 'up': None, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[108] = {
            'cam_x': 2828, 'cam_y': 359,
            'transitions': {
                'left': 107, 'right': 109, 'up': None, 'down': 124
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[109] = {
            'cam_x': 3085, 'cam_y': 359,
            'transitions': {
                'left': 108, 'right': 110, 'up': None, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[110] = {
            'cam_x': 3342, 'cam_y': 359,
            'transitions': {
                'left': 109, 'right': 111, 'up': None, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[111] = {
            'cam_x': 3599, 'cam_y': 359,
            'transitions': {
                'left': 110, 'right': 112, 'up': None, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[112] = {
            'cam_x': 3856, 'cam_y': 359,
            'transitions': {
                'left': 111, 'right': None, 'up': None, 'down': 128
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[119] = {
            'cam_x': 1800 - 257, 'cam_y': 182,
            'transitions': {
                'left': 118, 'right': 120, 'up': 103, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        # 시작 맵 (120) - 젤다 시작 동굴 화면
        self.map_data[120] = {
            'cam_x': 1800, 'cam_y': 182,  # OverWorld 카메라 좌표
            'transitions': {  # 이웃 맵 번호
                'left': 119, 'right': 121, 'up': 104, 'down': None
            },
            'obstacles': [  # (x1, y1, x2, y2) - 스크린 좌표 기준
                # 맵 경계 (길이 있는 곳 제외)
                (0, 0, 1280, 160),  # 하단 경계
                (400, 724, 558, 880),  # 상단문 좌측
                (720, 482, 1280, 880),  # 상단문 우측
                (0, 0, 150, 400),  # 좌측 경계
                (1120, 150, 1280, 400),
                (0, 486, 122, 880),
                (122, 578, 219, 880),
                (219, 663, 315, 880),
                (219, 800, 400, 880)
            ],
            'monsters': [
                (600, 300, 'Octorok')
            ],
            'Door': [(326, 725, 395, 800)],
            'NPCs': [],
            'items': []
        }

        # 우측 맵 (121)
        self.map_data[121] = {
            'cam_x': 1800 + 257, 'cam_y': 182,
            'transitions': {
                'left': 120, 'right': None, 'up': 105, 'down': None
            },
            'obstacles': [
                (0,482,100,880),
                (100,576,158,880),
                (0,0,72,400),
                (72,0,151,318),
                (151,0,1280,160),

                (158,721,237,880),
                (321,722,396,880),
                (481,720,551,880),
                (723,724,794,880),
                (886,719,952,880),
                (1045,721,1115,880),
                (1202,720,1280,880),

                (164, 480, 231, 554),  # 1-2번째 좌표
                (161, 320, 239, 393),  # 3-4번째 좌표
                (321, 321, 399, 391),  # 5-6번째 좌표
                (321, 482, 398, 555),  # 7-8번째 좌표
                (482, 561, 557, 636),  # 9-10번째 좌표
                (482, 396, 559, 476),  # 11-12번째 좌표
                (484, 238, 556, 317),  # 13-14번째 좌표
                (722, 241, 797, 314),  # 15-16번째 좌표
                (722, 401, 798, 474),  # 17-18번째 좌표
                (725, 562, 795, 633),  # 19-20번째 좌표
                (888, 560, 958, 633),  # 21-22번째 좌표
                (891, 400, 957, 474),  # 23-24번째 좌표
                (886, 242, 958, 315),  # 25-26번째 좌표
                (1043, 241, 1116, 312),  # 27-28번째 좌표
                (1049, 400, 1120, 475),  # 29-30번째 좌표
                (1040, 557, 1117, 633),  # 31-32번째 좌표
            ],
            'monsters': [
                (1174, 648, 'Octorok'),
                (1163, 508, 'Octorok'),
                (1160, 362, 'Octorok'),
                (1162, 210, 'Octorok')
            ],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[200] = {
            'cam_x': 1, 'cam_y': 1,
            'transitions': {  # 이웃 맵 번호
                'left': None, 'right': None, 'up': None, 'down': None
            },
            'obstacles': [
                (0,0,151,880),
                (0,0,546,150),
                (0,732,1280,880),
                (725,0,1280,150),
                (1123,156,1280,880)
            ],
            'monsters': [],
            'Door': [(570,0,700,50)],
            'NPCs': [(625,550, 'OldMan'),
                     (525,550, 'FireNPC'),
                     (725,550, 'FireNPC')
                     ],  # NPC 정보 추가
            'items': [(625,450, 'sword')]
        }

    def load_obstacles(self, map_num, player):
        """현재 맵의 장애물을 game_world와 충돌 시스템에 등록"""

        # 1. 이전 맵의 장애물들을 game_world와 collision_pairs에서 제거
        for o in self.current_obstacles:
            game_world.remove_object(o)
            game_world.remove_collision_object(o)
        self.current_obstacles.clear()

        # 2. 이전 맵의 몬스터들을 제거
        for o in self.current_monsters:
            game_world.remove_object(o)
            game_world.remove_collision_object(o)
        self.current_monsters.clear()

        # 3. 이전 맵의 문들을 제거
        for o in self.current_doors:
            game_world.remove_object(o)
            game_world.remove_collision_object(o)
        self.current_doors.clear()

        # 이전 맵의 NPC들을 제거
        for o in self.current_npcs:
            game_world.remove_object(o)
            game_world.remove_collision_object(o)
        self.current_npcs.clear()

        # 이전 맵의 아이템들을 제거
        for o in self.current_items:
            game_world.remove_object(o)
            game_world.remove_collision_object(o)
        self.current_items.clear()

        # 4. 새 맵의 장애물 로드
        obstacle_rects = self.get_obstacles(map_num)
        for rect in obstacle_rects:
            obstacle_obj = Obstacle(rect)
            self.current_obstacles.append(obstacle_obj)
            game_world.add_object(obstacle_obj, 0)
            game_world.add_collision_pair('player:obstacle', player, obstacle_obj)

        # 5. 새 맵의 몬스터 로드
        monsters_info = self.get_monsters(map_num)
        for x, y, name in monsters_info:
            monster_obj = Monster(x, y, name)
            self.current_monsters.append(monster_obj)
            game_world.add_object(monster_obj, 1)
            game_world.add_collision_pair('player:monster', player, monster_obj)
            for obstacle in self.current_obstacles:
                game_world.add_collision_pair('monster:obstacle', monster_obj, obstacle)

        # 6. 새 맵의 문 로드
        doors_info = self.get_doors(map_num)
        for x1, y1, x2, y2 in doors_info:
            door_obj = Obstacle((x1, y1, x2, y2))
            self.current_doors.append(door_obj)
            game_world.add_object(door_obj, 0)
            game_world.add_collision_pair('player:door', player, door_obj)

        # 7. 새 맵의 NPC 로드
        npcs_info = self.get_npcs(map_num)
        for x, y, name in npcs_info:
            if name == 'OldMan':
                npc_obj = OldManNPC(x, y)
                self.current_npcs.append(npc_obj)
                game_world.add_object(npc_obj, 1)
            elif name == 'FireNPC':
                npc_obj = FireNPC(x, y)
                self.current_npcs.append(npc_obj)
                game_world.add_object(npc_obj, 1)

        items_info = self.get_items(map_num)
        for x, y, item_type in items_info:
            item_obj = Item(x, y, item_type, player)
            self.current_items.append(item_obj)
            game_world.add_object(item_obj, 1)
            game_world.add_collision_pair('player:item', player, item_obj)

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

    def get_monsters(self, map_num):
        if map_num in self.map_data:
            return self.map_data[map_num].get('monsters', [])
        return []

    def get_doors(self, map_num):
        if map_num in self.map_data:
            return self.map_data[map_num].get('Door', [])
        return []

    def get_npcs(self, map_num):
        if map_num in self.map_data:
            return self.map_data[map_num].get('NPCs', [])
        return []

    def get_items(self, map_num):
        if map_num in self.map_data:
            return self.map_data[map_num].get('items', [])
        return []