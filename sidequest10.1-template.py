#
# CS1010S --- Programming Methodology
#
# Sidequest 10.1 Template
#
# Note that written answers are commented out to allow us to run your #
# code easily while grading your problem set.

from random import *
from puzzle import GameGrid

###########
# Helpers #
###########

def accumulate(fn, initial, seq):
    if not seq:
        return initial
    else:
        return fn(seq[0],
                  accumulate(fn, initial, seq[1:]))

def flatten(mat):
    return [num for row in mat for num in row]



###########
# Task 1  #
###########

def new_game_matrix(n):
    matrix = []
    while len(matrix) < n:
        row = []
        while len(row) < n:
            row += [0,]
        matrix += [row,]
    return matrix

def has_zero(mat):
    for row in mat:
        if 0 in row:
            return True
    return False

def add_two(mat):
    n = len(mat)
    ran1 = randint(0, n - 1)
    while 0 not in mat[ran1]: ran1 = randint(0, n - 1)
    ran2 = randint(0, n - 1)
    while mat[ran1][ran2] != 0: ran2 = randint(0, n - 1)
    mat[ran1][ran2] = 2
    return mat


#print(add_two( [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] ))


###########
# Task 2  #
###########

def game_status(mat):
    for row in mat:
        if 2048 in row:
            return 'win'
    if has_zero(mat):
        return "not over"
    else: #check if there are adjacent tiles with same value, at this point mat must be already full
        for i in range(len(mat)): #row indices
            for j in range((len(mat[i])-1)): #column indices
                if mat[i][j] == mat[i][j+1]:
                    return "not over"
        for i in range(len(mat)-1):  # row indices
            for j in range(len(mat[i])):  # column indices
                if mat[i][j] == mat[i+1][j]:
                    return "not over"
        return 'lose'




###########
# Task 3a #
###########

def transpose(mat):
    newmat = []
    for i in range(len(mat[0])):
        column = []
        for j in range(len(mat)):
            column += [mat[j][i],]
        newmat += [column,]
    return newmat




###########
# Task 3b #
###########

def reverse(mat):
    ans = []
    for row in mat:
        newrow = []
        for i in row:
            newrow = [i,] + newrow
        ans += [newrow,]
    return ans



############
# Task 3ci #
############

def merge_left(mat):
    newmat = []
    score = 0
    for row in mat:
        newrow = []
        i = 0
        lm = 0 #leftmost
        for i in row:
            if i!=0 and lm==0: lm=i
            elif lm!=0:
                if i==0:
                    continue #continue to the right of leftmost tile
                elif i==lm:
                    newrow += [2*i,]
                    score += 2*i
                    lm = 0
                else:
                    newrow += [lm,]
                    lm = i
        newrow += [lm,]
        while len(newrow) < 4: newrow += [0,]
        newmat += [newrow,]
    return (newmat,) + (newmat!=mat,) + (score,)


#############
# Task 3cii #
#############

def merge_right(mat):
    newmat = []
    score = 0
    for row in mat:
        newrow = []
        i = 0
        rm = 0
        for i in row[::-1]:
            if i!=0 and rm==0: rm=i
            elif rm!=0:
                if i==0:
                    continue
                elif i==rm:
                    newrow = [2*i,] + newrow
                    score += 2*i
                    rm = 0
                else:
                    newrow = [rm,] + newrow
                    rm = i
        newrow = [rm,] + newrow
        while len(newrow) < 4: newrow = [0,] + newrow
        newmat += [newrow,]
    return (newmat,) + (newmat!=mat,) + (score,)

#0, 0, 4], [4, 0, 8, 4], [2, 0, 0, 0]]
#print(merge_right(mat2))

def merge_up(mat):
    newmap = transpose(mat)
    newmap = merge_left(newmap)
    return (transpose(newmap[0]), newmap[1], newmap[2])


def merge_down(mat):
    newmap = transpose(mat)
    newmap = merge_right(newmap)
    return (transpose(newmap[0]), newmap[1], newmap[2])

#mat3 = transpose(mat2)
#print(mat3)
#print(merge_down(mat3))

###########
# Task 3d #
###########

def text_play():
    def print_game(mat, score):
        for row in mat:
            print(''.join(map(lambda x: str(x).rjust(5), row)))
        print('score: ' + str(score))
    GRID_SIZE = 4
    score = 0
    mat = add_two(add_two(new_game_matrix(GRID_SIZE)))
    print_game(mat, score)
    while True:
        move = input('Enter W, A, S, D or Q: ')
        move = move.lower()
        if move not in ('w', 'a', 's', 'd', 'q'):
            print('Invalid input!')
            continue
        if move == 'q':
            print('Quitting game.')
            return
        move_funct = {'w': merge_up,
                      'a': merge_left,
                      's': merge_down,
                      'd': merge_right}[move]
        mat, valid, score_increment = move_funct(mat)
        if not valid:
            print('Move invalid!')
            continue
        score += score_increment
        mat = add_two(mat)
        print_game(mat, score)
        status = game_status(mat)
        if status == "win":
            print("Congratulations! You've won!")
            return
        elif status == "lose":
            print("Game over. Try again!")
            return

# UNCOMMENT THE FOLLOWING LINE TO TEST YOUR GAME
text_play()

# How would you test that the winning condition works?
# Your answer:
#


##########
# Task 4 #
##########

def make_state(matrix, total_score):
    return (matrix, total_score)

def get_matrix(state):
    return state[0]

def get_score(state):
    return state[1]

def make_new_game(n):
    #create an nxn zero matrix
    mat = new_game_matrix(n)
    mat = add_two(mat)
    mat = add_two(mat)
    return make_state(mat, 0)


def left(state):
    mat = get_matrix(state)
    score = get_score(state)
    n = len(mat)
    merged = merge_left(mat)  # (mat, bool, score) this step is to merge
    mat = get_matrix(merged)
    bool = merged[1]

    if bool:
        # add a tile 2 at random
        mat = add_two(mat)
        # create new state and return answer
        newscore = score + merged[2]
        newstate = make_state(mat, newscore)
        return (newstate,) + (bool,)
    else:
        return (state,) + (bool,)


def right(state):
    mat = get_matrix(state)
    score = get_score(state)
    n = len(mat)
    merged = merge_right(mat)  # (mat, bool, score) this step is to merge
    mat = get_matrix(merged)
    bool = merged[1]

    if bool:
        # add a tile 2 at random
        mat = add_two(mat)
        # create new state and return answer
        newscore = score + merged[2]
        newstate = make_state(mat, newscore)
        return (newstate,) + (bool,)
    else:
        return (state,) + (bool,)

def up(state):
    mat = get_matrix(state)
    score = get_score(state)
    n = len(mat)
    merged = merge_up(mat)  # (mat, bool, score) this step is to merge
    mat = get_matrix(merged)
    bool = merged[1]

    if bool:
        # add a tile 2 at random
        mat = add_two(mat)
        # create new state and return answer
        newscore = score + merged[2]
        newstate = make_state(mat, newscore)
        return (newstate,) + (bool,)
    else:
        return (state,) + (bool,)

def down(state):
    mat = get_matrix(state)
    score = get_score(state)
    n = len(mat)
    merged = merge_down(mat)  # (mat, bool, score) this step is to merge
    mat = get_matrix(merged)
    bool = merged[1]

    if bool:
        # add a tile 2 at random
        mat = add_two(mat)
        # create new state and return answer
        newscore = score + merged[2]
        newstate = make_state(mat, newscore)
        return (newstate,) + (bool,)
    else:
        return (state,) + (bool,)


# Do not edit this #
game_logic = {
    'make_new_game': make_new_game,
    'game_status': game_status,
    'get_score': get_score,
    'get_matrix': get_matrix,
    'up': up,
    'down': down,
    'left': left,
    'right': right,
    'undo': lambda state: (state, False)
}

# UNCOMMENT THE FOLLOWING LINE TO START THE GAME (WITHOUT UNDO)
gamegrid = GameGrid(game_logic)


#################
# Optional Task #
#################

###########
# Task 5i #
###########

def make_new_record(mat, increment):
    "Your answer here"

def get_record_matrix(record):
    "Your answer here"

def get_record_increment(record):
    "Your answer here"

############
# Task 5ii #
############

def make_new_records():
    "Your answer here"

def push_record(new_record, stack_of_records):
    "Your answer here"

def is_empty(stack_of_records):
    "Your answer here"

def pop_record(stack_of_records):
    "Your answer here"

#############
# Task 5iii #
#############

# COPY AND UPDATE YOUR FUNCTIONS HERE
def make_state(matrix, total_score, records):
    "Your answer here"

def get_matrix(state):
    "Your answer here"

def get_score(state):
    "Your answer here"

def make_new_game(n):
    "Your answer here"

def left(state):
    "Your answer here"

def right(state):
    "Your answer here"

def up(state):
    "Your answer here"

def down(state):
    "Your answer here"

# NEW FUNCTIONS TO DEFINE
def get_records(state):
    "Your answer here"

def undo(state):
    "Your answer here"


# UNCOMMENT THE FOLLOWING LINES TO START THE GAME (WITH UNDO)
#game_logic = {
#    'make_new_game': make_new_game,
#    'game_status': game_status,
#    'get_score': get_score,
#    'get_matrix': get_matrix,
#    'up': up,
#    'down': down,
#    'left': left,
#    'right': right,
#    'undo': undo
#}
#gamegrid = GameGrid(game_logic)
