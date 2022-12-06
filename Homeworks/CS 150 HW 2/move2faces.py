from graphics import *
import time

def moveAll(shapeList, dx, dy):
    ''' Move all shapes in shapeList by (dx, dy).'''
    for shape in shapeList:
        shape.move(dx, dy)

def makeFace(center, win):
    '''display face centered at center in window win.
    Return a list of the shapes in the face.
    '''

    head = Circle(center, 25)
    head.setFill("black")
    head.draw(win)

    eye1Center = center.clone()  # face positions are relative to the center
    eye1Center.move(-10, 5)  # locate further points in relation to others
    eye1 = Circle(eye1Center, 5)
    eye1.setFill('blue')
    eye1.draw(win)

    eye2End1 = eye1Center.clone()
    eye2End1.move(15, 0)
    eye2End2 = eye2End1.clone()
    eye2End2.move(10, 0)

    eye2 = Line(eye2End1, eye2End2)
    eye2.setWidth(3)
    eye2.draw(win)

    mouthCorner1 = center.clone()
    mouthCorner1.move(-10, -10)
    mouthCorner2 = mouthCorner1.clone()
    mouthCorner2.move(20, -5)

    mouth = Oval(mouthCorner1, mouthCorner2)
    mouth.setFill("red")
    mouth.draw(win)

    return [head, eye1, eye2, mouth]

def main():
    win = GraphWin('Back n Forth', 300, 300)
    win.yUp()

    rect = Rectangle(Point(150, 40), Point(170, 60))
    rect.setFill('green')
    rect.draw(win)

    faceList = makeFace(Point(100, 100), win)
    faceList2 = makeFace(Point(100, 100), win)

    dx = 5
    dy = 3
    for i in range(100):
        moveAll(faceList, dx, dy)
        moveAll(faceList2, dx, dy)
        time.sleep(.5)

    win.promptClose(win.getwidth() / 2, 20)
    win.getMouse()
    win.close()

main()



