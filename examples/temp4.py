from graphics import *

def main():
    win = GraphWin()
    win.getMouse()
    win.Close()

    pt = Point(100, 50)
    pt.draw(win)

main()
