'''exercise to complete and test this function'''

'''Join all the strings in stringList into one string,
    and return the result, NOT printing it. For example:

    s = joinStrings(['very', 'hot', 'day']) # returns string
    print(s)
    veryhotday
    '''

def joinStrings(stringList):

    oneString = ''
    for x in stringList:
        oneString = oneString + x
    return oneString
    # finish the code for this function


def main():
    print(joinStrings(['very', 'hot', 'day']))
    print(joinStrings(['this', 'is', 'it']))
    print(joinStrings(['1', '2', '3', '4', '5']))

main()
