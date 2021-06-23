import pygame as pg
import random

class Snake():
    head_green, tail_green = (7, 170, 7), (7, 219, 7)
    

    opp_directions = {"up" : "down", "down" : "up", "left" : "right", "right" : "left"}
    direction_changes = {"up" : (0, -1), "down": (0, 1), "left" : (-1, 0), "right" : (1, 0)}
    
    def __init__(self, tile_px, num_tiles, body, direction):
        self.tile_px = tile_px
        self.num_tiles = num_tiles
        self.body = body
        self.direction = direction

    def set_direction(self, new_direction): 
        if new_direction != Snake.opp_directions[self.direction]:
            self.direction = new_direction

    def set_position(self):
        head_pos = self.body[0]
        change = Snake.direction_changes[self.direction]
        new_head_pos = tuple([head_pos[i] + change[i] for i in range(2)])
        self.body.insert(0, new_head_pos)
        self.body = self.body[:-1]

    def increase_length(self):
        tail_pos = self.body[-1]
        options = []
        for direction in Snake.direction_changes:
            new_tail_pos = tuple([tail_pos[i] + Snake.direction_changes[direction][i] for i in range(2)])
            x, y = new_tail_pos
            if x in range(self.num_tiles) and y in range(self.num_tiles):
                if new_tail_pos not in self.body:
                    options.append(new_tail_pos)
        new_tail_pos = random.choice(options)
        self.body.append(new_tail_pos)

    def create_rects(self, board_pos):
        self.rects = []
        for x, y in self.body:
            rect = pg.Rect(x*self.tile_px, y*self.tile_px, self.tile_px-1, self.tile_px-1)
            self.rects.append(rect)

