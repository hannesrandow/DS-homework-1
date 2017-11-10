import csv
import os


class Session(object):
    
    def __init__(self, game_status, game_id, game_name, new_game_path, game_solution_path, max_num_of_players, current_players):
        self.game_status = game_status
        self.game_id = game_id
        self.game_name = game_name
        self.new_game_path = new_game_path
        self.game_solution_path = game_solution_path
        self.max_num_of_players = int(max_num_of_players)
        self.current_players = current_players
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
    
    def update_game(self, information):
        
        information = information.split(':')
        row = int(information[1])
        column = int(information[2])
        number = int(information[3])
        
        if self.game_state[row][column] == 0:
            if self.game_solution[row][column] == number:
                self.game_state[row][column] = number

    def game_start(self):
        self.game_state = self.read_game(self.new_game_path)
        self.game_solution = self.read_game(self.game_solution_path)

    def game_finish():
        pass

    def terminate_session():
        pass

    def add_player(self, player):
        was_successful = False
        if self.max_num_of_players - len(self.current_players) > 0:
            self.current_players.append(player)
            was_successful = True
        return was_successful