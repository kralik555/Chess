import Board
import pygame, time
pygame.init()

clock = pygame.time.Clock()


def play():
    quit_game = False
    pygame.display.set_caption("Chess")
    Board.game_display.fill((150, 150, 150)) # grey
    while not quit_game:
        Board.display_board()
        Board.board.display_pieces()
        for event in pygame.event.get(): # quit upon pressing the X in the upper corner of the window
            if event.type == pygame.QUIT:
                quit_game = True
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN: # quit upon pressing Q
                if event.key == pygame.K_q:
                    quit_game = True
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(60)


play()
