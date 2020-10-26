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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if Board.player_color == "black":
                    col, row = 7 - ((x - 20) // 100), 7 - ((y - 20) // 100)
                else:
                    col, row = (x - 20) // 100, (y - 20) // 100
                try:
                    if Board.board.selected_any:
                        moves = Board.board.board[Board.board.selected_piece[0]][Board.board.selected_piece[1]].valid_moves()
                        if (col, row) in moves:
                            Board.board.board[Board.board.selected_piece[0]][Board.board.selected_piece[1]].move(col, row)
                            if Board.board.turn == "white":
                                Board.board.turn = "black"
                            else:
                                Board.board.turn = "white"
                        elif Board.board.board[col][row] != 0:
                            if Board.board.board[col][row].color == Board.board.turn:
                                Board.board.selected_any = True
                                Board.board.selected_piece = (col, row)

                    else:
                        if Board.board.board[col][row] != 0:
                            if Board.board.board[col][row].color == Board.board.turn:
                                Board.board.selected_any = True
                                Board.board.selected_piece = (col, row)
                except IndexError:
                    pass

        pygame.display.update()
        clock.tick(60)


play()
