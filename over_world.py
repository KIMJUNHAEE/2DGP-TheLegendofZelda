from pico2d import load_image

class OverWorld:

    def __init__(self):
        base_path = 'resource/Maps/'
        self.image = load_image(f'{base_path}TheLegendofZeldaOverworldOverworldFirstQuest.png')

    def draw(self):
        self.image.draw(0,0)

    def update(self):
        pass