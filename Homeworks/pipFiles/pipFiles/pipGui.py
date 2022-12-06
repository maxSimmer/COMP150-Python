#!/usr/bin/env python3
"""
GUI interface to the Pip simulator
By Nilanjan Podder and Andy Harrington

Start and click on help twice for more description.
See also the doc string for pip.py.
"""

import sys

from graphics import *  # Zelle's graphics module
from pipText import * # text driver for Pip.  Much output gets rerouted to GUI
from pipHelp import * # handles help windows
from pip import MAX_CODE, DATA_START, MEM_LEN, MAX_DATA

cpu = None  # only one created -- same as in pipText

commands=["QUIT", "UPDATE", "HELP", "NONE", "CODE", "DATA", "ALL", "BINARY",
          "STEP", "RUN", "INIT", "SAVE","LOAD"]

def initGUI():
    '''Initialize the graphical user interface.'''
    global awin # graphics window
    global msgRect
    global errmessage # main message
    global errNewness # old/new label
    global ac  # Entry for Accum
    global ipc # IP Entry
    global buttlist # list of button rectangles
    global fname # filename Entry
    global runsteps # Run Steps Entry
    global codeLabelBoxes # boxes around mem labels
    global codeLabels # individual mem label Entries 
    global dataVals # individual data values
    global dataLabels # labels for individual data values
    global codeVals # individual memory values - not init
    global moreCodeRect # heading of code - click here to lengthen code window

    global MAIN_RECT_TOP, CODE_DATA_MARGIN, ENTRY_DY, NUM_FROM_LT
    global LABELS_FROM_LT, LABEL_WIDE, LABEL_HIGH, LAB_BACK, LAB_HIGHLIGHT

    global lastHighlightedAddr # remember last address with highlight as IP

    # paramteres for code and data rect items 
    CODE_DATA_MARGIN = 15 #30
    ENTRY_DY = 25 #30
    NUM_FROM_LT = 18
    LABELS_FROM_LT = NUM_FROM_LT + 70 #64

    CODE_FROM_LT = LABELS_FROM_LT + 133 #127
    DAT_FROM_LT = LABELS_FROM_LT + 93 #87

    LABEL_WIDE = 80
    LABEL_HIGH = 22
    
    # parameters for main rectangles
    ABOVE_MAIN_SEP = 1 #5
    BELOW_MAIN_SEP = ABOVE_MAIN_SEP

    LOW_RECT_BOT = ABOVE_MAIN_SEP
    LOW_RECT_HIGH = 70
    LOW_RECT_TOP = LOW_RECT_HIGH + LOW_RECT_BOT  
    MAIN_RECT_BOT = LOW_RECT_TOP + BELOW_MAIN_SEP
    MAIN_RECT_HIGH = max(490, 5 + ENTRY_DY * max(MAX_CODE, MAX_DATA))

    MAIN_RECT_TOP = MAIN_RECT_HIGH + MAIN_RECT_BOT 
    HEAD_BOT = MAIN_RECT_TOP + ABOVE_MAIN_SEP 
    HEAD_HIGH = 28 #40
    HEAD_TOP = HEAD_BOT + HEAD_HIGH 
    WIN_TOP = HEAD_TOP + ABOVE_MAIN_SEP
    RECT_SEP_WIDE = 5
    CMD_RECT_LT = 10
    CMD_RECT_WIDE = 160
    CMD_RECT_RT = CMD_RECT_LT + CMD_RECT_WIDE 
    MEM_RECT_LT = CMD_RECT_RT + RECT_SEP_WIDE 
    MEM_RECT_WIDE = 300
    MEM_RECT_RT = MEM_RECT_LT + MEM_RECT_WIDE 
    DAT_RECT_LT = MEM_RECT_RT + RECT_SEP_WIDE 
    DAT_RECT_WIDE = 230
    DAT_RECT_RT = DAT_RECT_LT + DAT_RECT_WIDE
    WIN_WIDTH = DAT_RECT_RT + RECT_SEP_WIDE

    CODE_ENTRY_WIDTH = 17
    DATA_ENTRY_WIDTH = 8

    MSG_WIDE = DAT_RECT_RT - MEM_RECT_LT
    
    # button position parameters
    BUT_WIDE = 70
    BUT_LT = CMD_RECT_LT + (CMD_RECT_WIDE - BUT_WIDE)//2
    BUT_RT = BUT_LT + BUT_WIDE
    RUN_ENTRY_X = BUT_RT + 20
    BUT_HIGH = 23
    BUT_SEP = 9
    BUT_DY = BUT_SEP + BUT_HIGH 

    # parameters for other items in the cmd rect
    FILE_NAME_LABEL_DY = 20
    FILE_NAME_LABEL_XMID = CMD_RECT_LT + 43
    FILE_NAME_ENTRY_DY = 35
    
    LINE_GAP = 15
    LINE_LT = CMD_RECT_LT + LINE_GAP
    LINE_RT = CMD_RECT_RT - LINE_GAP
    
    # background colors    
    CMD_BACK = 'green'
    MEM_BACK = 'blue'
    MORE_CODE_BACK = 'lightblue'
    DAT_BACK = 'yellow'
    CPU_BACK = 'orange'
    MSG_BACK = 'red'
    BUT_BACK = 'magenta'    
    LAB_BACK = 'pink'
    LAB_HIGHLIGHT = 'orange'
        
    awin = GraphWin("PIP SIMULATOR in PYTHON", WIN_WIDTH,WIN_TOP)
    awin.setBackground("black")
    awin.setCoords(0,0, WIN_WIDTH, WIN_TOP)
    cmdRect = makeRect(CMD_RECT_LT,MAIN_RECT_BOT,CMD_RECT_WIDE,MAIN_RECT_HIGH,
                       CMD_BACK,awin) 
    memRect = makeRect(MEM_RECT_LT,MAIN_RECT_BOT,MEM_RECT_WIDE,MAIN_RECT_HIGH,
                       MEM_BACK, awin) 
    datRect = makeRect(DAT_RECT_LT,MAIN_RECT_BOT,DAT_RECT_WIDE,MAIN_RECT_HIGH,
                       DAT_BACK, awin) 
    cmdHeadRect = makeRect(CMD_RECT_LT,HEAD_BOT,CMD_RECT_WIDE,HEAD_HIGH,
                           CMD_BACK,awin) 
    memHeadRect = makeRect(MEM_RECT_LT,HEAD_BOT,MEM_RECT_WIDE,HEAD_HIGH,
                           MEM_BACK ,awin) 
    datHeadRect = makeRect(DAT_RECT_LT,HEAD_BOT,DAT_RECT_WIDE,HEAD_HIGH,
                           DAT_BACK ,awin) 
    moreCodeRect = makeRect(MEM_RECT_LT+2,HEAD_BOT+2,45,HEAD_HIGH-4,
                           MORE_CODE_BACK ,awin) 

    centerText(moreCodeRect,"+ line", awin)
    centerText(cmdHeadRect,"COMMANDS", awin)
    centerText(memHeadRect,"CODE", awin)
    centerText(datHeadRect,"DATA", awin)

    
    cpuRect = makeRect(CMD_RECT_LT, LOW_RECT_BOT, CMD_RECT_WIDE, LOW_RECT_HIGH,
                       CPU_BACK, awin)  
    Text(Point(CMD_RECT_LT + 25,cpuRect.getCenter().getY()),"CPU:").draw(awin) 
    Text(Point(CMD_RECT_LT + 50,topHalf(cpuRect)),"ACC:").draw(awin)
    Text(Point(CMD_RECT_LT + 60,bottomHalf(cpuRect)),"IP:").draw(awin)
    ac = Entry(Point(CMD_RECT_LT + 110,topHalf(cpuRect)), 8) #accumulator Entry
    ipc=Entry(Point(CMD_RECT_LT + 110,bottomHalf(cpuRect)), 8) # IP Entry
    ac.draw(awin)
    ipc.draw(awin)
    
    msgRect = makeRect(MEM_RECT_LT, LOW_RECT_BOT, MSG_WIDE, LOW_RECT_HIGH, 
                       MSG_BACK, awin)

    errmessage=Text(Point(msgRect.getCenter().getX(),bottomHalf(msgRect)+10),"")
    errmessage.draw(awin)
    errNewness=Text(Point(msgRect.getCenter().getX(), topHalf(msgRect)+ 5),"")
    errNewness.draw(awin)

    # draw contents of CMD rectangle
    buttlist=[]
    cmdXMid = cmdRect.getCenter().getX()
    centering = max(0, ENTRY_DY * (MAX_CODE - 19)//2)
    y= MAIN_RECT_BOT + BUT_SEP + BUT_HIGH//2 + centering
    for label in commands:
         buttlist.append(makeButton(cmdXMid, y, BUT_WIDE, BUT_HIGH, label,
                         BUT_BACK, awin))
         if label=="RUN":
             #creating the entry for no of steps
             runsteps = Entry(Point(RUN_ENTRY_X, y), 2)
             runsteps.draw(awin)
         if label in ['SAVE', 'STEP', 'NONE']:
             h = y - BUT_DY//2
             Line(Point(LINE_LT, h),Point(LINE_RT, h)).draw(awin)
         y += BUT_DY         
         if label=="BINARY":
             labelnametext=Text(Point(cmdXMid,y - 10),"LABELS:")
             labelnametext.setSize(10)
             labelnametext.draw(awin)
             y=y+25

    y -= 2 # tighter at top
    fname=Entry(Point(cmdXMid,y), 15)
    fname.draw(awin)

    y += (BUT_HIGH + FILE_NAME_LABEL_DY)//2
    fnameLabel=Text(Point(FILE_NAME_LABEL_XMID,y),"FILENAME:")
    fnameLabel.setSize(10)
    fnameLabel.draw(awin)

    [codeLabels, codeVals, codeLabelBoxes] = \
       setEntries(list(range(0, 2*MAX_CODE, 2)), CODE_ENTRY_WIDTH,
                  MEM_RECT_LT, CODE_FROM_LT)                 
    [dataLabels, dataVals, junk] = \
       setEntries(list(range(DATA_START, MEM_LEN)), DATA_ENTRY_WIDTH,
                  DAT_RECT_LT, DAT_FROM_LT) 
                
    lastHighlightedAddr = None # remember last address with highlight as IP
    allToGUI()        

def centerText(rect, text, win):
    """center text in the middle of the rectangle rect."""
    Text(rect.getCenter(), text).draw(win)

def bottomHalf(rect):
    """ returns y coord half way between P1 and center."""
    return (rect.getP1().getY() + rect.getCenter().getY())//2

def topHalf(rect):
    """ returns y coord half way between P2 and center."""
    return (rect.getP2().getY() + rect.getCenter().getY())//2

def setEntries(addrList, entryLen, xBase, entryOffs): 
    """return [labels, entries, boxes] for code or data display."""
    y = MAIN_RECT_TOP - CODE_DATA_MARGIN    
    numX = xBase + NUM_FROM_LT
    labelX = xBase + LABELS_FROM_LT
    entryX = xBase + entryOffs
    boxes=[]
    labels=[]
    entries=[]
    for addr in addrList:
        Text(Point(numX,y),str(addr)).draw(awin)
        box = centerRect(labelX,y, LABEL_WIDE,LABEL_HIGH,LAB_BACK,awin)
        boxes.append(box)
        labels.append(Text(Point(labelX,y),""))
        labels[-1].draw(awin)
        entries.append(Entry(Point(entryX,y), entryLen))
        entries[-1].draw(awin)
        y -= ENTRY_DY
    return [labels, entries, boxes]
 
def mainGUI(args = None):
    """Main GUI program.  Accepts a source filename parameter."""
    global cpu
    
    cpu = createCPU(args)
    setMakeErr(displayError) # errors to GUI
    setShowAll(False) # display individual log entries to shell window
    initGUI()
    show()
    errmessage.setText('Click Help twice if you are new to this simulator' +
                '\nSee the Shell window for a step-by-step execution history.');
    interact()
    awin.close()

def updateEntry(entry, s):
    if entry.getText() != s:
        entry.setText(s)
    
def allToGUI():
    """Update entire GUI from CPU."""
    for i in range(*cpu.dataLims):
        updateEntry(dataVals[i-DATA_START], cpu.dataStr(i))
    for i in range(MAX_DATA):
        updateEntry(dataLabels[i], cpu.labelStr(DATA_START+i)+":")
    for i in range(0, MAX_CODE):
        updateEntry(codeVals[i], cpu.codeStr(i*2))
    for i in range(0, MAX_CODE):
        updateEntry(codeLabels[i], cpu.labelStr(2*i)+":")
    cpuToGUI()

def cpuToGUI():
    """ Update GUI CPU section from simulator CPU."""
    updateEntry(ac, cpu.accStr())
    updateEntry(ipc, cpu.ip)
    updateIPHighlight()

def updateIPHighlight():
    """Keep current IP address line highlighted in GUI."""
    global lastHighlightedAddr
    if cpu.ip != lastHighlightedAddr:
        if lastHighlightedAddr != None:
            codeLabelBoxes[lastHighlightedAddr//2].setFill(LAB_BACK)            
        if cpu.ip != None:
            codeLabelBoxes[cpu.ip//2].setFill(LAB_HIGHLIGHT)            
        lastHighlightedAddr = cpu.ip    

def lengthenWindow():
    global MAX_CODE
    awin.close()
    MAX_CODE = cpu.incMaxCode()
    cpu.initCPU()
    initGUI()
    
                   
def getCmd():
    '''Wait for a mouseclick and return a location string.'''
    pt=awin.getMouse()
    for (i, rect) in enumerate(buttlist):
        if inside(rect,pt):
           return commands[i]
    if inside(msgRect, pt):
       return "CLEAR_MSG"
    if inside(moreCodeRect, pt):
        return "ADD_LINE"
    return "Nowhere"
      
def GUIToCPU():
    """Copy all of GUI to CPU and return False, or stop on first error and 
    return True.
    """
    acval=ac.getText()
    if acval!=cpu.accStr():
        if accum([acval]):    
           return True

    ipval=ipc.getText()
    if ipval!=cpu.ipStr():
        if ip([ipval]):
            return True
        updateIPHighlight()

    for i in range(DATA_START,MEM_LEN):
        datavalue=dataVals[i-DATA_START].getText()
        if cpu.dataStr(i)!=datavalue and editMem([str(i), datavalue]):
            return True

    for i in range(MAX_CODE):
        memoryvalue=""
        memvalue= codeVals[i].getText()
        memva=cpu.codeStr(2*i) 
        if  memvalue!=memva and editMem([str(2*i), memvalue]):
           return True
    return False

def interact():
    """Loop through all button presses until QUIT."""
    helpMode = False
    while True:
        cmd = getCmd()
        if helpMode:
            initHelp(cmd)
            helpMode = False
            displayError("  ")
            continue
        if cmd == "CLEAR_MSG":
            displayError("  ")
        elif errNewness.getText() == "New Error:":
            errNewness.setText("Old Error:")
        if cmd == "LOAD":
            load([fname.getText()])
            allToGUI()
            continue
        if cmd == "INIT":
            init([])
            cpuToGUI()
        elif cmd == "HELP":
            helpMode = True
            displayError(
              "Click HELP again for a summary, or on a button for help about it" +
              "\nor in the blue area for an assembler summary.", False)
            continue
        elif cmd == "QUIT":
            closeHelp()
            return
        if GUIToCPU(): # skip remaining commands on GUI error  
           continue
        if cmd == "SAVE":
            save([fname.getText()])
            continue
        if cmd in ["STEP", "RUN"]:
            if cmd == "STEP":
                step()
            else:
                runCPU([runsteps.getText()])
            allToGUI()
            continue
        if cmd == "NONE":   
            setLabels(False, False)
        elif cmd == "CODE":   
            setLabels(False, True)
        elif cmd == "DATA":   
            setLabels(True, False)
        elif cmd == "ALL":   
            setLabels(True, True)
        elif cmd == "BINARY":
            binary([])
        allToGUI()
        if cmd == "ADD_LINE":
            lengthenWindow()



def makeRect(xLow, yLow, width, height,color, win):
    """Create in win and return a Rect, give smallest coordinates and size."""
    pane= Rectangle(Point(xLow,yLow),Point(xLow+width,yLow+height))
    pane.setFill(color)
    pane.draw(win)
    return pane

def centerRect(xCenter, yCenter, width, height,color, win):
    """Create in win and return a Rect."""
    return makeRect(xCenter-width//2,yCenter-height//2, width, height, color,
                    win)
    
def makeButton(xCenter, yCenter, width, height, label, color, win ):
    """Create in window win and return a Rect with a centered label."""  
    button= centerRect(xCenter, yCenter, width, height, color, win)
    centerText(button, label, win)
    return button

def between(val, end1, end2):
    """ Return True if val is between end1 and end2 or equals either."""
    return end1 <= val <= end2 or end2 <= val <= end1

def inside(rect,pt):
    """ Return True if Point pt is inside Rect rect. """
    p1 = rect.getP1()
    p2 = rect.getP2()
    return between(pt.getX(), p1.getX(), p2. getX()) and \
           between(pt.getY(), p1.getY(), p2. getY())
           
def displayError(err, isError = True):
    """ Function passed to pipText to display errors in the right place.
    Ignores None or empty string, clears error if blank err, 
    otherwise displays new error."""
    if err == None:
        return False
    err = str(err)
    if not err:
        return False
    if not err.strip() or not isError:
        errNewness.setText("")
    else:
        errNewness.setText("New Error:")
    errmessage.setText(err)
    return isError

if __name__ == "__main__":
    mainGUI(sys.argv[1:])
