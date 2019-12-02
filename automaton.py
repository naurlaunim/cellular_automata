from tkinter import *
from functools import partial
import time
from cells import *


class EnvCanvas(Canvas):
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)


    def view_cell(self, cell, width=2):
        self.create_polygon(cell.points, fill=cell.fill, outline=cell.outline, width=width, tag = str(cell.x)+'-'+str(cell.y))
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
            new_cell = cell.step(self)
            new_cells[coords] = new_cell
            if type(cell) != type(new_cell):
                draw(new_cell)
        self.cells = new_cells


class Window:
    def __init__(self):
        self.root = Tk()
        self.num_generation = 0
        self.rows, self.columns, self.r_var = IntVar(), IntVar(), IntVar()
        self.rows.set(10)
        self.columns.set(20)
        self.r_var.set(30)
        self.r = 30
        self.make_buttons()
        self.create()
        self.stop = None
        mainloop()


    def make_buttons(self):
        self.menu_frame = Frame(self.root)
        self.env_frame = Frame(self.menu_frame)
        Label(self.env_frame, text='rows').grid(row=0, column=0)
        Entry(self.env_frame, textvariable=self.rows, width=4).grid(row=0, column=1)
        Label(self.env_frame, text='columns').grid(row=0, column=2)
        Entry(self.env_frame, textvariable=self.columns, width=4).grid(row=0, column=3)
        Label(self.env_frame, text='radius').grid(row=0, column=4)
        Entry(self.env_frame, textvariable=self.r_var, width=4).grid(row=0, column=5)
        Button(self.env_frame, text='new environment', command=self.create).grid(row=0, column=6)

        self.run_frame = Frame(self.menu_frame)
        self.start_button = Button(self.run_frame, text='▶', command=self.run)
        self.start_button.grid(row=0, column=0)
        self.stop_button = Button(self.run_frame, text = '∎', command=self.stop_)
        self.stop_button.grid(row=0, column=1)

        self.cells_choosing_frame = Frame(self.menu_frame)
        self.cell_type_to_born = CellA
        self.cellA_button = Canvas(self.cells_choosing_frame, width=20, height=20, bg='#eb7834')
        self.cellA_button.grid(row = 0, column = 0)
        self.cellA_button.bind('<Button-1>', lambda event: self.assign(CellA))
        self.cellB_button = Canvas(self.cells_choosing_frame, width=20, height=20, bg='#366feb')
        self.cellB_button.grid(row=0, column=1)
        self.cellB_button.bind('<Button-1>', lambda event: self.assign(CellB))
        self.cellD_button = Canvas(self.cells_choosing_frame, width=20, height=20, bg='#4d1b87')
        self.cellD_button.grid(row=0, column=2)
        self.cellD_button.bind('<Button-1>', lambda event: self.assign(CellD))

        self.env_frame.grid(row = 0, column = 1)
        self.run_frame.grid(row=0, column=0)
        self.cells_choosing_frame.grid(row=0, column=2)
        self.menu_frame.grid(row = 0, column = 0)


    def create(self):
        rows, columns, r = self.rows.get(), self.columns.get(), self.r_var.get()
        self.r = r
        self.env = Environment(rows, columns, r)
        try:
            self.canvas.grid_forget()
        except:
            pass
        self.canvas = EnvCanvas(self.root, width=columns * self.env.w, height=rows * 3 / 2 * r + r / 2)
        self.canvas.grid(row=1, column = 0)
        self.canvas.view_environment(self.env)
        for cell in self.env.cells.keys():
            self.canvas.tag_bind(str(cell[0])+'-'+str(cell[1]), '<Button-1>', partial(self.make_alive, cell[0], cell[1]))


    def generation(self):
        print(self.num_generation)
        self.env.generation(self.canvas.view_cell)
        time.sleep(1)
        self.num_generation += 1


    def run(self, event = None):
        self.stop = False
        while True:
            self.generation()
            if self.stop:
                break


    def make_alive(self, x, y, event):
            cell = self.cell_type_to_born(x, y, self.r)
            print(type(cell).__name__, x, y)
            self.env.cells[(x, y)] = cell
            self.canvas.view_cell(cell)


    def assign(self, cell_type):
        self.cell_type_to_born = cell_type


    def stop_(self):
        self.stop = True


if __name__ == '__main__':
    root = Window()