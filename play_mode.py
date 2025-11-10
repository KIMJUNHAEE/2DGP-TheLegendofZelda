from pico2d import *
import game_world
import game_framework
import over_world
from Player import player
from over_world import OverWorld
from map_manager import MapManager
from TopScreen import TopScreen

# 전역 변수 선언
player_obj = None
over_world_obj = None
map_manager_obj = None
current_map_num = 120 # 시작 맵 번호

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 1020 - event.y
            print(f"마우스 클릭 좌표: X={x}, Y={y}")
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player_obj.handle_event(event)

def init():
    global player_obj, over_world_obj, map_manager_obj, current_map_num

    # MapManager 초기화
    map_manager_obj = MapManager()

    # 시작 맵 번호 설정
    current_map_num = map_manager_obj.current_map_num  # 120
    player_obj = player()
    game_world.add_object(player_obj, 1)

    over_world_obj = OverWorld(player_obj)  # player 객체 전달
    game_world.add_object(over_world_obj,0)

    # MapManager에서 시작 카메라 위치 가져오기
    cam_x, cam_y = map_manager_obj.get_camera_pos(current_map_num)
    if cam_x is not None:
        over_world_obj.x = cam_x
        over_world_obj.y = cam_y

    game_world.add_object(over_world_obj, 0)  # 0번 레이어

    # [수정] 첫 번째 맵의 장애물들을 로드하고 충돌 시스템에 등록
    map_manager_obj.load_obstacles(current_map_num, player_obj)

    top_screen = TopScreen(player_obj)
    game_world.add_object(top_screen, 0)



def check_map_transition():
    """맵 경계를 벗어났는지 확인하고 맵을 전환 (이전 답변과 동일)"""
    global current_map_num, player_obj, over_world_obj, map_manager_obj

    new_map_num = None
    direction = None

    # 화면 경계 (트랜지션 영역) 설정
    screen_width, screen_height = 1280, 880
    # 플레이어 크기 보정값 (Player의 get_bb에 맞게 조절)
    player_size_offset = 15

    # 1. 어느 방향으로 맵을 나갔는지 확인
    if player_obj.x < player_size_offset:
        direction = 'left'
    elif player_obj.x > screen_width - player_size_offset:
        direction = 'right'
    elif player_obj.y < player_size_offset:
        direction = 'down'
    elif player_obj.y > screen_height - player_size_offset:
        direction = 'up'

    if direction:
        # 2. 해당 방향으로 다음 맵이 있는지 MapManager에 확인
        new_map_num = map_manager_obj.get_transition(current_map_num, direction)

    if new_map_num is not None:
        # 3. 맵 전환!
        print(f"맵 전환: {current_map_num} -> {new_map_num} (방향: {direction})")
        current_map_num = new_map_num
        map_manager_obj.current_map_num = new_map_num

        # 4. 새 맵의 카메라 위치로 OverWorld 업데이트
        cam_x, cam_y = map_manager_obj.get_camera_pos(current_map_num)
        if cam_x is not None:
            over_world_obj.x = cam_x
            over_world_obj.y = cam_y

        # 5. 플레이어 위치를 반대편 경계로 리셋
        if direction == 'left':
            player_obj.x = screen_width - player_size_offset - 5
        elif direction == 'right':
            player_obj.x = player_size_offset + 5
        elif direction == 'down':
            player_obj.y = screen_height - player_size_offset - 5
        elif direction == 'up':
            player_obj.y = player_size_offset + 5

        # 6. [수정] 새 맵의 장애물들을 로드 (이전 장애물은 자동 클리어됨)
        map_manager_obj.load_obstacles(current_map_num, player_obj)


def update():
    game_world.update()  # player.update()가 여기서 호출됨 (이동)
    game_world.handle_collision()  # 충돌 검사 및 처리
    check_map_transition()  # 맵 전환 검사


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    # [수정] collision_pairs도 비워주는 것이 좋습니다.
    game_world.collision_pairs.clear()


def pause(): pass


def resume(): pass