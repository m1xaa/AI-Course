import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = sum(row.count(X) for row in board)
    num_o = sum(row.count(O) for row in board)
    return X if num_x == num_o else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid move")
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if all(cell == row[0] and cell != EMPTY for cell in row):
            return row[0]

    # Check columns
    for col in range(3):
        if all(board[row][col] == board[0][col] and board[row][col] != EMPTY for row in range(3)):
            return board[0][col]

    # Check diagonals
    if all(board[i][i] == board[0][0] and board[i][i] != EMPTY for i in range(3)):
        return board[0][0]

    if all(board[i][2 - i] == board[0][2] and board[i][2 - i] != EMPTY for i in range(3)):
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

def minimax(board, maximizing_player, alpha, beta):
    if terminal(board):
        return utility(board)

    if maximizing_player:
        max_eval = -math.inf
        for action in actions(board):
            new_board = result(board, action)
            eval = minimax(new_board, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                return beta
        return alpha
    else:
        min_eval = math.inf
        for action in actions(board):
            new_board = result(board, action)
            eval = minimax(new_board, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                return alpha
        return beta

def find_best_move(board, is_maximizer):
    min = math.inf
    max = -math.inf
    posmin = None
    posmax = None

    for action in actions(board):
        new_board = result(board, action)
        value = minimax(new_board, is_maximizer, -math.inf, math.inf)

        if value < min:
            posmin = action
            min = value
        
        if value > max:
            posmax = action
            max = value
            
    if is_maximizer:
        return posmax
    return posmin