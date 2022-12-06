'''Quotient Return'''

def quotProblemStr(x ,y):
    quot = x // y
    rem = x % y
    return 'The quotient of {} and {} is {}, while the remainder is {}. '.format(x, y, quot, rem)

def main():
    print(quotProblemStr(3, 5))
    print(quotProblemStr(1234567890123, 535790269358))
    Line1 = int(input('Enter an integer: '))
    Line2 = int(input('Enter a second integer: '))
    print(quotProblemStr(Line1, Line2))

main()
    
