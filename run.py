import pygame as pg
from SweeperGui import SweeperGui
pg.init()

if __name__ == "__main__":
    pg.display.set_icon(pg.image.load("gui_files/bomb.png"))
    pg.display.set_mode((1280, 720))
    pg.display.set_caption("MINESWEEPER")
    gui = SweeperGui()
    gui.run_gui()
