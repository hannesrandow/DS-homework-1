from Tkinter import *
import Tkinter
import ttk
import tkMessageBox
import re

from sudoku.client.game_server_discovery import GameServerDiscovery
from sudoku.client.rpc_client import RpcClient
from sudoku.common import protocol


class EnterServerAddressDialog:
    def __init__(self, client):
        self.root = Tk()
        self.client = client
        self.address = ""
        self.lblAddress = Label(self.root, text="Please enter the address of the server: ")
        # self.lblAddress.pack(side=LEFT)
        self.lblAddress.grid(row=0)
        self.entryAddress = Entry(self.root)
        # self.entryAddress.pack(sid=LEFT)
        self.entryAddress.grid(row=0, column=1)
        self.btnAddress = Button(self.root, text="Confirm", command=self.confirm_server_address)
        # self.btnAddress.pack(sid=LEFT)
        self.btnAddress.grid(row=0, column=2)
        self.autoAddress = Button(self.root, text="Auto Disovery", command=self.auto_discovery)
        # self.autoAddress.pack(sid=LEFT)
        self.autoAddress.grid(row=0, column=3)
        self.serverList = Listbox(self.root)
        self.serverList.bind("<Double-Button-1>", self.select_server_from_list_on_double_click)
        self.serverList.grid(row=1, column=0,columnspan=4)
        self.rpcClient = None
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
                self.root.destroy()
            except:
                tkMessageBox.showerror("Connection refused", "Server not found")
        else:
            tkMessageBox.showinfo("Wrong Input", "You have to enter a server address like 168.0.0.1")


    def auto_discovery(self):
        # start progress bar
        popup = Tkinter.Toplevel()
        Tkinter.Label(popup, text="Looking for server(s)..").grid(row=0, column=0)

        popup.grab_set()
        progress_var = Tkinter.DoubleVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0)  # .pack(fill=tk.X, expand=1, side=tk.BOTTOM)
        popup.pack_slaves()

        game_server_discovery = GameServerDiscovery()
        discovered = game_server_discovery.get_list(popup, progress_var)
        game_server_discovery.stop()
        popup.grab_release()
        popup.destroy()
        self.serverList.delete(0, END)
        for item in discovered:
            self.serverList.insert(END, item)

    def select_server_from_list_on_double_click(self, event):
        '''
        double click on list element updates the name entry
        :param event: double click event on list
        :return: None
        '''
        # at first clear entry
        self.entryAddress.delete(0, 'end')
        self.entryAddress.insert(0, self.serverList.get(ACTIVE))