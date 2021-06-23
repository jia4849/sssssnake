import pygame as pg
from settings import categories_dict, categories_list, options_list

class Menu():
    
    def __init__(self, screen, button_size, settings_pos, settings_size, settings_sound, buttons_sound):
        self.b_pos = screen.get_width() - button_size[0], 0
        self.b_size = button_size
        self.s_pos = settings_pos
        self.s_size = settings_size
        self.settings_sound = settings_sound
        self.buttons_sound = buttons_sound

        self.difficulty_options = [i for i in categories_dict["Difficulty"]]
        self.difficulty = "Normal"
        self.sounds = "Sound Effects"
        
    def init_components(self, font, screen):
        self.menu_surf = pg.Surface(self.s_size)
        self.button_text = font.render("Settings", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(topright = (self.s_size[0], 0))   
        self.quit_text = font.render("Exit Settings", True, (255, 255, 255))
        self.quit_rect = self.quit_text.get_rect(topright = (self.s_size[0], 0))
                    
    def init_music(self):
        if self.sounds == "Track 1" or self.sounds == "Track 2":
            pg.mixer.music.load(categories_dict["Sounds"][self.sounds])
            pg.mixer.music.play(-1)

    def draw_settings_button(self, screen, surface=None):
        if surface == None:
            surface = self.menu_surf
        surface.fill((0, 0, 0))
        pg.draw.rect(surface, (62, 76, 150), self.button_rect)
        surface.blit(self.button_text, self.button_rect)
        screen.blit(surface, self.s_pos)

    def show_settings(self, font, screen):
        self.menu_surf.fill((211, 227, 235))
        self.difficulty_rects = []
        self.sounds_rects = []
        self.options_rects = []
        button_font = pg.font.SysFont("Times New Roman", 35)
        pg.draw.rect(self.menu_surf, (62, 76, 150), self.quit_rect)
        self.menu_surf.blit(self.quit_text, self.quit_rect)       
        num_categories = len(categories_list)
        
        for i in range(num_categories):
            category_name = categories_list[i] 
            category_text = font.render(category_name, True, (255, 255, 255))
            category_pos = self.s_pos[0] // 2, (i+1) * (self.s_size[1] // (num_categories+1))
            category_rect = category_text.get_rect(center = category_pos)
            pg.draw.rect(self.menu_surf, (93, 110, 201), category_rect)
            self.menu_surf.blit(category_text, category_rect)
            
            category_contents = list(categories_dict[category_name])
            options_widths = [(button_font.render(category_contents[n], True, (255, 255, 255))).get_width() for n in range(len(category_contents))]
            options_dist = (self.s_size[0] - sum(options_widths)) // (len(category_contents) + 1)

            for n in range(len(category_contents)):
                option_name = category_contents[n]
                if (category_name == "Difficulty" and option_name == self.difficulty) or (category_name == "Sounds" and option_name == self.sounds):
                    text_colour = (0, 0, 0)
                    rect_colour = (129, 173, 184) 
                else:
                    text_colour = (255, 255, 255)
                    rect_colour = (144, 188, 199)
                option_text = button_font.render(option_name, True, text_colour)
                x_pos = sum(options_widths[:n]) + ((n + 1) * options_dist)
                y_pos = (((i+1)+(i+2)) * (self.s_size[1] // (num_categories+1))) // 2
                option_pos = x_pos, y_pos
                option_rect = option_text.get_rect(midleft = option_pos)
                self.options_rects.append(option_rect)
                if category_name == "Difficulty":
                    self.difficulty_rects.append(option_rect)
                elif category_name == "Sounds":
                    self.sounds_rects.append(option_rect)
                pg.draw.rect(self.menu_surf, rect_colour, option_rect)
                self.menu_surf.blit(option_text, option_rect)
        screen.blit(self.menu_surf, self.s_pos) 
        pg.display.flip()

    def change_settings(self, option_rect):
        new_option_index = self.options_rects.index(option_rect)
        new_option = options_list[new_option_index]
        if option_rect in self.difficulty_rects:
            self.difficulty = new_option
        elif option_rect in self.sounds_rects:
            if new_option == "Sound Effects" or new_option == "Off":
                pg.mixer.music.stop()
            elif new_option != self.sounds and new_option in ["Track 1", "Track 2"]:
                pg.mixer.music.load(categories_dict["Sounds"][new_option])
                pg.mixer.music.play(-1)
            self.sounds = new_option
