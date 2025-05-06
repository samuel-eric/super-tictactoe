from window import Window
from tictactoe import MacroBoard

def main():
    win = Window()
    board = MacroBoard(win)
    board.draw()
    win.loop()

if __name__ == "__main__":
    main()