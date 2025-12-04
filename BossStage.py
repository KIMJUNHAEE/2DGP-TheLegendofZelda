from pico2d import load_image

# 시작 맵 번호와 좌표
start_num = 1
start_x = 1543
start_y = 1415

# OverWorld Class
# 맵 번호에 따라서 맵이 전환됨
# 이미지에서 맵 픽셀 크기 : 256x176
# 좌우 이동할 때 필요한 픽셀 : 257
# 상하 이동할 때 필요한 픽셀 : 177

class BossStage:
    def __init__(self, player=None):
        base_path = 'resource/Maps/'
        self.image = load_image(f'{base_path}BossStage.png')
        self.player = player

        # 화면과 맵 크기 (픽셀)
        self.screen_width = 1280
        self.screen_height = 880
        self.map_width = 2057
        self.map_height = 1417

        # 초기 카메라 위치 (맵 좌표)
        self.x = start_x
        self.y = start_y

    def draw(self):
        self.image.clip_draw(self.x, self.y, 256, 176, self.screen_width // 2, self.screen_height // 2, self.screen_width, self.screen_height)

    def update(self):
        # 필요하면 카메라를 플레이어에 따라 이동시키거나 추가 로직을 둠
        pass


