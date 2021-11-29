import pygame
from game import Game

g = Game()

while g.running:
    pygame.display.set_caption('Chess')
    g.curr_menu.display_menu()
    g.game_loop()
    pygame.display.update()
