'''Quotient Function Excersize'''

def quotProblem(x, y):
    quot = x // y
    rem = x % y
    sentence = 'The quotient of {} and {} is {}, while the remainder is {}. '.format(x, y, quot, rem) 
    print(sentence)
    

def main():
    quotProblem(3, 5)
    quotProblem(1234567890123, 535790269358)
    Line1 = int(input('Enter an integer: '))
    Line2 = int(input('Enter a second integer: '))
    quotProblem(Line1, Line2)

main()
