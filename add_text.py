from matplotlib.pyplot import pause
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
# font text is from https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
def add_text(screen, text):
    screen.fill(BLACK, (0, 0, 430, 100))
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(text, True, RED)
    textRect = text.get_rect()
    textRect.center = (215, 15)
    screen.blit(text, textRect)