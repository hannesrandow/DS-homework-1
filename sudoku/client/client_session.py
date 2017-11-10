class ClientSession(Client):

    def __init(self, game_state, game_id, game_name, game_solution, maximum_num_of_players, score):
        self.game_state = game_state
        self.game_id = game_id
        self.game_name = game_name
        self.game_solution = game_solution
        self.maximum_num_of_players = maximum_num_of_players
        self.score = score
    
    @abstractmethod
    def update_game():
        pass
    
