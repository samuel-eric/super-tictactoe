from window import Window
from tictactoe import MacroBoard, Game

def main():
    win = Window()
    game = Game()
    board = MacroBoard(win, game)
    board.draw()
    win.loop()

if __name__ == "__main__":
    main()