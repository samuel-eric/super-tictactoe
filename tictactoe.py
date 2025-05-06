from tkinter import Button, Frame

class Microboard:
    def __init__(self, parent):
        self.frame = Frame(parent, borderwidth=1, relief='solid')
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.data = [[None for _ in range(3)] for _ in range(3)]

    def draw(self):
        for i in range(3):
            self.frame.rowconfigure(i, weight=1)
            for j in range(3):
                self.frame.columnconfigure(j, weight=1)
                button = Button(master=self.frame, text=self.data[i][j], font=('Arial', 14))
                button.grid(row=i, column=j, sticky='nsew')

class MacroBoard:
    def __init__(self, win):
        self.root = win.root
        self.outer_frame = Frame(self.root, borderwidth=4, relief='solid')
        self.outer_frame.grid(row=0, column=0, sticky="nsew")
        self.data = [[Microboard(self.outer_frame) for _ in range(3)] for _ in range(3)]

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