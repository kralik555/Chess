class Piece:
    def __init__(self, col, row, color):
        self.col = col
        self.row = row
        self.color = color


class Pawn(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "pawn"
        self.value = 1
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"


class Bishop(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "bishop"
        self.value = 3
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"


class Rook(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "rook"
        self.value = 5
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"


class Knight(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "knight"
        self.value = 3
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"


class Queen(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "queen"
        self.value = 10
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"


class King(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "king"
        self.value = 9001
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"


class Board:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for i in range(8)]

        self.board[0][0] = Rook(0, 0, "black")
        self.board[1][0] = Knight(1, 0, "black")
        self.board[2][0] = Bishop(2, 0, "black")
        self.board[3][0] = Queen(3, 0, "black")
        self.board[4][0] = King(4, 0, "black")
        self.board[5][0] = Bishop(5, 0, "black")
        self.board[6][0] = Knight(6, 0, "black")
        self.board[7][0] = Rook(7, 0, "black")

        self.board[0][1] = Pawn(0, 1, "black")
        self.board[1][1] = Pawn(1, 1, "black")
        self.board[2][1] = Pawn(2, 1, "black")
        self.board[3][1] = Pawn(3, 1, "black")
        self.board[4][1] = Pawn(4, 1, "black")
        self.board[5][1] = Pawn(5, 1, "black")
        self.board[6][1] = Pawn(6, 1, "black")
        self.board[7][1] = Pawn(7, 1, "black")

        self.board[0][7] = Rook(0, 7, "white")
        self.board[1][7] = Knight(1, 7, "white")
        self.board[2][7] = Bishop(2, 7, "white")
        self.board[3][7] = Queen(3, 7, "white")
        self.board[4][7] = King(4, 7, "white")
        self.board[5][7] = Bishop(5, 7, "white")
        self.board[6][7] = Knight(6, 7, "white")
        self.board[7][7] = Rook(7, 7, "white")

        self.board[0][6] = Pawn(0, 6, "white")
        self.board[1][6] = Pawn(1, 6, "white")
        self.board[2][6] = Pawn(2, 6, "white")
        self.board[3][6] = Pawn(3, 6, "white")
        self.board[4][6] = Pawn(4, 6, "white")
        self.board[5][6] = Pawn(5, 6, "white")
        self.board[6][6] = Pawn(6, 6, "white")
        self.board[7][6] = Pawn(7, 6, "white")

        self.selected_any = False
        self.selected_piece = ()
        self.turn = "white"
        self.last_move =(-1, -1, -1, -1)

    def renew_board(self):
        self.board = [[0 for x in range(8)] for _ in range(8)]

        self.board[0][0] = Rook(0, 0, "black")
        self.board[1][0] = Knight(1, 0, "black")
        self.board[2][0] = Bishop(2, 0, "black")
        self.board[3][0] = Queen(3, 0, "black")
        self.board[4][0] = King(4, 0, "black")
        self.board[5][0] = Bishop(5, 0, "black")
        self.board[6][0] = Knight(6, 0, "black")
        self.board[7][0] = Rook(7, 0, "black")

        self.board[0][1] = Pawn(0, 1, "black")
        self.board[1][1] = Pawn(1, 1, "black")
        self.board[2][1] = Pawn(2, 1, "black")
        self.board[3][1] = Pawn(3, 1, "black")
        self.board[4][1] = Pawn(4, 1, "black")
        self.board[5][1] = Pawn(5, 1, "black")
        self.board[6][1] = Pawn(6, 1, "black")
        self.board[7][1] = Pawn(7, 1, "black")

        self.board[0][7] = Rook(0, 7, "white")
        self.board[1][7] = Knight(1, 7, "white")
        self.board[2][7] = Bishop(2, 7, "white")
        self.board[3][7] = Queen(3, 7, "white")
        self.board[4][7] = King(4, 7, "white")
        self.board[5][7] = Bishop(5, 7, "white")
        self.board[6][7] = Knight(6, 7, "white")
        self.board[7][7] = Rook(7, 7, "white")

        self.board[0][6] = Pawn(0, 6, "white")
        self.board[1][6] = Pawn(1, 6, "white")
        self.board[2][6] = Pawn(2, 6, "white")
        self.board[3][6] = Pawn(3, 6, "white")
        self.board[4][6] = Pawn(4, 6, "white")
        self.board[5][6] = Pawn(5, 6, "white")
        self.board[6][6] = Pawn(6, 6, "white")
        self.board[7][6] = Pawn(7, 6, "white")


board = Board()