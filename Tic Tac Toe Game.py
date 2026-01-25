6# Tic Tac Toe Game (Player X vs Computer O)

board = [' ' for _ in range(10)]  # index 0 unused

def insertBoard(letter, pos):
    global board
    board[pos] = letter

def spaceIsFree(pos):
    return board[pos] == ' '

def isWinner(bo, le):
    # Returns True if player with letter le has won on board bo
    return (
        (bo[7] == le and bo[8] == le and bo[9] == le) or  # top row
        (bo[4] == le and bo[5] == le and bo[6] == le) or  # middle row
        (bo[1] == le and bo[2] == le and bo[3] == le) or  # bottom row
        (bo[7] == le and bo[4] == le and bo[1] == le) or  # left col
        (bo[8] == le and bo[5] == le and bo[2] == le) or  # middle col
        (bo[9] == le and bo[6] == le and bo[3] == le) or  # right col
        (bo[7] == le and bo[5] == le and bo[3] == le) or  # diag
        (bo[9] == le and bo[5] == le and bo[1] == le)     # diag
    )

def playerMove():
    while True:
        move = input("Please select a position to place an 'X' (1-9): ")
        try:
            move = int(move)
            if 1 <= move <= 9:
                if spaceIsFree(move):
                    insertBoard('X', move)
                    return
                else:
                    print('This position is already occupied!')
            else:
                print('Please type a number within the range 1-9!')
        except ValueError:
            print('Please type a valid number!')

def selectRandom(li):
    import random
    return li[random.randrange(0, len(li))]

def compMove():
    # All free positions (ignore index 0)
    possibleMoves = [i for i, letter in enumerate(board) if letter == ' ' and i != 0]
    if not possibleMoves:
        return 0

    # Win or block
    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                return i

    # Take a corner
    cornersOpen = [i for i in possibleMoves if i in [1, 3, 7, 9]]
    if cornersOpen:
        return selectRandom(cornersOpen)

    # Take center
    if 5 in possibleMoves:
        return 5

    # Take an edge
    edgesOpen = [i for i in possibleMoves if i in [2, 4, 6, 8]]
    if edgesOpen:
        return selectRandom(edgesOpen)

    return 0

def isBoardFull(b):
    # index 0 is unused, so more than 1 space means moves remain
    return not (b.count(' ') > 1)

def printBoard():
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')

def main():
    print("Welcome to Tic Tac Toe!")
    print("To win, complete a straight line (diagonal, horizontal, or vertical).")
    print("Board positions are 1-9, starting at the top-left.")
    printBoard()

    while not isBoardFull(board):
        if not isWinner(board, 'O'):
            playerMove()
            printBoard()
        else:
            print("O's win this time...")
            break

        if not isWinner(board, 'X'):
            move = compMove()
            if move == 0:
                print('Game is a tie! No more spaces left to move.')
                break
            insertBoard('O', move)
            print(f"Computer placed an 'O' in position {move}:")
            printBoard()
        else:
            print("X's win, good job!")
            break

    if isBoardFull(board) and not isWinner(board, 'X') and not isWinner(board, 'O'):
        print('Game is a tie! No more spaces left to move.')

# Run and replay loop
if __name__ == "__main__":
    main()
    while True:
        answer = input('Do you want to play again? (Y/N): ').strip().lower()
        if answer in ('y', 'yes'):
            board = [' ' for _ in range(10)]
            print('-----------------------------------')
            main()
        else:
            print('Thanks for playing!')
            break
2