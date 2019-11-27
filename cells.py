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
    def __init__(self,x,y,r, alive = False):
        self.x = x
        self.y = y
        self.r = r
        self.points = get_points(x, y, r)
        self.alive = alive


    def step(self, env, draw):
        pass


    def get_neighbour_cells(self, env):
        neigh_coords = get_neighbours(self.x, self.y, self.r)
        neighbours = [env.cells.get(n) for n in neigh_coords if env.cells.get(n)]
        return neighbours


    def viewed(self, draw):
        draw(self)
        return self


class EmptyCell(Cell):
    def __init__(self, *args):
        Cell.__init__(self, *args)
        self.fill = '#6fd19b'
        self.outline = '#1c5234'


    def step(self, env, draw):
        neigh_cells = self.get_neighbour_cells(env)

        d_neighs = [cell for cell in neigh_cells if type(cell) == CellD]
        if len(d_neighs) in [1, 2]:
            bornD = random.uniform(0, 1) < 1/3
            if bornD:
                return CellD(self.x, self.y, self.r).viewed(draw)

        a_neighs = [cell for cell in neigh_cells if type(cell) == CellA]
        if len(a_neighs) >=3:
            p = 1
        elif len(a_neighs) == 2:
            p = 0.75
        elif len(a_neighs) == 1:
            p = 0.5
        else:
            p = 0
        bornA = random.uniform(0, 1) < p
        if bornA:
            return CellA(self.x, self.y, self.r).viewed(draw)

        b_neighs = [cell for cell in neigh_cells if type(cell) == CellB]
        if len(b_neighs) >= 4:
            p = 0.9
        elif len(b_neighs) == 3:
            p = 0.7
        elif len(b_neighs) == 2:
            p = 0.5
        elif len(b_neighs) == 1:
            p = 0.3
        else:
            p = 0
        bornB = random.uniform(0, 1) < p
        if bornB:
            return CellB(self.x, self.y, self.r).viewed(draw)

        return copy.deepcopy(self)


class CellA(Cell):
    '''
    Quick reproduction and easy dying.
    '''
    def __init__(self, *args):
        Cell.__init__(self, *args)
        self.fill = '#eb7834'
        self.outline = '#80411b'


    def step(self, env, draw):
        neigh_cells = self.get_neighbour_cells(env)
        d_neighs = [cell for cell in neigh_cells if type(cell) == CellD]
        if len(d_neighs) >= 2:
            return EmptyCell(self.x, self.y, self.r).viewed(draw)
        if len(d_neighs) == 1:
            if random.uniform(0, 1) < 0.5:
                return EmptyCell(self.x, self.y, self.r).viewed(draw)

        b_neighs = [cell for cell in neigh_cells if type(cell) == CellB]
        if len(b_neighs) >= 2:
            return EmptyCell(self.x, self.y, self.r).viewed(draw)

        return copy.deepcopy(self)


class CellB(Cell):
    '''
    Low reproduction and high viability.
    '''
    def __init__(self, *args):
        Cell.__init__(self, *args)
        self.fill = '#366feb'
        self.outline = '#123175'


    def step(self, env, draw):
        neigh_cells = self.get_neighbour_cells(env)
        d_neighs = [cell for cell in neigh_cells if type(cell) == CellD]
        if len(d_neighs) >= 3:
            return EmptyCell(self.x, self.y, self.r)
        if len(d_neighs) == 2:
            if random.uniform(0, 1) < 0.5:
                return EmptyCell(self.x, self.y, self.r).viewed(draw)

        a_neighs = [cell for cell in neigh_cells if type(cell) == CellA]
        if len(a_neighs) >= 4:
            return EmptyCell(self.x, self.y, self.r).viewed(draw)

        return copy.deepcopy(self)


class CellD(Cell):
    '''
    Voracious cells eating all the resources.
    '''
    def __init__(self, *args):
        Cell.__init__(self, *args)
        self.fill = '#4d1b87'
        self.outline = '#321159'


    def step(self, env, draw):
        neigh_cells = self.get_neighbour_cells(env)
        relatives = [cell for cell in neigh_cells if type(cell) == CellD]
        if len(relatives) >= 3:
            return EmptyCell(self.x, self.y, self.r).viewed(draw)
        else:
            return copy.deepcopy(self)