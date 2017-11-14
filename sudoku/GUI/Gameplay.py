from Tkinter import *
import tkMessageBox
import time
import sudoku.common.protocol as protocol
from sudoku.client.game_update_link import GameUpdateLink

LENGTH = 470
MARGIN = 10
WIDTH_ENTRIES = 1
CELL = (LENGTH - 2 * MARGIN) / 9

class Gameplay:
    def __init__(self, current_session, client):
        self.client = client
        self.root = Tk()
        self.row = 0
        self.col = 0
        self.current_session = current_session
        self.canvasSudoku = Canvas(self.root, width=LENGTH, height=LENGTH)
        self.canvasSudoku.grid(row=0)
        self.canvasSudoku.bind("<Button-1>", self.cell_clicked)
        self.canvasSudoku.bind("<Key>", self.key_pressed)
        self.draw_grid()
        self.draw_numbers()
        self.frameScoreInput = Frame(self.root)
        self.frameScoreInput.grid(row=0, column=1, padx=10, pady=10)
        self.titleScore = Label(self.frameScoreInput, text="Scores:", font="Arial 12 bold")
        self.titleScore.pack()
        # list for updating the scores
        self.varScores = []
        self.gameUpdateLink = GameUpdateLink(self, current_session)
        self.gameUpdateLink.create(client.name)

        while self.gameUpdateLink.latest_game.game_status == protocol._PENDING:
            print("wait up..")
            time.sleep(0.1)

        for player in self.current_session.current_players:
            self.varScore = StringVar()
            self.lblScore = Label(self.frameScoreInput, textvariable=self.varScore)
            self.varScore.set(player.nickname + ": " + str(player.score))
            self.varScores.append(self.varScore)
            self.lblScore.pack()

        # print("did you wait 10 secs?")

        '''
        # to allow just typing in 1 number in the entries
        self.rowValue = StringVar()
        self.rowValue.trace('w', self.limit_row_input)
        self.columnValue = StringVar()
        self.columnValue.trace('w', self.limit_column_input)
        self.valueValue = StringVar()
        self.valueValue.trace('w', self.limit_value_input)

        self.frameInput = Frame(self.frameScoreInput)
        self.frameInput.pack(pady=20)
        self.lblRow = Label(self.frameInput, text="Row: ")
        self.lblRow.grid(row=0)
        self.entryRow = Entry(self.frameInput, width=WIDTH_ENTRIES, textvariable=self.rowValue)
        self.entryRow.grid(row=0, column=1)
        self.lblColumn = Label(self.frameInput, text="Column: ")
        self.lblColumn.grid(row=0, column=2)
        self.entryColumn = Entry(self.frameInput, width=WIDTH_ENTRIES, textvariable=self.columnValue)
        self.entryColumn.grid(row=0, column=3)
        self.lblValue = Label(self.frameInput, text="Value: ")
        self.lblValue.grid(row=0, column=4)
        self.entryValue = Entry(self.frameInput, width=WIDTH_ENTRIES, textvariable=self.valueValue)
        self.entryValue.grid(row=0, column=5)
        self.btnLeaveSession = Button(self.frameScoreInput, text="Leave Game", width=20, command=self.leave_session)
        self.btnLeaveSession.pack(pady=100)
        '''
        self.btnLeaveSession = Button(self.frameScoreInput, text="Leave Game", width=20, command=self.leave_session)
        self.btnLeaveSession.pack(pady=100)
        self.root.mainloop()

        # TODO: pronounce the winner of the session
        tkMessageBox.showinfo("Game finished", "Winner is: ")

    def leave_session(self):
        # TODO: self.client.leave_session()
        self.root.destroy()

    '''
    def limit_row_input(self, *args):
        self.value = self.rowValue.get()
        if not self.value.isdigit() or self.value == 0:
            self.rowValue.set("")
        if len(self.value) > 1:
            self.rowValue.set(self.value[:1])

    def limit_column_input(self, *args):
        self.value = self.columnValue.get()
        if not self.value.isdigit() or self.value == 0:
            self.columnValue.set("")
        if len(self.value) > 1:
            self.columnValue.set(self.value[:1])

    def limit_value_input(self, *args):
        self.value = self.valueValue.get()
        if not self.value.isdigit() or self.value == 0:
            self.valueValue.set("")
        if len(self.value) > 1:
            self.valueValue.set(self.value[:1])
    '''

    def draw_grid(self):
        for i in range(10):
            # blue lines for 3x3 fields
            color = "blue" if i % 3 == 0 else "gray"
            x0 = MARGIN
            x1 = LENGTH - MARGIN
            y = MARGIN + i * CELL
            # horizontal lines
            self.canvasSudoku.create_line(x0, y, x1, y, fill=color)
            # vertical lines
            self.canvasSudoku.create_line(y, x0, y, x1, fill=color)

    def draw_numbers(self):
        self.canvasSudoku.delete("numbers")
        for i in range(9):
            for j in range(9):
                x = MARGIN + j * CELL + CELL / 2
                y = MARGIN + i * CELL + CELL / 2
                cellValue = str(self.current_session.game_state[i][j])
                color = "black"
                if self.current_session.game_state[i][j] != 0:
                    self.canvasSudoku.create_text(x, y, text=cellValue, font="Arial 12", tags="numbers", fill=color)

    def cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < LENGTH - MARGIN):
            self.canvasSudoku.focus_set()
        row, col = (y - MARGIN) / CELL, (x - MARGIN) / CELL
        # deselect cell if it was already selected
        if (row, col) == (self.row, self.col):
            self.row, self.col = -1, -1
        elif self.current_session.game_state[row][col] == 0:
            self.row, self.col = row, col
        self.draw_cursor()

    def draw_cursor(self):
        self.canvasSudoku.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * CELL + 1
            y0 = MARGIN + self.row * CELL + 1
            x1 = MARGIN + (self.col + 1) * CELL - 1
            y1 = MARGIN + (self.row + 1) * CELL - 1
            self.canvasSudoku.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    # calls client's update method to send wished change to server
    def key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and event.char in "123456789":  # and event.char not in [37, 38, 39, 40]:
            # to be sure that it is a number (not an arrow key or sth similar)
            try:
                int(event.char)
                self.client.update(self, self.row, self.col, event.char, self.current_session)
            except:
                return
            # self.current_session.game_state[self.row][self.col] = int(event.char)

    def update_scores(self):
        for idx, player in enumerate(self.current_session.current_players):
            self.varScores[idx].set(player.nickname + ": " + str(player.score))

    # 'public' method to be called from outside to refresh the GUI with updates
    def update(self, updated_session):
        self.current_session = updated_session
        # TODO: leave the game after sudoku is completely solved
        if self.current_session.game_state == self.current_session.game_solution:
            self.leave_session()
        self.draw_numbers()
        self.update_scores()

