#acknowledgement
__ACK = 'ACK'

#client requests 
__REQ_current_sessions = 'c1'
__REQ_join_session = 'c2'
__REQ_leave_session = 'c3'
__REQ_create_session = 'c4'
#make change to game
__REQ_update_game = 'c5'


#server responses
__RSP_current_session = 's1'
__RSP_session_joined = 's2.1'
__RSP_session_full = 's2.2'
__RSP_leave_session = 's3'
__RSP_session_created = 's4'
__RSP_game_update_correct = 's5.1'
__RSP_game_update_incorrect = 's5.2'




#field separator for sending multiple values ---------------------------------
__MSG_FIELD_SEP = ':'

#message terminator character
__TERMINATOR = '*'

def server_process(message):
    
    if message.startswith(__REQ_current_sessions + __MSG_FIELD_SEP) and message.endswith(__TERMINATOR):
        return __RSP_current_sessions