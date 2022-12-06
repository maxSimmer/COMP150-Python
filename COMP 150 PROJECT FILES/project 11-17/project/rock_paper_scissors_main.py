# =======================================================================
# COMP 150 Project
# Authors:
# Last Modified: 11/9/2021
# =======================================================================
# Imported Libraries
from graphics import *
import time
#import simpleaudio
import random
# =======================================================================
# Global Variables
win = GraphWin("Rock Paper Scissors", 1200, 800)

rock = Image(Point(200, 350), "COMP IMAGES/ROCK.png")
paper = Image(Point(600, 350), "COMP IMAGES/PAPER.png")
scissors = Image(Point(1000, 350), "COMP IMAGES/SCISSORS.png")

colorBoxBlue = Rectangle(Point(80, 300), Point(320, 500))
colorBoxBlue.setFill("light blue")
colorBoxRed = Rectangle(Point(480, 300), Point(720, 500))
colorBoxRed.setFill("red")
colorBoxGreen = Rectangle(Point(880, 300), Point(1120, 500))
colorBoxGreen.setFill("light green")
# =======================================================================
# Body
def playersPickBackgroundColor(mouseClick):
    if 80 < mouseClick.getX() < 320 and 300 < mouseClick.getY() < 500:
        return "light blue"
    if 480 < mouseClick.getX() < 720 and 300 < mouseClick.getY() < 500:
        return "red"
    if 880 < mouseClick.getX() < 1120 and 300 < mouseClick.getY() < 500:
        return "light green"

def playersPickRPS(mouseClick):
    if 100 < mouseClick.getX() < 300 and 259 < mouseClick.getY() < 441:
        return 1

    elif 479 < mouseClick.getX() < 721 and 252 < mouseClick.getY() < 448:
        return 2

    elif 882 < mouseClick.getX() < 1118 and 248 < mouseClick.getY() < 452:
        return 3

def drawChoices():
    rock.draw(win)
    paper.draw(win)
    scissors.draw(win)

def undrawChoices():
    rock.undraw()
    paper.undraw()
    scissors.undraw()

def drawColorBoxes():
    colorBoxBlue.draw(win)
    colorBoxRed.draw(win)
    colorBoxGreen.draw(win)

def undrawColorBoxes():
    colorBoxBlue.undraw()
    colorBoxRed.undraw()
    colorBoxGreen.undraw()

def determineRobotNumber():
    True

def scoreboard():
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
#center vs image
    #versusImage = Image(Point(600, 100), "transtest2.png")
    #versusImage.draw(win)
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
# ========================================================================
# Main
def main():
    drawColorBoxes()
    while not win.closed:
        background = playersPickBackgroundColor(win.getMouse())
        if background == "light blue":
            win.setBackground(background)
        if background == "red":
            win.setBackground(background)
        if background == "light green":
            win.setBackground(background)
        undrawColorBoxes()
        drawChoices()
        scoreboard()



    playersPickRPS(win.getMouse())


# ========================================================================
main()