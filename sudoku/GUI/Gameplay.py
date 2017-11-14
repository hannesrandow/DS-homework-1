from Tkinter import *
import tkMessageBox
import time
import sudoku.common.protocol as protocol
from sudoku.client.game_update_link import GameUpdateLink

from sudoku.common import protocol


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
        self.gameUpdateLink = GameUpdateLink(self, current_session)
        self.gameUpdateLink.create(self.client.client_ip)

        print("wait up for other player..")
        while self.gameUpdateLink.latest_game.game_status == protocol._PENDING:
            time.sleep(0.1)
        print("let's begin!")

        # list for updating the scores
        self.varScores = []
        # Labels for scores (will just be updated during the game
        for player in self.current_session.current_players:
            self.varScore = StringVar()
            self.lblScore = Label(self.frameScoreInput, textvariable=self.varScore)
            self.varScore.set(player.nickname + ": " + str(player.score))
            self.varScores.append(self.varScore)
            self.lblScore.pack()

        self.btnLeaveSession = Button(self.frameScoreInput, text="Leave Game", width=20, command=self.leave_session)
        self.btnLeaveSession.pack(pady=100)
        # overwrite the method to close the window (x)
        self.root.protocol("WM_DELETE_WINDOW", self.leave_session)
        self.root.mainloop()

    def leave_session(self):
        '''
        called when user pushes close or leaving session button or when game is solved
        pronounces the winner if sudoku is solved or all except one left
        closes the update link and the client's socket and the window itself
        :return: None
        '''
        # in case the game is finished by solving the sudoku or all except one left
        if self.current_session.game_status == protocol._COMPLETED:
            scores = [player.score for player in self.current_session.current_players]
            winner = self.current_session.current_players[scores.index(max(scores))]
            print("tadaaaa")
            if winner.client_ip == self.client.sock.getsockname():
                tkMessageBox.showinfo("Game finished", "You win!")
            else:
                tkMessageBox.showinfo("Game finished", "Winner is: " + winner.nickname)

        print("asdasdjklajsdkjasldjaskldj")
        self.gameUpdateLink.destroy()
        self.client.sock.close()
        self.root.destroy()

    def draw_grid(self):
        '''
        draws the horizontal and vertical lines for the sudoku field
        :return: None
        '''
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
        '''
        draws the numbers of the current session
        :return: None
        '''
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
        '''
        updates row and column to show the clicked cell of the sudoku field
        :param event: reaction on a click within the canvas (sudoku field)
        :return: None
        '''
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
        '''
        draws a red rectangle to highlight the chosen cell
        :return: None
        '''
        self.canvasSudoku.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * CELL + 1
            y0 = MARGIN + self.row * CELL + 1
            x1 = MARGIN + (self.col + 1) * CELL - 1
            y1 = MARGIN + (self.row + 1) * CELL - 1
            self.canvasSudoku.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    def key_pressed(self, event):
        '''
        calls client's update method to send wished change to server (numbers 1 to 9)
        :param event: used to react on keyboard input
        :return:
        '''
        if self.row >= 0 and self.col >= 0 and event.char in "123456789":  # and event.char not in [37, 38, 39, 40]:
            # to be sure that it is a number (not an arrow key or sth similar)
            try:
                int(event.char)
                self.client.update(self, self.row, self.col, event.char, self.current_session)
            # Arrow keys and other keys are handled as numbers (try-except to avoid this)
            except:
                return

    def update_scores(self):
        '''
        updates the score labels with the current cores
        :return: None
        '''
        for idx, player in enumerate(self.current_session.current_players):
            self.varScores[idx].set(player.nickname + ": " + str(player.score))

    def update(self, updated_session):
        '''
        'public' method to be called from outside to refresh the GUI
        :param updated_session: current_session is exchanged by this
        :return: None
        '''
        self.current_session = updated_session
        # leave the game after sudoku is completely solved
        self.draw_numbers()
        self.update_scores()
        if self.current_session.game_status == protocol._COMPLETED: # self.current_session.game_solution:
            print "this is leaving brudi"
            self.leave_session()


