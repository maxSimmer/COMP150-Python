# =======================================================================
# COMP 150 Project
# Authors:
# Last Modified: 11/9/2021
# =======================================================================

# Imported Libraries
from graphics import *
import time
import random
import simpleaudio
# =======================================================================

# Global Variables
win = GraphWin("Rochambeau", 1200, 800)
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

# Image object for scoreboard
#scoreboard = Image(Point(win.getWidth()/2, 100), "COMP IMAGES/scoreboard.png")
#scoreboard2 = Image(Point(win.getWidth()/2, win.getHeight()/2), "COMP IMAGES/scoreboard2.png")

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

# Text objects for instructions
title = Text(Point(win.getWidth()/2, 150), "Welcome to Rochambeau!\n\n")
title.setSize(36)
title.setStyle("bold")
instructions = Text(Point(win.getWidth() / 2, 250), "The objective of the game is to win by selecting an object that beats the"
                                          "\n\n computer's selection. Rock beats scissors, scissors beats paper, \n\n"
                                          "and paper beats rock.")
instructions.setSize(25)
instructions2 = Text(Point(win.getWidth() / 2, 600), "Choose rock, paper, or scissors!")
instructions2.setSize(36)
clickPrompt = Text(Point(win.getWidth()/2, 500), "Click to begin the next round!")
clickPrompt.setSize(36)
userLabel = Text(Point(250, 150), "User")
userLabel.setSize(36)
compLabel = Text(Point(950, 150), "Computer")
compLabel.setSize(36)
userWins = Text(Point(win.getWidth()/2, 650), "User wins this round!")
compWins = Text(Point(win.getWidth()/2, 650), "Computer wins this round!")
draw = Text(Point(win.getWidth()/2, 650), "This round's a draw!")
clickToContinue = Text(Point(600, 625), "Click anywhere to continue")
clickToContinue.setSize(30)
clickToContinue.setFace("arial")
clickToContinue.setStyle("bold")

# Text objects for results screen
resultsTitle = Text(Point(win.getWidth()/2, 100), "Final Results")
resultsTitle.setStyle("bold")
resultsTitle.setSize(36)
versus = Text(Point(600, 400), "V.S.")
versus.setFace("arial")
versus.setSize(36)
playerScore = 0
robotScore = 0
playerPick = 0
playerGameType = 0

# Random number for opponent
robotNum = random.randrange(1, 4)

# Sounds
loseSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/lose_sound.wav")
drawSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/draw_sound.wav")
rockSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/rock_sound.wav")
paperSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/paper_sound.wav")
scissorsSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/scissors_sound.wav")
shootSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/shoot_sound.wav")
mouseClickSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/mouse_click.wav")
winSound = simpleaudio.WaveObject.from_wave_file("SOUNDS/win_sound.wav")

#screboard
scoreboardBackground = Rectangle(Point(325, 800), Point(875, 700))
scoreboardBackground.setFill('orange')
scoreboardBackground.setOutline('yellow')

#center scoreboard
vsCircle = Circle(Point(600, 725), 75)
vsCircle.setFill('light blue')
vsCircle.setOutline('purple')
vsCircle.setWidth(5)

#center vs image
versusImage = Image(Point(600, 725), "transparentvs.png")

#Player Score on scoreboard
p1score = Text(Point(425, 750), "User Score: ")
p1score.setFill('black')
p1score.setSize(18)
p1score.setFace('arial')

#cpu score on scoreboard
cpuScore = Text(Point(775, 750), "CPU Score: ")
cpuScore.setFill('black')
cpuScore.setSize(18)
cpuScore.setFace('arial')

#WELCOMETEXTBOX
welcomeBox = Rectangle(Point(0, 60), Point(1200, 125))
welcomeBox.setFill('light blue')
welcomeBox.setOutline('light green')
welcomeBox.setWidth(2)

#Mid Game Title
midgameTitle = Text(Point(win.getWidth()/2, 100), "Rochambeau!")
midgameTitle.setSize(36)
midgameTitle.setFace('arial')
midgameTitle.setFill('black')

# =======================================================================
# Body

def playersPickGameType(mouseClick):
    """Click detection for what game type you choose."""
    if 80 < mouseClick.getX() < 320 and 450 < mouseClick.getY() < 600:
        mouseClickSound.play()
        return 1
    elif 480 < mouseClick.getX() < 720 and 450 < mouseClick.getY() < 600:
        mouseClickSound.play()
        return 2
    elif 880 < mouseClick.getX() < 1120 and 450 < mouseClick.getY() < 600:
        mouseClickSound.play()
        return 3

def playersPickRPS(mouseClick):
    """Click detection for what the player picks."""
    if 100 < mouseClick.getX() < 300 and 259 < mouseClick.getY() < 441:
        mouseClickSound.play()
        return 1
    elif 479 < mouseClick.getX() < 721 and 252 < mouseClick.getY() < 448:
        mouseClickSound.play()
        return 2
    elif 882 < mouseClick.getX() < 1118 and 248 < mouseClick.getY() < 452:
        mouseClickSound.play()
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
    countDown.draw(win)
    rockSound.play()
    time.sleep(1)
    countDown.undraw()

    countDown = Text(Point(600, 400), "2")
    countDown.setFace("arial")
    countDown.setSize(36)
    countDown.draw(win)
    paperSound.play()
    time.sleep(1)
    countDown.undraw()

    countDown = Text(Point(600, 400), "1")
    countDown.setFace("arial")
    countDown.setSize(36)
    countDown.draw(win)
    scissorsSound.play()
    time.sleep(1)
    countDown.undraw()

    countDown = Text(Point(600, 400), "Shoot!")
    countDown.setFace("arial")
    countDown.setSize(36)
    countDown.draw(win)
    shootSound.play()
    time.sleep(1)
    countDown.undraw()

def drawInstructions():
    title.draw(win)
    instructions.draw(win)

def drawChoices():
    """Draws the choice images."""
    rock.draw(win)
    paper.draw(win)
    scissors.draw(win)

def drawPickBoxes():
    """Draws the boxes that are clickable."""
    leftBox.draw(win)
    bestOfOne.draw(win)
    middleBox.draw(win)
    bestOfThree.draw(win)
    rightBox.draw(win)
    bestOfFive.draw(win)

def drawLabels():
    """Draws labels for user and computer choices."""
    userLabel.draw(win)
    compLabel.draw(win)

def undrawInstructions():
    title.undraw()
    instructions.undraw()

def undrawChoices1():
    """Undraws the choice images."""
    rock.undraw()
    paper.undraw()
    scissors.undraw()

def undrawChoices3():
    """Undraws the choice images."""
    rock3.undraw()
    paper3.undraw()
    scissors3.undraw()

def undrawChoices2():
    """Undraws the choice images."""
    rock2.undraw()
    paper2.undraw()
    scissors2.undraw()

def undrawPickBoxes():
    """Undraws the boxes that are clickable."""
    leftBox.undraw()
    bestOfOne.undraw()
    middleBox.undraw()
    bestOfThree.undraw()
    rightBox.undraw()
    bestOfFive.undraw()

def undrawLabels():
    """Undraws labels for user and computer choices."""
    userLabel.undraw()
    compLabel.undraw()

def resultsScreen():
    """Clears screen and displays results screen."""
    undrawLabels()
    undrawChoices1()
    undrawChoices2()
    undrawChoices3()
    versus.undraw()
    resultsTitle.draw(win)

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

def drawWelcomeBox():
    welcomeBox.draw(win)

def undrawWelcomeBox():
    welcomeBox.undraw()

def drawScoreboard():
    scoreboardBackground.draw(win)
    vsCircle.draw(win)
    versusImage.draw(win)
    p1score.draw(win)
    cpuScore.draw(win)

def undrawScoreboards():
    scoreboardBackground.undraw()
    vsCircle.undraw()
    versusImage.undraw()
    p1score.undraw()
    cpuScore.undraw()

def drawmidgameTitle():
    midgameTitle.draw(win)

def undrawmidgameTitle():
    midgameTitle.undraw()

# ========================================================================
# Main

def main():
    global robotNum, playerScore, robotScore, playerPick
    drawWelcomeBox()
    drawInstructions()
    drawPickBoxes()
    playerGameType = playersPickGameType(win.getMouse())
    uWin = None
    while not win.closed:
        if playerGameType == 1:
            undrawWelcomeBox()
            undrawInstructions()
            undrawPickBoxes()
            instructions2.draw(win)
            drawmidgameTitle()
            drawChoices()
            drawScoreboard()
            userScore = Text(Point(510, 750), str(playerScore))
            userScore.setStyle("bold")
            userScore.setSize(25)
            compScore = Text(Point(850, 750), str(robotScore))
            compScore.setStyle("bold")
            compScore.setSize(25)
            userScore.draw(win)
            compScore.draw(win)
            playerPick = playersPickRPS(win.getMouse())
            instructions2.undraw()
            undrawChoices1()
            countDown()
            determineRobotNumber(robotNum)
            drawLabels()
            battleScreenFunction()
            clickToContinue.draw(win)
            win.getMouse()
            clickToContinue.undraw()
            undrawScoreboards()


        elif playerGameType == 2:
            undrawWelcomeBox()
            undrawInstructions()
            undrawPickBoxes()

            while playerScore != 2:
                instructions2.draw(win)
                undrawLabels()
                undrawChoices1()
                undrawChoices2()
                undrawChoices3()
                drawChoices()
                drawScoreboard()
                drawmidgameTitle()
                userScore = Text(Point(510, 750), str(playerScore))
                userScore.setStyle("bold")
                userScore.setSize(25)
                compScore = Text(Point(850, 750), str(robotScore))
                compScore.setStyle("bold")
                compScore.setSize(25)
                userScore.draw(win)
                compScore.draw(win)
                playerPick = playersPickRPS(win.getMouse())
                instructions2.undraw()
                undrawChoices1()
                versus.undraw()
                countDown()
                determineRobotNumber(robotNum)
                battleScreenFunction()
                drawLabels()
                clickPrompt.draw(win)
                robotNumber()
                win.getMouse()
                mouseClickSound.play()

                undrawmidgameTitle()
                undrawScoreboards()
                userScore.undraw()
                compScore.undraw()
                clickPrompt.undraw()

                if robotScore == 2:
                    clickPrompt.undraw()
                    break

        elif playerGameType == 3:
            undrawWelcomeBox()
            undrawInstructions()
            undrawPickBoxes()

            while playerScore != 3:
                instructions2.draw(win)
                undrawLabels()
                undrawChoices1()
                undrawChoices2()
                undrawChoices3()
                drawChoices()
                drawScoreboard()
                drawmidgameTitle()
                userScore = Text(Point(510, 750), str(playerScore))
                userScore.setStyle("bold")
                userScore.setSize(25)
                compScore = Text(Point(850, 750), str(robotScore))
                compScore.setStyle("bold")
                compScore.setSize(25)
                userScore.draw(win)
                compScore.draw(win)
                playerPick = playersPickRPS(win.getMouse())
                instructions2.undraw()
                undrawChoices1()
                versus.undraw()
                countDown()
                determineRobotNumber(robotNum)
                battleScreenFunction()
                drawLabels()
                clickPrompt.draw(win)
                robotNumber()
                win.getMouse()
                mouseClickSound.play()

                undrawmidgameTitle()
                undrawScoreboards()
                userScore.undraw()
                compScore.undraw()
                clickPrompt.undraw()
                if robotScore == 3:
                    break

        if playerScore > robotScore:
            finalmsg = "User wins!"
            uWin = True
        elif playerScore < robotScore:
            finalmsg = "User loses."
            uWin = False
        else:
            finalmsg = "Draw."

        results = Text(Point(win.getWidth()/2, 700), finalmsg)
        results.setSize(36)

        if uWin == True:
            winSound.play()
        elif uWin == False:
            loseSound.play()
        else:
            drawSound.play()

        resultsScreen()
        results.draw(win)

        undrawmidgameTitle()
        userScore.undraw()
        compScore.undraw()
        userFinal = Text(Point(528, 400), str(playerScore))
        userFinal.setStyle("bold")
        userFinal.setSize(30)
        compFinal = Text(Point(675, 400), str(robotScore))
        compFinal.setStyle("bold")
        compFinal.setSize(30)
        userFinal.draw(win)
        compFinal.draw(win)
        win.promptClose(win.getWidth()/2, 750)




# ========================================================================

main()