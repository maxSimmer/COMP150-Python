import random
for i in range(5):
    print(i+1)

number = int(input('Enter a number: '))
for i in range(number):
    print(i+1)

for i in range(6):
    print(random.randrange(1, number+1))