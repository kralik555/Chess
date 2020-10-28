import pygame, Board, time, sys


def menu():
    while True:
        Board.game_display.fill((150, 150, 150)) # grey
        Board.display_text("Menu", Board.big_font, 200, 200, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    return True
                else:
                    return True
