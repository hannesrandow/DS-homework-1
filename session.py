import abc
import csv
import os
import protocol
#from server import Session

class Session(object):
    
    def __init__(self, game_status, game_id, game_name, new_game_path, game_solution_path, max_num_of_players, current_players):
        self.game_status = game_status
        self.game_id = game_id
        self.game_name = game_name
        self.new_game_path = new_game_path
        self.game_solution_path = game_solution_path
        self.max_num_of_players = max_num_of_players
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
        #protocol.__REQ_UPDATE_GAME + protocol.__MSG_FIELD_SEP + 
        #                          row + protocol.__MSG_FIELD_SEP + column + protocol.__MSG_FIELD_SEP + number
        #print protocol.__MSG_FIELD_SEP
        #print information
        #information = information.split(protocol.__MSG_FIELD_SEP)
        information = information.split(':')
        row = int(information[1])
        column = int(information[2])
        number = int(information[3])
        
        if self.game_state[row][column] == 0:
            if self.game_solution[row][column] == number:
                self.game_state[row][column] == number
                #rsp = protocol.__RSP_GAME_UPDATE_CORRECT"""

    
    def game_start(self):
        self.game_state = self.read_game(self.new_game_path)
        self.game_solution = self.read_game(self.game_solution_path)
    

    def game_finish():
        pass

    def terminate_session():
        pass
    

                