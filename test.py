import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("test")


while True:
	for event in pygame.event.get():
		if event.type ==  pygame.QUIT:
			sys.exit()
		pygame.draw.rect(screen, (250, 0, 0),pygame.Rect(0,0, 12,23))