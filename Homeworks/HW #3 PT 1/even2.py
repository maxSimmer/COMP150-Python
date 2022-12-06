def chooseEven(numbers):
    List = []
    for i in numbers:
        if i % 2 == 0: #modular division to see if its dividable by 2
            List.append(i) #if dividable by 2 it will add it to the list
    print(List)

chooseEven([10, 15, 20, 25, 30, 35]) #list of numbers to choose from
