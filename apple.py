import pygame as pg
import random

class Apple():
    apple_red = (219, 7, 7)
    
    def __init__(self, tile_px, num_tiles):
        self.tile_px = tile_px
        self.num_tiles = num_tiles

    def set_position(self, snake):
        x = random.randint(0, self.num_tiles - 1)
        y = random.randint(0, self.num_tiles - 1)
        while (x, y) in snake.body:
            x = random.randint(0, self.num_tiles - 1)
            y = random.randint(0, self.num_tiles - 1)
        self.position = (x, y)

    def create_rect(self, board_pos):
        x, y = self.position
        rect = pg.Rect(x*self.tile_px, y*self.tile_px, self.tile_px-1, self.tile_px-1)
        self.rect = rect
