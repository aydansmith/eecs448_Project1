from matplotlib.pyplot import pause
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
# font text is from https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
def add_text(screen, text):
    screen.fill(BLACK, (0, 0, 430, 80))
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(text, True, RED)
    textRect = text.get_rect()
    textRect.center = (215, 15)
    screen.blit(text, textRect)

def add_labels_ships(screen):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    counter = 0
    font = pygame.font.Font('freesansbold.ttf', 16)
    for x in range(40, 230, 20):
        text = font.render(letters[counter], True, RED)
        textRect = text.get_rect()
        textRect.center = (x, 90)
        screen.blit(text, textRect)
        counter = counter + 1

def add_labels_targets(screen):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    counter = 0
    font = pygame.font.Font('freesansbold.ttf', 16)
    for x in range(270, 460, 20):
        text = font.render(letters[counter], True, RED)
        textRect = text.get_rect()
        textRect.center = (x, 90)
        screen.blit(text, textRect)
        counter = counter + 1

def add_labels_middle(screen):
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    counter = 0
    font = pygame.font.Font('freesansbold.ttf', 16)
    for y in range(110, 300, 20):
        text = font.render(nums[counter], True, RED)
        textRect = text.get_rect()
        textRect.center = (245, y)
        screen.blit(text, textRect)
        counter = counter + 1
