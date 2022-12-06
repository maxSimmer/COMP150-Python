def sumList(numbers):
    '''Return the sum of the numbers in the list nums.'''
    sum = 0
    for num in numbers:
        sum = sum + num
    return sum

def main():
    print(sumList([5, 2, 4, 7]))
    print(sumList([52, 87, 97, 103]))
    print(sumList([]))

main()

