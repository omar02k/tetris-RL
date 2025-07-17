import numpy as np
import pygame as pg
from config import *
from piece import Piece
from grid import Grid


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    pg.display.set_caption("Tetris")

    font = pg.font.Font(None, 48)

    bag = list(SHAPES.keys())

    grid = Grid()
    piece = Piece(bag)

    running = True
    time_for_gravity = 0
    time_for_place = 0
    while running:
        if not bag:
            bag = list(SHAPES.keys())

        dt = clock.tick(15)
        time_for_gravity += dt
        if time_for_gravity >= GRAVITY:
            piece.pos[0] += 1
            time_for_gravity = 0

        hard_drop = False

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    hard_drop = True
                if event.key == pg.K_x:
                    piece.rotate(dir=-1, grid=grid)
                if event.key == pg.K_z:
                    piece.rotate(dir=1, grid=grid)
            if event.type == pg.QUIT:
                running = False
        screen.fill((0, 0, 0))

        score_text = font.render(f'Lines Cleared:   {str(grid.lines_cleared)}', True, 'white')
        screen.blit(score_text, (2*WIDTH/3, HEIGHT/2))
        grid.draw(screen)
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_DOWN]:
            time_for_gravity = 0
        piece.move(keys_pressed=keys_pressed, grid=grid)
        # piece.draw(screen)

        if hard_drop:
            while not piece.is_colliding_down(grid):
                piece.pos[0] += 1
            time_for_place = PLACE

        if piece.is_colliding_down(grid):
            time_for_place += dt
        else:
            time_for_place = 0
        
        piece.draw(screen)

        if time_for_place >= PLACE:
            piece.place(grid)
            piece = Piece(bag)

        grid.clear_lines()
        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()

# TODO: fix spawn of pieces
