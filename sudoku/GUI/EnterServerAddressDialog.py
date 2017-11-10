from Tkinter import *
import tkMessageBox
import re

class EnterServerAddressDialog:
    def __init__(self):
        self.root = Tk()
        self.lblAddress = Label(self.root, text="Please enter the address of the server: ")
        self.lblAddress.pack(side=LEFT)
        self.entryAddress = Entry(self.root)
        self.entryAddress.pack(sid=LEFT)
        self.btnAddress = Button(self.root, text="Confirm", command=self.confirm_server_address)
        self.btnAddress.pack(sid=LEFT)
        self.root.mainloop()

    def confirm_server_address(self):
        address = self.entryAddress.get()
        r = re.compile("\d*\.\d*\.\d*\.\d*")
        if r.match(address) is not None:
            self.root.destroy()
        else:
            tkMessageBox.showinfo("Wrong Input", "You have to enter a server address like 168.0.0.1")
        '''
        try:
            # TODO: connect with server
        catch SocketException e:
            tkMessageBox.showerror("Exception", "Connection Exception: Not connected")
        '''
