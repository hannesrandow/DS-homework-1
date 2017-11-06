from Tkinter import *
import tkMessageBox

LENGTH = 470
MARGIN = 10
WIDTH_ENTRIES = 1

class Gameplay:
    def __init__(self):
        self.root = Tk()
        self.canvasSudoku = Canvas(self.root, width=LENGTH, height=LENGTH)
        self.canvasSudoku.grid(row=0)
        self.draw_grid()
        self.frameScoreInput = Frame(self.root)
        self.frameScoreInput.grid(row=0, column=1, padx=10, pady=10)
        self.titleScore = Label(self.frameScoreInput, text="Scores:", font="Arial 12 bold")
        self.titleScore.pack()
        # TODO: receive names and scores from server
        scores = [("Me", 10), ("alpha", 5), ("beta", 7)]
        # list for updating the scores
        self.lblScores = []
        for score in scores:
            self.lblScore = Label(self.frameScoreInput, text=score[0] + ": " + str(score[1]))
            self.lblScores.append(self.lblScore)
            self.lblScore.pack()

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
        self.btnConfirmGuess = Button(self.frameInput, text="Guess", width=20, command=self.confirm_guess)
        self.btnConfirmGuess.grid(row=1, columnspan=6, pady=10)
        self.root.mainloop()
        tkMessageBox.showinfo("Game finished", "Winner is: ")

    def confirm_guess(self):
        # TODO: enter numbers in sudoku field
        self.root.destroy()

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

    def draw_grid(self):
        cellLength = (LENGTH - 2 * MARGIN) / 9
        for i in range(10):
            # blue lines for 3x3 fields
            color = "blue" if i%3 == 0 else "gray"
            x0 = MARGIN
            x1 = LENGTH - MARGIN
            y = MARGIN + i * cellLength
            # horizontal lines
            self.canvasSudoku.create_line(x0, y, x1, y, fill=color)
            # vertical lines
            self.canvasSudoku.create_line(y, x0, y, x1, fill=color)

Gameplay()
