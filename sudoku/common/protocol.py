GAME_UPDATE_PORT = 7035
HOST = '0.0.0.0'
PORT = 7805

# service discovery
multicast_group = ('224.0.0.71', 5004)
service_name = 'SUDOKU_GAME_2017'

# session status
_PENDING = 'ss0'
_READY = 'ss1'
_COMPLETED = 'ss2'
