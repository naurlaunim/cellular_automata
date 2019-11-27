from tkinter import *
from functools import partial
import copy
import random
import time
from cells import *


def get_points(x, y, r):
    return [(x, y-r), (x+r*3**(1/2)/2, y-r/2), (x+r*3**(1/2)/2, y+r/2), (x, y+r), (x-r*3**(1/2)/2, y+r/2), (x-r*3**(1/2)/2, y-r/2)]


def get_neighbours(x, y, r):
    w = r * 3 ** (1 / 2)
    neighbours = [(x + w/2, y - r*3/2), (x + w, y), (x + w/2, y + r*3/2), (x - w/2, y + r*3/2), (x - w, y), (x - w/2, y - r*3/2)]
    return [(round(n[0],2), round(n[1], 2)) for n in neighbours if n[0] > 1 and n[1] > 1]


class EnvCanvas(Canvas):
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)


    def view_cell(self, cell, width=2):
        self.create_polygon(cell.points, fill=cell.fill, outline=cell.outline, width=width, tag = str(cell.x)+'-'+str(cell.y))
        # self.tag_bind(str(cell.x) + '-' + str(cell.y), '<Button-1>', cell.make_alive)
        self.update()


    def view_environment(self, env):
        for cell in env.cells.values():
            self.view_cell(cell)


class Environment:
    def __init__(self, rows, columns, r):
        self.w = r * 3**(1/2)
        self.cells = {}
        x, y = self.w/2, r
        for i in range(rows):
            c = columns if i % 2 == 0 else columns - 1
            for j in range(c):
                x, y = round(x,2), round(y,2)
                self.cells[(x,y)] = EmptyCell(x,y,r)
                x += self.w
            x = self.w if i % 2 == 0 else self.w / 2
            y += r * 3/2


    def generation(self, draw):
        new_cells = {}
        for coords, cell in self.cells.items():
            new_cell = cell.step(self, draw)
            new_cells[coords] = new_cell
        self.cells = new_cells


class Window:
    def __init__(self):
        self.root = Tk()
        self.steps_per_run = 1
        self.make_buttons()
        self.num_generation = 0
        rows, columns, r = 10, 20, 30
        self.create(rows, columns, r)
        self.canvas.view_environment(self.env)
        for cell in self.env.cells.keys():
            self.canvas.tag_bind(str(cell[0])+'-'+str(cell[1]), '<Button-1>', partial(self.make_alive, cell[0], cell[1]))
        mainloop()


    def make_buttons(self):
        self.cell_type_to_born = CellA
        self.start_button = Button(self.root, text='⊲', command=self.run)
        self.start_button.grid(row=0, column=0)
        self.cellA_button = Canvas(self.root, width=20, height=20, bg='#eb7834')
        self.cellA_button.grid(row = 0, column = 5)
        self.cellA_button.bind('<Button-1>', lambda event: self.assign(CellA))
        self.cellB_button = Canvas(self.root, width=20, height=20, bg='#366feb')
        self.cellB_button.grid(row=0, column=6)
        self.cellB_button.bind('<Button-1>', lambda event: self.assign(CellB))
        self.cellD_button = Canvas(self.root, width=20, height=20, bg='#4d1b87')
        self.cellD_button.grid(row=0, column=7)
        self.cellD_button.bind('<Button-1>', lambda event: self.assign(CellD))


    def assign(self, cell_type):
        self.cell_type_to_born = cell_type


    def create(self, rows, columns, r):
        # self.w = r * 3 ** (1 / 2)
        self.env = Environment(rows, columns, r)
        self.canvas = EnvCanvas(self.root, width=columns * self.env.w, height=rows * 3 / 2 * r + r / 2)
        self.canvas.grid(row=1, column=0)
        # self.canvas.bind('<Button-1>', self.run)


    def generation(self):
        print(self.num_generation)
        self.env.generation(self.canvas.view_cell)

        # self.canvas.view_environment(self.env)
        time.sleep(1)
        self.num_generation += 1
        # self.canvas.update()


    def run(self, event = None):
        # self.canvas.unbind('<Button-1>')
        for i in range(self.steps_per_run):
            self.generation()
            # time.sleep(1)


    def make_alive(self, x, y, event):
            print('alive', x, y)
            # print(self.cell_type_to_born)
            cell = self.cell_type_to_born(x, y, 30)
            self.env.cells[(x, y)] = cell
            # cell.make_alive()
            self.canvas.view_cell(cell)


if __name__ == '__main__':
    root = Window()