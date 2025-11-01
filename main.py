from pico2d import *
import game_world
import over_world
from Player import player
from over_world import OverWorld


# Game object class here

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player_obj.handle_event(event)

def reset_world():
    global player_obj

    player_obj = player()
    game_world.add_object(player_obj, 1)

    over_world = OverWorld()
    game_world.add_object(over_world, 0)

def update_world():
    game_world.update()
    pass

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
