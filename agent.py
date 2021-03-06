"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
board_utility = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    if color == 1:
        return get_score(board)[0] - get_score(board)[1]
    else:
        return get_score(board)[1] - get_score(board)[0]


# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if color == 1:
        possible_moves = get_possible_moves(board, 2)
        if limit == 0 or len(possible_moves) == 0:
            return (None, compute_utility(board, color))
        best_utility = len(board) ** 2
        best_move = None
        for move in possible_moves:
            board_ = play_move(board, 2, move[0], move[1])
            if caching != 0 and board_ not in board_utility:
                max_node = minimax_max_node(board_, color, limit - 1, caching)
                board_utility[board_] = max_node
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
            elif caching != 0 and board_ in board_utility:
                max_node = board_utility[board_]
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
            else:
                max_node = minimax_max_node(board_, color, limit - 1, caching)
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
        return (best_move, best_utility)
    else:
        possible_moves = get_possible_moves(board, 1)
        if limit == 0 or len(possible_moves) == 0:
            return (None, compute_utility(board, color))
        best_utility = len(board) ** 2
        best_move = None
        for move in possible_moves:
            board_ = play_move(board, 1, move[0], move[1])
            if caching != 0 and board_ not in board_utility:
                max_node = minimax_max_node(board_, color, limit - 1, caching)
                board_utility[board_] = max_node
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
            elif caching != 0 and board_ in board_utility:
                max_node = board_utility[board_]
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
            else:
                max_node = minimax_max_node(board_, color, limit - 1, caching)
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
        return (best_move, best_utility)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility

    possible_moves = get_possible_moves(board, color)
    if limit == 0 or len(possible_moves) == 0:
        return (None, compute_utility(board, color))
    best_utility = -len(board) ** 2
    best_move = None
    for move in possible_moves:
        board_ = play_move(board, color, move[0], move[1])
        if caching != 0 and board_ in board_utility:
            min_node = board_utility[board_]
            if min_node[1] > best_utility:
                best_utility = min_node[1]
                best_move = move
        elif caching != 0 and board_utility not in board_utility:
            min_node = minimax_min_node(board_, color, limit - 1, caching)
            board_utility[board_] = min_node
            if min_node[1] > best_utility:
                best_utility = min_node[1]
                best_move = move
        else:
            min_node = minimax_min_node(board_, color, limit - 1, caching)
            if min_node[1] > best_utility:
                best_utility = min_node[1]
                best_move = move
    return (best_move, best_utility)


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    return minimax_max_node(board, color, limit)[0]


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if color == 1:
        possible_moves = get_possible_moves(board, 2)
        if limit == 0 or len(possible_moves) == 0:
            return (None, compute_utility(board, color))
        best_utility = len(board) ** 2
        best_move = None
        if ordering != 0:
            possible_moves.sort(key=lambda move: compute_utility(play_move(board, 2, move[0], move[1]), color))
        for move in possible_moves:
            board_ = play_move(board, 2, move[0], move[1])
            if caching != 0 and board_ in board_utility:
                max_node = board_utility[board_]
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
                if beta > best_utility:
                    beta = best_utility
                if beta <= alpha:
                    return (best_move, best_utility)
            elif caching != 0 and board_ not in board_utility:
                max_node = alphabeta_max_node(board_, color, alpha, beta, limit - 1, caching, ordering)
                board_utility[board_] = max_node
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
                if beta > best_utility:
                    beta = best_utility
                if beta <= alpha:
                    return (best_move, best_utility)
            else:
                max_node = alphabeta_max_node(board_, color, alpha, beta, limit - 1, caching, ordering)
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
                if beta > best_utility:
                    beta = best_utility
                if beta <= alpha:
                    return (best_move, best_utility)

    else:
        possible_moves = get_possible_moves(board, 1)
        if limit == 0 or len(possible_moves) == 0:
            return (None, compute_utility(board, color))
        best_utility = len(board) ** 2
        best_move = None
        if ordering != 0:
            possible_moves.sort(key=lambda move: compute_utility(play_move(board, 1, move[0], move[1]), color))
        for move in possible_moves:
            board_ = play_move(board, 1, move[0], move[1])
            if caching != 0 and board_ in board_utility:
                max_node = board_utility[board_]
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
                if beta > best_utility:
                    beta = best_utility
                if beta <= alpha:
                    return (best_move, best_utility)
            elif caching != 0 and board_ not in board_utility:
                max_node = alphabeta_max_node(board_, color, alpha, beta, limit - 1, caching, ordering)
                board_utility[board_] = max_node
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
                if beta > best_utility:
                    beta = best_utility
                if beta <= alpha:
                    return (best_move, best_utility)
            else:
                max_node = alphabeta_max_node(board_, color, alpha, beta, limit - 1, caching, ordering)
                if max_node[1] < best_utility:
                    best_utility = max_node[1]
                    best_move = move
                if beta > best_utility:
                    beta = best_utility
                if beta <= alpha:
                    return (best_move, best_utility)
    return (best_move, best_utility)


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    possible_moves = get_possible_moves(board, color)
    if limit == 0 or len(possible_moves) == 0:
        return (None, compute_utility(board, color))
    best_utility = -len(board) ** 2
    best_move = None
    if ordering != 0:
        possible_moves.sort(key = lambda move: compute_utility(play_move(board, color, move[0], move[1]), color))
    for move in possible_moves:
        board_ = play_move(board, color, move[0], move[1])
        if caching != 0 and board_ in board_utility:
            min_node = board_utility[board_]
            if min_node[1] > best_utility:
                best_utility = min_node[1]
                best_move = move
            if alpha < best_utility:
                alpha = best_utility
            if beta <= alpha:
                return (best_move, best_utility)
        elif caching != 0 and board_ not in board_utility:
            min_node = alphabeta_min_node(board_, color, alpha, beta, limit - 1, caching, ordering)
            board_utility[board_] = min_node
            if min_node[1] > best_utility:
                best_utility = min_node[1]
                best_move = move
            if alpha < best_utility:
                alpha = best_utility
            if beta <= alpha:
                return (best_move, best_utility)
        else:
            min_node = alphabeta_min_node(board_, color, alpha, beta, limit - 1, caching, ordering)
            if min_node[1] > best_utility:
                best_utility = min_node[1]
                best_move = move
            if alpha < best_utility:
                alpha = best_utility
            if beta <= alpha:
                return (best_move, best_utility)
    return (best_move, best_utility)


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    alpha = -len(board) ** 2
    beta = len(board) ** 2
    return alphabeta_max_node(board, color, alpha, beta, limit, caching, ordering)[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()