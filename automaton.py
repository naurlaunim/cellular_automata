from tkinter import *
from functools import partial
import copy
import random
import time


def get_points(x, y, r):
    return [(x, y-r), (x+r*3**(1/2)/2, y-r/2), (x+r*3**(1/2)/2, y+r/2), (x, y+r), (x-r*3**(1/2)/2, y+r/2), (x-r*3**(1/2)/2, y-r/2)]


def get_neighbours(x, y, r):
    w = r * 3 ** (1 / 2)
    neighbours = [(x + w/2, y - r*3/2), (x + w, y), (x + w/2, y + r*3/2), (x - w/2, y + r*3/2), (x - w, y), (x - w/2, y - r*3/2)]
    return [(round(n[0],2), round(n[1], 2)) for n in neighbours if n[0] > 1 and n[1] > 1]


class Cell:
    def __init__(self,x,y,r, alive = False, fill='#6fd19b', outline='#1c5234'):
        self.x = x
        self.y = y
        self.r = r
        self.points = get_points(x, y, r)
        self.alive = alive
        self.fill = fill
        self.outline = outline


    def step(self, env):
        neigh_coords = get_neighbours(self.x, self.y, self.r)
        neighbours = [env.cells.get(n) for n in neigh_coords if env.cells.get(n)]
        p = len([n for n in neighbours if n.alive == True])/len(neighbours)
        c = copy.deepcopy(self)
        life = random.uniform(0,1) < p
        if life:
            c.make_alive()
        return c


    def make_alive(self, event = None):
        self.alive = True
        self.fill = 'red'
        self.outline = 'black'


class EnvCanvas(Canvas):
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)


    def view_cell(self, cell, width=2):
        self.create_polygon(cell.points, fill=cell.fill, outline=cell.outline, width=width, tag = str(cell.x)+'-'+str(cell.y))
        # self.tag_bind(str(cell.x) + '-' + str(cell.y), '<Button-1>', cell.make_alive)


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
                self.cells[(x,y)] = Cell(x,y,r)
                x += self.w
            x = self.w if i % 2 == 0 else self.w / 2
            y += r * 3/2


    def generation(self):
        new_cells = {}
        for coords, cell in self.cells.items():
            new_cell = cell.step(self)
            new_cells[coords] = new_cell
        self.cells = new_cells


class Window:
    def __init__(self):
        self.root = Tk()
        self.steps_per_run = 5
        self.start_button = Button(self.root, text='⊲', command=self.run)
        self.start_button.grid(row=0, column=0)
        self.num_generation = 0
        rows, columns, r = 10, 20, 30
        self.create(rows, columns, r)
        self.canvas.view_environment(self.env)
        for cell in self.env.cells.keys():
            self.canvas.tag_bind(str(cell[0])+'-'+str(cell[1]), '<Button-1>', partial(self.make_alive, cell[0], cell[1]))
        mainloop()


    def create(self, rows, columns, r):
        # self.w = r * 3 ** (1 / 2)
        self.env = Environment(rows, columns, r)
        self.canvas = EnvCanvas(self.root, width=columns * self.env.w, height=rows * 3 / 2 * r + r / 2)
        self.canvas.grid(row=1, column=0)
        # self.canvas.bind('<Button-1>', self.run)


    def generation(self):
        print(self.num_generation)
        self.env.generation()

        self.canvas.view_environment(self.env)
        time.sleep(1)
        self.num_generation += 1


    def run(self, event = None):
        # self.canvas.unbind('<Button-1>')
        for i in range(self.steps_per_run):
            self.generation()
            # time.sleep(1)


    def make_alive(self, x, y, event):
            print('alive', x, y)
            cell = self.env.cells[(x,y)]
            cell.make_alive()
            self.canvas.view_cell(cell)


if __name__ == '__main__':
    root = Window()