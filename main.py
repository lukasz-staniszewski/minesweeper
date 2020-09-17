import pygame as pg
pg.init()

if __name__ == "__main__":
    pg.display.set_icon(pg.image.load("gui_files/bomb.png"))
    pg.display.set_mode((1280, 720))
    pg.display.set_caption("MINESWEEPER")
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()
