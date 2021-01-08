import pygame
import numpy as np
pygame.init()
lil_font = pygame.font.SysFont("arial", 20, bold=True, italic=False)
big_font = pygame.font.SysFont("arialblack", 40, bold=False, italic=False)
help_font = pygame.font.SysFont("arialblack", 30, bold=False, italic=False)

game_display = pygame.display.set_mode((840, 840))
player_color = "white"
computer_color = "black"
message = "Fuck you"
ai_difficulty = 3


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
        board.changed_to_queen = False
        board.stolen_piece = board.board[col][row]
        if self.piece_type == "pawn":
            if board.board[col][row] == 0 and (col == self.col - 1 or col == self.col + 1):
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
        if self.piece_type == "pawn":
            if self.row == 7 or self.row == 0:
                board.board[self.col][self.row] = Queen(self.col, self.row, self.color)
                board.changed_to_queen = True
        board.selected_piece = ()
        board.selected_any = False

        board.last_move = (col1, row1, self.col, self.row)

    def new_valid_moves(self):
        moves = self.valid_moves()
        removed_moves = []
        for move in moves:
            removed_piece = board.board[move[0]][move[1]]
            board.board[move[0]][move[1]] = self
            board.board[self.col][self.row] = 0
            if self.color == "white":
                danger_moves = board.get_all_moves("black")
                for dgmove in danger_moves:
                    try:
                        if board.board[dgmove[0]][dgmove[1]].piece_type == "king":
                            removed_moves.append(move)
                    except:
                        pass
            else:
                danger_moves = board.get_all_moves("white")
                for dgmove in danger_moves:
                    try:
                        if board.board[dgmove[0]][dgmove[1]].piece_type == "king":
                            removed_moves.append(move)
                    except:
                        pass
            board.board[move[0]][move[1]] = removed_piece
            board.board[self.col][self.row] = self
        for remmove in removed_moves:
            try:
                moves.remove(remmove)
            except ValueError:
                pass
        return moves

    def display_moves(self):
        for move in self.new_valid_moves():
            if player_color == "white":
                pygame.draw.circle(game_display, (0, 0, 255), (move[0]*100 + 70, move[1]*100 + 70), 10)
            else:
                pygame.draw.circle(game_display, (0, 0, 255), ((7-move[0]) * 100 + 70, (7-move[1]) * 100 + 70), 10)


class Pawn(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.piece_type = "pawn"
        self.value = 1
        self.selected = False
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"
        self.table = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0, 0, 0, 0, 0, 0, 0, 0]])

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
        self.table = np.array([
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]])

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
        self.unmoved = True
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"
        self.table = np.array([
            [0, 0, 0, 5, 5, 0, 0, 0],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]])

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
        self.table = np.array([
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 15, 20, 20, 15, 0, -30],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]])

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
        self.table = np.array([
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 5, 0, 0, 0, 0, -10],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-5, 0, 5, 5, 5, 5, 0, -5],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]])

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
        self.unmoved = True
        self.sprite = f"Sprites/{self.color}_{self.piece_type}.png"
        self.table = [[0 for _ in range(8)] for i in range(8)]

    def valid_moves(self):
        global computer_color
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
        if self.unmoved:
            try:
                # king side castling
                p1 = board.board[col + 1][row]
                p2 = board.board[col + 2][row]
                p3 = board.board[col + 3][row]
                if p1 == 0 and p2 == 0 and p3.unmoved:
                    moves.append((col + 2, row))
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
        self.changed_to_queen = False
        self.stolen_piece = None

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

        self.last_move = (-1, -1, -1, -1)
        self.en_passant = False
        self.changed_to_queen = False
        self.castling = None
        self.turn = "white"

    def display_pieces(self):
        for row in range(8):
            for col in range(8):
                if self.board[col][row] != 0:
                    p = self.board[col][row]
                    if player_color == "white":
                        p.display_sprite(game_display, col * 100 + 20, row * 100 + 20)
                    else:
                        p.display_sprite(game_display, (7 - col) * 100 + 20, (7 - row) * 100 + 20)

    def get_all_pieces(self, color):
        pieces = []
        for i in range(8):
            for j in range(8):
                p = self.board[i][j]
                if p != 0:
                    if p.color == color:
                        pieces.append((i, j))
        return pieces

    def get_all_moves(self, color):
        all_moves = []
        pieces = self.get_all_pieces(color)
        for piece in pieces:
            moves = self.board[piece[0]][piece[1]].valid_moves()
            for move in moves:
                all_moves.append(move)
        return all_moves

    def check(self, color): # checks if color gives check
        moves = self.get_all_moves(color)
        for move in moves:
            try:
                if self.board[move[0]][move[1]].piece_type == "king":
                    return True
            except:
                pass
        return False

    def check_mate(self, color1, color2): # checks if color1 is mated by color2
        pieces = self.get_all_pieces(color1)
        moves = []
        for piece in pieces:
            for move in self.board[piece[0]][piece[1]].new_valid_moves():
                moves.append(move)
        if not moves and self.check(color2):
            return True
        return False

    def stale_mate(self, color1, color2): # color1 has no moves but is not in check -> stale mate
        # add some shit to make to make the draw after 3 same moves or 50 non-capturing moves
        pieces = self.get_all_pieces(color1)
        moves = []
        for piece in pieces:
            for move in self.board[piece[0]][piece[1]].new_valid_moves():
                moves.append(move)
        if not moves and not self.check(color2):
            return True
        return False

    def undo_move(self):
        self.board[self.last_move[0]][self.last_move[1]] = self.board[self.last_move[2]][self.last_move[3]]
        self.board[self.last_move[0]][self.last_move[1]].col = self.last_move[0]
        self.board[self.last_move[0]][self.last_move[1]].row = self.last_move[1]
        self.board[self.last_move[2]][self.last_move[3]] = self.stolen_piece
        if self.en_passant:
            self.board[self.last_move[2]][self.last_move[1]] = Pawn(self.last_move[2], self.last_move[1], self.turn)
        elif self.castling == "kingside":
            self.board[7][self.last_move[1]] = Rook(7, self.last_move[1], self.board[4][self.last_move[1]].color)
            self.board[5][self.last_move[1]] = 0
        elif self.castling == "queenside":
            self.board[0][self.last_move[1]] = Rook(0, self.last_move[1], self.board[4][self.last_move[1]].color)
            self.board[3][self.last_move[1]] = 0
        elif self.changed_to_queen:
            self.board[self.last_move[0]][self.last_move[1]] = Pawn(self.last_move[0], self.last_move[1], self.board[self.last_move[0]][self.last_move[1]].color)
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        self.last_move = None
        self.changed_to_queen = False
        self.castling = None
        self.en_passant = False

    def evaluate_board(self, color):
        white = 0
        black = 0
        if self.stale_mate("black", "white") or self.stale_mate("white", "black"):
            return 0
        if self.check_mate("white", "black"):
            if color == "white":
                return -9001
            return 9001
        if self.check_mate("black", "white"):
            if color == "black":
                return -9001
            return 9001
        for col in range(8):
            for row in range(8):
                if self.board[col][row] != 0:
                    p = self.board[col][row]
                    if p.color == "white":
                        white += p.value
                        white += p.table[col][row] / 100
                    else:
                        black += p.value
                        black += p.table[7-col][row] / 100
        if color == "white":
            return white - black
        else:
            return black - white

    def game_ended(self):
        if self.check_mate("white", "black") or self.check_mate("black", "white"):
            return True
        if self.stale_mate("white", "black") or self.stale_mate("black", "white"):
            return True
        return False

    def damn_moves(self, color):
        all_moves = []
        pieces = self.get_all_pieces(color)
        for piece in pieces:
            moves = self.board[piece[0]][piece[1]].new_valid_moves()
            for move in moves:
                all_moves.append((piece, move))
        return all_moves

    def make_move(self, pos, end):
        self.board[pos[0]][pos[1]].col, self.board[pos[0]][pos[1]].row = end
        self.board[end[0]][end[1]] = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = 0

    def unmake_move(self, pos, end, piece):
        self.board[end[0]][end[1]].col, self.board[end[0]][end[1]].row = pos
        self.board[pos[0]][pos[1]] = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = piece

    def minimax(self, depth, alpha, beta, maxcolor, mincolor, max_player):
        if depth == 0 or self.game_ended():
            return self.evaluate_board(maxcolor)
        if max_player:
            maxEval = -10000
            moves = self.damn_moves(maxcolor)
            for move in moves:
                taken_piece = self.board[move[1][0]][move[1][1]]
                self.make_move(move[0], move[1])
                eval = self.minimax(depth - 1, alpha, beta, maxcolor, mincolor, max_player=False)
                self.unmake_move(move[0], move[1], taken_piece)
                if eval > maxEval:
                    bestMove = move
                    maxEval = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if depth == 2:
                return bestMove
            return maxEval
        else:
            minEval = 10000
            moves = self.damn_moves(mincolor)
            for move in moves:
                taken_piece = self.board[move[1][0]][move[1][1]]
                self.make_move(move[0], move[1])
                eval = self.minimax(depth - 1, alpha, beta, maxcolor, mincolor, max_player=True)
                self.unmake_move(move[0], move[1], taken_piece)
                minEval = min(minEval, eval)
                if eval <= alpha:
                    break
            return minEval


board = Board()
