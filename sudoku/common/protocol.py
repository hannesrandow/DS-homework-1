GAME_UPDATE_PORT = 7026
HOST = '127.0.0.1'
PORT = 7795

# acknowledgement
_ACK = 'ACK'

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
_RSP_CURRENT_SESSIONS = 'sr1'
_RSP_SESSION_JOINED = 'sr2.1'
_RSP_SESSION_FULL = 'sr2.2'
_RSP_LEAVE_SESSION = 'sr3'
_RSP_GAME_UPDATE_CORRECT = 'sr4.1'
_RSP_GAME_UPDATE_INCORRECT = 'sr4.2'

# server actions
_SA_CREATE_SESSION = 'sa1'
_SA_NEW_PLAYER = 'sa2'
_SA_NICKNAME = 'sa3'
_SA_CURRENT_SESSIONS = 'sa4'
_SA_UPDATE_GAME = 'sa5'
_SA_JOIN_SESSION = 'sa6'

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