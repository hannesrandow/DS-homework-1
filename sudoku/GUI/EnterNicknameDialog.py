from Tkinter import *
import tkMessageBox


class EnterNicknameDialog:
    def __init__(self):
        self.root = Tk()
        self.nickname = ""
        self.root.title('Nickname Dialog')
        self.lblNickname = Label(self.root, text="Please enter your Nickname: ")
        self.lblNickname.grid(row=0)
        self.enterNickname = Entry(self.root)
        self.enterNickname.grid(row=0, column=1)
        self.btnNickname = Button(self.root, text="confirm", command=self.confirm_nickname)
        self.btnNickname.grid(row=0, column=2)
        self.listNicknames = Listbox(self.root)
        self.listNicknames.bind("<Double-Button-1>", self.select_nickname_from_list_on_double_click)
        self.listNicknames.grid(row=2, columnspan=2)
        for item in ["alpha", "beta", "gamma", "delta"]:
            self.listNicknames.insert(END, item)
        self.root.mainloop()

    def confirm_nickname(self):
        '''
        checks if the name is alphanumerical and if it has at maximum 8 symbols
        if the name is fine the window is closed
        :return: None
        '''
        name = self.enterNickname.get()
        if len(name) <= 8 and name.isalnum():
            self.nickname = name
            self.root.destroy()
        else:
            tkMessageBox.showerror("Wrong Input", "Please just use numbers or letters (max 8)!")
        pass

    def select_nickname_from_list_on_double_click(self, event):
        '''
        double click on list element updates the name entry
        :param event: double click event on list
        :return: None
        '''
        # at first clear entry
        self.enterNickname.delete(0, 'end')
        self.enterNickname.insert(0, self.listNicknames.get(ACTIVE))
