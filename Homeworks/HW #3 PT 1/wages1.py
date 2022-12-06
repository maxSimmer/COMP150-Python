def calculateWeeklyWages(totalHours, hourlyWages):
    if totalHours <= 40:
        regularHours = totalHours
        ot = 0
    else:
        ot = totalHours - 40
        regularHours = 40
    return hourlyWages * regularHours + (1.5 * hourlyWages) * ot

def main():
    hrs = float(input('Enter hours worked: '))
    wage = float(input('Enter hourly wage: '))
    total = calculateWeeklyWages(hrs, wage)
    print('The wages for {hrs} hours at ${wage:.2f} per hour are ${total:.2f}'
          .format(**locals()))

main()
