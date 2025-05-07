from window import Window
from tictactoe import TicTacToe

def main():
    win = Window()
    game = TicTacToe(win)
    game.draw()
    win.loop()

if __name__ == "__main__":
    main()