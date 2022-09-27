import copy
import sys

# read the input from the given file, the exact format is similar to pattern in config.txt
def get_file_var(filename):
    f = open(filename, "r")
    content = f.readlines()
    lens = len(content)
    piece_pos = []
    num_enemy_pieces = []
    num_pieces = []
    row_num = int(content[0][5:-1])
    col_num = int(content[1][5:-1])
    enemy_piece_pos = []

    for j in content[2][72:-1].split():
        num_enemy_pieces.append(int(j))
    i = 4
    while not content[i].startswith('Number'):
        mid = content[i].find(',')
        end = content[i].find(']')
        pair = [content[i][1:mid], transfer_to_number_array(content[i][mid + 1:end])]
        enemy_piece_pos.append(pair)
        i = i + 1
    for j in content[i][70:-1].split():
        num_pieces.append(int(j))
    i += 2
    while i < lens:
        mid = content[i].find(',')
        end = content[i].find(']')
        pair = [content[i][1:mid], transfer_to_number_array(content[i][mid + 1:end])]
        piece_pos.append(pair)

        i = i + 1

    return row_num, col_num, num_enemy_pieces, enemy_piece_pos, num_pieces, piece_pos


# specify the influenced places by possible chess placed on board
class Piece:
    def __init__(self, type, is_enemy):
        self.type = type
        self.is_enemy = is_enemy

    @classmethod
    def Bishop(cls, pos, row_num, col_num, board, opponent):

        temp_row = pos[0]
        temp_col = pos[1]
        blocks = []
        while temp_row - 1 >= 0 and temp_col - 1 >= 0:
            if board[temp_row - 1][temp_col - 1].which_piece() is None:
                blocks.append([temp_row - 1, temp_col - 1])
                temp_row -= 1
                temp_col -= 1
            else:
                if board[temp_row-1][temp_col-1].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row-1][temp_col-1].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row-1, temp_col - 1])
                    break
        temp_row = pos[0]
        temp_col = pos[1]
        while temp_row - 1 >= 0 and temp_col + 1 < col_num:
            if board[temp_row - 1][temp_col + 1].which_piece() is None:
                blocks.append([temp_row - 1, temp_col + 1])
                temp_row -= 1
                temp_col += 1
            else:
                if board[temp_row-1][temp_col+1].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row-1][temp_col+1].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row-1, temp_col + 1])
                    break
        temp_row = pos[0]
        temp_col = pos[1]
        while temp_row + 1 < row_num and temp_col - 1 >= 0:
            if board[temp_row + 1][temp_col - 1].which_piece() is None:
                blocks.append([temp_row + 1, temp_col - 1])
                temp_row += 1
                temp_col -= 1
            else:
                if board[temp_row+1][temp_col-1].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row+1][temp_col-1].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row+1, temp_col - 1])
                    break
        temp_row = pos[0]
        temp_col = pos[1]
        while temp_row + 1 < row_num and temp_col + 1 < col_num:
            if board[temp_row + 1][temp_col + 1].which_piece() is None:
                blocks.append([temp_row + 1, temp_col + 1])
                temp_row += 1
                temp_col += 1
            else:
                if board[temp_row+1][temp_col+1].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row+1][temp_col+1].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row+1, temp_col + 1])
                    break

        return blocks

    @classmethod
    def Pawn(cls, pos, row_num, col_num, board, opponent):
        blocks = []
        if opponent:

            if pos[0] - 1 >= 0 and pos[1] - 1 >= 0 and not board[pos[0] - 1][pos[1] - 1].is_enemy():
                blocks.append([pos[0] - 1, pos[1] - 1])
            if pos[0] - 1 >= 0 and pos[1] + 1 < col_num and not board[pos[0] - 1][pos[1] + 1].is_enemy():
                blocks.append([pos[0] - 1, pos[1] + 1])
            if pos[0] - 1 >= 0 and board[pos[0] - 1][pos[1]].which_piece() is None:
                blocks.append([pos[0] - 1, pos[1]])
        else:
            if pos[0] + 1 < row_num and pos[1] - 1 >= 0 and board[pos[0] + 1][pos[1] - 1].is_enemy():
                blocks.append([pos[0] + 1, pos[1] - 1])
            if pos[0] + 1 < row_num and pos[1] + 1 < col_num and board[pos[0] + 1][pos[1] + 1].is_enemy():
                blocks.append([pos[0] + 1, pos[1] + 1])
            if pos[0] + 1 < row_num and board[pos[0] + 1][pos[1]].which_piece() is None:
                blocks.append([pos[0] + 1, pos[1]])

        return blocks

    @classmethod
    def Rook(cls, pos, row_num, col_num, board, opponent):

        temp_row = pos[0]
        temp_col = pos[1]
        blocks = []
        while temp_row - 1 >= 0:

            if board[temp_row - 1][temp_col].which_piece() is None:
                blocks.append([temp_row - 1, temp_col])
                temp_row -= 1
            else:
                if board[temp_row - 1][temp_col].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row - 1][temp_col].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row - 1, temp_col])
                    break

        temp_row = pos[0]
        temp_col = pos[1]
        while temp_col + 1 < col_num:

            if board[temp_row][temp_col + 1].which_piece() is None:
                blocks.append([temp_row, temp_col + 1])
                temp_col += 1
            else:
                if board[temp_row][temp_col+1].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row][temp_col+1].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row, temp_col + 1])
                    break
        temp_row = pos[0]
        temp_col = pos[1]
        while temp_row + 1 < row_num:
            if board[temp_row + 1][temp_col].which_piece() is None:
                blocks.append([temp_row + 1, temp_col])
                temp_row += 1
            else:
                if board[temp_row + 1][temp_col].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row+1][temp_col].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row+1, temp_col])
                    break
        temp_row = pos[0]
        temp_col = pos[1]
        while temp_col - 1 >= 0:
            if board[temp_row][temp_col - 1].which_piece() is None:
                blocks.append([temp_row, temp_col - 1])
                temp_col -= 1
            else:
                if board[temp_row][temp_col-1].which_piece().is_enemy and opponent:
                    break
                elif not board[temp_row][temp_col-1].which_piece().is_enemy and not opponent:
                    break
                else:
                    blocks.append([temp_row, temp_col - 1])
                    break

        return blocks

    @classmethod
    def Knight(cls, pos, row_num, col_num, board, opponent):
        blocks = []

        if pos[0] + 2 < row_num and pos[1] + 1 < col_num and board[pos[0] + 2][pos[1] + 1].can_move(opponent):
            blocks.append([pos[0] + 2, pos[1] + 1])
        if pos[0] + 1 < row_num and pos[1] + 2 < col_num and board[pos[0] + 1][pos[1] + 2].can_move(opponent):
            blocks.append([pos[0] + 1, pos[1] + 2])
        if pos[0] - 1 >= 0 and pos[1] - 2 >= 0 and board[pos[0] - 1][pos[1] - 2].can_move(opponent):
            blocks.append([pos[0] - 1, pos[1] - 2])
        if pos[0] - 2 >= 0 and pos[1] - 1 >= 0 and board[pos[0] - 2][pos[1] - 1].can_move(opponent):
            blocks.append([pos[0] - 2, pos[1] - 1])
        if pos[0] + 1 < row_num and pos[1] - 2 >= 0 and board[pos[0] + 1][pos[1] - 2].can_move(opponent):
            blocks.append([pos[0] + 1, pos[1] - 2])
        if pos[0] + 2 < row_num and pos[1] - 1 >= 0 and board[pos[0] + 2][pos[1] - 1].can_move(opponent):
            blocks.append([pos[0] + 2, pos[1] - 1])
        if pos[0] - 1 >= 0 and pos[1] + 2 < col_num and board[pos[0] - 1][pos[1] + 2].can_move(opponent):
            blocks.append([pos[0] - 1, pos[1] + 2])
        if pos[0] - 2 >= 0 and pos[1] + 1 < col_num and board[pos[0] - 2][pos[1] + 1].can_move(opponent):
            blocks.append([pos[0] - 2, pos[1] + 1])

        return blocks

    @classmethod
    def Queen(cls, pos, row_num, col_num, board, opponent):
        return Piece.Rook(pos, row_num, col_num, board, opponent) + Piece.Bishop(pos, row_num, col_num, board, opponent)

    @classmethod
    def King(cls, pos, row_num, col_num, board, opponent):
        blocks = []
        if pos[0] - 1 >= 0 and pos[1] - 1 >= 0 and board[pos[0] - 1][pos[1] - 1].can_move(opponent):
            blocks.append([pos[0] - 1, pos[1] - 1])
        if pos[0] - 1 >= 0 and pos[1] + 1 < col_num and board[pos[0] - 1][pos[1] + 1].can_move(opponent):
            blocks.append([pos[0] - 1, pos[1] + 1])
        if pos[0] + 1 < row_num and pos[1] + 1 < col_num and board[pos[0] + 1][pos[1] + 1].can_move(opponent):
            blocks.append([pos[0] + 1, pos[1] + 1])
        if pos[0] + 1 < row_num and pos[1] - 1 >= 0 and board[pos[0] + 1][pos[1] - 1].can_move(opponent):
            blocks.append([pos[0] + 1, pos[1] - 1])
        if pos[0] - 1 >= 0 and board[pos[0] - 1][pos[1]].can_move(opponent):
            blocks.append([pos[0] - 1, pos[1]])
        if pos[1] - 1 >= 0 and board[pos[0]][pos[1] - 1].can_move(opponent):
            blocks.append([pos[0], pos[1] - 1])
        if pos[0] + 1 < row_num and board[pos[0] + 1][pos[1]].can_move(opponent):
            blocks.append([pos[0] + 1, pos[1]])
        if pos[1] + 1 < col_num and board[pos[0]][pos[1] + 1].can_move(opponent):
            blocks.append([pos[0], pos[1] + 1])
        return blocks

    @classmethod
    def influence(cls, type, pos, row_num, col_num, board, opponent):
        if type == "Knight":
            blocks = Piece.Knight(pos, row_num, col_num, board, opponent)
        elif type == "Queen":
            blocks = Piece.Queen(pos, row_num, col_num, board, opponent)
        elif type == "King":
            blocks = Piece.King(pos, row_num, col_num, board, opponent)
        elif type == "Rook":
            blocks = Piece.Rook(pos, row_num, col_num, board, opponent)
        elif type == "Pawn":
            blocks = Piece.Pawn(pos, row_num, col_num, board, opponent)
        else:
            blocks = Piece.Bishop(pos, row_num, col_num, board, opponent)
        dict = {}
        for x in blocks:
            dict[transfer_to_char_array(x)] = x
        return dict
        # {'a0': [0,0]}


# initialize chess board
class Board:
    def __init__(self, row_num, col_num, enemy_piece_pos, piece_pos):
        self.row_num = row_num
        self.col_num = col_num

        self.enemy_piece_pos = enemy_piece_pos
        self.my_king_pos = []
        self.enemy_king_pos = []

        self.piece_pos = piece_pos
        self.sum_affected = 0

        self.board = [[0] * col_num for i in range(row_num)]
        # test board initialized correctly
        for i in range(0, row_num):
            for j in range(0, col_num):
                self.board[i][j] = Square(False, [i, j])

        for k in piece_pos:
            self.board[k[1]][ord(k[0]) - ord('a')].set_piece(piece_pos[k], False)

        for x in enemy_piece_pos:
            self.board[x[1]][ord(x[0]) - ord('a')].set_piece(enemy_piece_pos[x], True)


        for i in range(0, row_num):
            for j in range(0, col_num):
                potential_piece = self.board[i][j].which_piece()
                if potential_piece is not None and potential_piece.is_enemy is False:
                    if potential_piece.type == "King":
                        self.my_king_pos = [i, j]
                    all_can_moves = Piece.influence(potential_piece.type, [i, j], self.row_num, self.col_num,
                                                    self.board, False)

                    self.board[i][j].set_all_can_moves(all_can_moves)

                if potential_piece is not None and potential_piece.is_enemy is True:
                    if potential_piece.type == "King":
                        self.enemy_king_pos = [i, j]
                    all_can_moves = Piece.influence(potential_piece.type, [i, j], self.row_num, self.col_num,
                                                    self.board, True)

                    self.board[i][j].set_all_can_moves(all_can_moves)


# record the condition at each position on board.
class Square:
    def __init__(self, is_obs, pos):
        self.obs = is_obs
        self.num_piece_affected = 0
        self.all_can_moves = {}
        self.piece = None
        self.pos = pos
        self.possible_moves = []

    def set_obs(self):
        self.obs = True

    def set_piece(self, type, is_enemy):
        if type is None:
            self.piece = None
        else:
            self.piece = Piece(type, is_enemy)

    def set_num_piece_affected(self, num):
        self.num_piece_affected = num

    def set_all_can_moves(self, all_can_moves):
        self.all_can_moves = all_can_moves

    def is_obs(self):
        return self.obs

    def which_piece(self):
        return self.piece

    def get_num_piece_affected(self):
        return self.num_piece_affected

    def is_enemy(self):
        if self.piece is None:
            return False
        return self.piece.is_enemy

    def can_move(self, opponent):
        if self.piece is None:
            return True
        else:
            if self.piece.is_enemy and opponent:
                return False
            elif self.piece.is_enemy and not opponent:
                return True
            elif not self.piece.is_enemy and not opponent:
                return False
            else:
                return True


def transfer_to_number_array(string):
    char = string[0]
    return [int(string[1:]), ord(char) - ord('a')]


def tuple_to_num_arr(tuple):
    return [tuple[1], ord(tuple[0]) - ord('a')]

# check whether current king position is in check or not.
def is_incheck(my_king_pos, curr_opponent_piece_pos,board):
    for x in curr_opponent_piece_pos:
        square = tuple_to_num_arr(x)
        king = transfer_to_char_array(my_king_pos)
        enemy_piece = board.board[square[0]][square[1]].which_piece()
        if king in Piece.influence(enemy_piece.type, square, board.row_num, board.col_num, board.board, enemy_piece.is_enemy):
            return True


# check the utility gained from a movement, and different piece type have different utility.
# place move to is in 'a0' format, check place_move_to that can affect utility.
def check_utility(state, board, place_move_to):
    real_place = transfer_to_number_array(place_move_to)

    possible_piece = board.board[real_place[0]][real_place[1]].which_piece()
    if possible_piece is None:
        sum_utility = 0
    else:
        #print(possible_piece.is_enemy)
        weight = -1
        if state:
            weight = 1

        if possible_piece.type == "King":
            sum_utility = 1000 * weight
        elif possible_piece.type == "Knight":
            sum_utility = 70 * weight
        elif possible_piece.type == "Rook":
            sum_utility = 70 * weight
        elif possible_piece.type == "Bishop":
            sum_utility = 70 * weight
        elif possible_piece.type == "Queen":
            sum_utility = 90 * weight
        elif possible_piece.type == "Pawn":
            sum_utility = 10 * weight
        else:
            sum_utility = 0

    return sum_utility


def num_arr_to_tuple(arr):
    return tuple([chr(arr[1] + ord('a')),arr[0]])


# partially roll back the states for each square, simplifed version of reset.
def half_reset(board, place_move_to, curr_place, state):
    curr_square = board.board[curr_place[0]][curr_place[1]]
    curr_piece_type = curr_square.which_piece().type

    if state:

        if board.board[place_move_to[0]][place_move_to[1]].which_piece() is not None:
            del board.enemy_piece_pos[num_arr_to_tuple(place_move_to)]

        del board.piece_pos[num_arr_to_tuple(curr_place)]

        board.piece_pos[num_arr_to_tuple(place_move_to)] = curr_piece_type
    else:

        if board.board[place_move_to[0]][place_move_to[1]].which_piece() is not None:
            # print(board.piece_pos,board.enemy_piece_pos,place_move_to,curr_place)
            del board.piece_pos[num_arr_to_tuple(place_move_to)]

        del board.enemy_piece_pos[num_arr_to_tuple(curr_place)]
        board.enemy_piece_pos[num_arr_to_tuple(place_move_to)] = curr_piece_type

    curr_square.set_piece(None, None)
    curr_square.set_all_can_moves({})

    square_move_to = board.board[place_move_to[0]][place_move_to[1]]
    square_move_to.set_piece(curr_piece_type, not state)
    square_move_to.set_all_can_moves({})


# fully roll back the state on board and reset fully all can moves.
def reset_board(board, place_move_to, curr_place, state):
    curr_square = board.board[curr_place[0]][curr_place[1]]
    curr_piece_type = curr_square.which_piece().type

    if state:
        if board.board[place_move_to[0]][place_move_to[1]].which_piece() is not None:

            del board.enemy_piece_pos[num_arr_to_tuple(place_move_to)]

        del board.piece_pos[num_arr_to_tuple(curr_place)]

        board.piece_pos[num_arr_to_tuple(place_move_to)] = curr_piece_type
    else:

        if board.board[place_move_to[0]][place_move_to[1]].which_piece() is not None:
            # print(board.piece_pos,board.enemy_piece_pos,place_move_to,curr_place)
            del board.piece_pos[num_arr_to_tuple(place_move_to)]

        del board.enemy_piece_pos[num_arr_to_tuple(curr_place)]
        board.enemy_piece_pos[num_arr_to_tuple(place_move_to)] = curr_piece_type

    curr_square.set_piece(None, None)
    curr_square.set_all_can_moves({})

    square_move_to = board.board[place_move_to[0]][place_move_to[1]]
    square_move_to.set_piece(curr_piece_type, not state)
    square_move_to.set_all_can_moves({})
    col_num = board.col_num
    row_num = board.row_num
    for i in range(0, row_num):
        for j in range(0, col_num):
            potential_piece = board.board[i][j].which_piece()
            if potential_piece is not None and potential_piece.is_enemy is False:
                if potential_piece.type == "King":
                    board.my_king_pos = [i, j]
                    #print("myking", [i, j])
                all_can_moves = Piece.influence(potential_piece.type, [i, j], row_num, col_num,
                                                board.board, False)

                board.board[i][j].set_all_can_moves(all_can_moves)

            if potential_piece is not None and potential_piece.is_enemy is True:
                if potential_piece.type == "King":
                    board.enemy_king_pos = [i, j]
                    #("myking", [i, j])
                all_can_moves = Piece.influence(potential_piece.type, [i, j], row_num, col_num,
                                                board.board, True)

                board.board[i][j].set_all_can_moves(all_can_moves)


# Implement minimax with alpha-beta pruning algorithm here.
def ab(state, board, alpha, beta, depth):
    max_curr_utility = alpha
    min_curr_utility = beta


    should_prune = False
    curr_piece = None
    curr_pos = None
    original = None
    if state:
        for x in board.piece_pos:
            row = x[1]
            col = ord(x[0]) - ord('a')
            square = board.board[row][col]
            # check which places are able to achieve in one turn
            all_can_moves = Piece.influence(square.which_piece().type, [row, col], board.row_num,board.col_num,board.board, not state)
            if transfer_to_char_array(board.enemy_king_pos) in all_can_moves:

                return 1000, square.which_piece(), num_arr_to_tuple(board.enemy_king_pos), x
            for u in all_can_moves:

                if depth == 0:
                    curr_board = copy.deepcopy(board)
                    half_reset(curr_board, transfer_to_number_array(u), [row, col], state)
                    if square.which_piece().type == "King":
                        curr_board.my_king_pos = transfer_to_number_array(u)
                    if is_incheck(curr_board.my_king_pos, curr_board.enemy_piece_pos, curr_board):
                        new_utility = -1000

                    else:
                        new_utility = check_utility(state, board, u)
                    #print(board.enemy_piece_pos, board.piece_pos,x, u, new_utility)

                else:
                    curr_board = copy.deepcopy(board)
                    if square.which_piece().type == "King":
                        curr_board.my_king_pos = transfer_to_number_array(u)
                    # reset_board(curr_board, transfer_to_number_array(u), [row, col], state)
                    half_reset(curr_board, transfer_to_number_array(u), [row, col], state)
                    new_utility, piece, pos, curr_original = ab(not state, curr_board, max_curr_utility, beta,
                                                                depth + 1)
                if new_utility > beta:
                    should_prune = True

                    break
                if max_curr_utility < new_utility:
                    curr_pos = char_to_tuple(u)
                    curr_piece = square.which_piece()
                    max_curr_utility = new_utility
                    original = x

            if should_prune:
                break
        return max_curr_utility, curr_piece, curr_pos, original

    else:
        for x in board.enemy_piece_pos:
            row = x[1]
            col = ord(x[0]) - ord('a')
            square = board.board[row][col]
            all_can_moves = Piece.influence(square.which_piece().type, [row, col], board.row_num, board.col_num,
                                            board.board, not state)
            if transfer_to_char_array(board.my_king_pos) in all_can_moves:
                return -1000, square.which_piece(), num_arr_to_tuple(board.my_king_pos), x
            for u in all_can_moves:

                if depth == 0:
                    curr_board = copy.deepcopy(board)
                    half_reset(curr_board, transfer_to_number_array(u), [row, col], state)
                    if square.which_piece().type == "King":
                        curr_board.enemy_king_pos = transfer_to_number_array(u)
                    if is_incheck(curr_board.enemy_king_pos, curr_board.piece_pos, curr_board):
                        new_utility = 1000
                    else:
                    #print(21515)
                        new_utility = check_utility(state, board, u)
                else:
                    curr_board = copy.deepcopy(board)
                    # print(u, square.which_piece().type)
                    if square.which_piece().type == "King":
                        curr_board.enemy_king_pos = transfer_to_number_array(u)

                    half_reset(curr_board, transfer_to_number_array(u), [row, col], state)
                    new_utility, piece, pos, curr_original = ab(not state, curr_board, alpha, min_curr_utility,
                                                                depth + 1)
                if new_utility < alpha:
                    should_prune = True

                    break
                if min_curr_utility > new_utility:
                    curr_pos = char_to_tuple(u)
                    curr_piece = square.which_piece()
                    min_curr_utility = new_utility
                    original = x
            if should_prune:
                break
        return min_curr_utility, curr_piece, curr_pos, original
        # alternative version which considers more steps about a single movement, requiring more computational resources
        # else:
        #
        #     for x in board.enemy_piece_pos:
        #         row = x[1]
        #         col = ord(x[0]) - ord('a')
        #         square = board.board[row][col]
        #         # if len(square.all_can_moves) == 0:
        #         if transfer_to_char_array(board.my_king_pos) in square.all_can_moves:
        #             return -1000, square.which_piece(), num_arr_to_tuple(board.my_king_pos), x
        #         for u in square.all_can_moves:
        #             #print(square.which_piece().type, square.all_can_moves,u)
        #
        #             curr_board = copy.deepcopy(board)
        #             reset_board(curr_board, transfer_to_number_array(u), [row, col], state)
        #             #print(curr_board.enemy_piece_pos, curr_board.piece_pos, depth, state,transfer_to_char_array(board.enemy_king_pos), board.enemy_king_pos)
        #             new_utility, piece, pos, curr_original = ab(not state, curr_board, alpha, min_curr_utility,
        #                                                         depth + 1)
        #
        #             if new_utility < alpha:
        #                 should_prune = True
        #                 break
        #             if min_curr_utility > new_utility:
        #                 curr_pos = char_to_tuple(u)
        #                 curr_piece = square.which_piece()
        #                 min_curr_utility = new_utility
        #                 original = x
        #         if should_prune:
        #             break

       # return min_curr_utility, curr_piece, curr_pos, original  # which piece to move, where to move


def transfer_to_char_array(arr):
    char = chr(arr[1] + ord('a'))
    return char + str(arr[0])


def char_to_tuple(char_arr):
    return tuple([char_arr[0], int(char_arr[1:])])


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # row_num, col_num, num_enemy_pieces, enemy_piece_pos, num_pieces, piece_pos = get_file_var(input()) #Takes in config.txt Optional
    piece_pos = {}
    enemy_piece_pos = {}

    for x in gameboard:

        if gameboard[x][1] == "White":
            piece_pos[x] = gameboard[x][0]

        if gameboard[x][1] == "Black":
            enemy_piece_pos[x] = gameboard[x][0]

    board = Board(5, 5, enemy_piece_pos, piece_pos)
    utility, piece, place_move_to, original = ab(True, board, -100000, 100000, 0)
    # print(utility, piece, place_move_to, original)

    move = (original, place_move_to)
    return move  # Format to be returned (('a', 0), ('b', 3))
