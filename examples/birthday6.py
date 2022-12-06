from graphics import *

def userInput():
    x = float(input("Enter an integer: "))
    if x > 3:
        pass
    elif x < 3:
        exit()


def main():

    userInput()

    win = GraphWin("Maxes Test Game", 800, 800)
    win.setBackground('white')

    win.getMouse()
    win.close()

main()



