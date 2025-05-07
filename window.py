from tkinter import Tk, Canvas, BOTH, Frame

class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Super Tic-Tac-Toe")
        self.root.minsize(800, 600)

        # Status frame
        self.status_frame = Frame(self.root, height=100, bg='lightgray')
        self.status_frame.pack(side='bottom', fill='x')

        # Game board area (MacroBoard will go here)
        self.board_frame = Frame(self.root)
        self.board_frame.rowconfigure(0, weight=1)
        self.board_frame.columnconfigure(0, weight=1)
        self.board_frame.pack(fill='both', expand=True)

    def loop(self):
        self.root.mainloop()
