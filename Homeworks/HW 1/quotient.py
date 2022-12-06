'''Write a program, quotient.py, that prompts the user for two integers, and then prints them out in a sentence with an integer division problem'''
x=int(input('Enter a number: '))
y=int(input('Enter a second number: '))
quot = x//y
remain = x%y
print('The quotient of ', x, ' and ', y, ' is ', quot, ' with a remainder of ', remain, '.', sep='')
