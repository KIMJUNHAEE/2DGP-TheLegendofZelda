from pico2d import *
import game_framework
import play_mode
image = None
BG = None


def init():
    global image, BG
    image = load_image('resource/Title.png')
    BG = load_music('sound/BG/TitleScreen.mp3')
    BG.set_volume(64)
    BG.repeat_play()

def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        # 엔터키(SDLK_RETURN)를 누르면 play_mode로 전환
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 1280, 1020)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass