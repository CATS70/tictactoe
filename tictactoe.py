"""
Tic Tac Toe Player
"""
import copy
import math
import datetime

X = "X"
O = "O"
EMPTY = None

myfile = open("trace.txt",mode="w")
def initial_state():
    """
    Returns starting state of the board.
    """
    #return [[EMPTY, X, O],
    #        [O, X, EMPTY],
    #        [X, EMPTY, O]]
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #If you play as X, AI starts the game with O
    #If you play as O, you start with O
    #So, 1st play is always O
    #print("player")
    countX=0
    countO=0

    if board == initial_state():
        return X

    for line in board:
        countX += line.count(X)
        countO += line.count(O)
    if countX>countO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY or (not 0<=action[0]<=2) or (not 0<=action[1]<=2) :
        raise "Invalid action"
    else:
        current_player = player(board)
        board[action[0]][action[1]] = current_player

        return board




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    if utility(board)==1:
        return X
    elif utility(board)==-1:
        return O
    else: return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if (board[0].count(EMPTY)==0 and board[1].count(EMPTY)==0 and board[2].count(EMPTY)==0) or utility(board)!=0:
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    #test if win in a row
    diags = [[], []]
    columns = [[], [], []]
    indexdiag = 0
    indexcolumn = 0

    for line in board:
        if line.count(X) == 3:
            return 1
        elif line.count(O) == 3:
            return -1
        #build diag matrix
        diags[0].append(board[indexdiag][indexdiag])
        diags[1].append(board[indexdiag][abs(indexdiag - 2)])
        indexdiag += 1

        # build column matrix
        columns[0].append(board[indexcolumn][0])
        columns[1].append(board[indexcolumn][1])
        columns[2].append(board[indexcolumn][2])
        indexcolumn += 1

    # test if win in a column
    for column in columns:

        if column.count(X) == 3:
            return 1
        elif column.count(O) == 3:
            return -1

    # test if win in a diag
    for diag in diags:
        if diag.count(X) == 3:
            return 1
        elif diag.count(O) == 3:
            return -1

    return 0

    #raise NotImplementedError

def heuristic_value(board, joueur):
    score = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == joueur:
                score += 1
            elif board[i][j] != EMPTY:
                score -= 1
    return score

def alphabeta(state,alpha,beta,depth,tabs,level,player,ia_player=X):
    tabs = tabs + "\t"
    level+=1
    myfile.write(tabs+"alphabeta["+str(level)+"]: " + "(" + str(state)+","+str(depth)+","+","+ str(alpha)+","+str(beta)+","+player+","+ia_player+")\n")

    if terminal(state):
        u = utility(state)
        return u*10
    elif depth == 0:
        h = heuristic_value(state,ia_player)
        return h

    if player == X:
        v = -math.inf

        for action in actions(state):
            copied_board_m = copy.deepcopy(state)
            result_copied_board = result(copied_board_m, action)

            mv = alphabeta(result_copied_board,alpha,beta,depth-1,tabs,level,O,ia_player)
            v = max(v,mv)

            if v>beta:
                break
            alpha=max(alpha,v)
        return v
    else:
        v = math.inf

        for action in actions(state):
            copied_board_m = copy.deepcopy(state)
            result_copied_board = result(copied_board_m, action)

            mv=alphabeta(result_copied_board, alpha, beta, depth - 1, tabs, level, X,ia_player)

            v = min(v, mv)

            if v < alpha:
                break
            beta = min(beta, v)
        return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #With the board I can get the player, so the idea is to create a recurive function
    #assuming that X wants to maximize and O wants to minimize
    print(datetime.datetime.now())

    if terminal(board):
        return None
    best_action = ()

    #Get IA player
    ia_player = player(board)

    if ia_player == X:
        best_score = -math.inf
        for action in actions(board):
            minimax_board = copy.deepcopy(board)
            result_minimax_board = result(minimax_board, action)
            current_score = alphabeta(result_minimax_board,-math.inf,math.inf,4,"\t",0,O,ia_player)
            if current_score>best_score:
                best_score = current_score
                best_action = action
        print(datetime.datetime.now())
        return best_action
    else:
        best_score = math.inf
        for action in actions(board):

            minimax_board = copy.deepcopy(board)
            result_minimax_board = result(minimax_board, action)
            current_score = alphabeta(result_minimax_board, -math.inf, math.inf, 5, "\t", 0, X, ia_player)
            if current_score < best_score:
                best_score = current_score
                best_action = action
        print(datetime.datetime.now())
        return best_action