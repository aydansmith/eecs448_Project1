import copy
from operator import truediv
from matplotlib.pyplot import pause
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import get_game_mode
import battleship
import special_shot

from random import randint

pygame.init()
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
SCREEN = pygame.display.set_mode((490, 400))
font = pygame.font.Font('freesansbold.ttf', 16)
smallfont = pygame.font.SysFont('Corbel',35)
Specialtext = smallfont.render('Special shot' , True , color)
Specialtext1 = smallfont.render('Vip for more' , True , color)

def run():

    # get the number of ships that the user wants for the game and returns a 4 tupe with size and empty placed ships array
    arrays = get_ships_num.get_ships(battleship.player1ships, battleship.player2ships, battleship.SCREEN, battleship.player1placedShips, battleship.player2placedShips)
    battleship.player1ships = arrays[0]
    battleship.player2ships = arrays[1]
    battleship.player1placedShips = arrays[2]
    battleship.player2placedShips = arrays[3]
    Player1Specialtexttime = 1
    Player2Specialtexttime = 1
    thistimeSpecial = False
    #run while the game is not ended
    while not battleship.gameover:

        # gets the position of the mouse on the screen
        pos = pygame.mouse.get_pos()

    
        # if player 1 is not ready, pass to place_ships and have player 1 place their ships
        if not battleship.player1ready:
            place_ships.placePlayer1Ships(battleship.SCREEN, battleship.player1ships, battleship.player1placedShips, battleship.player1ShipBoard)
            battleship.player1ready = True
            #create non pointer copy
            battleship.copyPlayer1placedShips = battleship.createShallowCopy(battleship.player1placedShips)
            add_text.switch_turns(battleship.SCREEN)
        # repeat for player 2
        if not battleship.player2ready:
            place_ships.placePlayer2Ships(battleship.SCREEN, battleship.player2ships, battleship.player2placedShips, battleship.player2ShipBoard)
            battleship.player2ready = True
            battleship.copyPlayer2placedShips = battleship.createShallowCopy(battleship.player2placedShips)
            add_text.switch_turns(battleship.SCREEN)
        # add text saying battleship and add rows and cols
        add_text.add_text(battleship.SCREEN, 'Battleship')
        add_text.add_labels_targets(battleship.SCREEN)
        # if it is player 1 turn, say that and print their boards
        if(battleship.player1Turn):
            add_text.add_text(battleship.SCREEN, 'Player 1 Turn')
            battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits, battleship.player2misses)
            battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
            add_text.add_labels_middle(battleship.SCREEN)
            add_text.add_labels_ships(battleship.SCREEN)
        # if it is player 2 turn, say that and print their boards
        else:
            add_text.add_text(battleship.SCREEN, 'Player 2 Turn')
            battleship.printShipBoard(battleship.player2ShipBoard, battleship.player2placedShips, battleship.player1hits, battleship.player1misses)
            battleship.printBoard(battleship.player2TargetBoard, battleship.player2hits, battleship.player2misses)
            add_text.add_labels_middle(battleship.SCREEN)
            add_text.add_labels_ships(battleship.SCREEN)
        # handles events in pygame
        for event in pygame.event.get():
            # if the user wants to quit, close pygame
            # if the user clicks, we respond accordingly
            if 150 <= pos[0] <= 400 and 350 <= pos[1] <= 400:
                pygame.draw.rect(SCREEN,color_light,[150,350,2.0,50])
            else:
                pygame.draw.rect(SCREEN,color_dark,[150,350,200,50])
            if(battleship.player1Turn):
                Specialtexttime = Player1Specialtexttime
            else:
                Specialtexttime = Player2Specialtexttime
                
            if Specialtexttime > 0:
                SCREEN.blit(Specialtext,(165,360))
            else:
                SCREEN.blit(Specialtext1,(165,360))
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if it is player 1 turn, check for a hit and checkForCollision will handle all the logic for updating hits and misses
                if(battleship.player1Turn):
                    if Player1Specialtexttime > 0:
                        if 150 <= pos[0] <= 350 and 350 <= pos[1] <= 400:
                            thistimeSpecial = True
                            Player1Specialtexttime = Player1Specialtexttime-1
                            continue
                    if thistimeSpecial == True:
                        played = special_shot.check_collision(battleship.player1TargetBoard, battleship.player2ShipBoard, pos, battleship.player1hits, battleship.player1misses, battleship.player2placedShips, battleship.copyPlayer2placedShips)
                        if played: 
                            thistimeSpecial = False
                    else:
                        played = battleship.checkForCollision(battleship.player1TargetBoard, battleship.player2ShipBoard, pos, battleship.player1hits, battleship.player1misses, battleship.player2placedShips, battleship.copyPlayer2placedShips)
                    if played: 
                        # if they made a valid move, update the boards
                        battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits, battleship.player2misses)
                        battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
                        add_text.add_labels_middle(battleship.SCREEN)
                        add_text.add_labels_ships(battleship.SCREEN)
                        pygame.display.update()
                        # check for a sunk ship
                        sunkenShip = battleship.shipSunk(battleship.copyPlayer2placedShips)
                        # if they sunk a ship, check if all ships are sunk
                        if(sunkenShip):
                            add_text.add_text(battleship.SCREEN, 'You sunk a ship!')
                            pygame.display.update()
                            ended = battleship.gameIsOver(battleship.copyPlayer2placedShips)
                            if ended:
                                battleship.gameover = True
                                add_text.add_text(battleship.SCREEN, 'Player 1 won!')
                                pygame.display.update()
                                pause(3)
                        # wait for 1 seconds and switch turn
                        pause(1)
                        if not battleship.gameover:
                            add_text.switch_turns(battleship.SCREEN)
                        battleship.player1Turn = False
                else:
                    # otherwise repeat for player 2
                    if Player2Specialtexttime > 0:
                        if 150 <= pos[0] <= 350 and 350 <= pos[1] <= 400:
                            thistimeSpecial = True
                            Player2Specialtexttime = Player2Specialtexttime-1
                            continue
                    if thistimeSpecial == True:
                        played = special_shot.check_collision(battleship.player2TargetBoard, battleship.player1ShipBoard, pos, battleship.player2hits, battleship.player2misses, battleship.player1placedShips, battleship.copyPlayer1placedShips)
                        if played: 
                            thistimeSpecial = False
                    else:
                        played = battleship.checkForCollision(battleship.player2TargetBoard, battleship.player1ShipBoard, pos, battleship.player2hits, battleship.player2misses, battleship.player1placedShips, battleship.copyPlayer1placedShips)
                    if played:
                        battleship.printShipBoard(battleship.player2ShipBoard, battleship.player2placedShips, battleship.player1hits, battleship.player1misses)
                        battleship.printBoard(battleship.player2TargetBoard, battleship.player2hits, battleship.player2misses)
                        add_text.add_labels_middle(battleship.SCREEN)
                        add_text.add_labels_ships(battleship.SCREEN)
                        pygame.display.update()
                        sunkenShip = battleship.shipSunk(battleship.copyPlayer1placedShips)
                        if(sunkenShip):
                            add_text.add_text(battleship.SCREEN, 'You sunk a ship!')
                            pygame.display.update()
                            ended = battleship.gameIsOver(battleship.copyPlayer1placedShips)
                            if ended:
                                battleship.gameover = True
                                add_text.add_text(battleship.SCREEN, 'Player 2 won!')
                                pygame.display.update()
                                pause(3)
                        pause(1)
                        if not battleship.gameover:
                            add_text.switch_turns(battleship.SCREEN)
                        battleship.player1Turn = True

        pygame.display.update()