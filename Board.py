import pygame
pygame.init()
lil_font = pygame.font.SysFont("arial", 20, bold=True, italic=False)
big_font = pygame.font.SysFont("arialblack", 40, bold=False, italic=False)

game_display = pygame.display.set_mode((840, 840))
player_color = "white"


def display_board():
    for row in range(8):
        for col in range(8):
            x = 100 * col + 20
            y = 100 * row + 20
            if player_color == "white":
                if (row + col) % 2 == 0:
                    pygame.draw.rect(game_display, (255, 255, 255), (x, y, 100, 100))
                else:
                    pygame.draw.rect(game_display, (100, 100, 100), (x, y, 100, 100))
                for i in range(8):
                    display_text("ABCDEFGH"[i], lil_font, i * 100 + 65, 818, (0, 0, 0))
                    display_text("87654321"[i], lil_font, 7, i * 100 + 60, (0, 0, 0))
            else:
                if (row + col) % 2 != 0:
                    pygame.draw.rect(game_display, (100, 100, 100), (x, y, 100, 100))
                else:
                    pygame.draw.rect(game_display, (255, 255, 255), (x, y, 100, 100))
                for i in range(8):
                    display_text("HGFEDCBA"[i], lil_font, i * 100 + 65, 818, (0, 0, 0))
                    display_text("12345678"[i], lil_font, 7, i * 100 + 60, (0, 0, 0))


def display_text(text, font, x, y, color):
    displayed_text = font.render(text, True, color)
    game_display.blit(displayed_text, (x, y))


class Piece:
    def __init__(self, col, row, color):
        self.col = col
        self.row = row
        self.color = color
        self.unmoved = True
        self.sprite = None
        self.piece_type = None

    def display_sprite(self, window, x, y):
        sprite = pygame.image.load(self.sprite)
        window.blit(sprite, (x, y))

    def move(self, col, row):
        board.en_passant = False
        board.castling = None
        if self.piece_type == "pawn":
            if board.board[col][row] == 0 and col == self.col - 1:
                board.board[col][self.row] = 0
                board.en_passant = True
            elif board.board[col][row] == 0 and col == self.col + 1:
                board.board[col][self.row] = 0
                board.en_passant = True
        elif self.piece_type == "king":
            if col == self.col + 2:
                board.board[self.col + 1][row] = board.board[self.col + 3][row]
                board.board[self.col + 3][row].col, board.board[self.col + 3][row].row = self.col + 1, row
                board.board[self.col + 3][row] = 0
                board.castling = "kingside"
            elif col == self.col - 2:
                board.board[self.col - 1][row] = board.board[self.col - 4][row]
                board.board[self.col - 4][row].col, board.board[self.col - 4][row].row = self.col - 1, row
                board.board[self.col - 4][row] = 0
                board.castling = "queenside"
        col1, row1 = self.col, self.row
        self.col, self.row = col, row
        board.board[col][row] = self
        board.board[col1][row1] = 0
        board.selected_piece = ()
        board.selected_any = False
        board.last_move = (col1, row1, self.col, self.row)


class Pawn(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "pawn"
        self.value = 1
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"

    def valid_moves(self):
        row = self.row
        col = self.col
        moves = []

        if self.color == "black":
            if row < 7:
                p = board.board[col][row + 1]
                if p == 0:
                    moves.append((col, row + 1))
            if self.unmoved and self.row == 1:
                p1 = board.board[col][row + 1]
                p2 = board.board[col][row + 2]
                if p1 == 0 and p2 == 0:
                    moves.append((col, row + 2))
            if col < 7 and row < 7:
                p = board.board[col + 1][row + 1]
                if p != 0:
                    if p.color != self.color:
                        moves.append((col + 1, row + 1))
            if col > 0 and row < 7:
                p = board.board[col - 1][row + 1]
                if p != 0:
                    if p.color != self.color:
                        moves.append((col - 1, row + 1))
            try:
                if board.last_move == (col-1, row+2, col-1, row) and board.board[col - 1][row].piece_type == "pawn":
                    moves.append((col - 1, row + 1))
                if board.last_move == (col+1, row+2, col+1, row) and board.board[col + 1][row].piece_type == "pawn":
                    moves.append((col + 1, row + 1))
            except:
                pass
        elif self.color == "white":
            if row > 0:
                p = board.board[col][row-1]
                if p == 0:
                    moves.append((col, row-1))
            if self.unmoved and self.row == 6:
                p1 = board.board[col][row - 1]
                p2 = board.board[col][row - 2]
                if p1 == 0 and p2 == 0:
                    moves.append((col, row-2))
            if col < 7:
                p = board.board[col+1][row-1]
                if p != 0:
                    if p.color != self.color:
                        moves.append((col+1, row-1))
            if col > 0:
                p = board.board[col-1][row-1]
                if p != 0:
                    if p.color != self.color:
                        moves.append((col-1, row-1))
            try:
                if board.last_move == (col-1, row-2, col-1, row) and board.board[col-1][row].piece_type == "pawn":
                    moves.append((col-1, row-1))
                if board.last_move == (col+1, row-2, col+1, row) and board.board[col+1][row].piece_type == "pawn":
                    moves.append((col+1, row-1))
            except:
                pass
        return moves


class Bishop(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "bishop"
        self.value = 3
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"

    def valid_moves(self):
        col = self.col
        row = self.row
        moves = []

        # up right
        right = col + 1
        left = col - 1
        for i in range(row - 1, -1, -1):
            if right < 8:
                p = board.board[right][i]
                if p == 0:
                    moves.append((right, i))
                elif p.color != self.color:
                    moves.append((right, i))
                    break
                else:
                    break
            else:
                break
            right += 1
        # up left
        for i in range(row - 1, -1, -1):
            if left > -1:
                p = board.board[left][i]
                if p == 0:
                    moves.append((left, i))
                elif p.color != self.color:
                    moves.append((left, i))
                    break
                else:
                    break
            else:
                break
            left -= 1

        right = col + 1
        left = col - 1

        # down right
        for i in range(row + 1, 8):
            if right < 8:
                p = board.board[right][i]
                if p == 0:
                    moves.append((right, i))
                elif p.color != self.color:
                    moves.append((right, i))
                    break
                else:
                    break
            else:
                break
            right += 1
        # down left

        for i in range(row + 1, 8):
            if left > -1:
                p = board.board[left][i]
                if p == 0:
                    moves.append((left, i))
                elif p.color != self.color:
                    moves.append((left, i))
                    break
                else:
                    break
            else:
                break
            left -= 1

        return moves


class Rook(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "rook"
        self.value = 5
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"

    def valid_moves(self):
        row = self.row
        col = self.col
        moves = []

        # up
        for i in range(row - 1, -1, -1):
            p = board.board[col][i]
            if p == 0:
                moves.append((col, i))
            elif p.color != self.color:
                moves.append((col, i))
                break
            else:
                break

        # down
        for i in range(row + 1, 8):
            p = board.board[col][i]
            if p == 0:
                moves.append((col, i))
            elif p.color != self.color:
                moves.append((col, i))
                break
            else:
                break

        # left
        for i in range(col - 1, -1, -1):
            p = board.board[i][row]
            if p == 0:
                moves.append((i, row))
            elif p.color != self.color:
                moves.append((i, row))
                break
            else:
                break

        # right
        for i in range(col + 1, 8):
            p = board.board[i][row]
            if p == 0:
                moves.append((i, row))
            elif p.color != self.color:
                moves.append((i, row))
                break
            else:
                break

        return moves


class Knight(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "knight"
        self.value = 3
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"

    def valid_moves(self):
        col = self.col
        row = self.row
        moves = []

        if col < 7 and row < 6:
            p = board.board[col + 1][row + 2]
            if p == 0 or p.color != self.color:
                moves.append((col + 1, row + 2))
        if col < 7 and row > 1:
            p = board.board[col + 1][row - 2]
            if p == 0 or p.color != self.color:
                moves.append((col + 1, row - 2))
        if col > 0 and row < 6:
            p = board.board[col - 1][row + 2]
            if p == 0 or p.color != self.color:
                moves.append((col - 1, row + 2))
        if col > 0 and row > 1:
            p = board.board[col - 1][row - 2]
            if p == 0 or p.color != self.color:
                moves.append((col - 1, row - 2))
        if col < 6 and row < 7:
            p = board.board[col + 2][row + 1]
            if p == 0 or p.color != self.color:
                moves.append((col + 2, row + 1))
        if col < 6 and row > 0:
            p = board.board[col + 2][row - 1]
            if p == 0 or p.color != self.color:
                moves.append((col + 2, row - 1))
        if col > 1 and row < 7:
            p = board.board[col - 2][row + 1]
            if p == 0 or p.color != self.color:
                moves.append((col - 2, row + 1))
        if col > 1 and row > 0:
            p = board.board[col - 2][row - 1]
            if p == 0 or p.color != self.color:
                moves.append((col - 2, row - 1))

        return moves


class Queen(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "queen"
        self.value = 10
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"

    def valid_moves(self):
        col = self.col
        row = self.row
        moves = []

        # up right
        right = col + 1
        left = col - 1
        for i in range(row - 1, -1, -1):
            if right < 8:
                p = board.board[right][i]
                if p == 0:
                    moves.append((right, i))
                elif p.color != self.color:
                    moves.append((right, i))
                    break
                else:
                    break
            else:
                break
            right += 1
        # up left
        for i in range(row - 1, -1, -1):
            if left > -1:
                p = board.board[left][i]
                if p == 0:
                    moves.append((left, i))
                elif p.color != self.color:
                    moves.append((left, i))
                    break
                else:
                    break
            else:
                break
            left -= 1

        right = col + 1
        left = col - 1

        # down right
        for i in range(row + 1, 8):
            if right < 8:
                p = board.board[right][i]
                if p == 0:
                    moves.append((right, i))
                elif p.color != self.color:
                    moves.append((right, i))
                    break
                else:
                    break
            else:
                break
            right += 1
        # down left
        for i in range(row + 1, 8):
            if left > -1:
                p = board.board[left][i]
                if p == 0:
                    moves.append((left, i))
                elif p.color != self.color:
                    moves.append((left, i))
                    break
                else:
                    break
            else:
                break
            left -= 1

        # up
        for i in range(row - 1, -1, -1):
            p = board.board[col][i]
            if p == 0:
                moves.append((col, i))
            elif p.color != self.color:
                moves.append((col, i))
                break
            else:
                break

        # down
        for i in range(row + 1, 8):
            p = board.board[col][i]
            if p == 0:
                moves.append((col, i))
            elif p.color != self.color:
                moves.append((col, i))
                break
            else:
                break

        # left
        for i in range(col - 1, -1, -1):
            p = board.board[i][row]
            if p == 0:
                moves.append((i, row))
            elif p.color != self.color:
                moves.append((i, row))
                break
            else:
                break

        # right
        for i in range(col + 1, 8):
            p = board.board[i][row]
            if p == 0:
                moves.append((i, row))
            elif p.color != self.color:
                moves.append((i, row))
                break
            else:
                break

        return moves


class King(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "king"
        self.value = 9001
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"

    def valid_moves(self):
        row = self.row
        col = self.col
        moves = []
        if row > 0:
            # up left
            if col > 0:
                p = board.board[col-1][row-1]
                if p == 0:
                    moves.append((col-1, row-1))
                elif p.color != self.color:
                    moves.append((col-1, row-1))
            # up
            p = board.board[col][row-1]
            if p == 0 or p.color != self.color:
                moves.append((col, row-1))
            # up right
            if col < 7:
                p = board.board[col+1][row-1]
                if p == 0 or p.color != self.color:
                    moves.append((col+1, row-1))
        if row < 7:
            # down left
            if col > 0:
                p = board.board[col-1][row+1]
                if p == 0:
                    moves.append((col-1, row+1))
                elif p.color != self.color:
                    moves.append((col-1, row+1))
            # down
            p = board.board[col][row+1]
            if p == 0 or p.color != self.color:
                moves.append((col, row+1))
            # down right
            if col < 7:
                p = board.board[col+1][row+1]
                if p == 0 or p.color != self.color:
                    moves.append((col+1, row+1))
        if col > 0:
            # left
            p = board.board[col-1][row]
            if p == 0 or p.color != self.color:
                moves.append((col-1, row))
        if col < 7:
            # right
            p = board.board[col+1][row]
            if p == 0 or p.color != self.color:
                moves.append((col+1, row))
        # castling king side
        if self.unmoved: # and self.is not atatcked
            try:
                # king side castling
                p1 = board.board[col+1][row]
                p2 = board.board[col+2][row]
                p3 = board.board[col+3][row]
                if p1 == 0 and p2 == 0 and p3.unmoved:
                    moves.append((col+2, row))
                # castling queen side
                p1 = board.board[col - 1][row]
                p2 = board.board[col - 2][row]
                p3 = board.board[col - 3][row]
                p4 = board.board[col - 4][row]
                if p1 == 0 and p2 == 0 and p3 == 0 and p4.unmoved:
                    moves.append((col - 2, row))
            except:
                pass


        return moves


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
        self.en_passant = False
        self.castling = None

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

    def display_pieces(self):
        for row in range(8):
            for col in range(8):
                if self.board[col][row] != 0:
                    p = self.board[col][row]
                    if player_color == "white":
                        p.display_sprite(game_display, col * 100 + 20, row * 100 + 20)
                    else:
                        p.display_sprite(game_display, (7 - col) * 100 + 20, (7 - row) * 100 + 20)


board = Board()
