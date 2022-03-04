import pygame
import battleship
import add_text
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
SCREEN = pygame.display.set_mode((490, 400))

def special_shot(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy):
    return checkForCollision(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy)

def get_coordinates(board, rect):
    row = battleship.getRow(board, rect)
    col = battleship.getCol(board, rect)
    coor = [(row-1, col-1), (row, col-1), (row+1, col-1), (row-1,col), (row, col), (row+1,col), (row-1,col+1), (row, col+1), (row+1,col+1)]
    return coor

def valid_coordinates(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy):
    hit = False
    valid = []
    # get the rect object and row and col
    rect = battleship.getRectangle(targetBoard, pos)
    coordinates = get_coordinates(targetBoard, rect)
    temp_row = battleship.getRow(targetBoard, rect)
    temp_col = battleship.getCol(targetBoard, rect)
    # if you have an invalid row, then you did not hit anything and need new user input
    if temp_row != -1 or temp_col != -1:
        for coor in coordinates:
            row = coor[0]
            col = coor[1]
            # if you have an invalid row, then you did not hit anything and need new user input
            if row >= 0 and row <= 9 and col >= 0 and col <= 9:
                # otherwisecheck if you already hit the ship or already missed it, since you would need new user input
                tempRectShip = (shipBoard[row])[col]
                alreadyHit = battleship.inHits(hits, tempRectShip)
                alreadyMissed = battleship.inMisses(misses, tempRectShip)
                if not alreadyHit or not alreadyMissed:
                    valid.append((row,col));
                    print(valid)
    # return true since if you make it this far is was a valud move
    return valid

def check_collision(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy):
    valid = valid_coordinates(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy)
    if len(valid) > 0:
        for coor in valid:
            tempRectTarget = (targetBoard[coor[0]])[coor[1]]
            tempRectShip = (shipBoard[coor[0]])[coor[1]]
            # if it is in their ships, you have a hit
            inShipsList = battleship.inShips(shipsPlaced, tempRectShip)
            if inShipsList:
                add_text.add_text(SCREEN, 'You hit some ship!')
                hits.append(tempRectTarget)
                hits.append(tempRectShip)
                battleship.removeFromShipsCopy(tempRectShip, shipsCopy)
            else:
                # otherwise you missed
                add_text.add_text(SCREEN, 'You did not hit a ship!')
                misses.append(tempRectTarget)
                misses.append(tempRectShip)
        return True
    return False