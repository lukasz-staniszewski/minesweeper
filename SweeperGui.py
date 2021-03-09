import pygame as pg
import time
import Sweeper
import Timer
from Button import Button
pg.init()

WHITE_COLOR = (255, 255, 255)
RED_COLOR = (230, 0, 0)
GREEN_COLOR = (0, 179, 0)
BLACK_COLOR = (0, 0, 0)
GREY_COLOR = (225, 225, 225)
OTHER_GREY_COLOR = (200, 200, 200)
DARK_GREY_COLOR = (150, 150, 150)
SIZE = 24
SQ_SIZE = 24
HC_BOMBS = 50
GAME_LEN = 5


class SweeperGui:
    def __init__(self, window_size=(720, 720), ic_dir="gui_files/new-bomb.png",
                 caption="MINESWEEPER"):
        self.window_size = window_size
        self.screen = pg.display.set_mode(window_size)
        self.set_window_atributes(ic_dir, caption)
        self.start = (self.window_size[0] / 2 - (SIZE / 2 * SQ_SIZE),
                      self.window_size[1] / 2 - (SIZE / 2 * SQ_SIZE))
        self.digits = []
        for x in range(9):
            self.digits.append(pg.image.load(f"gui_files/digits/{x}.png"))
        self.flag_img = pg.image.load("gui_files/flag.png")
        self.was_left_clicked = False
        self.was_right_clicked = False
        self.cl_dig = []
        for x in range(10):
            self.cl_dig.append(pg.image.load(f"gui_files/cl/{x}.png"))
        self.colon = pg.image.load(f"gui_files/cl/colon.png")
        self.left_click = None
        self.right_click = None
        self.mouse_position = None

    def set_window_atributes(self, ic_dir, capt):
        pg.display.set_caption(capt)
        pg.display.set_icon(pg.image.load(ic_dir))

    def run_gui(self):
        self.screen.fill(WHITE_COLOR)
        self.draw_beg_board()
        # self.run_dev()
        self.run_user()

    def run_dev(self):
        self.game = Sweeper.Sweeper(SIZE, HC_BOMBS)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            self.mouse_position = pg.mouse.get_pos()
            self.left_click = pg.mouse.get_pressed()[0]
            full_size = SIZE * SQ_SIZE
            if (self.start[0] <= self.mouse_position[0] <= self.start[0] + full_size and
                    self.start[1] <= self.mouse_position[1] <= self.start[1] + full_size):
                if self.left_click == 1:
                    info = self.game.l_click((self.mouse_position[0] - self.start[0]) // SIZE,
                                             (self.mouse_position[1] - self.start[1]) // SIZE)
                    if info == 1:
                        self.show_bombs(False)
                        self.show_distances(True)
            pg.display.update()

    def run_user(self):
        self.Timer = Timer.Timer(GAME_LEN)
        restButton = Button(self.screen, self.window_size[0] / 2 - 25, 20,
                            icon="gui_files/glasses.png")
        self.game = Sweeper.Sweeper(SIZE, HC_BOMBS)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            if not self.game.finished:
                self.show_clock()
            self.mouse_position = pg.mouse.get_pos()
            self.left_click = pg.mouse.get_pressed()[0]
            self.right_click = pg.mouse.get_pressed()[2]
            self.perform_clicks()
            if self.Timer.isPassed():
                self.show_bombs(True)
                self.game.finished = True
            rest_info = restButton.check_button(self.mouse_position, self.left_click)
            if rest_info == 1:
                self.restartGui()
            restButton.draw_button()
            if self.left_click == 0:
                self.was_left_clicked = False
            if self.right_click == 0:
                self.was_right_clicked = False
            pg.display.update()

    def perform_clicks(self):
        full_size = SIZE * SQ_SIZE
        if ((self.start[0] <= self.mouse_position[0] <= self.start[0] + full_size)
           and (self.start[1] <= self.mouse_position[1] <= self.start[1] + full_size)):
            if (self.left_click == 1 and not self.game.finished and not self.was_left_clicked):
                info = self.game.l_click((self.mouse_position[0] - self.start[0]) // SIZE,
                                         (self.mouse_position[1] - self.start[1]) // SIZE)
                self.was_left_clicked = True
                if info == 1:
                    self.show_distances()
                elif info == 2:
                    self.show_bombs(True)
                    self.game.finished = True
                elif info == 3:
                    self.show_distances()
                    self.show_bombs(False)
                    self.game.finished = True
            elif (self.right_click == 1 and not self.game.finished
                  and not self.was_right_clicked):
                pos_x = int((self.mouse_position[0] - self.start[0]) // SIZE)
                pos_y = int((self.mouse_position[1] - self.start[1]) // SIZE)
                self.was_right_clicked = True
                if self.game.discovered_fields[pos_x][pos_y] == 0:
                    self.screen.blit(self.flag_img,
                                     (self.start[0] + pos_x * SQ_SIZE,
                                      self.start[1] + pos_y * SQ_SIZE))
                    self.game.discovered_fields[pos_x][pos_y] = 2
                elif self.game.discovered_fields[pos_x][pos_y] == 2:
                    pg.draw.rect(self.screen, GREY_COLOR,
                                 (self.start[0] + pos_x * SQ_SIZE,
                                  self.start[1] + pos_y * SQ_SIZE,
                                  SQ_SIZE, SQ_SIZE))
                    pg.draw.rect(self.screen, DARK_GREY_COLOR,
                                 (self.start[0] + pos_x * SQ_SIZE,
                                  self.start[1] + pos_y * SQ_SIZE,
                                  SQ_SIZE, SQ_SIZE), 1)
                    self.game.discovered_fields[pos_x][pos_y] = 0

    def draw_beg_board(self):
        pg.draw.rect(self.screen, GREY_COLOR, (self.start[0], self.start[1],
                                               SIZE * SQ_SIZE, SIZE * SQ_SIZE))
        for x in range(SIZE):
            for y in range(SIZE):
                pg.draw.rect(self.screen, DARK_GREY_COLOR,
                             (self.start[0] + x * SQ_SIZE,
                              self.start[1] + y * SQ_SIZE,
                              SQ_SIZE, SQ_SIZE), 1)

    def show_bombs(self, blownup):
        if blownup is True:
            bomb_img = pg.image.load("gui_files/explosion.png")
        else:
            bomb_img = pg.image.load("gui_files/bomb-24.png")
        for x in range(SIZE):
            for y in range(SIZE):
                if self.game.bombs[x][y] == 1:
                    if blownup is True:
                        pg.draw.rect(self.screen, RED_COLOR,
                                     (self.start[0] + x * SQ_SIZE,
                                      self.start[1] + y * SQ_SIZE,
                                      SQ_SIZE, SQ_SIZE))
                    else:
                        pg.draw.rect(self.screen, GREEN_COLOR,
                                     (self.start[0] + x * SQ_SIZE,
                                      self.start[1] + y * SQ_SIZE,
                                      SQ_SIZE, SQ_SIZE))
                    pg.draw.rect(self.screen, DARK_GREY_COLOR,
                                 (self.start[0] + x * SQ_SIZE,
                                  self.start[1] + y * SQ_SIZE,
                                  SQ_SIZE, SQ_SIZE), 1)
                    self.screen.blit(bomb_img, (self.start[0] + x * SQ_SIZE,
                                                self.start[1] + y * SQ_SIZE))
                    time.sleep(0.02)
                    pg.display.update()

    def show_distances(self, is_dev=False):
        for x in range(SIZE):
            for y in range(SIZE):
                if self.game.bombs[x][y] != 1:
                    if is_dev or self.game.discovered_fields[x][y] == 1:
                        pg.draw.rect(self.screen, OTHER_GREY_COLOR,
                                     (self.start[0] + x * SQ_SIZE,
                                      self.start[1] + y * SQ_SIZE,
                                      SQ_SIZE, SQ_SIZE))
                        pg.draw.rect(self.screen, DARK_GREY_COLOR,
                                     (self.start[0] + x * SQ_SIZE,
                                      self.start[1] + y * SQ_SIZE,
                                      SQ_SIZE, SQ_SIZE), 1)
                        ind = int(self.game.distances[x][y])
                        self.screen.blit(self.digits[ind],
                                         (self.start[0] + x * SQ_SIZE,
                                          self.start[1] + y * SQ_SIZE))

    def show_clock(self):
        time_left = self.Timer.get_time_left()
        minutes = time_left.seconds // 60
        seconds = time_left.seconds % 60
        dig1 = minutes // 10
        dig2 = minutes % 10
        dig3 = seconds // 10
        dig4 = seconds % 10
        pg.draw.rect(self.screen, WHITE_COLOR,
                     (5, 5, 145, 46))
        self.screen.blit(self.cl_dig[dig1], (5, 5))
        self.screen.blit(self.cl_dig[dig2], (33, 5))
        self.screen.blit(self.colon, (61, 5))
        self.screen.blit(self.cl_dig[dig3], (89, 5))
        self.screen.blit(self.cl_dig[dig4], (117, 5))

    def restartGui(self):
        self.draw_beg_board()
        self.game.restartGame()
        self.Timer.restartTimer()
