from Tkinter import *
import tkMessageBox
import re

from sudoku.common import protocol


class EnterServerAddressDialog:
    def __init__(self, client):
        self.root = Tk()
        self.client = client
        self.address = ""
        self.lblAddress = Label(self.root, text="Please enter the address of the server: ")
        self.lblAddress.pack(side=LEFT)
        self.entryAddress = Entry(self.root)
        self.entryAddress.pack(sid=LEFT)
        self.btnAddress = Button(self.root, text="Confirm", command=self.confirm_server_address)
        self.btnAddress.pack(sid=LEFT)
        self.root.mainloop()

    def confirm_server_address(self):
        '''
        checks the entry input if it is in the right format and after this if it is possible to connect to the server
        if the address is fine the connection is established and the window itself is closed
        :return: None
        '''
        address = self.entryAddress.get()
        r = re.compile("\d*\.\d*\.\d*\.\d*")
        if r.match(address) is not None:
            try:
                self.client.sock.connect((address, protocol.PORT))
                self.address = address
                self.root.destroy()
            except:
                tkMessageBox.showerror("Connection refused", "Server not found")
        else:
            tkMessageBox.showinfo("Wrong Input", "You have to enter a server address like 168.0.0.1")
