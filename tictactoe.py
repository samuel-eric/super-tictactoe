from tkinter import Button, Frame

class Microboard:
    def __init__(self, parent, macro_i, macro_j, handle_click):
        self.macro_i = macro_i
        self.macro_j = macro_j
        self.handle_click = handle_click
        self.frame = Frame(parent, borderwidth=1, relief='solid')
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.data = [[None for _ in range(3)] for _ in range(3)]

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

class MacroBoard:
    def __init__(self, win):
        self.root = win.root
        self.outer_frame = Frame(self.root, borderwidth=4, relief='solid')
        self.outer_frame.grid(row=0, column=0, sticky="nsew")
        self.data = [[Microboard(self.outer_frame, i, j, self.make_move) for j in range(3)] for i in range(3)]
        self.turn = "O"

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
            text=self.turn,
            state="disabled",
            disabledforeground="red" if self.turn == "X" else "blue"
        )
        self.turn = "O" if self.turn == "X" else "X"
        print(f"Clicked macro ({macro_i}, {macro_j}) → micro ({micro_i}, {micro_j})")
