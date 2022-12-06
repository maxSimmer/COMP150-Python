"""bases.py
Change of base functions
"""

def decimal(i):
    '''Return a string of decimal digits reprsenting the nonnegative integer i.
    Illustrates the repeated remainder and division algorithm.'''
    if i == 0:
        return "0"
    numeral = ""
    while i != 0:
        digit = i % 10
        numeral = str(digit) + numeral # add next digit on the LEFT
        i = i//10
    return numeral

def digitChar(n):
    '''return single character for digits with value 0 through 15
    emphasizing each conversion for 10, 11, ... 15'''
    if n < 10:               # alternate just return format(n,'H')
        return str(n)
    if n == 10:
        return 'A'
    if n == 11:
        return 'B'
    if n == 12:
        return 'C'
    if n == 13:
        return 'D'
    if n == 14:
        return 'E'
    if n == 15:
        return 'F'
    
def intToBase(i, base):
    """Return a string representing the nonnrgative integer i
    in the specified base, from 2 to 16."""
    i = int(i)  # if i is a string, convert to int
    if i == 0:
        return '0'
    numeral = ""
    while i != 0:
        digit = i % base
        numeral = digitChar(digit) + numeral  # add next digit on LEFT
        i = i//base
    return numeral        


# the next four functions use a variety of string operations
#discussed in Chapter 2 of the Hands-on Python Tutorial.

digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def intToBaseAlt(i, base):
    """Return a string representing the nonnrgative integer i
    in the specified base, from 2 to 36, using string indexing."""
    i = int(i)  # if i is a string, convert to int
    if i == 0:
        return '0'
    numeral = ""
    while i != 0:
        rem = i % base
        numeral = digits[rem] + numeral  # add next digit on LEFT
        i = i//base
    return numeral

def zstrip(numeral):
    """Strip leading zero characters from the numeral string"""
    numeral = numeral.lstrip('0') # strip all '0' from left end of string
    if numeral == '': # case if initially only 0's -- and all removed
        numeral = '0'
    return numeral

def hexToBin(hexString):
    """Converts a hexadecimal string to a binary string of 4 times the length.
    Illustrates dealing with one hex digit at a time."""
    bin4s = []
    for hexDigit in hexString:
        n = digits.find(hexDigit) # converts to an integer
        bin = intToBase(n, 2)
        bin4 = bin.rjust(4, '0')  # pad on left with '0' to have 4 characters
        bin4s.append(bin4)
    return "".join(bin4s)

def binToHex(binString):
    """Converts a binary string to a hexadecimal string.
    Illustrates dealing with groups of 4 bits at a time."""
    hexDigits = []
    while len(binString) % 4  != 0: # pad 0 ON LEFT until multiple of 4 bits
        binString = '0' + binString
    for i in range(0, len(binString), 4):  # every 4th index
        bin4 = binString[i:i+4]  # get next 4 bits
        n = int(bin4, 2)
        hexDigit = digits[n]
        hexDigits.append(hexDigit) # add corresponding hex digit
    return "".join(hexDigits)


def testAll():
    """Convert a list of numbers to binary and hexadecimal and back.
    Only show conversions back if they are different."""
    for n in [0, 1, 2, 5, 12, 45, 97, 123, 255, 2**27 + 1, 2**27 - 1]:
        print("The decimal number {} is:".format(n))
        binString = intToBase(n, 2)
        print("   {} in binary".format(binString))
        hexString = binToHex(binString)
        print("   {} in hexadecimal".format(hexString))
        binBack = hexToBin(hexString)
        binStrip = zstrip(binBack)
        if binBack != binStrip:
            print("   {} back to padded binary".format(binBack))
        if binStrip != binString:
            print("ERROR:  got {} binary, not {}!".format(binStrip, binString))
        n2 = int(binBack, 2)
        if n != n2:
            print("ERROR:  got {} decimal, not {}!".format(n2, n))

def table():
    '''Print a table of conversion between
    hex digits and decimal and padded 4-bit binary.'''
    print('Dec Hex  Bin')
    for i in range(16):
        print('{:-3} {:-3X} {}'.format(i, i, hexToBin(digitChar(i))))
