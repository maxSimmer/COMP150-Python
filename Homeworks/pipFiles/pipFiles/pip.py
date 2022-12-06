""" This pip.py file contains the data model and some display components for
an assembler/disassembler and single step executor for the simulated
CPU used in the Pippin applet that comes with the Analytical Engine by
Decker and Hirshfield.  This version allows an extended assembler
allowing symbolic code labels as well as numeric address labels.  Also
the number of instructions displayed and tested may be increased.  In
this simulation, the CPU is nothing but a IP value and an Accumulator
value, with no reference to the fetch/execute cycle shown so
completely (and slowly!) in the Pippin applet.  In particular this version
can single step rapidly, or quickly generate a full execution log.

File formats:  Illegal files are not loaded.  An error message is given.
.dat:  Java binary format compatible with the Pippin applet, as long as 
       constants are left as CODE_MAX = 16, DATA_START = 128, MAX_DATA = 8.
.bin:  Text binary, may be shorter than full memory -- then, automatically,
       NOP's are added before address DATA_START, 0 after address DATA_START
.asm   Assembler lines with the form
       [<label>:] <op> [#][<operand>] [;<comment>]

The label may be symbolic or be the decimal string for the actual address.
Labels are restricted to 8 characters.

There are MAX_DATA data addresses, starting at DATA_START.
Earlier addresses are assumed to be code.  Programs start at IP 0.

Inside the program display format may be changed between all binary
and assembler.  Ther are further options to display only numberic code
labels, or see any symbolic labels.  Similarly for data labels and
operands.  

Files in any format can be loaded and then saved to another format.  Of
course symbolic information is lost going to binary or .dat format.  If
symbols are desired for display after a binary file is loaded, the Pippin
data symbols and purely numeric code labels are assumed.

If an assembler program uses the Pippin data symbols, then the corresponding
Pippin data addresses are assumed.  Otherwise the assembler just allocated
memory locations in order from DATA_START.

The Pip simulator maintains a log showing a history of IP, accumulator, and
all referenced data locations.

Included with this module are a text driver, pipText.py, and a GUI driver,
pipGui.py.  Both allow multiple forms of display, single stepping, or
executing a number of steps rapidly (! unlike the Pippin applet!).

"""

import os
import time
import traceback
import sys

import hexBin

mnem2c = {'ADD':0, 'SUB':1, 'MUL':2, 'DIV':3,
        'LOD' : 4, 'STO':5,
        'AND' : 8, 'NOT':9, 'CPZ':10, 'CPL':11,
        'JMP':12, 'JMZ':13, 'NOP':14, 'HLT':15}

mnems = list(mnem2c.keys())

c2mnem = hexBin.invertMap(mnem2c)

jmpOp = ['JMP', 'JMZ']
noByte2 = ['HLT', 'NOP', 'NOT']
noDataRef = jmpOp + noByte2
noDirect = noDataRef + ['STO', 'CPZ', 'CPL']

DAT = ".dat"
BIN = ".bin"
ASM = ".asm"

TOT_UNSIGNED = 256 
MIN_SIGNED = -TOT_UNSIGNED//2
MAX_SIGNED = TOT_UNSIGNED//2 - 1

# Constants below are set so Decker+Hirshfield applet .dat files make sense.
# If files are only used in asm or .bin format, the constants can be changed.
MAX_CODE_FOR_DAT_FILE = 16
DATA_START_FOR_DAT_FILE = 128
MAX_DATA_FOR_DAT_FILE = 8 

MAX_CODE = 19 # no longer MAX_CODE_FOR_DAT_FILE 
DATA_START = DATA_START_FOR_DAT_FILE
MAX_DATA = MAX_DATA_FOR_DAT_FILE
VARS = list('WXYZ') + ['T' + str(_i) for _i in range(1, MAX_DATA-3)]
# - - - - -

MEM_LEN = DATA_START + MAX_DATA
DATA_RANGE = (DATA_START, MEM_LEN)

numLabels = [str(_i) for _i in range(MEM_LEN)]
DAT_LABELS = numLabels[:DATA_START]+VARS

def mnem2code(mnem):
    '''Return code 0-15 for a mnemonic, or None if illegal.'''
    return mnem2c.get(mnem.upper(), None)
    
def code2mnem(intCode):
    '''Return a mnemonic, or None if intCode not in 0..15.'''
    return c2mnem.get(intCode, None)

def javaData(x):
    """Create apparent Java data file format, to match pip dat files."""
    if isinstance(x, str):
        x = x.encode()
    if isinstance(x, bytes):
        return javaData(len(x))[2:] + x
    if isinstance(x, int):
        s = b""  # 4 bytes, most significant first
        for i in range(4):
            s = bytes([x & 255]) + s
            x >>= 8
        return s
    raise Exception('Only can convert str, bytes, and int')

datStart = javaData('This is a legal state file') + javaData('CPUState')

def makeOpcode(mnem = 'NOP', direct = False):
    """Return int for opcode byte.
    """
    op = mnem2code(mnem)
    if op is None:
        raise Exception('Illegal mnemonic: ' + str(mnem))

    if direct:  
        if mnem in noDirect:
            raise Exception('Direct operand illegal for ' + mnem)
        op += 0x10
    return op

def machineCode(mnem = 'NOP', operand = 0, direct = False):
    """Return a list of two int bytes, opcode and operand, 0-255
    Accepts operand in range -128 to 127 if direct, otherwise 0 to 255
    Allow mem copied - so also allow -128 to 255 for direct data?
    """
    return [makeOpcode(mnem, direct), makePosByte(operand)]

def makePosByte(dat):
    """Force a byte value to be unsigned.
    Range -128 to 255 converted to 0 to 255.
    """
    if dat < 0:
        dat += TOT_UNSIGNED
    return dat
    
def makeSignedByte(dat):
    """Force a byte value to be signed.
    Range 0 to 255 converted to -128 to 127.
    """
    if dat > MAX_SIGNED:
        dat -= TOT_UNSIGNED
    return dat

def legalSignedByte(val):
    return MIN_SIGNED <= val <= MAX_SIGNED

def parseLines(s):
    """Returns a list of AssemblerLines or throw Exception
    """
    codes= []
    rawLine = 1
    addr = 0
    for line in s.splitlines():
       i = line.find(';')
       if i != -1:
           line = line[:i].strip()
       if line.strip():
           codes.append(AssemblerLine(line, rawLine, addr))
           addr += 2
       rawLine += 1
    return codes
  
def only01(s):
    '''True if all character 0, 1 or whitespace.'''
    for c in s:
        if not(c.isspace() or c in '01'):
            return False
    return True
    
def binEntryBytes(binStr):
    """Convert a sequence of whitespace separated tokens
    each containing no more than 8 0's and 1's to a list of bytes. 
    Raise Exception if illegal.
    """
    bytes = []
    for i, token in enumerate(binStr.split()):
        if len(token) > 8:
          raise Exception("Token {} is more than 8 bits: {}".format(i+1,token))
        bytes.append(int(token, 2))  # should be OK if only01(binStr) run first        
    return bytes

def binStr2Bytes(binStr):
    """Convert a sequence of whitespace separated tokens
    each containing no more than 8 0's and 1's to bytes in mem.
    Pad mem with nop's and 0's.
    Raise Exception if illegal.
    """
    return padMem(binEntryBytes(binStr))

def byte2bin(b):
    """Assume b is 0-255, return 8 char binary string."""
    return hexBin.nBitBin(b) 

def bytes2bin(mem, i):
    """ convert two bytes (mem[i], mem[i+1]) to binary bytes."""
    return byte2bin(mem[i]) + " " + byte2bin(mem[i+1]) 

def padMem(bytes):
    '''Return bytes padded to fill memory.'''
    if len(bytes) % 2 == 1:
        bytes += [0]
    bytes += max(0, (DATA_START - len(bytes))//2) * machineCode()
    pad = MEM_LEN - len(bytes)
    if pad < 0:
        raise Exception('Too many bytes by ' + str(-pad))
    bytes += [0]*pad
    return bytes

def legalMem(mem):
    '''Return an error or ''.  '''
    for i in range(0, DATA_START, 2):  # allow longer program than displays
        err = illegalOp(mem[i], mem[i+1])
        if err:
            return 'Address {}: {}'.format(i, err)
    return ''

def illegalOp(b1, b2):
    """Return "" or error description."""
    if not 0<=b1< 32:
        return "Illegal direct parameter nibble in {}.".format(byte2bin(b1))
    mnem = code2mnem(b1 % 16)
    if mnem is None:
        return "Illegal op code nibble in {}.".format(byte2bin(b1))
    direct = b1//16 == 1
    if direct and (mnem in noDirect):
        return "Op code {} does not allow direct operand".format(mnem)
    return checkB2(mnem, direct, b2)

def checkB2(mnem, direct, b2):
    '''Return '' or error description for illegal byte 2.'''
    if not 0<=b2<=255:
        return "Operand byte {} not in range.".format(b2)
    if (mnem in noByte2) and b2 != 0:
        return "Zero parameter required with {}".format(mnem)
    if not direct and b2 >= MEM_LEN: 
        return "Address byte is beyond the memory limit " + str(MEM_LEN-1)
    return ""
    
def mem2bin(mem):
    """ Return all of memory as binary string, two bytes per line for code,
    one for data (address DATA_START+)
    """
    bin = [bytes2bin(mem, i) for i in range(0, DATA_START, 2)]
    bin += [byte2bin(mem[i]) for i in range(*DATA_RANGE)]     
    return "\n".join(bin) 

# format:  two Java strings
# then 64 4-byte ints, each from 2 mem bytes, ( saving mem bytes 0-127)
# then 8 4-byte ints, each from one data byte (saving mem bytes 128-135)
def mem2dat(mem):
    """Return the .dat file format string."""
    if DATA_START != 128:
        raise Exception('Memory parameters inconsistent with .dat format!')
    code = [javaData(mem[i]*256 + mem[i+1])
            for i in range(0, 128, 2)]
    data = [javaData(mem[i]) for i in range(128, 136)]
    return datStart + b''.join(code + data)

def bytes2asm(mem, i, doPrint = False, labels = None):
    """Convert two bytes (mem[i], mem[i+1]) to assembler string
    with decimal operands if labels is None.
    If illegal op, leave two binary byte string, and if doPrint,
    print an error description.
    """
    b1 = mem[i]
    b2 = mem[i+1]
    err = illegalOp(b1, b2)
    if err:
        if doPrint:
            print("Address {}:  {}.".format(i, err))
        return bytes2bin(mem, i) 
    mnem = code2mnem(b1 % 16)
    direct = b1//16 == 1
    asm = mnem
    if not mnem in noByte2:
        asm += ' '
        param = str(b2)
        if direct:
            asm += '#'
            param = str(makeSignedByte(b2)) 
        elif labels:
            param = labels[b2]
        asm += param
    return asm

def useDataLabels(labels, dataLabels):
    '''Make data labels symbolic.'''
    labels[DATA_START:DATA_START + len(dataLabels)] = dataLabels

def bool2int(b):
    '''Make b boolean and then an integer.'''
    return int(bool(b))

def legalName(s):
    '''True if in legal identifier format.'''
    return s.replace('_','').isalnum() and not s[0].isdigit()

def elementsIn(seq1, seq2):
##    for e in seq1:       # for Python 2.4
##        if not e in seq2:
##            return False
##    return True
    return set(seq1).issubset(set(seq2))

def label2Addr(label, labels):
    """ Return int address associated with label or None.
    label is a string, either digits or symbolic.
    Array labels has labels for all addresses in mem.
    """
    if label.isdigit():
        return int(label)
    if label in labels:
        return labels.index(label)


class AssemblerLine:
    def __init__(self, line, lineNum, addr):
        """Parse assembler line and assemble as far as possible.
        If operand is a symbol, creation of operand byte is deferred.
        Parameters:
          line: string -- raw stripped, nonempty line without comment
          lineNum:  int -- for debugging, line in original file
                           or 0 if use addr
          addr:  int -- address where code goes (compare against any int label)

        Create fields:
          line: str -- original line
          lineNum: int -- original lineNum
          addr:  int -- memory address
          label: string -- nonnumeric label or empty string
          operand: string -- possibly a symbolic label initially
          b1: int -- opcode byte
          b2: int operand byte or None if not yet determined

        Checks for errors not requiring symbolic operand conversion.
        Throws descriptive exceptions including lineNum.
        If symbolic operand, later set b2 with convertOperandLabel.
        """
        self.line = line
        self.lineNum = lineNum
        self.addr = addr
        if lineNum > 0:
            locLabel = "Line {}: ".format(lineNum)
        else:
            locLabel = "Address {}: ".format(addr) 
        n = line.find(':')
        if n == -1:
            self.label = ""
        else:
            self.label = line[:n].strip()
            line = line[n+1:].strip()
            if not self.label:
                raise Exception("{}Empty line label".format(locLabel))
            if len(self.label) > 8:
                raise Exception("{}Label {} longer than 8"
                                .format(locLabel, self.label))
            if self.label.isdigit():
                sayAddr = int(self.label)
                if sayAddr != addr:
                    raise Exception(
                        "{}Expect address label {}, not {}"
                                    .format(locLabel, addr, sayAddr) )
                self.label = ""
            elif not legalName(self.label):
                raise Exception("{}Illegal address label {}"
                                .format(locLabel, self.label))
        tokens = line.split()
        if not tokens:
            raise Exception(locLabel + "No opcode")            
        mnem = tokens[0].upper()
        isDirect = False

        self.operand = '0'
        if len(tokens) > 1:
            if tokens[1].startswith('#'):
                isDirect = True
                tokens[1] = tokens[1][1:]
            self.operand = ' '.join(tokens[1:]).strip()

        if not mnem in mnems:
            raise Exception("{}Illegal mnemonic {}"
                            .format(locLabel, mnem))            
        if isDirect and (mnem in noDirect):
            raise Exception("{}Op code does not allow direct operand: {}"
                            .format(locLabel, mnem))

        self.b1 = makeOpcode(mnem, isDirect)
        self.b2 = None

        try:
            self.b2 = int(self.operand)
        except:
            pass
        if self.b2 == None:
            if not legalName(self.operand):
                raise Exception("{}Illegal identifier in operand: {}" 
                                .format(locLabel, self.operand))            
            if len(self.operand) > 8:
                raise Exception("{}Operand identifier is too long: {}" 
                                .format(locLabel, self.operand))
            if isDirect: 
                raise Exception("{}: Direct operand cannot be label: {}"
                                .format(locLabel, self.operand))
        elif isDirect:
            if not legalSignedByte(self.b2):
                raise Exception("{}Direct operand out of range: {}"
                                .format(locLabel, self.b2))
            self.b2 = makePosByte(self.b2)
        else:
            err = checkB2(mnem, isDirect, self.b2)
            if err:
                raise Exception(locLabel + err)
            
    def convertOperandLabel(self, labels):
        '''Convert all unset 2nd bytes to a label or None if fail.'''
        if self.b2 == None:
            self.b2 = label2Addr(self.operand, labels)
        
    def getCode(self):
        '''Return code as [b1, b2].'''
        return [self.b1, self.b2]
        
    #end of class AssemberLine
    
        
class Pip:
    """The state of the Pip simulated machine of Hirshfield.
    Contains state fields of the applet:
        ip: int  0-127 -- error if greater
        acc: int displayed signed or binary
        mem int[136] -- bytes of memory (but stored in int).
            Data stored as 0 to 255;
            data is interpret as signed

    Assume data all at addr >= DATA_START, code before

    fields for display:
        showAsm: bool (vs all binary)
        alphaLabels: string[MEM_LEN] -- containing all asm labels
        labels: string[MEM_LEN] -- containing current labels
                (maybe more numeric than alphaLabels)
        log: string[] -- headings for ip acc, dataAddr,
               special lines for halt, reset, dataAddr list change, edit 
        --- derived from mem, labels 
        dataAddr: int[] -- sorted list of referenced data addresses
        dataLims: None or (int, int)
        codeLim: int -- address where only nop's follow
        
       
    stepping uses the following fields for display:
        halted: bool -- true if halt instruction executed, needs reset
        lastIP: int or None -- IP of instruction just executed
       
    General editing OK if no symbolic labels.
    If in symbolic mode, dump labels for code or data if affected by:
       no address before or after
       same addr and same addr use, either code or data
    """
    
    def __init__(self, fileName = None, ):
        '''Create cleared CPU of take from a specifed file.'''
        self.showAsm = True
        self.clearAll()
        if fileName:
            try:
                self.loadFile(fileName)
                return
            except Exception as e:
                print("\n" + str(e))
        self.initCPU()

    def clearAll(self):
        '''Clear everything about memory and log.
        Assume AE applet data labels.
        '''
        self.mem = machineCode() * 64 + [0]* MAX_DATA
        self.initLabels()
        self.calcMemDerived()
        self.log = []
        self.lastLogHeading = ""    

    def initCPU(self, cause = ""):
        '''Clear CPU; set CPU ready to go from the start of memory.'''
        self.ip = 0
        self.acc = 0
        self.halted = False
        self.lastIP = None
        self.logEntry("------ CPU initialized {} ---------".format(cause), True)
        self.dataLims = DATA_RANGE

    def initLabels(self):
        """ initially assume match AE applet:
          decimal code labels,
          data at DATA_START: W, X, Y, Z, T1, T2, T3, T4. ...
        """
        self.alphaLabels = [""]*MEM_LEN
        self.labels = [""]*MEM_LEN
        self.alphaLabels = DAT_LABELS[:]
        self.useAlphaDataLabels()
        self.useAlphaCodeLabels()

    def useAlphaDataLabels(self, useAlpha = True):
        """Use alpha data labels based on useAlpha,
        and return true if this is a change.
        """
        if useAlpha:
            changed = self.labels[DATA_START:] != self.alphaLabels[DATA_START:]
            if changed:
                self.labels[DATA_START:] = self.alphaLabels[DATA_START:]
        else:
            changed = self.labels[DATA_START:] != numLabels[DATA_START:]
            if changed:
                self.labels[DATA_START:] = numLabels[DATA_START:]
        return changed
        
    def useAlphaCodeLabels(self, useAlpha = True):   
        """Use alpha code labels based on useAlpha,
        and return true if this is a change.
        """
        if useAlpha:
            changed = self.labels[:DATA_START] != self.alphaLabels[:DATA_START]
            if changed:
                self.labels[:DATA_START] = self.alphaLabels[:DATA_START]
        else:
            changed = self.labels[:DATA_START] != numLabels[:DATA_START]
            if changed:
                self.labels[:DATA_START] = numLabels[:DATA_START]
        return changed

    def useBinary(self, yesBinary = True):
        '''Switch to binary display if requested.'''
        if self.showAsm != (not yesBinary):
            self.showAsm = not yesBinary
            self.logHeading()

    def calcMemDerived(self):
        '''Calc and record bound on addresses of data.'''
        self.dataAddr = []
        for i in range(0,DATA_START, 2):
            n = self.getDataRef(i)
            if n != None and n not in self.dataAddr:
                self.dataAddr.append(n)
        self.dataAddr.sort()
        if self.dataAddr:
            self.dataLims = (self.dataAddr[0], self.dataAddr[-1] + 1)
        else:
            self.dataLims = None


    def loadFile(self, fileName):
        """
        reset PIP with file data and return log addition.
        On error throw exception.
        figure out if the file is in
          PIP dat format or  (allow arbitray binary with right header, length)
          text with only space space and 0's and 1's (error f not in 8's)
          or assembler with or without symbolic labels (require legal assembler)
        """
        MAX_DATA = 30000
        try:
            f = open(fileName, "rb")  # for AE version need binary:  dump?
        except IOError:
            raise Exception("Error opening " + fileName)
        try:
            # check for ridiculous length
            s = f.read(MAX_DATA);
        except IOError:
            raise Exception("Error reading " + fileName)
        if len(s) == MAX_DATA:  # in case an enormous file chosen by mistake
            raise Exception("File too large -- pick another.")
        if len(s) == 326 and s.startswith(datStart):
            self.dat2mem(s)
        else:
            s = s.decode()
            if only01(s):
                mem = binStr2Bytes(s)
                err = legalMem(mem)
                if err:
                    raise Exception(err)
                self.mem = mem
                self.initLabels()
            else:
                self.assemble(s)
        self.calcMemDerived()
        self.initCPU("from " + fileName)

    def saveFile(self, fileName, addExtension = True, showNumLabels = False):
        """
        save data based on file extension if possible (.dat, .asm, .bin)
        or the current display mode.
        On error throw exception.
        """
        if fileName.lower().endswith(DAT):
            s = mem2dat(self.mem)
        elif fileName.lower().endswith(BIN):
            s = mem2bin(self.mem)
        elif fileName.lower().endswith(ASM):
            s = self.mem2asm(showNumLabels) 
        elif self.labels == DAT_LABELS: # no loss of information
            fileName += DAT
            s = mem2dat(self.mem)
        elif not self.showAsm:
            fileName += BIN
            s = mem2bin(self.mem) 
        else:
            fileName += ASM
            s = self.mem2asm() 
        if isinstance(s, str):
            mode = "w"
        else:
            mode = "wb"
        try:
            f = open(fileName, mode)
        except IOError:
            raise Exception("Error opening " + fileName)
        try:
            f.write(s);
        except IOError:
            raise Exception("Error writing " + fileName)
        return fileName

    def dat2mem(self, s):
        '''Use dat file bytes to initialize memory and labels.'''
        if DATA_START != 128:
            raise Exception('Memory parameters inconsistent with .dat format!')
        if len(s) != 326 or not s.startswith(datStart):
            raise Exception('Bad dat file structure.')
        s = s[len(datStart):]
        for i in range(0,DATA_START, 2):
            self.mem[i] = s[2*i + 2]
            self.mem[i+1] = s[2*i + 3]
        s = s[256:]
        for i in range(0,MAX_DATA):
            self.mem[i+DATA_START] = s[4*i + 3]
        self.initLabels()

    def mem2asm(self, showNumLabels = False):
        '''Return an assembler code string for memory.'''
        # set self.codeLim
        nopCode = mnem2code('NOP') 
        for i in range(DATA_START - 2, 0, -2):
            if self.mem[i] != nopCode:
                break
        lines = [self.lineStr(addr, showNumLabels, True)
                 for addr in range(0, i+2, 2)]
        return "\n".join(lines)
        
    def assemble(self, s):
        """Set mem and labels.
        Only temp variables set until all cleared as legal.
        Exception on error.
        """        
        codes = parseLines(s) # break into parsed asm lines
        if len(codes) > DATA_START//2:
            raise Exception("Too many lines in the program")            
        labels = [str(i) for i in range(MEM_LEN)]
        #process each line label into labels, labelDict, extract from line
        for code in codes:  # extract code labels
            if code.label in labels:
                raise Exception("Line {}: Duplicate label {}"
                                .format(code.lineNum, code.label) )
            elif code.label:
                labels[code.addr] = code.label
        # extract code labels in jump operands, collect data symbols
        dataLabels = []
        for code in codes:  # extract code labels
            if code.b2 == None:
                if code2mnem(code.b1) in jmpOp:
                    code.b2 = label2Addr(code.operand, labels)                    
                    if  code.b2 == None:
                        raise Exception("Line {}: Operand not a code label: {}"
                                        .format(code.lineNum, code.operand) )
                elif not code.operand in dataLabels:
                    dataLabels.append(code.operand)

        #put each found data label in labels, labelDict
        if len(dataLabels) > MAX_DATA:
            raise Exception("More than {} data labels".format(MAX_DATA) )           
        if elementsIn(dataLabels, VARS):
            dataLabels = VARS
        useDataLabels(labels, dataLabels)
        
        # remove data symbols from assembler code: must work at this point
        for code in codes:
            code.convertOperandLabel(labels)
        
        # create machine code  
        codeSeq = []
        for code in codes:
            codeSeq += code.getCode()
        # should be unneeded -- all checks done already, but double check
        for i in range(0, len(codeSeq), 2):
            err = illegalOp(codeSeq[i], codeSeq[i+1])
            if err:
                raise Exception("Late found error, address {}: {}"
                                .format(i, err))            
                
        self.mem = padMem(codeSeq) 
        self.alphaLabels = labels
        self.useAlphaDataLabels()
        self.useAlphaCodeLabels()

    def getDataRef(self, i):
        """Return the data address referred to by instruction at address i.
        Assume legal opcode sequence.  Return None if no data reference."""
        b1 = self.mem[i]
        mnem = code2mnem(b1 % 16)
        
        if b1 > 15 or (mnem in noDataRef):
            return None
        return self.mem[i+1]
        
    def wroteLast(self): 
        """Return True if just executed STO."""
        return self.getLastDataEffect() == 3

    def getLastDataEffect(self): #underused for now - could elaborate markers
        """return
           0 if lastIP is None or no data
           1 if immediate used
           2 if data read but not written
           3 if data written.
        Assume legal opcode sequence. (?)
        """
        if not self.lastIP:
            return 0
        code = self.mem[self.lastIP]
        if code >= 16:
            return 1
        mnem = code2mnem(code % 16)
        if (mnem in noDataRef):
            return 0
        if mnem == 'STO':
            return 3
        return 2
    
    def codeStr(self, addr, forceAsm = False):
        """Return code string for instruction at mem addr (no line label).
        """
        if self.showAsm or forceAsm:
            return bytes2asm(self.mem, addr, False, self.labels)
        return bytes2bin(self.mem, addr)

    def lineStr(self, addr, showNumLabels = True, forceAsm = False):
        """Return code string for instruction at mem addr,
        with label if either required or showNumLabels is true.
        In any case space is left for 8 character labels.
        IF no space for labels is desired at all, use codeStr(addr).
        """
        if showNumLabels or not self.labelStr(addr).isdigit():
            prefix = "{:8}: ".format(self.labelStr(addr, forceAsm))
        else:
            prefix = "{:10}".format("")
        return prefix + self.codeStr(addr, forceAsm)


    def dataStr(self, addr):
        '''Return string for the data at addr.'''
        return self.dataByteStr(self.mem[addr])

    def dataByteStr(self, b):
        '''Return a string for specified data byte.'''
        if self.showAsm:
            return str(makeSignedByte(b))
        return hexBin.nBitBin(b)

    def labelStr(self, addr, forceAsm = False):
        '''Return label for address, in current form or symbolic if forced.'''
        if self.showAsm or forceAsm:
            return self.labels[addr]
        return hexBin.nBitBin(addr)

    def lastIPStr(self):
        """Return code string for last ip or '--'."""
        if self.lastIP is None:
            return "--"
        else:
            return self.labelNumStr(self.lastIP)

    def ipStr(self):
        """Return code string for ip or '--'."""
        if self.halted:
            return "--"
        else:
            return self.labelNumStr(self.ip)

    def labelNumStr(self, addr):
        '''Return numeric label for addr.'''
        if self.showAsm:
            return str(addr)
        return hexBin.nBitBin(addr)

    def accStr(self):
        '''Return the accumulator string.'''
        return self.dataByteStr(self.acc)

    def legalIPVal(self, val):
        '''Return True if current IP legal.'''
        return  0 <= val < 2*MAX_CODE  and val % 2 == 0
        
    def incMaxCode(self):        
        global MAX_CODE
        MAX_CODE += 1
        return MAX_CODE

    def legalDataAddr(self, addr):
        '''Return True if address legal for data.'''
        return  DATA_START <= addr < MEM_LEN
        
    def clearLog(self):
        '''Empty the log.'''
        self.log = []
        
    def logLine(self, line):
        """Add a line to the log and return it."""
        self.log.append(line)
        return line
    
    def logHeading(self, addToLog=True):
        """return log column headings, and append to log if addToLog.
        """
        if self.showAsm:
            maxIPLabel = 2
            dataWidth = 4
        else:
            dataWidth = 8
            maxIPLabel = 8
        line = "{:{}}-{:<{}} {:>{}}".format("IP", maxIPLabel, 
                                     "->", maxIPLabel, "ACC", dataWidth)
        for addr in self.dataAddr:
            name = self.labelStr(addr)
            width = max(dataWidth, len(name))
            line += " {:>{}}".format(name, width)
        if addToLog or self.lastLogHeading != line:
            self.logLine(line)
            self.lastLogHeading = line    
        return line
    
    def logEntry(self, prefix='', addHeading = False, addToLog = True):
        """Return and add to log current CPU state including data columns.
        """
        if prefix:
            prefix += '\n'
        if addHeading:
            prefix += self.logHeading(False) + '\n'
        if self.showAsm:
            maxIPLabel = 2
            dataWidth = 4
        else:
            dataWidth = 8
            maxIPLabel = 8
        line = "{:>{}}|{:>{}} {:>{}}".format(self.lastIPStr(), maxIPLabel,
                        self.ipStr(), maxIPLabel, self.accStr(), dataWidth)
        for addr in self.dataAddr:
            width = max(dataWidth, len(self.labelStr(addr)))
            line += " {:>{}}".format(self.dataStr(addr), width)
        line = prefix+line    
        if addToLog:
            self.logLine(line)
        return line
        
    def getLogLines(self, nLines = 1):
        """ get nLines from end of log.  If nLines is 0, get all."""
        if not nLines or nLines >= len(self.log):
            part = self.log
        else:
            part = self.log[-nLines:]
        return "\n".join(part)
    
    def step(self):
        """Single step the processor,
        also maintain self.lastIP, self.halted.  Also halt on error.
        Does legality check, except ignores direct flag if illegal and
        ignores data where there should be no data
        Returns None or Error string
        """
        if self.halted:
            self.lastIP = None
            return "Halted already -- You must Reset the IP."
        b1 = self.mem[self.ip]
        b2 = self.mem[self.ip + 1]
        err = illegalOp(b1, b2)
        if err:
            return err
        self.lastIP = self.ip
        
        mnem = code2mnem(b1 % 16)
        if mnem == 'HLT':
            self.halted = True
            nextIP = self.ip
        elif mnem == 'JMP':
            nextIP = b2
        elif mnem == 'JMZ':
            if self.acc == 0:
                nextIP = b2
            else:
                nextIP = self.ip + 2
        else: # normal sequential instruction
            nextIP = self.ip + 2
            if mnem == 'STO':
                self.mem[b2] = self.acc
            elif mnem == 'NOP':
                pass
            elif mnem == 'NOT':
                self.acc = bool2int(not self.acc)
            else: # remaining options have a data value
                if b1 >= 16:
                    data = b2
                else:
                    data = self.mem[b2]
                data = makeSignedByte(data)
                accData = makeSignedByte(self.acc)
                if mnem == 'LOD':
                    self.acc = makePosByte(data)
                elif mnem == 'AND':
                    self.acc = bool2int(accData and data)                
                elif mnem == 'CPZ':
                    self.acc = bool2int(not data)
                elif mnem == 'CPL':
                    self.acc = bool2int(data < 0)
                else: # may be overflow
                    if mnem == 'ADD':
                        maybe = accData + data
                    elif mnem == 'SUB':
                        maybe = accData - data
                    elif mnem == 'MUL':
                        maybe = accData * data
                    elif mnem == 'DIV':
                        if data == 0:
                            self.halted = True
                            return self.logLine("Division by 0")
                        maybe = accData // data
                    else:
                        self.halted = True
                        return self.logLine("Illegal op code")
                    if  not legalSignedByte(maybe):
                        self.halted = True
                        return self.logLine("Result out of range")
                    self.acc = makePosByte(maybe)
        if not self.legalIPVal(nextIP):
            self.halted = True
            self.ip = 0
            return self.logLine(
               "Instruction Pointer {} too large; increase max.".format(nextIP))
        self.ip = nextIP
        self.logEntry()

    def accEdit(self, val):
        """Give new value to Accumulator.
        Returns None or Error string
        """
        try:
            val = int(val)
        except:
            return "Value not in legal integer format."
        if val == self.acc:
            return
        if not legalSignedByte(val):
            return "Value not in signed byte range."
        self.acc = val
        self.logEntry("---- Accumulator edited -----")

    def ipEdit(self, val):
        """Give new value to IP.
        Returns None or Error string
        """
        try:
            val = int(val)
        except:
            return "Value not in legal integer format."
        if val == self.ip:
            return
        if not self.legalIPVal(val):
            return "Instruction address too large."
        self.ip = val
        self.halted = False
        self.logEntry("---- IP edited -----")
        self.lastIP = None

    def dataEdit(self, addr, val):
        """Give new value to data location.
        Returns None or Error string
        """
        if not self.legalDataAddr(addr):
            return "Address out of data range"
        if self.showAsm:
            try:
                val = int(val)
            except:
                return "Value not in legal integer format."
            if not legalSignedByte(val):
                return "Value not in signed byte range."
        else:
            try:
                bytes = binEntryBytes(val)
            except Exception as e:
                return str(e)
            if len(bytes) != 1:
                return 'Data needs to be exactly one byte!'
            val = bytes[0]
        if val == self.mem[addr]:
            return
        self.mem[addr] = val
        self.logEntry("---- Data location {} edited -----".format(addr))

    def codeEdit(self, addr, codeStr):
        """Give new 2-byte value to code location.
        Returns None or Error string
        """
        if not self.legalIPVal(addr):
            return "Address too large: {}".format(addr)
        if self.showAsm:
            try:
                asm = AssemblerLine(codeStr, 0, addr)
            except Exception as e:
                return str(e)
            asm.convertOperandLabel(self.alphaLabels)
            if asm.b2 == None:
                return "Unknown operand at code address {}".format(addr)
            bytes = asm.getCode()
        else:
            try:
                bytes = binEntryBytes(codeStr)
            except Exception as e:
                return str(e)
            if len(bytes) != 2:
                return 'Binary instructions need to be exactly two bytes!'
            err = illegalOp(*bytes)
            if err:
                return err
        if  bytes != self.mem[addr:addr+2]:
            self.mem[addr:addr+2] = bytes
            self.logLine("---- Code address {} edited -----".format(addr))

    def memEdit(self, label, editStr): 
        """label is string label - either numeric or symbolic
        editStr gives the new value.
        Make the edit and return None or return an error string.
        """
        addr = label2Addr(label, self.alphaLabels)
        if addr == None:
            return "Unknown memory label " + label
        if addr < DATA_START:
            return self.codeEdit(addr, editStr)
        return self.dataEdit(addr, editStr)
