import os
import sys
import time
import random
import matplotlib.cm as cm

# Add project root to path, so pslab can be found, even if not installed:
base_dir = os.path.dirname(__file__)
sys.path = [os.path.join(base_dir, "pslab")] + sys.path

import pslab

DEBUG = False


class Enjou:
    def __init__(self, width, height, num_row, num_col):
        window = pslab.Window(width, height)
        self.window = window
        self.window.setTitle("Enjou")
        self.num_col = num_col
        self.num_row = num_row
        self.cell_width = width // num_col
        self.cell_height = height // num_row

        self.color_range = (0, 100)
        self.color_fluctor = (-3, 3)

        self.slab = pslab.Slab(self.cell_width, self.cell_height)

        if DEBUG:
            for i in range(num_col):
                for j in range(num_row):
                    color = random.randint(1, 0xFFFFFF)
                    self.draw_cell(i, j, color)

        self.cell_color = [[0 for _ in range(num_col)] for _ in range(num_row + 1)] # padding

    def draw_cell(self, i, j, color):
        self.slab.fill(color)
        self.slab.burnInto(self.window, j * self.cell_width, i * self.cell_height)

    def color_clip(self, color):
        if color < self.color_range[0]:
            return self.color_range[0]
        elif color > self.color_range[1]:
            return self.color_range[1]
        else:
            return color

    def color(self, n):
        n = self.color_clip(n)

        n = (n - self.color_range[0]) / float(self.color_range[1] - self.color_range[0]) # range to 0~1
        c = cm.hot(n)  # rgba tuple
        red = int(c[0] * 255) << 16 & 0xFF0000
        blue = int(c[1] * 255) << 8 & 0x00FF00
        green = int(c[2] * 255) & 0x0000FF
        rgb = 0x000000 | red | blue | green
        return rgb
    
    def noize(self):
        # random.randint(*self.color_fluctor)
        return int(random.normalvariate(0, self.color_fluctor[1]))

    def update_cell(self):
        for i in range(self.num_col):
            self.cell_color[-2][i] = random.randint(self.color_range[0], self.color_range[1])

        for i in range(self.num_row - 2, -1, -1):
            for j in range(self.num_col):
                    sum = (self.cell_color[i + 1][(j - 1) % self.num_col] +
                           self.cell_color[i + 1][j] +
                           self.cell_color[i + 2][j] +
                           self.cell_color[i + 1][(j + 1) % self.num_col])
                    n = 3 if i == self.num_row - 2 else 4
                    self.cell_color[i][j] = self.color_clip(sum // n + self.noize())

        if DEBUG:
            for i in range(self.num_row):
                for j in range(self.num_col):
                    print(self.cell_color[i][j], end=" ")
                print()

        for i in range(self.num_col):
            for j in range(self.num_row):
                color = self.color(self.cell_color[i][j])
                self.draw_cell(i, j, color)

    def draw(self):
        while True:
            self.update_cell()
            self.window.update()
            time.sleep(0.1)


if __name__ == '__main__':
    enjou = Enjou(200, 200, 100, 100)
    enjou.draw()
    time.sleep(2)
