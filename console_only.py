import overlappingFunctions
import connectfour
from connectfour import GameOverError, InvalidMoveError

def run_user_interface() -> None:
    '''Runs the user interface and maintains the game until end.'''
    overlappingFunctions.print_welcome_message()
    game_state = connectfour.new_game()
    overlappingFunctions.display_board(game_state)

    while connectfour.winner(game_state) == connectfour.NONE:
        GamePlusMove = overlappingFunctions.execute_move(game_state)
        game_state = GamePlusMove.GameState
        overlappingFunctions.display_board(game_state)
    else:
        overlappingFunctions.print_winner(game_state)
    
if __name__ == "__main__":
    run_user_interface()    
