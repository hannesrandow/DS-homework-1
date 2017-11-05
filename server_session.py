import abc
from server import Session

class ServerSession(Session):
    
    def __init(self, game_state, game_id, game_name, game_solution, max_num_of_players):
        self.game_state = game_state
        self.game_id = game_id
        self.game_name = game_name
        self.game_solution = game_solution
        self.max_num_of_players = max_num_of_players
    
    
    @abstractmethod
    def update_game():
        pass
    
    def game_start():
        pass
    

    def game_finish():
        pass

    def terminate_session():
        pass