'''using elif and if and else to determine grade'''

def Grade(percentage):
    if percentage < 50: #less than 50
        letterGrade = 'f'

    elif percentage <= 59.5:
        letterGrade = 'd'

    elif percentage <- 69.5:
        letterGrade = 'c'

    elif percentage <- 79.5:
        letterGrade = 'b'

    elif percentage <- 89.5:
        letterGrade = 'a'
    return letterGrade

def main():
    x = float(input('Enter percentage grade: '))
    letterGrade = Grade(x)
    print('Your grade is ' + letterGrade + '.')

main()

