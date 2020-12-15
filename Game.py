import Board, Menu, Oponent
import pygame, time
pygame.init()

clock = pygame.time.Clock()


def play():
    go_to_menu = False
    Board.board.renew_board()
    quit_game = False
    pygame.display.set_caption("Chess")
    Board.game_display.fill((150, 150, 150)) # grey
    while not quit_game:
        Board.display_board()
        Board.board.display_pieces()
        try:
            Board.board.selected_piece.display_moves()
        except:
            pass
        pygame.display.update()
        if go_to_menu:
            Board.display_text(Board.message, Board.big_font, 300, 300, (255, 0, 0))
            pygame.display.update()
            time.sleep(3)
            return True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit upon pressing the X in the upper corner of the window
                quit_game = True
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN: # quit upon pressing Q
                if event.key == pygame.K_q:
                    quit_game = True
                    pygame.quit()
                    quit()
                if event.key == pygame.K_z:  # undo move upon pressing z (y on czech keyboard)
                    try:
                        Board.board.undo_move()
                    except:
                        pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Board.board.turn == Board.player_color:
                    x, y = pygame.mouse.get_pos()
                    if Board.player_color == "black":
                        col, row = 7 - ((x - 20) // 100), 7 - ((y - 20) // 100)
                    else:
                        col, row = (x - 20) // 100, (y - 20) // 100
                    try:
                        if Board.board.selected_any:
                            moves = Board.board.selected_piece.new_valid_moves()
                            if (col, row) in moves:
                                Board.board.selected_piece.move(col, row)
                                if Board.board.turn == "white":
                                    Board.board.turn = "black"
                                    if Board.board.check_mate("black", "white"):
                                        Board.message = "Black got a check mate"
                                        go_to_menu = True
                                    elif Board.board.stale_mate("black", "white"):
                                        Board.message = "Stalemate"
                                        go_to_menu = True
                                else:
                                    Board.board.turn = "white"
                                    if Board.board.check_mate("white", "black"):
                                        Board.message = "White got a check mate"
                                        go_to_menu = True
                                    elif Board.board.stale_mate("white", "black"):
                                        go_to_menu = True
                                        Board.message = "Stalemate"
                            elif Board.board.board[col][row] != 0:
                                if Board.board.board[col][row].color == Board.board.turn:
                                    Board.board.selected_any = True
                                    Board.board.selected_piece = Board.board.board[col][row]

                        else:
                            if Board.board.board[col][row] != 0:
                                if Board.board.board[col][row].color == Board.board.turn:
                                    Board.board.selected_any = True
                                    Board.board.selected_piece = Board.board.board[col][row]
                                    Board.board.selected_piece.display_moves()
                    except:
                        pass
        if Board.board.turn == Board.computer_color:
            Oponent.computer.play()
        pygame.display.update()
        clock.tick(60)


while True:
    Menu.menu()
    play()
