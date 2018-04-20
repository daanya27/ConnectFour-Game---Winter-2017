import overlappingFunctions
import consoleOnly
import socketHandling
import connectfour
from connectfour import GameOverError, InvalidMoveError

def interpret_response(connection: socketHandling.Connection, response: str, gstate: connectfour.GameState) -> connectfour.GameState:
    '''Decides how many responses to request/print based on a given
    response.'''

    if response=="OKAY":
        
        move_response = socketHandling.receive_response(connection)
        socketHandling.print_response(move_response)
        updated_gstate = AI_move(gstate, move_response)

        final_response = socketHandling.receive_response(connection)
        if final_response != "READY":
            is_connected = socketHandling.close(connection)
        
        return updated_gstate
        
    elif response=="INVALID":
        socketHandling.print_response(response)
        socketHandling.print_response(socketHandling.receive_response(connection))
        return gstate
    
    elif response=="WINNER_RED":
        print("You win. Game over.")
        is_connected = socketHandling.close(connection)
        return gstate
    
    else:
        print('socket responses do not match protocol.')
        is_connected = socketHandling.close(connection)
        return gstate

def AI_move(gstate: connectfour.GameState, move:str) -> connectfour.GameState:
    '''Enacts a move from the AI under the assumption that the move is valid.'''
    commands = move.split()
    column = int(commands[1])
    if commands[0] == 'DROP':
        return connectfour.drop(gstate, column - 1)
    else:
        return connectfour.pop(gstate, column - 1)
    
    

def run_user_interface() -> None:
    '''Runs the user interface and maintains the game until end.'''
    host = socketHandling.input_host()
    port = socketHandling.input_port()

    print('Connecting to {} (port {})...'.format(host, port))
    connection = socketHandling.connect(host, port)
    print('Connection successful.')
    name = socketHandling.input_username()

    is_connected = socketHandling.initial_protocol(connection, name)

    if is_connected != False:
        overlappingFunctions.print_welcome_message()
        gstate = connectfour.new_game()
        overlappingFunctions.display_board(gstate)

    while is_connected != False and connectfour.winner(gstate) == connectfour.NONE:  
        if gstate.turn == connectfour.RED:
            GamePlusMove = overlappingFunctions.execute_move(gstate)
            socketHandling.send_message(connection,GamePlusMove.move)
            gstate = GamePlusMove.GameState
            overlappingFunctions.display_board(gstate)
        elif gstate.turn == connectfour.YELLOW:
            response = socketHandling.receive_response(connection)
            gstate = interpret_response(connection, response, gstate)
            overlappingFunctions.display_board(gstate)
            
    if is_connected != False:        
        overlappingFunctions.print_winner(gstate)
    
    
if __name__ == "__main__":
    is_connected = bool(None)
    run_user_interface()    
    
