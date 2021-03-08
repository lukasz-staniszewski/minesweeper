import pygame as pg
pg.init()


class inputBox:
    def __init__(self, screen, pos_x, pos_y, **kwargs):
        self.text = ""
        self.is_typing = False
        self.block = False
        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = kwargs.get("size_x", 200)
        self.size_y = kwargs.get("size_y", 50)
        self.min_size_x = self.size_x
        self.max_size_x = self.size_x + 10 * self.size_y * 1.5
        self.font = pg.font.SysFont(None, self.size_y)

    def draw_box(self):
        if self.is_typing:
            frame_col = (26, 83, 255)
        else:
            frame_col = (255, 80, 80)
        pg.draw.rect(self.screen, (255, 255, 255),
                     (self.pos_x, self.pos_y, self.max_size_x,
                      self.size_y))
        pg.draw.rect(self.screen, frame_col,
                     (self.pos_x, self.pos_y, self.size_x,
                      self.size_y), 1)
        text = self.font.render(self.text, True, frame_col)
        self.screen.blit(text, (self.pos_x + 5,
                                self.pos_y - 7 + self.size_y / 4))

    def repair_size(self, added):
        if added is True:
            if self.size_x <= self.size_y * 0.5 * len(self.text) + 10:
                if (self.size_x + self.size_y) <= self.max_size_x:
                    self.size_x += self.size_y
        else:
            if (self.size_y * len(self.text)) / 2 < self.size_x:
                if self.size_x - self.size_y >= self.min_size_x:
                    self.size_x = self.size_x - self.size_y

    def get_text(self):
        return self.text

    def button_act(self, m_pos, l_click, key):
        if self.is_typing is False:
            if ((self.pos_x <= m_pos[0] <= self.pos_x + self.size_x)
               and (self.pos_y <= m_pos[1] <= self.pos_y + self.size_y)):
                if l_click == 1 and not self.block:
                    self.is_typing = True
                    self.block = True
                elif l_click == 0:
                    self.block = False
        else:
            if l_click == 1 and not self.block:
                self.is_typing = False
                self.block = True
            elif l_click == 0:
                self.block = False
        if key.type == pg.KEYDOWN:
            if self.is_typing:
                if key.key == pg.K_BACKSPACE:
                    self.bsp_text()
                    self.repair_size(False)
                elif key.key == pg.K_RETURN:
                    self.is_typing = False
                    self.block = False
                else:
                    self.add_text(key.unicode)
                    self.repair_size(True)

    def bsp_text(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]

    def add_text(self, char):
        if len(self.text) < 10:
            self.text += char


if __name__ == "__main__":
    screen = pg.display.set_mode((720, 720))
    screen.fill((255, 255, 255))
    box = inputBox(screen, 50, 50, size_x=10, size_y=50)
    while True:
        m_pos = pg.mouse.get_pos()
        l_click = pg.mouse.get_pressed()[0]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            info = box.button_act(m_pos, l_click, event)
        box.draw_box()
        pg.display.update()
