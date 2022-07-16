import pygame as pg
import time
import src.Sweeper as Sweeper
import src.Timer as Timer
from src.Button import Button
from src import constants

pg.init()


class SweeperGui:
    def __init__(
        self,
        window_size=constants.WIN_SIZE,
        ic_dir="resources/new-bomb.png",
        caption="MINESWEEPER",
    ):
        self.window_size = window_size
        self.screen = pg.display.set_mode(window_size)
        self.set_window_atributes(ic_dir, caption)

        self.start = (
            self.window_size[0] / 2
            - (constants.SIZE / 2 * constants.SQ_SIZE),
            self.window_size[1] / 2
            - (constants.SIZE / 2 * constants.SQ_SIZE),
        )

        self.load_imgs()

        self.l_clck = None
        self.was_l_clck = False
        self.r_clck = None
        self.was_r_clck = False
        self.ms_pos = None

    def load_imgs(self):
        self.digits = []
        for x in range(9):
            self.digits.append(
                pg.image.load(f"resources/digits/{x}.png")
            )

        self.cl_dig = []
        for x in range(10):
            self.cl_dig.append(pg.image.load(f"resources/cl/{x}.png"))

        self.flag_img = pg.image.load("resources/flag.png")
        self.col = pg.image.load(f"resources/cl/colon.png")

    def set_window_atributes(self, ic_dir, capt):
        pg.display.set_caption(capt)
        pg.display.set_icon(pg.image.load(ic_dir))

    def run_gui(self, run_dev=False):
        self.screen.fill(constants.WHITE_COLOR)
        self.draw_beg_board()

        if run_dev:
            self.run_dev()
        else:
            self.run_user()

    def run_dev(self):
        self.game = Sweeper.Sweeper(constants.SIZE, constants.HC_BOMBS)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            self.ms_pos = pg.mouse.get_pos()
            self.l_clck = pg.mouse.get_pressed()[0]
            full_size = constants.SIZE * constants.SQ_SIZE

            if (
                self.start[0]
                <= self.ms_pos[0]
                <= self.start[0] + full_size
                and self.start[1]
                <= self.ms_pos[1]
                <= self.start[1] + full_size
                and self.l_clck == 1
            ):
                info = self.game.l_click(
                    (self.ms_pos[0] - self.start[0]) // constants.SIZE,
                    (self.ms_pos[1] - self.start[1]) // constants.SIZE,
                )
                if info == 1:
                    self.show_bombs(False)
                    self.show_distances(True)

            pg.display.update()

    def run_user(self):
        self.Timer = Timer.Timer(constants.GAME_LEN)
        restButton = Button(
            self.screen,
            self.window_size[0] / 2 - 25,
            20,
            icon="resources/glasses.png",
        )
        self.game = Sweeper.Sweeper(constants.SIZE, constants.HC_BOMBS)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            if not self.game.finished:
                self.show_clock()

            self.ms_pos = pg.mouse.get_pos()
            self.l_clck = pg.mouse.get_pressed()[0]
            self.r_clck = pg.mouse.get_pressed()[2]
            self.perform_clicks()

            if self.Timer.isPassed():
                self.show_bombs(True)
                self.game.finished = True
            rest_info = restButton.check_button(
                self.ms_pos, self.l_clck
            )
            if rest_info == 1:
                self.restartGui()
            restButton.draw_button()
            if self.l_clck == 0:
                self.was_l_clck = False
            if self.r_clck == 0:
                self.was_r_clck = False

            pg.display.update()

    def perform_clicks(self):
        full_size = constants.SIZE * constants.SQ_SIZE

        if (
            self.start[0] <= self.ms_pos[0] <= self.start[0] + full_size
        ) and (
            self.start[1] <= self.ms_pos[1] <= self.start[1] + full_size
        ):

            if (
                self.l_clck == 1
                and not self.game.finished
                and not self.was_l_clck
            ):
                info = self.game.l_click(
                    (self.ms_pos[0] - self.start[0]) // constants.SIZE,
                    (self.ms_pos[1] - self.start[1]) // constants.SIZE,
                )
                self.was_l_clck = True
                if info == 1:
                    self.show_distances()
                elif info == 2:
                    self.show_bombs(True)
                    self.game.finished = True
                elif info == 3:
                    self.show_distances()
                    self.show_bombs(False)
                    self.game.finished = True

            elif (
                self.r_clck == 1
                and not self.game.finished
                and not self.was_r_clck
            ):
                pos_x = int(
                    (self.ms_pos[0] - self.start[0]) // constants.SIZE
                )
                pos_y = int(
                    (self.ms_pos[1] - self.start[1]) // constants.SIZE
                )
                self.was_r_clck = True

                if self.game.discovered_fields[pos_x][pos_y] == 0:
                    self.screen.blit(
                        self.flag_img,
                        (
                            self.start[0] + pos_x * constants.SQ_SIZE,
                            self.start[1] + pos_y * constants.SQ_SIZE,
                        ),
                    )
                    self.game.discovered_fields[pos_x][pos_y] = 2

                elif self.game.discovered_fields[pos_x][pos_y] == 2:
                    pg.draw.rect(
                        self.screen,
                        constants.GREY_COLOR,
                        (
                            self.start[0] + pos_x * constants.SQ_SIZE,
                            self.start[1] + pos_y * constants.SQ_SIZE,
                            constants.SQ_SIZE,
                            constants.SQ_SIZE,
                        ),
                    )
                    pg.draw.rect(
                        self.screen,
                        constants.DARK_GREY_COLOR,
                        (
                            self.start[0] + pos_x * constants.SQ_SIZE,
                            self.start[1] + pos_y * constants.SQ_SIZE,
                            constants.SQ_SIZE,
                            constants.SQ_SIZE,
                        ),
                        1,
                    )
                    self.game.discovered_fields[pos_x][pos_y] = 0

    def draw_beg_board(self):
        pg.draw.rect(
            self.screen,
            constants.GREY_COLOR,
            (
                self.start[0],
                self.start[1],
                constants.SIZE * constants.SQ_SIZE,
                constants.SIZE * constants.SQ_SIZE,
            ),
        )

        for x in range(constants.SIZE):
            for y in range(constants.SIZE):
                pg.draw.rect(
                    self.screen,
                    constants.DARK_GREY_COLOR,
                    (
                        self.start[0] + x * constants.SQ_SIZE,
                        self.start[1] + y * constants.SQ_SIZE,
                        constants.SQ_SIZE,
                        constants.SQ_SIZE,
                    ),
                    1,
                )

    def show_bombs(self, blownup):
        if blownup is True:
            bomb_img = pg.image.load("resources/explosion.png")
        else:
            bomb_img = pg.image.load("resources/bomb-24.png")

        for x in range(constants.SIZE):
            for y in range(constants.SIZE):
                if self.game.bombs[x][y] == 1:
                    if blownup is True:
                        pg.draw.rect(
                            self.screen,
                            constants.RED_COLOR,
                            (
                                self.start[0] + x * constants.SQ_SIZE,
                                self.start[1] + y * constants.SQ_SIZE,
                                constants.SQ_SIZE,
                                constants.SQ_SIZE,
                            ),
                        )

                    else:
                        pg.draw.rect(
                            self.screen,
                            constants.GREEN_COLOR,
                            (
                                self.start[0] + x * constants.SQ_SIZE,
                                self.start[1] + y * constants.SQ_SIZE,
                                constants.SQ_SIZE,
                                constants.SQ_SIZE,
                            ),
                        )
                    pg.draw.rect(
                        self.screen,
                        constants.DARK_GREY_COLOR,
                        (
                            self.start[0] + x * constants.SQ_SIZE,
                            self.start[1] + y * constants.SQ_SIZE,
                            constants.SQ_SIZE,
                            constants.SQ_SIZE,
                        ),
                        1,
                    )
                    self.screen.blit(
                        bomb_img,
                        (
                            self.start[0] + x * constants.SQ_SIZE,
                            self.start[1] + y * constants.SQ_SIZE,
                        ),
                    )

                    time.sleep(0.02)
                    pg.display.update()

    def show_distances(self, is_dev=False):
        for x in range(constants.SIZE):
            for y in range(constants.SIZE):
                if self.game.bombs[x][y] != 1 and (
                    is_dev or self.game.discovered_fields[x][y] == 1
                ):
                    pg.draw.rect(
                        self.screen,
                        constants.OTHER_GREY_COLOR,
                        (
                            self.start[0] + x * constants.SQ_SIZE,
                            self.start[1] + y * constants.SQ_SIZE,
                            constants.SQ_SIZE,
                            constants.SQ_SIZE,
                        ),
                    )
                    pg.draw.rect(
                        self.screen,
                        constants.DARK_GREY_COLOR,
                        (
                            self.start[0] + x * constants.SQ_SIZE,
                            self.start[1] + y * constants.SQ_SIZE,
                            constants.SQ_SIZE,
                            constants.SQ_SIZE,
                        ),
                        1,
                    )
                    ind = int(self.game.distances[x][y])
                    self.screen.blit(
                        self.digits[ind],
                        (
                            self.start[0] + x * constants.SQ_SIZE,
                            self.start[1] + y * constants.SQ_SIZE,
                        ),
                    )

    def show_clock(self):
        time_left = self.Timer.get_time_left()
        minutes = time_left.seconds // 60
        seconds = time_left.seconds % 60
        dig1 = minutes // 10
        dig2 = minutes % 10
        dig3 = seconds // 10
        dig4 = seconds % 10

        pg.draw.rect(
            self.screen, constants.WHITE_COLOR, (5, 5, 145, 46)
        )
        self.screen.blit(self.cl_dig[dig1], (5, 5))
        self.screen.blit(self.cl_dig[dig2], (33, 5))
        self.screen.blit(self.col, (61, 5))
        self.screen.blit(self.cl_dig[dig3], (89, 5))
        self.screen.blit(self.cl_dig[dig4], (117, 5))

    def restartGui(self):
        self.draw_beg_board()
        self.game.restartGame()
        self.Timer.restartTimer()
