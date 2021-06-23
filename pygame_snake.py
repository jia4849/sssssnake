import pygame as pg
from pygame.locals import *
import sys
import os
import itertools
import random
from settings import categories_dict
from game import Game
from menu import Menu

def terminate():
    pg.quit()
    sys.exit()

def pause_event_loop():
    restart = False
    unpause = False
    while unpause == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_ESCAPE, pg.K_q]:
                    terminate()
                elif event.key in [pg.K_SPACE, pg.K_r]:
                    restart = True
                    unpause = True
                    break
                elif event.key == pg.K_p:
                    if menu.sounds == "Sound Effects":
                        menu.settings_sound.play()
                    unpause = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                menu_event_loop(game, menu, font, screen, event)
    return restart

def menu_event_loop(game, menu, font, screen, event):
    mouse_pos = event.pos[0] - menu.s_size[0], event.pos[1]
    if menu.button_rect.collidepoint(mouse_pos):
            if menu.sounds == "Sound Effects":
                menu.settings_sound.play()
            menu.show_settings(font, screen)
            show_settings = True
            while show_settings:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        terminate()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos[0] - menu.s_size[0], event.pos[1]
                        if menu.quit_rect.collidepoint(mouse_pos):
                            if menu.sounds == "Sound Effects":
                                menu.settings_sound.play()
                            show_settings = False
                            break
                        else:
                            for option_rect in menu.options_rects:
                                if option_rect.collidepoint(mouse_pos):
                                    if menu.sounds == "Sound Effects":
                                        menu.buttons_sound.play()
                                    menu.change_settings(option_rect)
                                    menu.show_settings(font, screen)                       
                                    break       
            game.title_instructions(font, screen, menu)
            pg.display.flip()

def game_event_loop(game, event):
    if event.key in [pg.K_UP, pg.K_w]:
        game.snake.set_direction("up")
    elif event.key in [pg.K_DOWN, pg.K_s]:
        game.snake.set_direction("down")
    elif event.key in [pg.K_LEFT, pg.K_a]:
        game.snake.set_direction("left")
    elif event.key in [pg.K_RIGHT, pg.K_d]:
        game.snake.set_direction("right")
           
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD1 = (182, 220, 207)
BOARD2 = (245, 255, 249)

SCREEN_SIZE = (1280, 720)
BOARD_COLOURS = itertools.cycle((BOARD1, BOARD2))
BOARD_PX = 475
BOARD_POS = tuple([((SCREEN_SIZE[0] // 2) - BOARD_PX) // 2 for i in range(2)])
TILE_PX = 25
NUM_TILES = BOARD_PX // TILE_PX
MID = NUM_TILES // 2
SETTINGS_BUTTON_SIZE = (80, 50)
SETTINGS_POS = SCREEN_SIZE[0] // 2, 0
SETTINGS_SIZE = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1])
INSTRUCTIONS_POS = SCREEN_SIZE[0] // 2, 0
INSTRUCTIONS_SIZE = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1])

pg.init()
font = pg.font.SysFont("Times New Roman", 52)
screen = pg.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
pg.display.set_caption("Snake!")
clock = pg.time.Clock()

apple_sound = pg.mixer.Sound("apple_sound.ogg")
game_over_sound = pg.mixer.Sound("game_over_sound.ogg")
settings_sound = pg.mixer.Sound("settings_sound.ogg")
buttons_sound = pg.mixer.Sound("buttons_sound.ogg")                  
              
game = Game(BOARD_COLOURS, BOARD_PX, BOARD_POS, TILE_PX, NUM_TILES, INSTRUCTIONS_POS, INSTRUCTIONS_SIZE, game_over_sound, apple_sound)
board = pg.Surface((BOARD_PX, BOARD_PX))
objects = pg.Surface((BOARD_PX, BOARD_PX))
objects.set_colorkey(BLACK)
menu = Menu(screen, SETTINGS_BUTTON_SIZE, SETTINGS_POS, SETTINGS_SIZE, settings_sound, buttons_sound)
menu.init_components(font, screen)

running = True
playing = True
menu.init_music()
while running == True:     
    game.init_components(board, objects)
    while playing == True:      
        difficulty = menu.difficulty
        restart = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_ESCAPE, pg.K_q]:
                    terminate()
                elif event.key in [pg.K_SPACE, pg.K_r]:
                    restart = True
                elif event.key == pg.K_p:
                    if menu.sounds == "Sound Effects":
                        settings_sound.play()
                    restart = pause_event_loop()
                else:
                    game_event_loop(game, event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                menu_event_loop(game, menu, font, screen, event)
        if restart:
            playing = False
            if menu.sounds == "Sound Effects":
                settings_sound.play()
            break
        game.snake.set_position()
        game.snake.create_rects(BOARD_POS)
        game.apple.create_rect(BOARD_POS)   
        if game.is_over(menu.sounds) == False:
            game.check_apple_eaten(menu.sounds)
            game.render(font, screen)
            game.display_scores(font, screen)
        else:
            pg.time.wait(500)        
            game.display_game_over(font, screen)        
            playing = False
        menu.draw_settings_button(screen)
        game.title_instructions(font, screen, menu)
        pg.display.flip()
        clock.tick(categories_dict["Difficulty"][difficulty])
    else:
        loop = True
        while loop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.KEYDOWN:
                    if event.key in [pg.K_ESCAPE, pg.K_q]:
                        terminate()
                    elif event.key in [pg.K_SPACE, pg.K_r]:
                        loop = False
                        playing = True           
                        break
                elif event.type == pg.MOUSEBUTTONDOWN:
                    menu_event_loop(game, menu, font, screen, event)
    playing = True
    pg.time.wait(500)
terminate()


