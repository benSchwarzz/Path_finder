import pygame as pg
import math
from queue import PriorityQueue

pg.init()

WIDTH = 800
screen = pg.display.set_mode((WIDTH, WIDTH))
pg.display.set_caption("A* PathFinder")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col*width
        self.y = row*width
        self.width = width
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == TURQUOISE
    def is_end(self):
        return self.color == ORANGE
    
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_start(self):
        self.color = TURQUOISE
    def make_end(self):
        self.color = ORANGE
    def make_path(self):
        self.color = PURPLE
    def reset(self):
        self.color = WHITE
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def get_neighbors(self, grid):
        if self.row < self.total_rows and not grid[self.row + 1][self.col].is_barrier: #Down
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier: #Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows and not grid[self.row][self.col + 1].is_barrier: #Right
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier: #Left
            self.neighbors.append(grid[self.row][self.col - 1])


def h(p1, p2) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows) -> list:
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, (WIDTH // rows), rows)
            grid[i].append(node)
    return grid


def draw_grid(screen, grid: list):
    for row in grid:
        for node in row:
            node.draw(screen)


def get_mouse_pos(rows, pos):
    x, y = pos
    gap = WIDTH // rows
    col = x // gap
    row = y // gap
    return row, col



def main():
    ROWS = 50
    grid = make_grid(ROWS)

    start = None
    end = None

    run = True
    started = False
    while run:
        screen.fill(WHITE)
        draw_grid(screen, grid)

        if pg.mouse.get_pressed()[0]:
            pos = pg.mouse.get_pos()
            row, col = get_mouse_pos(ROWS, pos)

            node = grid[row][col]
            if not start:
                node.make_start()
                start = node
                pg.time.delay(100)

            elif not end:
                node.make_end()
                end = node
                pg.time.delay(100)

            elif node != end and node != start: 
                node.make_barrier()

        elif pg.mouse.get_pressed()[2]:
            pos = pg.mouse.get_pos()
            row, col = get_mouse_pos(ROWS, pos)
            node = grid[row][col]

            node.reset()
            if node == start:
                node.reset()
                start = None
                pg.time.delay(100)

            elif node == end:
                node.reset()
                end = None
                pg.time.delay(100)
        

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if started:
                continue
    pg.quit()

main()

