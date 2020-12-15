import Board, random


class Computer:
    def __init__(self):
        self.color = Board.computer_color

    def play(self):
        pieces = Board.board.get_all_pieces(self.color)
        piece = random.choice(pieces)
        try:
            move = random.choice(Board.board.board[piece[0]][piece[1]].new_valid_moves())
            Board.board.board[piece[0]][piece[1]].move(move[0], move[1])
        except:
            if Board.board.check_mate(self.color, Board.player_color):
                return None
            self.play()
        Board.board.turn = Board.player_color

    def play_smart(self):
        if Board.board.check_mate(self.color, Board.player_color):
            return None
        pieces = Board.board.get_all_pieces(self.color)
        for piece in pieces:
            if Board.board.board[piece[0]][piece[1]].new_valid_moves():
                for move in Board.board.board[piece[0]][piece[1]].new_valid_moves():
                    p = Board.board.board[move[0]][move[1]]
                    if p != 0:
                        if p.value > Board.board.board[piece[0]][piece[1]].value:
                            Board.board.board[piece[0]][piece[1]].move(move[0], move[1])
                            Board.board.turn = Board.player_color
                            return True
                    if p not in Board.board.get_all_moves(Board.player_color):
                        Board.board.board[piece[0]][piece[1]].move(move[0], move[1])
                        Board.board.turn = Board.player_color
                        return True
        self.play()


computer = Computer()
