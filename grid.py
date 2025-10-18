import numpy as np
import pygame as pg
from config import *

class Grid:
    def __init__(self):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.int8)
        self.lines_cleared = 0

    def draw(self, screen):
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col]:
                    pg.draw.rect(
                        screen, 
                        COLORS[self.grid[row][col]], 
                        ((WIDTH - 30 * 10)/2 + col * 30, row * 30, 30, 30)
                    )
                else:
                    pg.draw.rect(
                        screen, 
                        'grey', 
                        ((WIDTH - 30 * 10)/2 + col * 30, row * 30, 30, 30), 
                        width=1
                    )
    
    def clear_lines(self):
        rows_to_clear = []
        for row in range(GRID_HEIGHT):
            if 0 not in self.grid[row]:
                rows_to_clear.append(row)
    
        for row in rows_to_clear:
            self.grid = np.delete(self.grid, row, axis=0)
            self.grid = np.vstack([np.zeros((1, GRID_WIDTH), dtype=np.int8), 
                                   self.grid])
            self.lines_cleared += 1