import copy
from operator import truediv
from matplotlib.pyplot import pause
from numpy import diff
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import get_game_mode
import battleship

def run():

    difficulty = get_game_mode.set_difficulty(battleship.SCREEN)


    # set the ships



    # run game loop for each difficulty
    if(difficulty == 1):
        print(1)
        #run while the game is not ended
        '''
        while not battleship.gameover:
        
            # gets the position of the mouse on the screen
            pos = pygame.mouse.get_pos()


            pygame.display.update()
        '''
    if(difficulty == 2):
        print(2)

    if(difficulty == 3):
        print(3)
