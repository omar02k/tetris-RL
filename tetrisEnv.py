import numpy as np
import pygame as pg
from config import *
from piece import Piece
from grid import Grid
import gym
from gym import spaces


class TetrisEnv(gym.Env):
    def __init__(self, do_render=False):
        super().__init__()
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) if do_render else None
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 48)

        # action space: left, right, hard drop, cw rotate, ccw rotate, none
        self.action_space = spaces.Discrete(6)

        # observation space: full state
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(GRID_HEIGHT, GRID_WIDTH), dtype=np.int8
        )

        self.reset()

    def reset(self):
        self.grid = Grid()
        self.bag = list(SHAPES.keys())
        self.piece = Piece(self.bag)
        self.time_for_place = 0
        # return

    def step(self, action):
        # fills 7-bag when empty
        if not self.bag:
            self.bag = list(SHAPES.keys())

        reward = 0
        actions = []
        # handle action
        if action == 0 or action == 1:   # left and right movement
            actions.append(action)
        # rotation
        elif action == 2: # rotate CW
            self.piece.rotate(dir=-1, grid=self.grid)
        elif action == 3: # rotate CCW
            self.piece.rotate(dir=1, grid=self.grid)
        hard_drop = action == 4
        # action == 5: do nothing

        self.piece.move(actions=actions, grid=self.grid)
        
        # hard drop logic
        if hard_drop:
            while not self.piece.is_colliding_down(self.grid):
                self.piece.pos[0] += 1
            self.time_for_place = FRAMES_TO_PLACE

        # wait x amount of frames before permenant-placing
        if self.piece.is_colliding_down(self.grid):
            self.time_for_place += 1
        else:
            self.time_for_place = 0

        # place piece and spawn new one
        if self.time_for_place >= FRAMES_TO_PLACE:
            # place place and clear full lines
            lines_cleared_before = self.grid.lines_cleared
            self.piece.place(self.grid)
            self.grid.clear_lines()
            lines_cleared_after = self.grid.lines_cleared
            # calculate reward
            lines_cleared = lines_cleared_after - lines_cleared_before
            reward = lines_cleared
            # spawn new piece
            self.piece = Piece(self.bag)
            if self.piece.spawn_collision(self.grid):
                terminated = True
                truncated = False
                reward = -10
                return self._get_obs(), reward, terminated, truncated, {}
            
        if self.screen:
            self.draw()
        
        # end condition
        terminated = self.grid.lines_cleared >= 40
        truncated = False
        return self._get_obs(), reward, terminated, truncated, {}

    def _get_obs(self):
        obs = self.grid.grid.copy()
        for row in range(self.piece.size[0]):
            for col in range(self.piece.size[1]):
                if self.piece.grid[row][col]:
                    obs[self.piece.pos[0] + row][self.piece.pos[1] + col] = 1
        return obs
    
    def close(self):
        pg.quit()
    
    def draw(self):
        # clears screen
        self.screen.fill((0, 0, 0))
        
        # render score
        score_text = self.font.render(
            f'Lines Cleared:   {str(self.grid.lines_cleared)}', True, 'white'
        )
        # render grid
        self.screen.blit(score_text, (2*WIDTH/3, HEIGHT/2))
        self.grid.draw(self.screen)

        # render tetromino piece
        self.piece.draw(self.screen)
