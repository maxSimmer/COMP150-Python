'''Exercise to complete printLocations as described below.
Create file locations.py.'''

def printLocations(s, target):
    '''s is a string to search through, and target is the substring to look for.
    Print each index where the target starts.
    For example:
    >>> printLocations('Here, there, everywhere!', 'ere')
    1
    8
    20
    '''

    repetitions = s.count(target)
    #  ?? add initialization
    end = 0
    for i in range(repetitions):
        start = s.find(target, end) + 1
        end = s.find(target, start)
        print(start - 1)
        #  ?? add loop body lines


def main():
    printLocations('Where are all my eggs?', 'e')

main()
