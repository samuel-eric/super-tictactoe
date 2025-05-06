from tkinter import Tk, Canvas, BOTH

class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Super Tic-Tac-Toe")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.minsize(800, 600)

    def loop(self):
        self.root.mainloop()
