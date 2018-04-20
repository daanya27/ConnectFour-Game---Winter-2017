import connectfour
import collections


GameStateAndMove = collections.namedtuple('GameStateAndMove', ['GameState','move'])



def print_welcome_message() -> None:
    ''' Prints welcome message '''
    welcome_message = 'Welcome to Connect Four!\nPlay by choosing column number to drop or pop (remove) your piece in or from.\nFirst player to 4-in-a-row wins.\n"DROP col#" to drop a piece.\n"POP col#" to pop a piece.'
    print(welcome_message)
    print()

def display_board(gstate: connectfour.GameState) -> None:
    ''' Prints out given GameState board '''
    matrix = ""
    for row in range(connectfour.BOARD_ROWS):
        string = ""
        for col in range(connectfour.BOARD_COLUMNS):
            if gstate.board[col][row] == connectfour.NONE:
                string = string + " . "
            if gstate.board[col][row] == connectfour.RED:
                string = string + " R "
            if gstate.board[col][row] == connectfour.YELLOW:
                string = string + " Y "

        matrix = matrix + string + "\n"

    display_column_numbers()
    print(matrix)

def display_column_numbers() -> None:
    ''' Prints only top line of column numbers '''  # subfunction of display_board()
    string = ""
    for col in range(connectfour.BOARD_COLUMNS):
        string = string + (" " + str(col + 1) + " ")
    print(string)

def print_winner(gstate: connectfour.GameState) -> None:
    ''' Prints winner '''       
    if connectfour.winner(gstate) == connectfour.RED:
        print("RED player, is victorious!")
    elif connectfour.winner(gstate) == connectfour.YELLOW:
        print("YELLOW player is victorious!")

def input_move(turn: int) -> str:
    '''Requests player move according to int parameter and returns string.'''
    if turn == connectfour.RED:
        move = input("RED, your turn:")
    elif turn == connectfour.YELLOW:
        move = input("YELLOW, your turn:")
    else:
        move = ""
        
    return move.strip()





def execute_move(gstate: connectfour.GameState) -> GameStateAndMove:
    ''' Repeatedly calls input_move until valid move,
        then returns updated GameState and move string.'''
    while True:
        attempted_move = input_move(gstate.turn)
        try:
            commands = attempted_move.split()
            column = int(commands[1])

            updated_gstate = gstate

            if commands[0] == 'DROP':
                updated_gstate = connectfour.drop(gstate, column - 1)
                d_gstate = connectfour.drop(gstate, column - 1)
            elif commands[0] == "POP":
                updated_gstate = connectfour.pop(gstate, column - 1)
            elif commands[0] not in ["DROP", "POP"]:
                raise SyntaxError
            
            return GameStateAndMove(updated_gstate, attempted_move)
        
        except SyntaxError:
            print('Please provide "DROP" or "POP" followed by a space and a valid column number.')
        except ValueError:
            print("Please provide a valid column nubmer.")
        except IndexError:
            print('Please provide "DROP" or "POP" followed by a space and a valid column number.')
        except InvalidMoveError:
            print("That is an invalid move. Try again.")
        except GameOverError:    #don't need this
            print("Game is over." + print_winner(gstate))
            break
