import pygame
pygame.init()
lil_font = pygame.font.SysFont("arial", 20, bold=True, italic=False)
big_font = pygame.font.SysFont("arialblack", 40, False, False)

game_display = pygame.display.set_mode((840, 840))
player_color = "black"


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

    def display_sprite(self, window, x, y):
        sprite = pygame.image.load(self.sprite)
        window.blit(sprite, (x, y))


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