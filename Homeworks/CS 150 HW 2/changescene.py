from graphics import *
def main():
    win = GraphWin('Make a box', 350, 350)
    win.yUp()
    win.setBackground('blue')
    msg = Text(Point(win.getWidth()/2, 30), 'Click on one point')
    msg.setTextColor('green')
    msg.setSize(20)
    msg.draw(win)

    win.getMouse()
    win.setBackground('yellow')

    win.getMouse()
    win.close()


main()


