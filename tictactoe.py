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
        self.overlay_win = None
        self.winner = None
        self.disabled = False

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
            self.draw_overlay_win(self.winner)

    def draw_overlay_win(self, winner):
        if self.overlay_win:
            self.overlay_win.destroy()
        self.overlay_win = Canvas(self.frame, bg=self.frame.cget("bg"), highlightthickness=0)
        self.overlay_win.place(relx=0, rely=0, relwidth=1, relheight=1)
        def draw_text():
            width = self.overlay_win.winfo_width()
            height = self.overlay_win.winfo_height()
            self.overlay_win.create_text(
                width / 2,
                height / 2,
                text=winner,
                font=('Arial', 48, 'bold'),
                fill='red' if winner == "X" else 'blue',
                anchor='center'
            )
        self.overlay_win.after_idle(draw_text)

    def draw_active_board(self, active):
        border_color = 'yellow' if active else 'black'
        self.frame.config(highlightbackground=border_color, highlightcolor=border_color, highlightthickness=2)

        for row in self.data:
            for button in row:
                button.config(state="normal" if active and button['text'] == " " else "disabled")


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
            microboard.draw_overlay_win(self.game.macrodata[macro_i][macro_j])
        self.refresh_microboard_states()
        print(f"Clicked macro ({macro_i}, {macro_j}) → micro ({micro_i}, {micro_j})")

    def refresh_microboard_states(self):
        for i in range(3):
            for j in range(3):
                micro = self.data[i][j]
                if micro.winner is None:
                    is_active = (self.game.active_macro == (i, j)) or (self.game.active_macro == (None, None))
                    micro.draw_active_board(is_active)
                else:
                    micro.draw_active_board(False)


class Game:
    def __init__(self):
        self.microdata = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.macrodata = [[None for _ in range(3)] for _ in range(3)]
        self.turn = "O"
        self.winner = None
        self.active_macro = (None, None)

    def make_move(self, macro_i, macro_j, micro_i, micro_j):
        self.microdata[macro_i][macro_j][micro_i][micro_j] = self.turn
        self.check_result()
        next_macro_i, next_macro_j = micro_i, micro_j
        if self.macrodata[next_macro_i][next_macro_j] is not None or self.is_microboard_full(next_macro_i, next_macro_j):
            self.active_macro = (None, None)
        else:
            self.active_macro = (next_macro_i, next_macro_j)
        self.turn = "O" if self.turn == "X" else "X"

    def is_microboard_full(self, macro_i, macro_j):
        board = self.microdata[macro_i][macro_j]
        for row in board:
            for cell in row:
                if cell is None:
                    return False
        return True


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

