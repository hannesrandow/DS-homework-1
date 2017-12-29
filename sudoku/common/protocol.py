GAME_UPDATE_PORT = 7035
HOST = '0.0.0.0'
PORT = 7805

# service discovery
multicast_group = ('224.0.0.71', 5004)
service_name = 'SUDOKU_GAME_2017'


# acknowledgement
_ACK = 'ACK'
_INIT = 'INIT'

# client requests
_REQ_INITIAL_CONNECT = 'c0'
_REQ_CURRENT_SESSIONS = 'c1'
_REQ_JOIN_SESSION = 'c2'
_REQ_LEAVE_SESSION = 'c3'
_REQ_CREATE_SESSION = 'c4'
_REQ_NICKNAME = 'c5'
# make change to game
_REQ_UPDATE_GAME = 'c7'

# server responses
_RSP_OK = 'sr0'
_RSP_SOME_ERROR = 'sr0.1'
_RSP_CURRENT_SESSIONS = 'sr1'
_RSP_SESSION_JOINED = 'sr2.1'
_RSP_SESSION_FULL = 'sr2.2'
_RSP_LEAVE_SESSION = 'sr3'
_RSP_GAME_UPDATE_CORRECT = 'sr4.1'
_RSP_GAME_UPDATE_INCORRECT = 'sr4.2'
_RSP_NO_GAME_FOUND = 'sr5'
_RSP_USER_NOT_EXISTING = 'sr6'

# server actions
_SA_CREATE_SESSION = 'sa1'
_SA_NEW_PLAYER = 'sa2'
_SA_NICKNAME = 'sa3'
_SA_CURRENT_SESSIONS = 'sa4'
_SA_UPDATE_GAME = 'sa5'
_SA_JOIN_SESSION = 'sa6'
_SA_LEAVE_SESSION = 'sa7'

# session status
_PENDING = 'ss0'
_READY = 'ss1'
_COMPLETED = 'ss2'

# field separator for sending multiple values ---------------------------------
_MSG_FIELD_SEP = ':'

# message terminator character
_TERMINATOR = '*'


def server_process(message):
    if message.startswith(_REQ_INITIAL_CONNECT):
        return _SA_NEW_PLAYER

    elif message.startswith(_REQ_NICKNAME + _MSG_FIELD_SEP):
        return _SA_NICKNAME

    elif message.startswith(_REQ_CURRENT_SESSIONS):
        return _SA_CURRENT_SESSIONS

    elif message.startswith(_REQ_CREATE_SESSION + _MSG_FIELD_SEP):
        return _SA_CREATE_SESSION

    elif message.startswith(_REQ_UPDATE_GAME + _MSG_FIELD_SEP):
        return _SA_UPDATE_GAME

    elif message.startswith(_REQ_JOIN_SESSION + _MSG_FIELD_SEP):
        return _SA_JOIN_SESSION

    elif message.startswith(_REQ_LEAVE_SESSION):
        return _SA_LEAVE_SESSION