import pygame as pg
from src import constants

pg.init()


class Button:
    def __init__(self, screen, pos_x=0, pos_y=0, **kwargs):
        self.is_clicked = False
        self.actual_color = constants.GREY_COLOR
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.size_x = kwargs.get("size_x", constants.HC_BOMBS)
        self.size_y = kwargs.get("size_y", constants.HC_BOMBS)

        if "icon" in kwargs.keys():
            self.icon = pg.image.load(kwargs.get("icon", ""))
        else:
            self.icon = None

    def draw_button(self):
        pg.draw.rect(
            self.screen,
            self.actual_color,
            (self.pos_x, self.pos_y, self.size_x, self.size_y),
        )

        if self.icon:
            self.screen.blit(self.icon, (self.pos_x, self.pos_y))

        pg.draw.rect(
            self.screen,
            constants.DARK_GREY_COLOR,
            (self.pos_x, self.pos_y, self.size_x, self.size_y),
            1,
        )

    def check_button(self, m_pos, l_click):
        if (self.pos_x <= m_pos[0] <= self.pos_x + self.size_x) and (
            self.pos_y <= m_pos[1] <= self.pos_y + self.size_y
        ):
            if l_click == 1:
                self.actual_color = constants.DARK_GREY_COLOR
                self.is_clicked = True
                return 0

            else:
                self.actual_color = constants.OTHER_GREY_COLOR
                if self.is_clicked is True:
                    self.is_clicked = False
                    return 1
                return 0

        else:
            self.actual_color = constants.GREY_COLOR
            if self.is_clicked is True:
                self.is_clicked = False
                return 1
            return 0


if __name__ == "__main__":
    screen = pg.display.set_mode(constants.WIN_SIZE)
    screen.fill((constants.WHITE_COLOR))
    but = Button(
        screen,
        constants.HC_BOMBS,
        constants.HC_BOMBS,
        size_x=150,
        icon="resources/bomb.png",
    )

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        m_pos = pg.mouse.get_pos()
        l_click = pg.mouse.get_pressed()[0]
        info = but.check_button(m_pos, l_click)
        if info == 1:
            print("Clicked!\n")
        but.draw_button()
        pg.display.update()
