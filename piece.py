import numpy as np
import pygame as pg
import random
from config import *

class Piece:
    def __init__(self, bag):
        choice = random.choice(bag)
        bag.remove(choice)
        self.grid = np.array(SHAPES[choice]['grid']) * (SHAPES[choice]['color_idx'])
        self.pos = [0, 4]

    def rotate(self, dir, grid):
        new_grid = np.rot90(self.grid, k=dir)
        for row in range(new_grid.shape[0]):
            for col in range(new_grid.shape[1]):
                if (0 <= self.pos[0] + row < GRID_HEIGHT 
                    and 0 <= self.pos[1] + col < GRID_WIDTH 
                    and grid.grid[self.pos[0] + row][self.pos[1] + col]):
                    return
        self.grid = new_grid
        if self.pos[1] + self.empty_count['left'] < 0: # correct left
            self.pos[1] = -self.empty_count['left']
        if self.pos[1] + self.size[1] > GRID_WIDTH: # correct right
            self.pos[1] = -self.size[1] + GRID_WIDTH
        if self.pos[0] + self.size[0] > GRID_HEIGHT: # correct down
            self.pos[0] = -self.size[0] + GRID_HEIGHT
    
    def move(self, keys_pressed, grid):
        if keys_pressed:
            self.pos[0] = (self.pos[0] + 1 if keys_pressed[pg.K_DOWN] and 
                           not self.is_colliding_down(grid) else self.pos[0])
            self.pos[1] = (self.pos[1] + 1 if keys_pressed[pg.K_RIGHT] and 
                           not self.is_colliding_right(grid) else self.pos[1])
            self.pos[1] = (self.pos[1] - 1 if keys_pressed[pg.K_LEFT] and 
                           not self.is_colliding_left(grid) else self.pos[1])

    def place(self, grid):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.grid[row][col]:
                    grid.grid[self.pos[0]+row][self.pos[1]+col] = self.grid[row][col]
    
    def draw(self, screen):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.grid[row, col]:
                    pg.draw.rect(
                        screen,
                        COLORS[self.grid[row][col]],
                        ((WIDTH - 30 * 10) / 2 + (self.pos[1] + col) * 30,
                         (self.pos[0] + row) * 30, 30, 30)
                    )

    def is_colliding_down(self, grid):
        """
        Checks whether any tile in the grid to the down of any tile in the 
        piece is occupied, or if it's colliding with the edges of the board.
        """
        return True in [
            True
            for col in range(self.size[1])
            for row in range(self.size[0])
            if self.grid[row][col]
            and 0 <= self.pos[0] + row + 1 < GRID_HEIGHT
            and 0 <= self.pos[1] + col < GRID_WIDTH
            and grid.grid[self.pos[0] + row + 1][self.pos[1] + col]
            or self.pos[0] + self.size[0] - self.empty_count['down'] == GRID_HEIGHT
        ]
    
    def is_colliding_right(self, grid):
        """
        Checks whether any tile in the grid to the right of any tile in the 
        piece is occupied, or if it's colliding with the edges of the board.
        """
        return True in [
            True 
            for col in range(self.size[1])
            for row in range(self.size[0])
            if self.grid[row][col]
            and 0 <= self.pos[0] + row < GRID_HEIGHT
            and 0 <= self.pos[1] + col + 1 < GRID_WIDTH
            and grid.grid[self.pos[0] + row][self.pos[1] + col + 1]
            or self.pos[1] + self.size[1] - self.empty_count['right'] >= GRID_WIDTH
        ]

    def is_colliding_left(self, grid):
        """
        Checks whether any tile in the grid to the left of any tile in the 
        piece is occupied, or if it's colliding with the edges of the board.
        """
        return True in [
            True
            for col in range(self.size[1])
            for row in range(self.size[0])
            if self.grid[row][col]
            and 0 <= self.pos[0] + row < GRID_HEIGHT
            and 0 <= self.pos[1] + col - 1 < GRID_WIDTH
            and grid.grid[self.pos[0] + row][self.pos[1] + col - 1]
            or self.pos[1] + self.empty_count['left'] <= 0
        ]

    @property
    def size(self):
        return self.grid.shape
    
    @property
    def empty_count(self):
        empty_count = {'down': 0, 'right': 0, 'left': 0}
        row_is_empty = np.any(self.grid, axis=1)[::-1]
        idx = 0
        while not row_is_empty[idx]:
            empty_count['down'] += 1
            idx += 1
        right_is_empty = np.any(self.grid, axis=0)[::-1]
        idx = 0
        while not right_is_empty[idx]:
            empty_count['right'] += 1
            idx += 1
        left_is_empty = np.any(self.grid, axis=0)
        idx = 0
        while not left_is_empty[idx]:
            empty_count['left'] += 1
            idx += 1
        return empty_count