from time import sleep

from Tkinter import *
import tkMessageBox

from sudoku.common import protocol


class MultiplayerGameDialog:
    def __init__(self, client):
        self.root = Tk()
        self.client = client
        self.root.title('Games Dialog')
        # self.session = None     # either filled with the create_session or join_session
        self.gameName = ""
        self.lblName = Label(self.root, text="Name: ")
        self.lblName.grid(row=0)
        self.enterName = Entry(self.root)
        self.enterName.grid(row=0, column=1)
        self.lblNumber = Label(self.root, text="Number of Players: ")
        self.lblNumber.grid(row=0, column=2)
        self.enterNumber = Entry(self.root)
        self.enterNumber.grid(row=0, column=3)
        self.btnCreateNewSession = Button(self.root, text="create", command=self.create_session)
        self.btnCreateNewSession.grid(row=0, column=4)
        self.listSessions = Listbox(self.root)
        self.listSessions.bind("<Double-Button-1>", self.select_session_from_list_on_double_click)
        self.listSessions.grid(row=1, columnspan=4)
        # Done: request sessions from server
        self.currentSessions = self.get_current_sessions(self.client)
        for item in self.currentSessions:
            self.listSessions.insert(END, item.game_name)
        self.root.mainloop()


    def create_session(self):
        '''
        client creates a new session by using the typed in name and number of players
        :return: None
        '''
        self.gameName = self.enterName.get()
        self.number = self.enterNumber.get()
        print("gamename: ", self.gameName)
        if self.client.create_session(self.gameName, self.number) == protocol._ACK:
            sleep(1)
            print "success"
            # further operations for getting the init session is done at GamePlay __init__()
        else:
            print "oh, crap!"
        self.root.destroy()

    def select_session_from_list_on_double_click(self, event):
        '''
        client joins an existing session by double clicking on the list of available sessions
        in case of a full session an error message occurs
        :param event: used to react on a double click
        :return: None
        '''
        index = event.widget.curselection()[0]
        self.currentSession = self.currentSessions[int(index)]
        rsp = self.client.rpcClient.call(protocol._REQ_JOIN_SESSION + protocol._MSG_FIELD_SEP + str(self.currentSession.game_id))
        # TODO: use simpler output for the joining session (on server!)
        if rsp.startswith(protocol._ACK):
            self.session = self.currentSession  # TODO: maybe not necessary
            self.gameName = self.currentSession.game_name
            self.root.destroy()
            return rsp
        elif rsp.startswith(protocol._RSP_SESSION_FULL):
            tkMessageBox.showinfo('Session is full!', 'Oops.. people already having fun on this session. Try another!')
        else:
            print 'UUID is not available?' # TODO: what's this? perhaps need another flag in response for this situation!

    def get_current_sessions(self,client):
        '''
        lists the current sessions (to join them by clicking)
        :param client: client for this GUI
        :return: None
        '''
        return client.get_current_sessions()