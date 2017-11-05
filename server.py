from server_session import ServerSession

current_sessions = []
current_players = []

def list_sessions():
    return current_sessions

def process_message(m):
    pass
    
                
                
if __name__ == '__main__':
    
    server_session = ServerSession('running', 1, 'new_game', 
                                   'sudoku_puzzles/sudoku_easy_1.csv', 
                                   'sudoku_puzzles/sudoku_easy_1_solution.csv', 
                                   5)
    server_session.game_start()
    
    for i in server_session.game_solution:
        print i
    
    