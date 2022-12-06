"""
Help window of GUI interface to the Pip simulator
Andy Harrington
"""

from graphics import *
HELP_WIDTH = 680
HELP_HEIGHT = 550
helpWin = None

helpMap = {}
helpMap["Nowhere"] = """Pip Assember Summary
| Symbols Used                                                |
|   X for a symbolic or numeric data address.                 |
|   #N for a literal number N as data                         |
|   Acc refers to the accumulator                             |
|   L refers to a symbolic code label or numeric code address |
|                                                             |
| Instructions     Pseudo Python syntax for what happens      |
| Data Flow                                                   |
|   LOD X (or #N)  Acc = X  (or N)                            |
|   STO X          X = Acc (copy Acc to location X)           |
| Control                                                     |
|   JMP L          IP = L   (go to instruction L)             |
|   JMZ L          if Acc==0: IP = L else: IP = IP+2 (normal) |
|   NOP            No operation; just go to next instruction  |
|   HLT            Halt execution                             |
| Arithmetic-Logic                                            |
|   ADD X (or #N)  Acc = Acc + X  (or N)                      |
|   SUB X (or #N)  Acc = Acc - X  (or N)                      |
|   MUL X (or #N)  Acc = Acc * X  (or N)                      |
|   DIV X (or #N)  Acc = Acc / X  (or N)                      |
|   AND X (or #N)  if Acc != 0 and X != 0: Acc=1 else: Acc=0  |
|   NOT            if Acc == 0: Acc = 1 else: Acc = 0         |
|   CPZ X          if X == 0: Acc = 1 else: Acc = 0           |
|   CPL X          if X < 0: Acc = 1 else: Acc = 0            |
|                                                             |
| In source files:  An instruction may be preceded by a label |
| and a colon.  Any line may end with a comment.  A comment   |
| starts with ';' and extend to the end of the line.          |"""

nSummaryLines = helpMap["Nowhere"].count('\n') + 1

helpMap["QUIT"] = """Quit:  Terminate the program."""
helpMap["UPDATE"] = """Update:  Validate and record edits to text fields,
  including changes to code, memory data, the IP or Accumulator."""
helpMap["HELP"] = """Help: Click on a location for context sensative help."""
helpMap["NONE"] = \
        """None: Display no symbolic labels.  Only show numeric addresses."""
helpMap["CODE"] = \
        """Code: Display symbolic code labels and numeric data addresses."""
helpMap["DATA"] = \
        """Data: Display symbolic data labels and numeric code addresses."""
helpMap["ALL"] = """All: Display symbolic code and data labels."""
helpMap["BINARY"] ="""Binary:  display all data in binary.
  Click None, Code, Data or All to terminate binary display."""
helpMap["STEP"] ="""Step:  step through a single CPU instruction."""
helpMap["RUN"] ="""Run:  Run up to 100 CPU steps.
  A smaller numerical limit may be entered in the text box."""
helpMap["INIT"] ="Init:  Initialize IP and ACC to 0"
helpMap["SAVE"] ="""Save:  Save to a filename listed in the Filename text area.
  See LOAD for file formats."""
helpMap["LOAD"] = """Load:  Load a filename listed in the Filename text area.
  The following formats and extensions are allowed: ------------
     .asm -- an assembler text file with symbolic labels allowed
             Follow labels by ':'.  Comments start with ';'.
     .bin -- text groups of 8  0's and 1's, whitespace separated
     .dat -- the binary format of the  Analytical Engine applets"""
helpMap["CLEAR_MSG"] =  \
  """Bottom right red rectangle:  Error messages appear here.
  Clicking here clears any old message."""
helpMap["ADD_LINE"] =  \
  """Light blue '+ line' button above code:  Show another code line."""
helpMap["Intro"] = \
"""Click in the blue CODE area for an assember summary.\n"""
order = ["QUIT", "UPDATE", "HELP", "NONE", "CODE", "DATA", "ALL", "BINARY",
          "STEP", "RUN", "INIT", "SAVE","LOAD", "Intro"]
order.reverse()
order.append("CLEAR_MSG")
order.append("ADD_LINE")
allMsg = "\n".join([helpMap[cmd] for cmd in order])
allMsg = allMsg.splitlines()
allMsg = "\n".join(["| {} |".format(line.ljust(64)) for line in allMsg])

def initHelp(cmd):
    global helpWin
    closeHelp()
    if cmd == "HELP":
        lines = allMsg
    else:
        lines = helpMap[cmd]
    lines += "\n\nClick the top right red X button to close the Help Window."

    nLines = lines.count('\n') + 1
    # print nLines
    if cmd == "Nowhere":
        cmd = "Assembler Instructions"
    height = HELP_HEIGHT * (nLines + 2) // nSummaryLines
    helpWin = GraphWin("Help on {}".format(cmd), HELP_WIDTH, height)
    text = Text(Point(HELP_WIDTH//2, height//2), lines)
    text.setFace('courier')
    text.draw(helpWin)

def closeHelp():
    if helpWin and not helpWin.isClosed():
        helpWin.close()
