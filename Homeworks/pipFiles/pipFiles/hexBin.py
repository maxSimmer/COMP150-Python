hToB = {'0':'0000', '1':'0001', '2':'0010', '3':'0011',
       '4':'0100', '5':'0101', '6':'0110', '7':'0111',
       '8':'1000', '9':'1001', 'A':'1010', 'B':'1011',
       'C':'1100', 'D':'1101', 'E':'1110', 'F':'1111'}

def invertMap(map):
    """Invert a one-to-one mapping."""
    inv = {}
    for (k, v) in list(map.items()): # generates sequence of (key, value) pairs
        inv[v] = k           # backwards -- from v to k
    if len(map) != len(inv): # if set inv[v] more than once for some v
        raise Exception('Map not one-to-one: no inverse.') # makes program bomb
    return inv
    
bToH = invertMap(hToB)

def hexToBin(hexString, strip = False): # rightmost parameters may have defaults
    binString = '' 
    for hexDigit in hexString:
        binString += hToB[hexDigit]
    if strip:
        while binString.startswith('0'):
            binString = binString[1:] # remove leading '0'
        if not binString: # case if initially only 0's -- and all removed
            binString = '0'
    return binString

def binToHex(binString):
    hexString = ''
    while len(binString) % 4  != 0: # pad 0 ON LEFT until multiple of 4 bits
        binString = '0' + binString
    for i in range(0, len(binString), 4):  # every 4th index
        bin4 = binString[i:i+4]  # get next 4 bits
        hexString += bToH[bin4] # add corresponding hex digit
    return hexString

digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def intToBase(i, base):
    i = int(i)  # if i is a string, convert to int
    if i == 0:
        return '0'
    numeral = ""
    while i != 0:
        rem = i % base
        numeral = digits[rem] + numeral  # add next digit on LEFT
        i //= base
    return numeral

def base2int(numStr, base): # this one is actually built in!
    return int(numStr, base)

def charPad(s, n, ch):
    return ch*(n-len(s)) + s

def nBitBin(i, n=8):
    """Truncate i so at most n bits binary string and if less, pad with '0's."""
    ##return intToBase(i,2)[-8:].rjust(n,'0')
    return charPad(intToBase(i,2)[-8:],n,'0')
    

def main():
    for hexString in ['A1B2C3D4E5F67890', '1B2', '3', '0']:
        print("first hex:", hexString, '-----------')
        for doPad in [False, True]:
            binString = hexToBin(hexString, doPad)
            print("bin", binString)
            print("hex", binToHex(binString))

        
if __name__ == '__main__':
    main()
