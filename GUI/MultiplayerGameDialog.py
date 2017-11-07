from Tkinter import *
import tkMessageBox


class MultiplayerGameDialog:
    def __init__(self):
        self.root = Tk()
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
        # TODO: request sessions from server
        for item in ["session1", "session2"]:
            self.listSessions.insert(END, item)
        self.root.mainloop()

    def create_session(self):
        name = self.enterName.get()
        number = int(self.enterNumber.get())

        pass

    def select_session_from_list_on_double_click(self, event):
        pass
