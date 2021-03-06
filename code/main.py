import os
import sys
import TkGui as Gui
from tkinter import Tk


def main():
    print(f'{sys.version}')
    print(f'{os.getcwd()}')

    root = Tk()
    root.title("Antenna Matching")
    root.resizable(False, False)
    Gui.TkGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
