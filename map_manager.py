# map_manager.py
import game_world
from pico2d import draw_rectangle
import config
from Monster import Monster, Arrow
from NPC import OldManNPC, FireNPC
from Item import Item

# 장애물 클래스
class Obstacle:
    def __init__(self, rect):
        # (x1, y1, x2, y2) 형태
        self.rect = rect

    def get_bb(self):
        return self.rect[0], self.rect[1], self.rect[2], self.rect[3]

    def handle_collision(self, group, other):
        pass

    def update(self):
        pass

    def draw(self):
        if config.Show_BB:
            draw_rectangle(*self.get_bb())
        elif config.Show_BB == False:
            pass

class MapManager:
    def __init__(self):
        self.map_data = {}
        self.current_map_num = 120  # over_world.py의 start_num과 일치
        self.current_obstacles = [] # 현재 맵의 장애물 객체 리스트
        self.current_monsters = []
        self.current_doors = []
        self.current_npcs = []
        self.current_items = []
        self.defeated_monsters = set()  # 처치된 몬스터를 기록하는 집합 추가
        self.load_map_data()

    def load_map_data(self):
        # over_world.py의 주석과 변수를 기반으로 맵 데이터 정의
        # 맵 1칸당 월드 좌표계 오프셋: (dx=257, dy=177)
        # 맵 스크린 좌표계 크기: (0, 0) ~ (1280, 880)

        self.map_data[1] = {
            'cam_x': 1543, 'cam_y': 1,
            'transitions': {
                'left': None, 'right': None, 'up': None, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[97] = {
            'cam_x': 1, 'cam_y': 182 + 177,
            'transitions': {
                'left': None, 'right': 98, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 0, 151, 880),
                (161, 0, 1280, 152),
                (1123, 161, 1280, 231),
                (1204, 240, 1280, 313),
                (1125, 644, 1280, 880),
                (1202, 562, 1280, 639)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[98] = {
            'cam_x': 1800 - 1542, 'cam_y': 182 + 177,
            'transitions': {
                'left': 97, 'right': 99, 'up': None, 'down': 114
            },
            'obstacles': [
                (965, 559, 1280, 880),
                (966, 0, 1280, 310),
                (0, 0, 794, 312),
                (0, 565, 792, 880)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[99] = {
            'cam_x': 1800 - 1285, 'cam_y': 182 + 177,
            'transitions': {
                'left': 98, 'right': 100, 'up': None, 'down': 115
            },
            'obstacles': [
                (1123, 642, 1280, 880),
                (646, 0, 1117, 313),
                (1122, 0, 1280, 232),
                (566, 722, 713, 880),
                (0, 560, 396, 880),
                (0, 0, 472, 312),
                (646,313,713,722)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[100] = {
            'cam_x': 1800 - 1028, 'cam_y': 182 + 177,
            'transitions': {
                'left': 99, 'right': 101, 'up': None, 'down': 116
            },
            'obstacles': [
                (0, 642, 157, 880),
                (162, 720, 314, 880),
                (245, 559, 311, 634),
                (247, 402, 313, 474),
                (246, 239, 317, 314),
                (0, 0, 151, 236),
                (164, 0, 551, 152),
                (807, 0, 873, 153),
                (970, 0, 1031, 151),
                (1128, 0, 1198, 231),
                (1203, 0, 1280, 312),
                (483, 480, 555, 554),
                (482, 319, 554, 396),
                (802, 241, 876, 313),
                (804, 403, 872, 468),
                (803, 559, 874, 632),
                (966, 403, 1037, 475),
                (483, 724, 551, 880),
                (803, 720, 873, 880),
                (965, 722, 1037, 880),
                (1123, 644, 1198, 880),
                (1204, 562, 1280, 880)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[101] = {
            'cam_x': 1800 - 771, 'cam_y': 182 + 177,
            'transitions': {
                'left': 100, 'right': 102, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 0, 1280, 158),
                (0, 169, 72, 319),
                (77, 165, 157, 314),
                (155, 167, 235, 232),
                (480, 321, 549, 389),
                (482, 483, 552, 553),
                (0, 607, 83, 880),
                (60, 565, 147, 880),
                (135, 610, 239, 880),
                (398, 770, 466, 880),
                (468, 727, 556, 880),
                (559, 805, 637, 880),
                (644, 724, 683, 880),
                (688, 771, 718, 880),
                (882, 767, 946, 880),
                (941, 728, 1005, 880),
                (1008, 772, 1038, 880),
                (1120, 769, 1188, 880),
                (1186, 726, 1280, 880)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[102] = {
            'cam_x': 1800 - 514, 'cam_y': 182 + 177,
            'transitions': {
                'left': 101, 'right': 103, 'up': None, 'down': 118
            },
            'obstacles': [
                (559, 0, 1280, 156),
                (400, 0, 557, 401),
                (401, 483, 558, 880),
                (800, 403, 877, 480),
                (959, 483, 1036, 559),
                (798, 562, 874, 641),
                (801, 243, 873, 317),
                (959, 320, 1035, 399),
                (800, 724, 881, 880),
                (961, 723, 1038, 880),
                (1121, 723, 1280, 880),
                (0, 0, 315, 152),
                (0, 725, 156, 880)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[103] = {
            'cam_x': 1800 - 257, 'cam_y': 182 + 177,
            'transitions': {
                'left': 102, 'right': 104, 'up': None, 'down': 119
            },
            'obstacles': [
                (0, 0, 957, 153),
                (1120, 0, 1197, 242),
                (1200, 0, 1280, 320),
                (239, 243, 556, 320),
                (640, 321, 875, 393),
                (239, 404, 559, 478),
                (639, 485, 883, 559),
                (240, 563, 558, 639),
                (0, 724, 554, 880),
                (642, 724, 1280, 880),
                (1122, 642, 1280, 723),
                (1202, 569, 1280, 644),
                (559, 804, 639, 880)
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
                (1201, 242, 1280, 320),
                (0, 158, 80, 320),
                (80, 158, 158, 237),

                (240, 243, 318, 320),
                (399, 242, 479, 320),
                (399, 404, 479, 476),
                (238, 404, 319, 478),
                (239, 566, 318, 640),
                (397, 569, 482, 639),
                (960, 242, 1037, 308),
                (957, 400, 1040, 475),
                (962, 565, 1039, 638),

                (0, 569, 76, 879),
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
                (158, 2, 234, 153),
                (324, 2, 393, 151),
                (486, 3, 554, 155),
                (726, 1, 794, 157),
                (885, 5, 949, 151),
                (1046, 2, 1113, 153),
                (1204, 4, 1279, 315),
                (163, 321, 238, 394),
                (163, 480, 233, 553),
                (325, 559, 395, 632),
                (324, 399, 391, 475),
                (328, 245, 390, 312),
                (481, 399, 556, 480),
                (726, 240, 790, 309),
                (727, 404, 795, 467),
                (726, 566, 794, 633),
                (883, 404, 947, 478),
                (1047, 243, 1114, 311),
                (1042, 403, 1111, 470),
                (1043, 564, 1111, 631),
                (163, 729, 232, 877),  # 1-2번째 좌표
                (318, 724, 393, 879),  # 3-4번째 좌표
                (480, 726, 556, 877),  # 5-6번째 좌표
                (720, 722, 794, 878),  # 7-8번째 좌표
                (881, 726, 952, 875),  # 9-10번째 좌표
                (1042, 723, 1117, 880),  # 11-12번째 좌표
                (1203, 563, 1276, 879),  # 13-14번째 좌표
                (2, 566, 69, 881),  # 15-16번째 좌표
                (81, 651, 162, 882),  # 17-18번째 좌표
                (0, 3, 79, 316),  # 19-20번째 좌표
                (74, 1, 155, 235)  # 21-22번째 좌표
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
                (0, 563, 75, 881),
                (80, 640, 160, 878),
                (160, 723, 557, 879),
                (0, 0, 72, 313),
                (77, 0, 152, 231),
                (161, 0, 1280, 150),
                (164, 482, 232, 555),
                (161, 321, 235, 395),
                (402, 561, 474, 634),
                (403, 399, 475, 475),
                (404, 242, 478, 315),
                (724, 484, 1280, 880)
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
                (0, 0, 1280, 150),
                (0, 482, 561, 880),
                (885, 719, 1116, 879),
                (1202, 720, 1280, 881),
                (963, 478, 1033, 554),
                (964, 323, 1036, 394)
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
                (0, 0, 876, 150),
                (1122, 2, 1201, 231),
                (1200, 9, 1280, 312),
                (801, 240, 877, 312),
                (643, 326, 714, 392),
                (483, 319, 557, 391),
                (162, 319, 240, 396),
                (165, 481, 244, 553),
                (483, 479, 553, 557),
                (642, 480, 715, 553),
                (804, 402, 876, 471),
                (804, 562, 872, 632),
                (0, 718, 76, 880),
                (162, 718, 235, 880),
                (484, 720, 556, 880),
                (642, 721, 714, 880),
                (804, 721, 953, 880),
                (1045, 723, 1278, 880),
                (1127, 638, 1278, 714),
                (1206, 560, 1280, 635)
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
                (0, 0, 474, 312),
                (0, 560, 315, 880),
                (403, 315, 480, 880),
                (483, 641, 558, 880),
                (562, 721, 956, 880),
                (1045, 722, 1280, 880),
                (1044, 241, 1280, 627),
                (484, 0, 553, 230),
                (564, 0, 1280, 153)
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

        self.map_data[113] = {
            'cam_x': 1, 'cam_y': 182,
            'transitions': {
                'left': None, 'right': 114, 'up': None, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[114] = {
            'cam_x': 258, 'cam_y': 182,
            'transitions': {
                'left': 113, 'right': 115, 'up': 98, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[115] = {
            'cam_x': 515, 'cam_y': 182,
            'transitions': {
                'left': 114, 'right': 116, 'up': 99, 'down': None
            },
            'obstacles': [

            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[116] = {
            'cam_x': 772, 'cam_y': 182,
            'transitions': {
                'left': 115, 'right': 117, 'up': 100, 'down': None
            },
            'obstacles': [
                (1202, 562, 1280, 880),  # 1-2번째 좌표
                (1126, 642, 1197, 880),  # 3-4번째 좌표
                (1126, 0, 1278, 231),  # 5-6번째 좌표
                (1204, 240, 1277, 311),  # 7-8번째 좌표
                (0, 0, 1120, 152),  # 9-10번째 좌표
                (802, 400, 874, 474),  # 11-12번째 좌표
                (805, 721, 874, 880),  # 13-14번째 좌표
                (0, 242, 554, 636),  # 15-16번째 좌표
                (0, 721, 556, 880),  # 17-18번째 좌표
                (963,721,1035,880)
            ],
            'monsters': [],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[117] = {
            'cam_x': 1029, 'cam_y': 182,
            'transitions': {
                'left': 116, 'right': 118, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 568, 79, 880),
                (86, 653, 117, 879),
                (131, 696, 153, 879),
                (161, 723, 1280, 880),
                (1122, 688, 1199, 721),
                (1164, 649, 1198, 685),
                (1202, 241, 1278, 661),
                (0, 237, 80, 319),
                (77, 170, 157, 238),
                (150, 94, 1120, 154),
                (1122, 156, 1199, 244)
            ],
            'monsters': [],
            'Door': [(641, 485, 717, 552)],
            'NPCs': [],
            'items': []
        }

        self.map_data[118] = {
            'cam_x': 1286, 'cam_y': 182,
            'transitions': {
                'left': None, 'right': 119, 'up': 102, 'down': None
            },
            'obstacles': [
                (400, 720, 1280, 880),  # 1-2번째 좌표
                (400, 0, 559, 721),  # 3-4번째 좌표
                (639, 561, 719, 640),  # 5-6번째 좌표
                (639, 402, 718, 477),  # 7-8번째 좌표
                (641, 242, 717, 318),  # 9-10번째 좌표
                (799, 323, 877, 400),  # 11-12번째 좌표
                (800, 483, 878, 560),  # 13-14번째 좌표
                (960, 562, 1040, 640),  # 15-16번째 좌표
                (961, 403, 1038, 480),  # 17-18번째 좌표
                (960, 241, 1036, 322),  # 19-20번째 좌표
                (559, 0, 1280, 159),  # 21-22번째 좌표
                (0, 0, 397, 155),  # 23-24번째 좌표
                (0, 163, 159, 237),  # 25-26번째 좌표
                (0, 240, 72, 880),  # 1-2번째 좌표
                (82, 650, 156, 880),  # 3-4번째 좌표
                (158, 804, 319, 880),  # 5-6번째 좌표
                (246, 727, 318, 803),  # 7-8번째 좌표
                (239, 405, 317, 483),  # 9-10번째 좌표
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
                (0, 3, 1121, 163),
                (1121, 166, 1197, 321),
                (1198, 318, 1277, 401),
                (1123, 561, 1199, 881),
                (0, 726, 961, 880),
                (160, 404, 232, 476),
                (401, 403, 474, 479),
                (639, 403, 709, 473),
                (642, 564, 715, 641),
                (802, 482, 875, 554),
                (801, 325, 876, 397),
                (640, 242, 715, 317),
                (1202,486,1280,880)
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
                (600, 300, 'Tektite'),
            ],
            'Door': [(326, 725, 395, 800)],
            'NPCs': [],
            'items': []
        }

        # 우측 맵 (121)
        self.map_data[121] = {
            'cam_x': 1800 + 257, 'cam_y': 182,
            'transitions': {
                'left': 120, 'right': 122, 'up': 105, 'down': None
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

        self.map_data[122] = {
            'cam_x': 1800 + 514, 'cam_y': 182,
            'transitions': {
                'left': 121, 'right': 123, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 769, 71, 880),
                (80, 688, 143, 880),
                (141, 644, 238, 880),
                (161, 605, 235, 880),
                (184, 579, 240, 880),
                (224, 577, 315, 880),
                (240, 526, 323, 880),
                (302, 501, 394, 880),
                (320, 446, 400, 880),
                (380, 421, 478, 880),
                (0, 0, 79, 160),
                (75, 0, 475, 159),
                (320, 158, 392, 240),
                (397, 156, 444, 233),
                (438, 160, 471, 202),
                (477, 0, 518, 155),
                (517, 0, 551, 124),
                (557, 0, 600, 140),
                (599, 0, 633, 158),
                (636, 0, 960, 157),
                (959, 0, 1037, 241),
                (1037, 0, 1118, 396),
                (1112, 0, 1280, 396),
                (639, 404, 715, 477),
                (718, 325, 794, 391),
                (800, 406, 872, 468),
                (721, 486, 795, 558),
                (480, 733, 529, 880),
                (530, 772, 635, 880),
                (626, 724, 1280, 880),
                (962, 686, 1033, 722),
                (985, 671, 1030, 686),
                (1026, 646, 1042, 662),
                (1041, 529, 1280, 720),
                (1065, 488, 1280, 560)
            ],
            'monsters': [
                (676,522,'Tektite'),
                (676,357,'Tektite'),
                (839,357,'Tektite'),
                (839,522,'Tektite'),
                (996,613,'Tektite')
            ],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[123] = {
            'cam_x': 1800 + 771, 'cam_y': 182,
            'transitions': {
                'left': 122, 'right': 124, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 488, 65, 880),
                (50, 529, 78, 880),
                (79, 530, 150, 880),
                (111, 509, 172, 880),
                (144, 482, 198, 880),
                (179, 495, 216, 880),
                (211, 528, 234, 880),
                (243, 573, 294, 880),
                (288, 607, 315, 880),
                (326, 646, 363, 880),
                (366, 688, 400, 880),
                (397, 689, 554, 880),
                (424, 669, 475, 689),
                (466, 648, 523, 686),
                (564, 729, 603, 880),
                (609, 769, 645, 880),
                (644, 769, 712, 880),
                (662, 749, 704, 772),
                (710, 726, 794, 880),
                (725, 686, 785, 722),
                (746, 671, 788, 712),
                (790, 646, 1280, 880),
                (800, 529, 880, 642),
                (822, 511, 882, 537),
                (869, 492, 933, 565),
                (926, 526, 961, 565),
                (962, 528, 1032, 561),
                (978, 505, 1027, 533),
                (1029, 490, 1084, 564),
                (1089, 529, 1116, 564),
                (1122, 529, 1178, 559),
                (1149, 511, 1280, 557),
                (1190, 480, 1280, 504),

                (0, 0, 40, 396),
                (40, 328, 65, 366),
                (75, 326, 116, 368),
                (116, 368, 156, 402),
                (159, 363, 200, 397),
                (195, 345, 233, 364),
                (229, 299, 264, 315),
                (265, 262, 304, 284),
                (311, 215, 345, 233),
                (353, 192, 384, 204),
                (409, 187, 432, 206),
                (432, 206, 470, 240),
                (483, 216, 506, 233),
                (506, 189, 546, 203),

                (547, 150, 555, 189),
                (556, 136, 588, 154),
                (585, 117, 598, 135),
                (599, 111, 626, 125),
                (629, 109, 662, 123),
                (666, 123, 684, 147),
                (687, 147, 710, 158),
                (720, 156, 738, 196),
                (739, 196, 762, 220),
                (762, 221, 786, 240),

                (799, 242, 824, 360),
                (824, 360, 843, 389),
                (844, 389, 868, 400),
                (872, 380, 903, 395),
                (904, 372, 914, 385),
                (918, 356, 943, 365),
                (948, 337, 972, 351),
                (972, 351, 990, 371),
                (993, 371, 1007, 391),
                (1007, 391, 1028, 400),
                (1029, 378, 1049, 389),
                (1049, 388, 1064, 394),
                (1069, 367, 1080, 375),
                (1079, 354, 1104, 366),
                (1109, 342, 1130, 350),
                (1130, 351, 1144, 359),
                (1145, 361, 1160, 382),
                (1161, 381, 1190, 399),
                (1190, 380, 1210, 399),
                (1212, 383, 1228, 398),
                (1230, 380, 1255, 393),
                (1256, 376, 1280, 400)
            ],
            'monsters': [
                (414,647,'Tektite'),
                (650,542,'Tektite'),
                (832,542,'Tektite'),
                (1058,440,'Tektite')
            ],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[124] = {
            'cam_x': 1800 + 1028, 'cam_y': 182,
            'transitions': {
                'left': 123, 'right': 125, 'up': 108, 'down': None
            },
            'obstacles': [
                (0, 480, 116, 880),
                (129, 526, 160, 880),
                (162, 531, 376, 880),
                (405, 573, 449, 880),
                (446, 608, 484, 880),
                (478, 652, 529, 880),
                (528, 692, 560, 880),
                (558, 720, 880, 880),
                (1120, 720, 1280, 880),
                (561, 0, 1280, 400),
                (163, 519, 215, 531),
                (219, 502, 314, 530),
                (231, 483, 318, 502),
                (323, 493, 364, 529),
                (381, 537, 407, 573),

                (0, 376, 30, 399),
                (35, 374, 61, 395),
                (69, 371, 104, 395),
                (109, 363, 123, 372),
                (125, 342, 147, 361),
                (155, 324, 173, 350),
                (174, 351, 194, 381),
                (202, 377, 229, 396),
                (232, 377, 268, 400),
                (276, 372, 301, 394),
                (306, 367, 344, 395),
                (344, 364, 361, 372),
                (364, 345, 395, 363),
                (378, 300, 394, 335),
                (399, 284, 424, 315),
                (428, 279, 445, 288),
                (444, 257, 466, 284),
                (458, 232, 475, 270),
                (469, 218, 502, 235),
                (506, 201, 517, 218),
                (518, 186, 559, 201)

            ],
            'monsters': [

            ],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[125] = {
            'cam_x': 1800 + 1285, 'cam_y': 182,
            'transitions': {
                'left': 124, 'right': 126, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 720, 1280, 880),
                (0, 0, 1280, 400)
            ],
            'monsters': [

            ],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[126] = {
            'cam_x': 1800 + 1542, 'cam_y': 182,
            'transitions': {
                'left': 125, 'right': 127, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 720, 1280, 880),
                (0, 0, 1280, 400)
            ],
            'monsters': [
                (439,690,'Octorok'),
                (835,530,'Octorok'),
                (1020,594,'Octorok'),
                (1124,445,'Octorok')
            ],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[127] = {
            'cam_x': 1800 + 1799, 'cam_y': 182,
            'transitions': {
                'left': 126, 'right': 128, 'up': None, 'down': None
            },
            'obstacles': [
                (0, 0, 1280, 400),
                (0, 720, 162, 880),
                (159, 608, 237, 880),
                (200, 584, 227, 605),
                (227, 565, 316, 595),
                (318, 570, 355, 604),
                (357, 602, 392, 647),
                (400, 609, 441, 640),
                (445, 584, 470, 596),
                (468, 565, 714, 593),
                (715, 569, 729, 606),
                (733, 573, 764, 603),
                (765, 603, 793, 644),
                (801, 604, 825, 629),
                (827, 591, 856, 611),
                (857, 580, 876, 607),
                (866, 563, 954, 593),
                (957, 569, 981, 599),
                (984, 573, 1005, 612),
                (1006, 604, 1038, 640),
                (1040, 609, 1065, 636),
                (1062, 596, 1080, 606),
                (1081, 582, 1103, 595),
                (1105, 563, 1130, 583),
                (1133, 573, 1166, 641),
                (1168, 610, 1197, 641),
                (1204, 607, 1243, 634),
                (1251, 582, 1280, 607),
                (1266, 567, 1280, 576),
                (178, 591, 197, 605),
                (417, 595, 441, 608),
                (1222, 588, 1247, 607)
            ],
            'monsters': [

            ],
            'Door': [],
            'NPCs': [],
            'items': []
        }

        self.map_data[128] = {
            'cam_x': 1800 + 2056, 'cam_y': 182,
            'transitions': {
                'left': 127, 'right': None, 'up': 112, 'down': None
            },
            'obstacles': [
                (0, 0, 722, 400),
                (722, 405, 752, 880),
                (0, 567, 45, 606),
                (44, 606, 74, 632),
                (83, 606, 107, 624),
                (103, 593, 138, 612),
                (148, 562, 330, 594),
                (333, 572, 365, 601),
                (365, 606, 399, 880),
                (119, 581, 142, 593),
                (699, 409, 716, 432)
            ],
            'monsters': [

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
                     ],
            'items': [(625,450, 'sword')]
        }

    def add_defeated_monster(self, map_num, monster_index):
        """처치된 몬스터를 기록"""
        self.defeated_monsters.add((map_num, monster_index))

    def is_monster_defeated(self, map_num, monster_index):
        """몬스터가 처치되었는지 확인"""
        return (map_num, monster_index) in self.defeated_monsters

    def load_obstacles(self, map_num, player):
        """현재 맵의 장애물을 game_world와 충돌 시스템에 등록"""

        # 1. 충돌 페어 완전 정리
        game_world.collision_pairs.clear()

        # 2. 기존 객체들 제거
        for obj_list in [self.current_obstacles, self.current_monsters,
                         self.current_doors, self.current_npcs, self.current_items]:
            for obj in obj_list:
                game_world.remove_object(obj)
            obj_list.clear()

        # 3. 화살들 완전 제거
        for layer in game_world.world:
            for obj in layer[:]:  # 복사본으로 순회
                if isinstance(obj, Arrow):
                    game_world.remove_object(obj)

        # 4. 플레이어 기본 충돌 페어만 재등록
        game_world.add_collision_pair('player:arrow', player, None)
        game_world.add_collision_pair('player:obstacle', player, None)
        game_world.add_collision_pair('player:monster', player, None)
        game_world.add_collision_pair('player:door', player, None)

        # 4. 새 맵의 장애물 로드
        obstacle_rects = self.get_obstacles(map_num)
        for rect in obstacle_rects:
            obstacle_obj = Obstacle(rect)
            self.current_obstacles.append(obstacle_obj)
            game_world.add_object(obstacle_obj, 0)
            game_world.add_collision_pair('player:obstacle', None, obstacle_obj)
            game_world.add_collision_pair('arrow:obstacle', None, obstacle_obj)  # 화살과 장애물 충돌 페어 추가


        # 5. 새 맵의 몬스터 로드
        monsters_info = self.get_monsters(map_num)
        for index, (x, y, name) in enumerate(monsters_info):
            if not self.is_monster_defeated(map_num, index):  # 처치되지 않은 몬스터만 생성
                monster_obj = Monster(x, y, name, map_num, index)  # map_num과 index 전달
                self.current_monsters.append(monster_obj)
                game_world.add_object(monster_obj, 1)
                game_world.add_collision_pair('player:monster', player, monster_obj)
                for obstacle in self.current_obstacles:
                    if not monster_obj.name == 'Tektite':
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