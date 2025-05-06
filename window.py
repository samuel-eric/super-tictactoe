from tkinter import Tk, Canvas, BOTH

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Super Tic-Tac-Toe")
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)

    def loop(self):
        self.__root.mainloop()
