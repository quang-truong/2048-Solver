#
# CS1010S --- Programming Methodology
#
# Contest 10.2 Template
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from random import *
from puzzle_AI import *

history_matrix = []
history_move = []
def accumulate(fn, initial, seq):
    if not seq:
        return initial
    else:
        return fn(seq[0],
                  accumulate(fn, initial, seq[1:]))
def transpose(mat):
    return list(map(list,zip(*mat)))
def reverse(mat):
    return list(map(lambda row: list(reversed(row)),mat))
def merge_left(matrix):
    def merge_row(row):
        merged_row, prev_tile, score_increment = [], 0, 0
        # pack element by element left-wards
        for tile in row:
            if tile == 0: continue
            if prev_tile == 0:
                prev_tile = tile
            elif prev_tile != tile:
                merged_row.append(prev_tile)
                prev_tile = tile
            else:
                merged_row.append(prev_tile*2)
                score_increment += prev_tile*2
                prev_tile = 0
        merged_row.append(prev_tile) # valid regardless whether there are merges or not
        # top up zeros
        while len(merged_row) != len(row):
            merged_row.append(0)
        return (merged_row, merged_row != row, score_increment)

    return accumulate(lambda first, rest: ([first[0]] + rest[0],
                                            first[1] or rest[1],
                                            first[2] + rest[2]),
                      ([], False, 0),
                      list(map(merge_row, matrix)))

def merge_right(mat):
    mat, valid, score = merge_left(reverse(mat))
    return (reverse(mat), valid, score)

def merge_up(mat):
    mat, valid, score = merge_left(transpose(mat))
    return (transpose(mat), valid, score)

def merge_down(mat):
    mat, valid, score = merge_left(reverse(transpose(mat)))
    return (transpose(reverse(mat)), valid, score)
def calc_score(mat):
    score = 0
    for row in range(4):
        for column in range(4):
            score += mat[row][column]
    return score
def undo_move(mat):
    history_move.pop()
    history_matrix.pop()
    mat = history_matrix[-1]
    return mat
def record_matrix_and_move(mat, decision):
    history_matrix.append(mat)
    history_move.append(decision)
    return
def add_two(mat):
    if not has_zero(mat):
        return mat
    a = randint(0, len(mat)-1)
    b = randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = randint(0, len(mat)-1)
        b = randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat
def AI_command(mat, n):
    result_mat = mat[:]
    bonus = 0
    if n == 0:
        result_mat, valid,bonus = merge_up(result_mat)
    elif n == 1:
        result_mat, valid,bonus = merge_left(result_mat)
    elif n == 2:
        result_mat, valid,bonus = merge_right(result_mat)
    elif n == 3:
        result_mat, valid,bonus = merge_down(result_mat)
    add_two(result_mat)
    #record_matrix_and_move(result_mat, n)
    return result_mat, bonus
def monotone(mat):
    bonus = 0
    row = 0
    column = 0
    const1, const2, const3, const4 = biggest_tiles(mat)
    if row == 0 and column == 0 and mat[row][column] != 0:
        if mat[row][column] >= mat[row][column+1] >= mat[row][column +2] >= mat[row][column+3]\
                and mat[row][column] == const1:
            bonus += const1
            if mat[row][column+1] == const1 or mat[row][column+1] == const2:
                bonus += const1*2
                if mat[row][column+2] == const2 or mat[row][column+2] == const3:
                    bonus += const1*3
                    if mat[row][column+3] == const3 or mat[row][column+3] == const4:
                        bonus += const1*4
    return bonus
def biggest_tiles(mat):
    biggest = 0
    sec_big = 0
    third_big = 0
    fourth_big = 0
    for i in range(4):
        for j in range(4):
            big = mat[i][j]
            if big > biggest:
                biggest = big
    for i in range(4):
        for j in range(4):
            big = mat[i][j]
            if sec_big < big < biggest:
                sec_big = big
    for i in range(4):
        for j in range(4):
            big = mat[i][j]
            if third_big < big < sec_big:
                third_big = big
    for i in range(4):
        for j in range(4):
            big = mat[i][j]
            if fourth_big < big < third_big:
                fourth_big = big
    return biggest, sec_big, third_big, fourth_big
def AI_text(mat, turn):
    best_score = -1
    best_move = -1
    score = 0
    for move in range(4):
        if validified(mat, move):
            mat, bonus = AI_command(mat, move)
            score += bonus
            score += monotone(mat)
            score += second_row(mat)
            score += third_row(mat)
            record_matrix_and_move(mat, move)
            if turn == 2:
                #score += bonus
                if history_matrix[-1][0][0] < history_matrix[-2][0][0]:
                    score -= biggest_tiles(mat)[0]*2
            else:
                if game_status(mat) == "not over":
                    score += AI_command(mat, AI_text(mat, turn+1))[1]
            mat = undo_move(mat)
            if score > best_score:
                best_score = score
                best_move = move
            score = 0
    return best_move
def second_row(mat):
    bonus = 0
    const3 = biggest_tiles(mat)[2]
    if mat[1][2] >= mat[1][1] and mat[1][2] <= const3:
        bonus += const3
        if mat[1][1] >= mat[1][0]:
            bonus += const3
    return bonus
def third_row(mat):
    bonus = 0
    const4 = biggest_tiles(mat)[3]
    if mat[2][0] >= mat[2][1] and mat[2][0] <= mat[1][0]:
        bonus += const4
    return bonus

def validified(mat,n):
    validity = None
    if n == 0:
        validity = merge_up(mat)[1]
    elif n == 1:
        validity = merge_left(mat)[1]
    elif n == 2:
        validity = merge_right(mat)[1]
    elif n == 3:
        validity = merge_down(mat)[1]
    return validity

def AI(mat):
    # replace the following line with your code
    dup_mat = mat[:]
    record_matrix_and_move(dup_mat, -1)
    decision = AI_text(dup_mat, 0)
    return ('w','a','d','s')[decision]



# UNCOMMENT THE FOLLOWING LINES AND RUN TO WATCH YOUR SOLVER AT WORK
game_logic['AI'] = AI
gamegrid = GameGrid(game_logic)

# UNCOMMENT THE FOLLOWING LINE AND RUN TO GRADE YOUR SOLVER
# Note: Your solver is expected to produce only valid moves.
get_average_AI_score(AI, True)
