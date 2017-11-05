#acknowledgement
__ACK = 'ACK'

#client requests 
__REQ_INITIAL_CONNECT = 'c0'
__REQ_CURRENT_SESSIONS = 'c1'
__REQ_JOIN_SESSIONS = 'c2'
__REQ_LEAVE_SESSION = 'c3'
__REQ_CREATE_SESSION = 'c4'
__REQ_NICKNAME = 'c5'
#make change to game
__REQ_UPDATE_GAME = 'c6'


#server responses
__RSP_CURRENT_SESSIONS = 'sr1'
__RSP_SESSION_JOINED = 'sr2.1'
__RSP_SESSION_FULL = 'sr2.2'
__RSP_LEAVE_SESSION = 'sr3'
__RSP_GAME_UPDATE_CORRECT = 'sr4.1'
__RSP_GAME_UPDATE_INCORRECT = 'sr4.2'

#server actions
__SA_CREATE_SESSION = 'sa1'
__SA_NEW_PLAYER = 'sa2' 
__SA_NICKNAME = 'sa3'


#field separator for sending multiple values ---------------------------------
__MSG_FIELD_SEP = ':'

#message terminator character
__TERMINATOR = '*'

def server_process(message):
    
    if message.startswith(__REQ_INITIAL_CONNECT + __MSG_FIELD_SEP) and message.endswith(__TERMINATOR):
        return __SA_NEW_PLAYER
    
    elif message.startswith(__REQ_NICKNAME + __MSG_FIELD_SEP) and message.endswith(__TERMINATOR):
        return __SA_NICKNAME
    
    elif message.startswith(__REQ_CURRENT_SESSIONS + __MSG_FIELD_SEP) and message.endswith(__TERMINATOR):
        return __RSP_current_sessions
    
    elif message.startswith(__REQ_CREATE_SESSION + __MSG_FIELD_SEP) and message.endswith(__TERMINATOR):
        return __SA_CREATE_SESSION
    
    elif message.startswith(__REQ_UPDATE_GAME + __MSG_FIELD_SEP) and message.endswith(__TERMINATOR):
        return __REQ_UPDATE_GAME