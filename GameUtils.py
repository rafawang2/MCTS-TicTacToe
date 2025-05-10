from dataclasses import dataclass

@dataclass
class STATE:
    board: list
    current_player: int = -1

def ANSI_string(s="", color=None, background=None, bold=False):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    background_colors = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m',
        'reset': '\033[0m',
        'gray': '\033[100m',  # 新增的灰色背景
        'light_gray': '\033[47m'  # 新增的淺灰色背景
    }

    styles = {
        'bold': '\033[1m',
        'reset': '\033[0m'
    }
    color_code = colors[color] if color in colors else ''
    background_code = background_colors[background] if background in colors else ''
    bold_code = styles['bold'] if bold else ''

    return f"{color_code}{background_code}{bold_code}{s}{styles['reset']}"

def isTie(board):
    return all([cell != 0 for row in board for cell in row])

def isWinner(board, player):  # 回傳 player 是否為贏家
    # 橫排
    for row in board:
        if all([cell == player for cell in row]):
            return True
    # 直排
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    # 對角線
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False


def GetWinner(board):
    if isWinner(board, -1):
        return -1
    if isWinner(board, 1):
        return 1
    if isTie(board):
        return 0
    return None

def print_board(board):
    print('+~~~~~~~+')
    for i in range(3):
        print('|',end=' ')
        for j in range(3):
            if board[i][j] == 0:
                print('-', end=' ')
            elif board[i][j] == -1:
                print(ANSI_string('X',color='green'), end=' ')
            elif board[i][j] == 1:
                print(ANSI_string('O',color='yellow'), end=' ')
        print('|')
    print('+~~~~~~~+')

def is_ValidMove(board, r, c):
    if r<0 or c<0 or r>2 or c>2:
        return False

    return True if board[r][c] == 0 else False

def getValidMoves(board):
    moves = []
    for r in range(3):
        for c in range(3):
            if is_ValidMove(board, r, c):
                moves.append((r, c))
    return moves

def make_move(board, r, c, player):
    if (r,c) and is_ValidMove(board, r,c):
        board[r][c] = player
    else:
        print("Invalid Move")