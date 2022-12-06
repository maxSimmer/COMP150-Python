'''numDict Excersize'''

def dictionaryKeys():
    '''Returns a string to integer dictionary'''
    keys = dict()
    keys['One'] = int(1)
    keys['Two'] = int(2)
    keys['Three'] = int(3)
    keys['Four'] = int(4)
    return keys

def runKeys():
    dictionary = dictionaryKeys()
    print(dictionary['One'])
    print(dictionary['Two'])

runKeys()
