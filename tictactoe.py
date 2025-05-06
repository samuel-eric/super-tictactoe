from tkinter import Button, Frame, Canvas
from functools import reduce

class Microboard:
    def __init__(self, parent, macro_i, macro_j, handle_click):
        self.macro_i = macro_i
        self.macro_j = macro_j
        self.handle_click = handle_click
        self.frame = Frame(parent, borderwidth=1, relief='solid')
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.data = [[None for _ in range(3)] for _ in range(3)]
        self.canvas = None
        self.winner = None

    def draw(self):
        for i in range(3):
            self.frame.rowconfigure(i, weight=1)
            for j in range(3):
                self.frame.columnconfigure(j, weight=1)
                if self.data[i][j] is None:
                    button = Button(
                        master=self.frame,
                        text=" ",
                        font=('Arial', 20, "bold"),
                        width=4,
                        height=2,
                        command=lambda mi=i, mj=j: self.handle_click(self.macro_i, self.macro_j, mi, mj)
                    )
                    button.grid(row=i, column=j, sticky='nsew')
                    self.data[i][j] = button
        if self.winner:
            self.draw_overlay(self.winner)

    def draw_overlay(self, winner):
        if self.canvas:
            self.canvas.destroy()
        self.canvas = Canvas(self.frame, bg=self.frame.cget("bg"), highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        def draw_text():
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            self.canvas.create_text(
                width / 2,
                height / 2,
                text=winner,
                font=('Arial', 48, 'bold'),
                fill='red' if winner == "X" else 'blue',
                anchor='center'
            )
        self.canvas.after_idle(draw_text)

class MacroBoard:
    def __init__(self, win, game):
        self.root = win.root
        self.outer_frame = Frame(self.root, borderwidth=4, relief='solid')
        self.outer_frame.grid(row=0, column=0, sticky="nsew")
        self.data = [[Microboard(self.outer_frame, i, j, self.make_move) for j in range(3)] for i in range(3)]
        self.game = game

    def draw(self):
        for i in range(3):
            self.outer_frame.rowconfigure(i, weight=1, minsize=80)
            for j in range(3):
                self.outer_frame.columnconfigure(j, weight=1, minsize=80)
                micro = self.data[i][j]
                padx = (4, 1) if j == 0 else (1, 1) if j == 1 else (1, 4)
                pady = (4, 1) if i == 0 else (1, 1) if i == 1 else (1, 4)
                micro.frame.grid(row=i, column=j, padx=padx, pady=pady)
                micro.draw()

    def make_move(self, macro_i, macro_j, micro_i, micro_j):
        microboard = self.data[macro_i][macro_j]
        button = microboard.data[micro_i][micro_j]
        if button["state"] == "disabled":
            return
        button.config(
            text=self.game.turn,
            state="disabled",
            disabledforeground="red" if self.game.turn == "X" else "blue"
        )
        self.game.make_move(macro_i, macro_j, micro_i, micro_j)
        if self.game.macrodata[macro_i][macro_j] is not None:
            microboard.winner = self.game.macrodata[macro_i][macro_j]
            microboard.draw_overlay(self.game.macrodata[macro_i][macro_j])
        print(f"Clicked macro ({macro_i}, {macro_j}) → micro ({micro_i}, {micro_j})")

class Game:
    def __init__(self):
        self.microdata = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.macrodata = [[None for _ in range(3)] for _ in range(3)]
        self.turn = "O"
        self.winner = None

    def make_move(self, macro_i, macro_j, micro_i, micro_j):
        self.microdata[macro_i][macro_j][micro_i][micro_j] = self.turn
        self.check_result()
        self.turn = "O" if self.turn == "X" else "X"

    def check_result(self):
        for i in range(3):
            for j in range(3):
                microboard = self.microdata[i][j]
                self.check_microgame(microboard, i, j)
        self.check_macrogame(self.macrodata)

    def check_microgame(self, microboard, macro_i, macro_j):
        # Horizontal
        for i in range(3):
            row = microboard[i]
            if row[0] is not None and row[0] == row[1] == row[2]:
                self.macrodata[macro_i][macro_j] = row[0]
                return

        # Vertical
        for j in range(3):
            if microboard[0][j] is not None and microboard[0][j] == microboard[1][j] == microboard[2][j]:
                self.macrodata[macro_i][macro_j] = microboard[0][j]
                return

        # Diagonal TL-BR
        if microboard[0][0] is not None and microboard[0][0] == microboard[1][1] == microboard[2][2]:
            self.macrodata[macro_i][macro_j] = microboard[0][0]
            return

        # Diagonal TR-BL
        if microboard[0][2] is not None and microboard[0][2] == microboard[1][1] == microboard[2][0]:
            self.macrodata[macro_i][macro_j] = microboard[0][2]
            return

    def check_macrogame(self, macroboard):
        # Horizontal
        for i in range(3):
            row = macroboard[i]
            if row[0] is not None and row[0] == row[1] == row[2]:
                self.winner = row[0]
                return

        # Vertical
        for j in range(3):
            if macroboard[0][j] is not None and macroboard[0][j] == macroboard[1][j] == macroboard[2][j]:
                self.winner = macroboard[0][j]
                return

        # Diagonal TL-BR
        if macroboard[0][0] is not None and macroboard[0][0] == macroboard[1][1] == macroboard[2][2]:
            self.winner = macroboard[0][0]
            return

        # Diagonal TR-BL
        if macroboard[0][2] is not None and macroboard[0][2] == macroboard[1][1] == macroboard[2][0]:
            self.winner = macroboard[0][2]
            return

