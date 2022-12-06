''' last integer will be 0'''

sumAll = 0
while(True):
    x = int(input('Enter an integer: '))
    if x == 0:
        break
    sumAll = sumAll + x
print('Sum = '+str(sumAll))

