from graphics import *


def scoreboard():

    win = GraphWin("Rock Paper Scissors", 1200, 800)
    win.setBackground("light blue")
#screboard
    scoreboardBackground = Rectangle(Point(0, 0), Point(1200, 200))
    scoreboardBackground.setFill('orange')
    scoreboardBackground.setOutline('pink')
    scoreboardBackground.draw(win)

#center scoreboard
    vsCircle = Circle(Point(600, 100), 100)
    vsCircle.setFill('light blue')
    vsCircle.setOutline('purple')
    vsCircle.setWidth(5)
    vsCircle.draw(win)

    #scoreboardDivider = Line(Point(600, 0), Point(600, 200))
    #scoreboardDivider.setFill('purple')
    #scoreboardDivider.setWidth(5)
    #scoreboardDivider.draw(win)

#center vs image
    versusImage = Image(Point(600, 100), "transtest2.png")
    versusImage.draw(win)

#Player Score on scoreboard
    playerScore = Text(Point(300, 100), "Player Score: ")
    playerScore.setFill('black')
    playerScore.setSize(30)
    playerScore.setFace('arial')
    playerScore.draw(win)
#cpu score on scoreboard
    cpuScore = Text(Point(900, 100), "CPU Score: ")
    cpuScore.setFill('black')
    cpuScore.setSize(30)
    cpuScore.setFace('arial')
    cpuScore.draw(win)




    win.getMouse()
    win.close()

scoreboard()

