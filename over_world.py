from pico2d import load_image


# 시작 맵 번호와 좌표
start_num = 120
start_x = 1800
start_y = 182

# OverWorld Class
# 맵 번호에 따라서 맵이 전환됨
class OverWorld:

    def __init__(self, player=None):
        base_path = 'resource/Maps/'
        self.image = load_image(f'{base_path}TheLegendofZeldaOverworldOverworldFirstQuest.png')
        self.num = start_num
        self.x = start_x
        self.y = start_y
        self.Camera_x = player.x
        self.Camera_y = player.y
        self.width = 256
        self.height = 175


    def draw(self):
        self.image.clip_draw(0,0,self.width,self.height, self.Camera_x,self.Camera_y, 1280,880)

    def update(self):
        pass