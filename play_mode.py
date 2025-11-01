from pico2d import *
import game_world
import game_framework
import over_world
from Player import player as Player
from over_world import OverWorld


# Game object class here

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global player_obj

    player_obj = player()
    game_world.add_object(player_obj, 1)

    over_world = OverWorld()
    game_world.add_object(over_world, 0)

def update():
    game_world.update()
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass