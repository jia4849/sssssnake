import pygame as pg
from snake import Snake
from apple import Apple

class Game():
    high_score = 0
    
    def __init__(self, board_colours, board_px, board_pos, tile_px, num_tiles, instructions_pos, instructions_size, game_over_sound, apple_sound):
        self.board_colours = board_colours
        self.board_px = board_px
        self.board_pos = board_pos
        self.tile_px = tile_px
        self.num_tiles = num_tiles
        self.inst_pos = instructions_pos
        self.inst_size = instructions_size
        self.inst_surf = pg.Surface(self.inst_size)
        self.mid = num_tiles // 2
        self.game_over_sound = game_over_sound
        self.apple_sound = apple_sound
        
    def init_components(self, board, objects):
        for y in range(self.num_tiles):
            for x in range(self.num_tiles):
                rect = pg.Rect(x * self.tile_px, y * self.tile_px, self.tile_px - 1, self.tile_px - 1)
                pg.draw.rect(board, next(self.board_colours), rect)
            if self.num_tiles % 2 == 0:
                next(self.board_colours)
        if self.num_tiles ** 2 % 2 != 0:
            next(self.board_colours)
            
        snake_body = [(self.mid, self.num_tiles-i) for i in range(5)][::-1]
        snake = Snake(self.tile_px, self.num_tiles, snake_body, "up")
        apple = Apple(self.tile_px, self.num_tiles)
        apple.set_position(snake)
              
        self.score = 0
        self.board = board
        self.snake = snake
        self.apple = apple      
        self.objects = objects
        
    def check_apple_eaten(self, sounds):
        head_pos = self.snake.body[0]
        if head_pos == self.apple.position:
            self.score += 1  
            if self.score > Game.high_score:
                Game.high_score += 1
            self.apple.set_position(self.snake)
            self.snake.increase_length()
            if sounds == "Sound Effects":
                self.apple_sound.play()

    def render(self, font, screen):
        screen.fill((0,0,0))
        screen.blit(self.board, self.board_pos)
        self.objects.fill((0,0,0))
        snake_rects = self.snake.rects
        apple_rect = self.apple.rect
        pg.draw.rect(self.objects, Apple.apple_red, apple_rect)
        for rect in snake_rects:
            if rect == snake_rects[0]:
                pg.draw.rect(self.objects, Snake.head_green, rect)
            else:
                pg.draw.rect(self.objects, Snake.tail_green, rect)           
        screen.blit(self.objects, self.board_pos)

    def display_scores(self, font, screen):
        score_y = (screen.get_height() + self.board_px + 50) // 2
        score = font.render("Score: " + str(self.score), True, (60, 95, 255))
        score_rect = score.get_rect(midleft = (self.board_pos[0], score_y))     
        high_score = font.render("High score: " + str(Game.high_score), True, (60, 95, 255))
        high_score_rect = high_score.get_rect(midleft = (score_rect.w + 120, score_y))

        pg.draw.rect(screen, (220, 220, 220), score_rect)
        screen.blit(score, score_rect)
        pg.draw.rect(screen, (220, 220, 220), high_score_rect) 
        screen.blit(high_score, high_score_rect)
  
    def title_instructions(self, font, screen, menu):
        title_font = pg.font.SysFont("Times New Roman", 52, bold=True)
        inst_font = pg.font.SysFont("Times New Roman", 35, italic=True)

        menu.draw_settings_button(screen, self.inst_surf)
        inst_1 = inst_font.render("Arrow keys or WASD- move the snake", True, (0, 0, 0))
        inst_2 = inst_font.render("Space or R- restart game", True, (0, 0, 0))
        inst_3 = inst_font.render("P- pause/unpause game", True, (0, 0, 0))
        inst_4 = inst_font.render("Esc or Q- quit", True, (0, 0, 0))
        all_inst = [inst_1, inst_2, inst_3, inst_4]
        num_inst = len(all_inst)
        for i in range(num_inst):
            inst_text = all_inst[i]
            inst_pos = self.inst_pos[0] // 2, (i+1) * (self.inst_size[1] // (num_inst+1))
            inst_rect = inst_text.get_rect(center = inst_pos)
            pg.draw.rect(self.inst_surf, (200, 200, 200), inst_rect)
            self.inst_surf.blit(inst_text, inst_rect)
        screen.blit(self.inst_surf, self.inst_pos)
        
    def is_over(self, sounds):
        new_position = self.snake.body[0]
        if self.snake.body.count(new_position) > 1:
            if sounds == "Sound Effects":
                self.game_over_sound.play()
            return True 
        elif self.board.get_rect().contains(self.snake.rects[0]) == False:
            if sounds == "Sound Effects":
                self.game_over_sound.play()
            return True
        else:
            return False

    def display_game_over(self, font, screen):
        game_over = font.render("GAME OVER!", True, Apple.apple_red)
        game_over_rect = game_over.get_rect(center = (self.board_pos[0] + (self.board_px // 2), self.board_pos[1] // 2))
        pg.draw.rect(screen, (200, 200, 200), game_over_rect)
        screen.blit(game_over, game_over_rect)
