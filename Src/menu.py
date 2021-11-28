import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.main_font = pygame.font.Font('Src/8-BIT WONDER.TTF', 30)
        self.options_font = pygame.font.Font('Src/8-BIT WONDER.TTF', 20)
        self.bg = pygame.transform.scale(pygame.image.load('Src/BG_menu_chess.jpg'), (self.game.DISPLAY_W, self.game.DISPLAY_H))

    def draw_cursor(self):
        tick_label = self.options_font.render('*', 30, (255, 0, 0))
        self.game.window.blit(tick_label, (self.cursor_rect.x - 80, self.cursor_rect.y))

    def blit_screen(self):
        pygame.display.update()
        self.game.reset_keys()

    def draw_text(self, text, font, size, x, y):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.game.window.blit(text_surface, text_rect)

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w + 30, self.mid_h + 47
        self.creditsx, self.creditsy = self.mid_w + 30, self.mid_h + 77
        self.instructionsx, self.instructionsy = self.mid_w + 30, self.mid_h + 107
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.window.blit(self.bg, (0, 0))
            mainMenu_label = self.main_font.render('Main Menu', 1, (255, 255, 255))
            startGame_label = self.options_font.render('Start Game', 1, (255, 255, 255))
            credits_label = self.options_font.render('Credits', 1, (255, 255, 255))
            instructions_label = self.options_font.render('Instructions', 1, (255, 255, 255))
            self.game.window.blit(mainMenu_label, (self.mid_w - (mainMenu_label.get_width()/2), self.mid_h - 20))
            self.game.window.blit(startGame_label, (self.mid_w - (startGame_label.get_width()/2), self.mid_h + 50))
            self.game.window.blit(credits_label, (self.mid_w - (credits_label.get_width()/2), self.mid_h + 80))
            self.game.window.blit(instructions_label, (self.mid_w - (instructions_label.get_width()/2), self.mid_h + 110))
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Instructions':
                self.game.curr_menu = self.game.instructions 
            self.run_display = False
            
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            
            self.game.display.fill((0, 0, 0))
            self.game.window.blit(self.bg, (0, 0))
            
            credits_label = self.main_font.render('Credits', 1, (255, 0, 0))
            self.game.window.blit(credits_label, (self.game.DISPLAY_W/2 - credits_label.get_width()/2, 50))

            f = open("Src/credits.txt", "r", encoding="utf8")
            lines = f.read().splitlines()
            y = 150
            for line in lines:
                self.draw_text(line, 'Src/arial.ttf', 24, 40, y)
                y += 40
            self.blit_screen()

class InstructionsMenu(Menu):
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            
            self.game.display.fill((0, 0, 0))
            self.game.window.blit(self.bg, (0, 0))

            instruction_label = self.main_font.render('Instructions', 1, (255, 0, 0))
            self.game.window.blit(instruction_label, (self.game.DISPLAY_W/2 - instruction_label.get_width()/2, 50))
            f = open("Src/guide.txt", "r", encoding="utf8")
            lines = f.read().splitlines()
            y = 150
            for line in lines:
                self.draw_text(line, 'Src/arial.ttf', 24, 40, y)
                y += 40
            self.blit_screen()    

