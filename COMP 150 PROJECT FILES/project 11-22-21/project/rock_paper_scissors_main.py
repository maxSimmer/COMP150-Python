# =======================================================================
# COMP 150 Project
# Authors:
# Last Modified: 11/9/2021
# =======================================================================
# Imported Libraries
from graphics import *
import time
import simpleaudio
import random

# =======================================================================
# Global Variables
win = GraphWin("Rock Paper Scissors", 1200, 800)
win.setBackground("light blue")

# Image objects for choices
rock = Image(Point(200, 350), "COMP IMAGES/ROCK.png")
paper = Image(Point(600, 350), "COMP IMAGES/PAPER.png")
scissors = Image(Point(1000, 350), "COMP IMAGES/SCISSORS.png")

rock2 = Image(Point(200, 350), "COMP IMAGES/ROCK2.png")
paper2 = Image(Point(200, 350), "COMP IMAGES/PAPER2.png")
scissors2 = Image(Point(200, 350), "COMP IMAGES/SCISSORS2.png")

rock3 = Image(Point(1000, 350), "COMP IMAGES/ROCK3.png")
paper3 = Image(Point(1000, 350), "COMP IMAGES/PAPER3.png")
scissors3 = Image(Point(1000, 350), "COMP IMAGES/SCISSORS3.png")

# Box objects for menu
leftBox = Rectangle(Point(80, 450), Point(320, 600))
leftBox.setFill("light green")
middleBox = Rectangle(Point(480, 450), Point(720, 600))
middleBox.setFill("light green")
rightBox = Rectangle(Point(880, 450), Point(1120, 600))
rightBox.setFill("light green")

# Text objects for boxes
bestOfOne = Text(Point(200, 525), "Best of one")
bestOfOne.setSize(30)
bestOfOne.setFace("arial")
bestOfThree = Text(Point(600, 525), "Best of three")
bestOfThree.setSize(30)
bestOfThree.setFace("arial")
bestOfFive = Text(Point(1000, 525), "Best of five")
bestOfFive.setSize(30)
bestOfFive.setFace("arial")

versus = Text(Point(600, 400), "V.S.")
versus.setFace("arial")
versus.setSize(36)

robotNum = random.randrange(1, 4)
playerScore = 0
robotScore = 0
playerPick = 0
playerGameType = 0


# =======================================================================
# Body
def playersPickGameType(mouseClick):
    """Click detection for what game type you choose."""
    if 80 < mouseClick.getX() < 320 and 450 < mouseClick.getY() < 600:
        return 1
    elif 480 < mouseClick.getX() < 720 and 450 < mouseClick.getY() < 600:
        return 2
    elif 880 < mouseClick.getX() < 1120 and 450 < mouseClick.getY() < 600:
        return 3


def playersPickRPS(mouseClick):
    """Click detection for what the player picks."""
    if 100 < mouseClick.getX() < 300 and 259 < mouseClick.getY() < 441:
        return 1
    elif 479 < mouseClick.getX() < 721 and 252 < mouseClick.getY() < 448:
        return 2
    elif 882 < mouseClick.getX() < 1118 and 248 < mouseClick.getY() < 452:
        return 3


def determineRobotNumber(randomPick):
    """Accepts random numbers to evaluate what image to display."""
    if randomPick == 1:
        rock3.draw(win)
    if randomPick == 2:
        paper3.draw(win)
    if randomPick == 3:
        scissors3.draw(win)


def countDown():
    """Countdown animation before reveal."""
    countDown = Text(Point(600, 400), "3")
    countDown.setFace("arial")
    countDown.setSize(36)
    for i in reversed(range(0, 3)):
        countDown.draw(win)
        time.sleep(1)
        countDown.undraw()
        countDown.setText(str(i))
    shoot = Text(Point(600, 400), "Shoot!")
    shoot.setFace("arial")
    shoot.setSize(36)
    shoot.draw(win)
    time.sleep(1)
    shoot.undraw()
    countDown.undraw()


def drawChoices():
    """Draws the choice images."""
    rock.draw(win)
    paper.draw(win)
    scissors.draw(win)


def undrawChoices():
    """Undraws the choice images."""
    rock.undraw()
    paper.undraw()
    scissors.undraw()


def undrawChoices2():
    """Undraws the choice images."""
    rock2.undraw()
    paper2.undraw()
    scissors2.undraw()


def undrawChoices3():
    """Undraws the choice images."""
    rock3.undraw()
    paper3.undraw()
    scissors3.undraw()


def drawPickBoxes():
    """Draws the boxes that are clickable."""
    leftBox.draw(win)
    bestOfOne.draw(win)
    middleBox.draw(win)
    bestOfThree.draw(win)
    rightBox.draw(win)
    bestOfFive.draw(win)


def undrawPickBoxes():
    """Undraws the boxes that are clickable."""
    leftBox.undraw()
    bestOfOne.undraw()
    middleBox.undraw()
    bestOfThree.undraw()
    rightBox.undraw()
    bestOfFive.undraw()


def battleScreenFunction():
    """Determines the game type and computes if win/lose/tie in the versus screen."""
    global playerScore, robotScore
    if playerPick == 1:
        rock.undraw()
        rock.draw(win)
        versus.draw(win)
        if robotNum == 1:
            pass
        if robotNum == 2:
            robotScore += 1
        if robotNum == 3:
            playerScore += 1
    elif playerPick == 2:
        paper2.undraw()
        paper2.draw(win)
        versus.draw(win)
        if robotNum == 1:
            playerScore += 1
        if robotNum == 2:
            pass
        if robotNum == 3:
            robotScore += 1
    elif playerPick == 3:
        scissors2.undraw()
        scissors2.draw(win)
        versus.draw(win)
        if robotNum == 1:
            robotScore += 1
        if robotNum == 2:
            playerScore += 1
        if robotNum == 3:
            pass


def robotNumber():
    """Robot pick randomizer."""
    global robotNum
    robotNum = random.randrange(1, 4)


# ========================================================================
# Main
def main():
    global robotNum, playerScore, robotScore, playerPick
    drawPickBoxes()
    while not win.closed:
        playerGameType = playersPickGameType(win.getMouse())
        if playerGameType == 1:
            undrawPickBoxes()
            drawChoices()
            playerPick = playersPickRPS(win.getMouse())
            undrawChoices()
            countDown()
            determineRobotNumber(robotNum)
            battleScreenFunction()
            break
        elif playerGameType == 2:
            undrawPickBoxes()
            while playerScore != 2:
                undrawChoices()
                undrawChoices2()
                undrawChoices3()
                drawChoices()
                playerPick = playersPickRPS(win.getMouse())
                undrawChoices()
                countDown()
                determineRobotNumber(robotNum)
                battleScreenFunction()
                win.getMouse()
                robotNumber()
                versus.undraw()
                if robotScore == 2:
                    break

        elif playerGameType == 3:
            undrawPickBoxes()
            while playerScore != 3:
                undrawChoices()
                undrawChoices2()
                undrawChoices3()
                drawChoices()
                playerPick = playersPickRPS(win.getMouse())
                undrawChoices()
                countDown()
                determineRobotNumber(robotNum)
                battleScreenFunction()
                win.getMouse()
                robotNumber()
                versus.undraw()
                if robotScore == 3:
                    break

        undrawChoices2()
        undrawChoices3()
        undrawChoices()
        if playerScore > robotScore:
            print("player wins")
        else:
            print("player loses")


# ========================================================================
main()