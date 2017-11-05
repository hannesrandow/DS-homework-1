import abc
import csv
import os
#from server import Session

class ServerSession(object):
    
    def __init__(self, game_status, game_id, game_name, new_game_path, game_solution_path, max_num_of_players):
        self.game_status = game_status
        self.game_id = game_id
        self.game_name = game_name
        self.new_game_path = new_game_path
        self.game_solution_path = game_solution_path
        self.max_num_of_players = max_num_of_players
        self.game_state = []
        self.game_solution = []
        
      
    
    def read_game(self, path):
        """        
        read sudoko game from csv file
        """
        cwd = os.getcwd()
        
        game = []
        with open(path) as sudoku:
            read_sudoku = csv.reader(sudoku, delimiter=',')
            for row in read_sudoku:
                row = [int(x) for x in row]
                game.append(row)
                
        return game
    
    

    def update_game():
        pass

    
    def game_start(self):
        self.game_state = self.read_game(self.new_game_path)
        self.game_solution = self.read_game(self.game_solution_path)
    

    def game_finish():
        pass

    def terminate_session():
        pass
    

                