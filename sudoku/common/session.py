import csv
import os

from sudoku.common import protocol


class Session(object):
    """
    A session holds one game that is being played. It also holds all the necessary information regarding the game.
    For example all the number of players that are currently in the game, the id of the game, the solution to the game.
    """
    
    def __init__(self, game_status, game_id, game_name, new_game_path, game_solution_path,
                 max_num_of_players, current_players):
        """
        :param game_status: The status of the game. Pending or ready to play.
        :param game_id: The id of the game. First game on server gets id 1, then increases by one for each new session.
        :param game_name: The name the user gave the game.
        :param new_game_path: The path to the sudoku puzzle.
        :param game_solution_path: The path to the solution of the sudoku puzzle.
        :param max_num_of_players: The maximum possible number of players for the game, specified by the user.
        :param current_players: A list holding all the players that are currently in the game.
        """
        self.game_status = game_status
        self.game_id = game_id
        self.game_name = game_name
        self.new_game_path = new_game_path
        self.game_solution_path = game_solution_path
        self.max_num_of_players = int(max_num_of_players)
        self.current_players = current_players
        self.game_state = []        #Current game state. Numbers in the cells (empty cells have a 0)
        self.game_solution = []     #The solution to the sudoku puzzle. Nested list.
        
    def read_game(self, name):
        """
        This method parses a sudoku puzzle. Sudoku puzzles must be in csv files.
        :param name: Name of the csv file containing the sudoku puzzle
        :return: A nested list of the sudoku puzzle. Each row in the sudoku is one list.
        """
        puzzle = os.getcwd() + '/sudoku/puzzles/' + name + '.csv'
        
        game = []
        with open(puzzle) as sudoku:
            read_sudoku = csv.reader(sudoku, delimiter=',')
            for row in read_sudoku:
                row = [int(x) for x in row]
                game.append(row)
        return game
    
    def update_game(self, information, player):
        """
        This method gets calles when a user makes an update to the current game.
        :param information: The row & column that the user wants to modify, as well as the number he wants to insert.
        :param player: THe player that wants to make the change
        :return: Boolean value that indicates whether the requested change was correct or incorrect.
        """
        def update_score(correct):
            """
            Method that updates the score of the player that wanted to make the change accordingly.
            +1 for a correct number.
            -1 for an incorrect number.
            :param correct: Boolean value that indicates whether the requested change was correct or incorrect.
            :return: None
            """
            index_of_updating_player = self.current_players.index(player)
            if correct:
                self.current_players[index_of_updating_player].score += 1
            else:
                self.current_players[index_of_updating_player].score -= 1
        
        information = information.split(':')
        row = int(information[1])
        column = int(information[2])
        number = int(information[3])
        
        correct = False
        if self.game_state[row][column] == 0:
            if self.game_solution[row][column] == number:
                self.game_state[row][column] = number
                correct = True
        if self.game_state == self.game_solution:
            self.game_status = protocol._COMPLETED
        #update score of the player that made the change
        update_score(correct)
        return correct
        
        

    def game_start(self):
        """
        Read the empty game and the solution to the game
        :return: None
        """
        self.game_state = self.read_game(self.new_game_path)
        self.game_solution = self.read_game(self.game_solution_path)

    def game_finish(self):
        pass

    def terminate_session(self):
        pass

    def add_player(self, player):
        """
        This method gets called when this session has been running and a new player requests to join the session.
        If the maximum number of players has not been reached the player can join the session, otherwise the request
        gets rejected.
        :param player: The player
        :return: Boolean value whether the player was added to the session or not.
        """
        was_successful = False
        if self.max_num_of_players - len(self.current_players) > 0:
            self.current_players.append(player)
            if self.max_num_of_players == len(self.current_players):
                self.game_status = protocol._READY
            was_successful = True
        return was_successful

    def remove_player(self, uuid):
        if uuid in self.current_players.keys():
            del(self.current_players[uuid])
            # in case just one player stays in game, the game is over
            if len(self.current_players) == 1:
                self.game_status = protocol._COMPLETED
            return True
        return False
