import numpy as np
import random


class Sweeper:
    def __init__(self, size, n_of_bombs):
        self.size = size
        self.board = np.zeros((size, size))
        self.is_generated = False
        self.n_of_bombs = n_of_bombs
        self.discovered_fields = np.zeros((size, size))
        self.finished = False
        self.n_of_disc = 0

    def is_won(self):
        if self.n_of_disc == (self.size * self.size - self.n_of_bombs):
            return True
        else:
            return False

    def left_click(self, pos_x, pos_y):
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        if not self.is_generated:
            self.generate_bombs(pos_x, pos_y)
            self.generate_distances()
            self.discover_fields(pos_x, pos_y)
            self.is_generated = True
            return 1
        elif self.bombs[pos_x][pos_y] != 1 and self.discovered_fields[pos_x][pos_y] == 0:
            self.discover_fields(pos_x, pos_y)
            if self.is_won() is True:
                return 3
            else:
                return 1
        elif self.bombs[pos_x][pos_y] == 1 and self.discovered_fields[pos_x][pos_y] == 0:
            return 2
        return 0

    def discover_fields(self, pos_x, pos_y):
        if self.distances[pos_x][pos_y] != 0:
            self.discovered_fields[pos_x][pos_y] = 1
            self.n_of_disc += 1
        else:
            self.discovered_fields[pos_x][pos_y] = 1
            self.n_of_disc += 1
            bad_numbers = set([-1, self.size])
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x, y) != (0, 0) and pos_x + x not in bad_numbers and pos_y + y not in bad_numbers:
                        if self.discovered_fields[pos_x + x][pos_y + y] != 1:
                            self.discover_fields(pos_x + x, pos_y + y)

    def generate_distances(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.distances[x][y] != -1:
                    self.count_neighbours(x, y)

    def count_neighbours(self, pos_x, pos_y):
        counter = 0
        bad_numbers = set([-1, self.size])
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0) and pos_x + x not in bad_numbers and pos_y + y not in bad_numbers:
                    if self.bombs[pos_x + x][pos_y + y] == 1:
                        counter += 1
        self.distances[pos_x][pos_y] = counter

    def generate_bombs(self, pos_x, pos_y):
        self.bombs = np.zeros((self.size, self.size))
        self.distances = np.zeros((self.size, self.size))
        safe_area = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                safe_area.append((pos_x + x, pos_y + y))
        safe_area = set(safe_area)
        counter = 0
        while counter < self.n_of_bombs:
            ran_x = random.randint(0, self.size - 1)
            ran_y = random.randint(0, self.size - 1)
            if self.bombs[ran_x][ran_y] == 0:
                if (ran_x, ran_y) not in safe_area:
                    self.bombs[ran_x][ran_y] = 1
                    self.distances[ran_x][ran_y] = -1
                    counter += 1
