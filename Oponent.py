import Board
import random


class Computer:
    def __init__(self):
        self.color = Board.computer_color

    def play(self):  # easy level
        # plays a random move
        pieces = Board.board.get_all_pieces(self.color)
        piece = random.choice(pieces)
        try:
            move = random.choice(Board.board.board[piece[0]][piece[1]].new_valid_moves())
            Board.board.board[piece[0]][piece[1]].move(move[0], move[1])
            if Board.board.board[move[0]][move[1]].piece_type == "king":
                Board.board.board[move[0]][move[1]].unmoved = False
        except:
            self.play()
        Board.board.turn = Board.player_color

    def play_smart(self):  # medium level
        # plays random moves except when it can make a worth trade
        pieces = Board.board.get_all_pieces(self.color)
        max_value = 0
        for piece in pieces:
            if Board.board.board[piece[0]][piece[1]].new_valid_moves():
                for move in Board.board.board[piece[0]][piece[1]].new_valid_moves():
                    p = Board.board.board[move[0]][move[1]]
                    if p != 0:
                        taken_piece = p
                        Board.board.board[move[0]][move[1]] = Board.board.board[piece[0]][piece[1]]
                        if (move[0], move[1]) not in Board.board.get_all_moves(Board.player_color):
                            Board.board.board[piece[0]][piece[1]].move(move[0], move[1])
                            Board.board.turn = Board.player_color
                            if Board.board.board[move[0]][move[1]].piece_type == "king":
                                Board.board.board[move[0]][move[1]].unmoved = False
                            return
                        Board.board.board[move[0]][move[1]] = taken_piece
                        Board.board.board[move[0]][move[1]] = p
                        if p.value >= Board.board.board[piece[0]][piece[1]].value:
                            Board.board.board[piece[0]][piece[1]].move(move[0], move[1])
                            Board.board.turn = Board.player_color
                            if Board.board.board[move[0]][move[1]].piece_type == "king":
                                Board.board.board[move[0]][move[1]].unmoved = False
                            return
        self.play()

    def play_minimax(self):  # hardest level, plays using the minimax algorithm
        move_piece = Board.board.minimax(4, -10000, 10000, self.color, Board.player_color, max_player=True)
        Board.board.board[move_piece[0][0]][move_piece[0][1]].move(move_piece[1][0], move_piece[1][1])
        if Board.board.board[move_piece[1][0]][move_piece[1][1]].piece_type == "king":
            Board.board.board[move_piece[1][0]][move_piece[1][1]].unmoved = False
        Board.board.turn = Board.player_color


computer = Computer()
