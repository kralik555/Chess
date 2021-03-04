import pygame, time, random, math, timeit
pygame.init()
game_display = pygame.display.set_mode((800, 800))
player_color = "black"
ai_color = "white"
directions = [8, -8, -1, 1, 7, 9, -9, -7]
s = pygame.Surface((100, 100))
s.set_alpha(64)
s.fill((255, 0, 0))
gr = pygame.Surface((100, 100))
gr.set_alpha(64)
gr.fill((0, 255, 0))
board_states = []
ai_difficulty = 3
piece_values = {"pawn": 100, "queen": 900, "rook": 500, "bishop": 300, "knight": 300, "king": 100000}


class Board:

    def __init__(self):
        self.board = [0 for _ in range(64)]
        self.to_move = "white"
        self.chosen = -1
        self.castlings = "KQkq"
        self.squares_to_edge = {}
        self.en_passant = None
        self.half_moves = 0
        self.full_moves = 0
        self.pieces = {"pawn": {"white": [], "black": []},
                       "bishop": {"white": [], "black": []},
                       "knight": {"white": [], "black": []},
                       "rook": {"white": [], "black": []},
                       "queen": {"white": [], "black": []},
                       "king": {"white": [], "black": []}}
        self.states = []
        self.searching = False
        self.piece_square_tables = {
            "pawn": [0,  0,  0,  0,  0,  0,  0,  0,
                     50, 50, 50, 50, 50, 50, 50, 50,
                     10, 10, 20, 30, 30, 20, 10, 10,
                     5,  5, 10, 25, 25, 10,  5,  5,
                     0,  0,  0, 20, 20,  0,  0,  0,
                     5, -5, -10,  0,  0, -10, -5,  5,
                     5, 10, 10, -32, -31, 10, 10,  5,
                     0,  0,  0,  0,  0,  0,  0,  0],
            "knight": [-50, -40, -30, -30, -30, -30, -40, -50,
                       -40, -20,  0,  0,  0,  0, -20, -40,
                       -30,  0, 10, 15, 15, 10,  0, -30,
                       -30,  5, 15, 20, 20, 15,  5, -30,
                       -30,  0, 15, 20, 20, 15,  0, -30,
                       -30,  5, 10, 15, 15, 10,  5, -30,
                       -40, -20, 0, 5, 5, 0, -20, -40,
                       -50, -40, -30, -30, -30, -30, -40, -50],
            "bishop": [-20, -10, -10, -10, -10, -10, -10, -20,
                       -10,  0,  0,  0,  0,  0,  0, -10,
                       -10,  0,  5, 10, 10,  5,  0, -10,
                       -10,  5,  5, 10, 10,  5,  5, -10,
                       -10,  0, 10, 10, 10, 10,  0, -10,
                       -10, 10, 10, 10, 10, 10, 10, -10,
                       -10,  5,  0,  0,  0,  0,  5, -10,
                       -20, -10, -10, -10, -10, -10, -10, -20],
            "rook": [0,  0,  0,  0,  0,  0,  0,  0,
                     5, 10, 10, 10, 10, 10, 10,  5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     0,  0,  0,  5,  5,  0,  0,  0],
            "queen": [-20, -10, -10, -5, -5, -10, -10, -20,
                      -10,  0,  0,  0,  0,  0,  0, -10,
                      -10,  0,  5,  5,  5,  5,  0, -10,
                      -5,  0,  5,  5,  5,  5,  0, -5,
                      0,  0,  5,  5,  5,  5,  0, -5,
                      -10,  5,  5,  5,  5,  5,  0, -10,
                      -10,  0,  5,  0,  0,  0,  0, -10,
                      -20, -10, -10, -5, -5, -10, -10, -20],
            "king": [-30, -40, -40, -50, -50, -40, -40, -30,
                     -30, -40, -40, -50, -50, -40, -40, -30,
                     -30, -40, -40, -50, -50, -40, -40, -30,
                     -30, -40, -40, -50, -50, -40, -40, -30,
                     -20, -30, -30, -40, -40, -30, -30, -20,
                     -10, -20, -20, -20, -20, -20, -20, -10,
                     20, 20,  0,  0,  0,  0, 20, 20,
                     20, 30, 10,  0,  0, 10, 30, 20]}


def moves(tile):
    if board.board[tile] == 0:
        return []
    if board.board[tile].piece_type in ["bishop", "queen", "rook"]:
        return sliding_moves(tile)
    if board.board[tile].piece_type == "king":
        return king_moves(tile)
    if board.board[tile].piece_type == "knight":
        return knight_moves(tile)
    if board.board[tile].piece_type == "pawn":
        return pawn_moves(tile)


def pawn_moves(tile):
    moves = []
    if board.board[tile].color == "white":
        if board.board[tile + 8] == 0:
            moves.append((tile, tile+8))
        if tile // 8 == 1:
            if board.board[tile + 8] == 0 and board.board[tile + 16] == 0:
                moves.append((tile, tile+16))
        if board.board[tile+7] != 0 and tile % 8 != 0:
            if board.board[tile + 7].color != board.board[tile].color:
                moves.append((tile, tile+7))
        if tile + 9 in range(64):
            if board.board[tile+9] != 0 and tile % 8 != 7:
                if board.board[tile + 9].color != board.board[tile].color:
                    moves.append((tile, tile+9))
        # add en passant, something with fen
        if board.en_passant == tile + 7 or board.en_passant == tile + 9:
            moves.append((tile, board.en_passant))
    else:
        if board.board[tile - 8] == 0:
            moves.append((tile, tile-8))
        if tile // 8 == 6:
            if board.board[tile - 8] == 0 and board.board[tile - 16] == 0:
                moves.append((tile, tile-16))
        if board.board[tile-7] != 0 and tile % 8 != 7:
            if board.board[tile - 7].color != board.board[tile].color:
                moves.append((tile, tile-7))
        if board.board[tile-9] != 0 and tile % 8 != 0:
            if board.board[tile - 9].color != board.board[tile].color:
                moves.append((tile, tile-9))
        if board.en_passant == tile - 7 or board.en_passant == tile - 9:
            moves.append((tile, board.en_passant))
    return moves


def king_moves(tile):
    directions = [9, 1, -7, 8, -8, -9, -1, 7]
    colors = ["white", "black"]
    opponent_color = colors[colors.index(board.board[tile].color)-1]
    moves = []
    if tile % 8 == 7:
        for direction in directions[3:]:
            if tile + direction in range(64):
                if board.board[tile+direction] != 0:
                    if board.board[tile+direction].color == board.board[tile].color:
                        continue
                    removed = board.board[tile+direction]
                    board.board[tile+direction] = 0
                    rem_king = board.board[tile]
                    board.board[tile] = 0
                    if tile+direction in attacked_squares(removed.color):
                        board.board[tile + direction] = removed
                        board.board[tile] = rem_king
                        continue
                    board.board[tile + direction] = removed
                    board.board[tile] = rem_king
                moves.append((tile, tile+direction))
    elif tile % 8 == 0:
        for direction in directions[:-3]:
            if tile + direction in range(64):
                if board.board[tile + direction] != 0:
                    if board.board[tile + direction].color == board.board[tile].color:
                        continue
                    removed = board.board[tile + direction]
                    rem_king = board.board[tile]
                    board.board[tile + direction] = 0
                    board.board[tile] = 0
                    if tile + direction in attacked_squares(removed.color):
                        board.board[tile + direction] = removed
                        board.board[tile] = rem_king
                        continue
                    board.board[tile + direction] = removed
                    board.board[tile] = rem_king
                moves.append((tile, tile + direction))
    else:
        for direction in directions:
            if tile + direction in range(64):
                if board.board[tile + direction] != 0:
                    if board.board[tile + direction].color == board.board[tile].color:
                        continue
                    removed = board.board[tile + direction]
                    rem_king = board.board[tile]
                    board.board[tile] = 0
                    board.board[tile + direction] = 0
                    if tile + direction in attacked_squares(removed.color):
                        board.board[tile + direction] = removed
                        board.board[tile] = rem_king
                        continue
                    board.board[tile + direction] = removed
                    board.board[tile] = rem_king
                moves.append((tile, tile + direction))
    try:
        if board.board[tile].color == "white" and tile == 4:
            if "K" in get_fen().split(" ")[2] and board.board[tile+1] == 0 and board.board[tile+2] == 0 \
                    and tile not in attacked_squares(opponent_color) and tile+1 not in attacked_squares(opponent_color):
                moves.append((tile, tile+2))
            if "Q" in get_fen().split(" ")[2] and board.board[tile-1] == 0 and board.board[tile-2] == 0 and board.board[tile-3] == 0:
                moves.append((tile, tile-2))
        if board.board[tile].color == "black" and tile == 60:
            if "k" in get_fen().split(" ")[2] and board.board[tile+1] == 0 and board.board[tile+2] == 0:
                moves.append((tile, tile+2))
            if "q" in get_fen().split(" ")[2] and board.board[tile-1] == 0 and board.board[tile-2] == 0 and board.board[tile-3] == 0:
                moves.append((tile, tile-2))
    except:
        pass
    i = 0
    removed = board.board[tile]
    board.board[tile] = 0
    while i < len(moves):
        if moves[i][1] in attacked_squares(opponent_color):
            moves.pop(i)
        else:
            i += 1
    board.board[tile] = removed
    return moves


def simple_king_moves(color):
    directions = [9, 1, -7, 8, -8, -9, -1, 7]
    king_tile = board.pieces["king"][color][0]
    moves = []
    if king_tile % 8 == 7:
        for i in directions[3::]:
            if king_tile + i in range(64):
                moves.append(king_tile + i)
    elif king_tile % 8 == 0:
        for i in directions[:-3:]:
            if king_tile + i in range(0, 64):
                moves.append(king_tile + i)
    else:
        for i in directions:
            if king_tile + i in range(0, 64):
                moves.append(king_tile + i)
    return moves


def knight_moves(tile):
    moves = []
    directions = [15, -15, 17, -17, 6, -6, 10, -10]
    col = tile % 8
    row = tile // 8
    if row == 7:
        if 15 in directions: directions.remove(15)
        if 17 in directions: directions.remove(17)
        if 6 in directions: directions.remove(6)
        if 10 in directions: directions.remove(10)
    if row == 6:
        if 15 in directions: directions.remove(15)
        if 17 in directions: directions.remove(17)
    if row == 0:
        if -15 in directions: directions.remove(-15)
        if -17 in directions: directions.remove(-17)
        if -6 in directions: directions.remove(-6)
        if -10 in directions: directions.remove(-10)
    if row == 1:
        if -15 in directions: directions.remove(-15)
        if -17 in directions: directions.remove(-17)
    if col == 7:
        if 17 in directions: directions.remove(17)
        if 10 in directions: directions.remove(10)
        if -6 in directions: directions.remove(-6)
        if -15 in directions: directions.remove(-15)
    if col == 6:
        if -6 in directions: directions.remove(-6)
        if 10 in directions: directions.remove(10)
    if col == 0:
        if 6 in directions: directions.remove(6)
        if 15 in directions: directions.remove(15)
        if -10 in directions: directions.remove(-10)
        if -17 in directions: directions.remove(-17)
    if col == 1:
        if 6 in directions: directions.remove(6)
        if -10 in directions: directions.remove(-10)
    for direction in directions:
        if tile + direction < 64:
            if board.board[tile+direction] != 0:
                if board.board[tile+direction].color == board.board[tile].color:
                    continue
            moves.append((tile, tile+direction))
    return moves


def sliding_moves(tile):
    start = 0
    end = 8
    if board.board[tile].piece_type == "rook":
        end = 4
    elif board.board[tile].piece_type == "bishop":
        start = 4
    moves = []
    for i in range(start, end):
        for j in range(board.squares_to_edge[tile][i]):
            target_square = tile + directions[i] * (j+1)
            if board.board[target_square] != 0:
                if board.board[target_square].color == board.board[tile].color:
                    break
            moves.append((tile, target_square))
            if board.board[target_square] != 0:
                if board.board[target_square].color != board.board[tile].color:
                    break
    return moves


def squares_to_edge():
    list_offsets = {}
    for col in range(8):
        for row in range(8):
            num_top = 7-row
            num_bot = row
            num_right = 7 - col
            num_left = col
            square_index = row * 8 + col
            list_offsets[square_index] = [num_top, num_bot, num_left, num_right, min(num_left, num_top),
                                          min(num_right, num_top), min(num_bot, num_left), min(num_bot, num_right)]
    return list_offsets


class Piece:
    piece_types = ["king", "queen", "bishop", "rook", "knight", "pawn"]

    def __init__(self, color, tile, piece_type):
        self.color = color
        self.tile = tile
        self.piece_type = piece_type


def display_board():
    for i in range(8):
        for j in range(8):
            if (i+j) % 2 == 0:
                pygame.draw.rect(game_display, (255, 255, 255), (j*100, i*100, 100, 100))
            else:
                pygame.draw.rect(game_display, (150, 150, 150), (j * 100, i * 100, 100, 100))


def display_pieces():
    for i in board.board:
        if i != 0:
            sprite = pygame.image.load(f"Sprites/{i.color}_{i.piece_type}.png")
            if player_color == "black":
                game_display.blit(sprite, (i.tile % 8 * 100, i.tile // 8 * 100))
            else:
                game_display.blit(sprite,  (i.tile % 8 * 100, (7 - i.tile // 8) * 100))


def apply_fen(fen_str):
    pieces_symbols = {"k": "king", "q": "queen", "b": "bishop", "n": "knight", "r": "rook", "p": "pawn"}
    board_str = fen_str.split(" ")[0]
    x = 0
    y = 7
    # board
    for i in range(64):
        board.board[i] = 0
    for char in board_str:
        if char == "/":
            x = 0
            y -= 1
        else:
            if char in "12345678":
                x += eval(char)
            else:
                if char.islower():
                    color = "black"
                else:
                    color = "white"
                board.board[8*y + x] = Piece(color, 8*y + x, pieces_symbols[char.lower()])
                x += 1
                board.pieces[pieces_symbols[char.lower()]][color].append(8*y + x-1)
    string = fen_str.split(" ")
    # to move
    if string[1] == "w":
        board.to_move = "white"
    else:
        board.to_move = "black"
    # castlings
    board.castlings = string[2]
    letters = "abcdefgh"
    # en passants
    if string[3] == "-":
        board.en_passant = None
    else:
        board.en_passant = letters.index(string[3][0]) + (int(string[3][1]) - 1) * 8
    # half moves
    board.half_moves = int(string[4])
    # full moves
    board.full_moves = int(string[5])


def get_fen():
    piece_dic = ["k", "q", "b", "r", "n", "p"]
    fen_string = ""
    empty_num = 0
    # piece positions
    for i in range(0, 64):
        j = i // 8 * 8 + 7 - (i % 8)
        if i % 8 == 0 and i != 0:
            if empty_num != 0:
                fen_string += str(empty_num)
                empty_num = 0
            fen_string += "/"
        elif i == 63 and board.board[j] == 0:
            empty_num += 1
            fen_string += str(empty_num)
        if board.board[j] != 0:
            if board.board[j].color == "white":
                letter = piece_dic[board.board[j].piece_types.index(board.board[j].piece_type)].upper()
            else:
                letter = piece_dic[board.board[j].piece_types.index(board.board[j].piece_type)]
            if empty_num == 0:
                fen_string += letter
            else:
                fen_string += str(empty_num)
                fen_string += letter
                empty_num = 0
        else:
            empty_num += 1
    # move
    fen_string = fen_string[::-1]
    if fen_string[0] == "/":
        fen_string = fen_string[::-1]
        fen_string += "8"
        fen_string = fen_string[::-1]
    fen_string += " "
    fen_string += board.to_move[0]
    # castling
    fen_string += " "
    fen_string += board.castlings
    # en passants
    fen_string += " "
    if not board.en_passant:
        fen_string += "-"
    else:
        letters = "abcdefgh"
        fen_string += f"{letters[board.en_passant % 8]}{board.en_passant // 8 + 1}"
    # halfmoves
    fen_string += " "
    fen_string += f"{board.half_moves}"
    # full moves
    fen_string += " "
    fen_string += f"{board.full_moves}"

    return fen_string


def move(start, end):
    board.states.append(get_fen())
    new_passant = board.en_passant
    board.en_passant = None
    if board.board[start].piece_type != "pawn" and board.board[end] == 0:
        board.half_moves += 1
    else:
        board.half_moves = 0
    if not board.searching:
        if board.board[start].piece_type == "king":
            if board.board[start].color == "white":
                board.castlings = board.castlings.replace("K", "")
                board.castlings = board.castlings.replace("Q", "")
            else:
                board.castlings = board.castlings.replace("k", "")
                board.castlings = board.castlings.replace("q", "")
        if start == 0 or end == 0:
            board.castlings = board.castlings.replace("Q", "")
        if start == 7 or end == 0:
            board.castlings = board.castlings.replace("K", "")
        if start == 63 or end == 63:
            board.castlings = board.castlings.replace("k", "")
        if start == 56 or end == 56:
            board.castlings = board.castlings.replace("q", "")
    if board.castlings == "":
        board.castlings = "-"
    if board.board[start].piece_type == "king" and end == start + 2:
        board.board[end - 1] = Piece(board.board[start].color, end - 1, "rook")
        board.board[end - 1].tile = end - 1
        board.board[end + 1] = 0
    if board.board[start].piece_type == "king" and end == board.chosen - 2:
        board.board[end + 1] = Piece(board.board[start].color, end + 1, "rook")
        board.board[end + 1].tile = end + 1
        board.board[end - 2] = 0
    board.board[end] = 0
    board.board[end] = board.board[start]
    board.board[end].tile = end
    if board.board[end].piece_type == "pawn":
        if end == start + 16:
            board.en_passant = end - 8
        if end == start - 16:
            board.en_passant = end + 8
        if new_passant == end and end > start:
            board.board[end - 8] = 0
        if new_passant == end and end < start:
            board.board[end + 8] = 0
    board.board[start] = 0
    board.chosen = -1
    if board.to_move == "white":
        board.to_move = "black"
    else:
        board.to_move = "white"
    if end < 8 or end > 55:
        if board.board[end].piece_type == "pawn":
            board.board[end] = Piece(board.board[end].color, end, "queen")
    if board.to_move == "white":
        board.full_moves += 1
    fen_srt = get_fen()
    board.pieces = {k: {i: [] for (i, _) in v.items()} for (k, v) in board.pieces.items()}
    apply_fen(fen_srt)


def pawn_attacks(color):
    attacks = []
    for i in board.pieces["pawn"][color]:
        if color == "white":
            if i % 8 != 0:
                attacks.append(i + 7)
            if i % 8 != 7:
                attacks.append(i + 9)
        else:
            if i % 8 != 0:
                attacks.append(i - 9)
            if i % 8 != 7:
                attacks.append(i - 7)
    return attacks


def attacked_squares(color):
    attacked_tiles = []
    tiles = []
    for i in ["queen", "rook", "bishop", "knight"]:
        if board.pieces[i][color]:
            for tile in board.pieces[i][color]:
                attacked_tiles.extend(moves(tile))
    pawn_attacks = []
    for i in board.pieces["pawn"][color]:
        if color == "white":
            if i % 8 != 0:
                pawn_attacks.append(i + 7)
            if i % 8 != 7:
                pawn_attacks.append(i + 9)
        else:
            if i % 8 != 0:
                pawn_attacks.append(i - 9)
            if i % 8 != 7:
                pawn_attacks.append(i - 7)
    for i in attacked_tiles:
        tiles.append(i[1])
    tiles.extend(pawn_attacks)
    tiles.extend(simple_king_moves(color))
    return tiles


def get_some_range(king_tile, attack_tile):
    if king_tile > attack_tile:
        if king_tile % 8 == attack_tile % 8:  # same column
            return list(range(attack_tile, king_tile, 8))
        if king_tile // 8 == attack_tile // 8:
            return list(range(attack_tile, king_tile))
        if king_tile % 8 - attack_tile % 8 == king_tile // 8 - attack_tile // 8:
            return list(range(attack_tile, king_tile, 9))
        if king_tile % 8 - attack_tile % 8 == -(king_tile // 8 - attack_tile // 8):
            return list(range(attack_tile, king_tile, 7))
    else:
        if king_tile % 8 == attack_tile % 8:
            return list(range(king_tile, attack_tile + 1, 8))[1:]
        if king_tile // 8 == attack_tile // 8:
            return list(range(king_tile + 1, attack_tile + 1))
        if attack_tile % 8 - king_tile % 8 == attack_tile // 8 - king_tile // 8:
            return list(range(king_tile, attack_tile + 1, 9))[1:]
        if attack_tile % 8 - king_tile % 8 == king_tile // 8 - attack_tile // 8:
            return list(range(king_tile, attack_tile + 1, 7))[1:]
    return []


def all_moves(color):
    colors = ["white", "black"]
    opponent_color = colors[colors.index(color) - 1]
    king_tile = board.pieces["king"][color][0]
    new_moves = [moves(king_tile)][0]
    pinned = pinned_pieces(color)
    if pinned[1] >= 2:  # double check
        if not new_moves:
            check_mate()
        return new_moves
    elif pinned[1] == 1:  # check
        checking = pinned[3][0]
        # if in check by horse: remove horse or move king
        if checking in board.pieces["knight"][opponent_color]:  # checked by horse
            for k in board.pieces.keys():
                for i in board.pieces[k][color]:  # every piece
                    if i not in pinned[0]:
                        for move in moves(i):
                            if checking == move[1]:
                                new_moves.append(move)
            return new_moves
        # if in check by pawn: remove pawn or move king
        if checking in board.pieces["pawn"][opponent_color]:  # checked by pawn
            for k in board.pieces.keys():
                for i in board.pieces[k][color]:  # every piece
                    if i not in pinned[0]:
                        for move in moves(i):
                            if checking == move[1]:
                                new_moves.append(move)
            return new_moves
        sq_to_rem_check = get_some_range(king_tile, checking)  # squares to get rid of check
        # does sth only if checked by sliding piece (queen, rook, bishop)
        for k in board.pieces.keys():
            for i in board.pieces[k][color]:  # for every piece of the color
                if i in pinned[0]:  # if piece is pinned
                    pinning = pinned[2][pinned[0].index(i)]
                    if checking in get_some_range(king_tile, pinning):
                        new_moves.append((i, checking))
                else:
                    # get squares it can go to to prevent check: between piece and king
                    for move in moves(i):
                        if move[1] in sq_to_rem_check:
                            new_moves.append(move)
        if not new_moves:
            check_mate()
        return new_moves
    # elif king_tile not in attacked_squares(opponent_color):
    else:
        new_moves = []
        # check for pinned pieces
        for k in board.pieces.keys():
            for i in board.pieces[k][color]:
                if i in pinned[0]:
                    for move in moves(i):
                        if move[1] in get_some_range(king_tile, pinned[2][pinned[0].index(i)]):
                            new_moves.append(move)
                else:
                    for move in moves(i):
                        new_moves.append(move)
    if not new_moves:
        stale_mate()
    return new_moves


def pinned_pieces(color):
    pinned_tiles = []
    global directions
    colors = ["white", "black"]
    opponent_color = colors[colors.index(color)-1]
    king_pos = board.pieces["king"][color][0]
    checks = 0
    pinning_tiles = []
    checking_squares = []
    # directions
    for i in range(8):
        pinned_piece = None
        direction = directions[i]
        piece_in_dir = False
        pinned_piece = None
        # all squares in direction
        for j in range(board.squares_to_edge[king_pos][i]):
            square = king_pos + direction * (j+1)
            if board.board[square] != 0:
                if board.board[square].color == color:
                    if not piece_in_dir:
                        pinned_piece = square
                        piece_in_dir = True
                    else:
                        break
                elif (board.board[square].piece_type in ["rook", "queen"] and i < 4) or \
                        (board.board[square].piece_type in ["bishop", "queen"] and i > 3):
                    if piece_in_dir:
                        pinned_tiles.append(pinned_piece)
                        pinning_tiles.append(square)
                    else:
                        checks += 1  # something with check
                        checking_squares.append(square)
                    if checks >= 2:
                        return pinned_tiles, checks, pinning_tiles, checking_squares
                    break
                else:
                    break
    for i in board.pieces["knight"][opponent_color]:
        for move in moves(i):
            if move[1] == king_pos:
                checks += 1
                checking_squares.append(i)
    for i in board.pieces["pawn"][opponent_color]:
        for move in moves(i):
            if move[1] == king_pos:
                checks += 1
                checking_squares.append(i)
    return pinned_tiles, checks, pinning_tiles, checking_squares


def check_mate():
    if not board.searching:
        display_text("check mate", big_font, 200, 380, (0, 255, 0))
        pygame.display.update()
        time.sleep(2)
        menu()


def stale_mate():
    if not board.searching:
        display_text("stale mate", big_font, 200, 380, (0, 0, 255))
        pygame.display.update()
        time.sleep(2)
        menu()


def endgame_eval():
    eval = 0
    colors = ["white", "black"]
    color = board.to_move
    opponent_color = colors[colors.index(color) - 1]
    op_king_col = board.pieces["king"][opponent_color][0] % 8
    op_king_row = board.pieces["king"][opponent_color][0] // 8
    op_king_to_c_col = max(3 - op_king_col, op_king_col - 4)
    op_king_to_c_row = max(3 - op_king_row, op_king_row - 4)
    op_dist_to_centre = op_king_to_c_col + op_king_to_c_row
    eval += op_dist_to_centre

    fr_king_col, fr_king_row = board.pieces["king"][color][0] % 8, board.pieces["king"][color][0] // 8
    dist_bet_kings_col = abs(fr_king_col - op_king_col)
    dist_bet_kings_row = abs(fr_king_row - op_king_row)
    eval += (14 - dist_bet_kings_col - dist_bet_kings_row)*1000

    return eval * 20


def eval_board():  # returns eval for the color that is supposed to move now
    # maybe add endgame eval so the computer can actually win XD
    white_eval = 0
    black_eval = 0
    endgame = True
    end_eval = 0
    for k in board.pieces.keys():
        if board.to_move == "white":
            if board.pieces[k]["black"] and k != "king":
                endgame = False
        else:
            if board.pieces[k]["white"] and k != "king":
                endgame = False
    if endgame:
        board.piece_square_tables["king"] = \
            [-50, -40, -30, -20, -20, -30, -40, -50,
             -30, 0, 0,  0,  0, 0, 0, 0,
             -30, 0, 0, 0, 0, 0, 0, -30,
             -30, 0, 0, 0, 0, 0, 0, -30,
             -30, 0, 0, 0, 0, 0, 0, -30,
             -30, 0, 0, 0, 0, 0, -0, -30,
             -30, 0,  0,  0,  0,  0, 0, -30,
             -50, -30, -30, -30, -30, -30, -30, -50]
        end_eval = endgame_eval()
        print("We're in the endgame now")
    for k in board.pieces.keys():
        white_eval += piece_values[k] * len(board.pieces[k]["white"])
        for i in board.pieces[k]["white"]:
            white_eval += board.piece_square_tables[k][-i - 1]
        black_eval += piece_values[k] * len(board.pieces[k]["black"])
        for i in board.pieces[k]["black"]:
            black_eval += board.piece_square_tables[k][i // 8 * 8 + 7 - i % 8]
    if board.to_move == "white":
        return white_eval - black_eval + end_eval
    else:
        return black_eval - white_eval + end_eval


def move_ordering(moves):
    colors = ["white", "black"]
    opponent_color = colors[colors.index(board.to_move) - 1]
    move_scores = {}
    multiplier = 10
    for i in range(len(moves)):
        score = 0
        if board.board[moves[i][1]] != 0:
            score = multiplier * piece_values[board.board[moves[i][1]].piece_type] - piece_values[board.board[moves[i][0]].piece_type]
        if board.board[moves[i][0]].piece_type == "pawn":
            if moves[i][1] in range(8) or moves[i][1] in range(56, 64):
                score += 900
        else:
            if moves[i][1] in pawn_attacks(opponent_color):
                score -= 350
        move_scores[i] = score
    # sort moves
    for i in range(len(moves)-1):
        for j in range(1, i+1):
            swap_index = j - 1
            if move_scores[swap_index] < move_scores[j]:
                moves[j], moves[swap_index] = moves[swap_index], moves[j]
                move_scores[j], move_scores[swap_index] = move_scores[swap_index], move_scores[j]
    return moves


def capture_search(alpha, beta):
    eval = eval_board()
    if eval >= beta:
        return beta
    if eval > alpha:
        alpha = eval
    for mov in all_moves(board.to_move):
        if board.board[mov[1]] != 0:
            move(mov[0], mov[1])
            eval = -capture_search(-beta, -alpha)
            apply_fen(board.states[-1])
            board.states.pop()
            if eval >= beta:
                return beta
            if eval > alpha:
                alpha = eval

    return alpha


def minimax(depth, alpha, beta):  # sorta kinda works not really XD
    board.searching = True
    moves = move_ordering(all_moves(board.to_move))
    best_move = None
    if not moves:
        if pinned_pieces(board.to_move)[1]:
            board.searching = False
            return -math.inf
        else:
            board.searching = False
            return 0
    if depth == 0:
        if ai_difficulty == 3:
            eval = capture_search(alpha, beta)
            board.searching = False
            return eval
        return eval_board()
    for mov in moves:
        move(mov[0], mov[1])
        evaluate = -minimax(depth - 1, -beta, -alpha)
        board.pieces = {k: {i: [] for (i, _) in v.items()} for (k, v) in board.pieces.items()}
        apply_fen(board.states[-1])
        board.states.pop()
        if evaluate > beta:
            return beta
        if evaluate > alpha:
            alpha = evaluate
            best_move = mov
    board.searching = False
    if depth == 2:
        return best_move
    return alpha


def ai_play():
    if ai_difficulty == 1:  # random
        move0 = random.choice(all_moves(ai_color))
        move(move0[0], move0[1])
    elif ai_difficulty == 2:  # sees one full move into the future
        time0 = time.time()
        mov = minimax(2, -math.inf, math.inf)
        if not mov:
            if pinned_pieces(board.to_move)[1]:
                check_mate()
            else:
                stale_mate()
        print(time.time() - time0)
        move(mov[0], mov[1])
    else:  # uses capture move search after depth 0 in minimax
        time0 = time.time()
        mov = minimax(2, -math.inf, math.inf)
        if not mov:
            if pinned_pieces(board.to_move)[1]:
                check_mate()
            else:
                stale_mate()
        print(time.time() - time0)
        move(mov[0], mov[1])


def play():
    board.states = []
    apply_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    board.squares_to_edge = squares_to_edge()
    while True:
        display_board()
        display_pieces()
        if board.chosen != -1:
            for i in moves(board.chosen):
                if i in all_moves(player_color):
                    if player_color == "black":
                        game_display.blit(s, (i[1] % 8 * 100, i[1] // 8 * 100, 100, 100))
                    else:
                        game_display.blit(s, (i[1] % 8 * 100, (7 - i[1] // 8) * 100, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_y:
                    try:
                        apply_fen(board.states[-2])
                        board.states.pop()
                        board.states.pop()
                    except IndexError:
                        pass
                if event.key == pygame.K_m:
                    menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if player_color == "black":
                    tile = y // 100 * 8 + x // 100
                else:
                    tile = (7 - y // 100) * 8 + x // 100
                if board.chosen != -1:
                    if (board.chosen, tile) in all_moves(player_color) and board.to_move == player_color:
                        move(board.chosen, tile)
                    elif board.board[tile] == 0:
                        board.chosen = -1
                    elif board.board[tile].color == player_color:
                        board.chosen = tile
                elif board.board[tile] != 0:
                    if board.to_move == player_color and board.board[tile].color == player_color:
                        board.chosen = tile
                else:
                    board.chosen = -1
        display_board()
        display_pieces()
        if board.chosen != -1:
            for i in moves(board.chosen):
                if i in all_moves(player_color):
                    if player_color == "black":
                        game_display.blit(s, (i[1] % 8 * 100, i[1] // 8 * 100, 100, 100))
                    else:
                        game_display.blit(s, (i[1] % 8 * 100, (7 - i[1] // 8) * 100, 100, 100))
        pygame.display.update()
        if board.to_move == ai_color:
            ai_play()
            board.to_move = player_color
        pygame.display.update()


# code for menu here
big_font = pygame.font.SysFont("arialblack", 40, bold=False, italic=False)
help_font = pygame.font.SysFont("arialblack", 30, bold=False, italic=False)


class Button:
    def __init__(self, color, x, y, width, height, text, func):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.func = func

    def display(self):  # displays the button with text in the middle
        pygame.draw.rect(game_display, self.color, (self.x, self.y, self.width, self.height))
        tw, th = big_font.size(self.text)
        display_text(self.text, big_font, self.x + self.width / 2 - tw / 2,
                     self.y + self.height / 2 - th / 2, (255, 255, 255))


def display_text(text, font, x, y, color):  # display text when mate or stalemate occurs
    displayed_text = font.render(text, True, color)
    game_display.blit(displayed_text, (x, y))


def help_screen():
    game_display.fill((100, 100, 100))
    # just display some advice on how to work with the app
    display_text("This is a help for the absolutely dumb ones.", help_font, 80, 50, (0, 0, 0))
    display_text("To quit this app press Q or click QUIT in menu.", help_font, 50, 100, (0, 0, 0))
    display_text("In the menu, press any key (except for Q) ", help_font, 0, 150, (0, 0, 0))
    display_text("to go to the game or just click PLAY.", help_font, 60, 200, (0, 0, 0))
    display_text("To quit this app press Q or click QUIT in menu.", help_font, 60, 250, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            else:
                return True
        pygame.display.update()


def make_quit():
    pygame.quit()
    quit()
    return True


def to_white():  # swaps player color to white
    global player_color
    global ai_color
    player_color = "white"
    ai_color = "black"


def to_black():  # swaps player color to black
    global player_color
    global ai_color
    player_color = "black"
    ai_color = "white"


def to_random():  # randomly chooses player color
    global player_color
    global ai_color
    player_color = random.choice(["white", "black"])
    if player_color == "white":
        ai_color = "black"
    else:
        ai_color = "white"


# difficulties
def easy():
    global ai_difficulty
    ai_difficulty = 1


def medium():
    global ai_difficulty
    ai_difficulty = 2


def hard():
    global ai_difficulty
    ai_difficulty = 3


def menu():  # displays menu
    # all the buttons in menu
    buttons = [Button((0, 0, 0), 320, 50, 200, 100, "Play", play),
               Button((0, 0, 0), 70, 210, 200, 100, "White", to_white),
               Button((0, 0, 0), 570, 210, 200, 100, "Random", to_random),
               Button((0, 0, 0), 320, 210, 200, 100, "Black", to_black),
               Button((0, 0, 0), 70, 380, 200, 100, "Easy", easy),
               Button((0, 0, 0), 320, 380, 200, 100, "Medium", medium),
               Button((0, 0, 0), 570, 380, 200, 100, "Hard", hard),
               Button((0, 0, 0), 320, 530, 200, 100, "Help", help_screen),
               Button((0, 0, 0), 320, 680, 200, 100, "Quit", make_quit)]
    while True:
        game_display.fill((150, 150, 150))  # grey
        for button in buttons:
            button.display()
        display_text("Choose your color", big_font, 220, 150, (0, 0, 0))
        display_text("Choose difficulty", big_font, 233, 310, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():  # checks events
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    return True
                else:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in buttons:
                    if x in range(button.x, button.x + button.width + 1) and y in range(button.y, button.y + button.height + 1):
                        button.func()


board = Board()
menu()

