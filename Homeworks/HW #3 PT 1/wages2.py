def caluclateWeeklyWages(totalHrs, hourlyWage):

    if totalHrs <= 40:
        regularHrs = totalHrs
        overtime = 0
    elif 40 < totalHrs <= 60:
        overtime = totalHrs - 40
        regularHrs = 40
    else:
        overtime = 20
        regularHrs = 40
        dblOT = totalHrs - (overtime + regularHrs)
        return hourlyWage * regularHrs + (1.5 * hourlyWage) * overtime + (2*hourlyWage) * dblOT

def main():
    hours = float(input('Enter the hours you worked:'))
    wage = float(input('Enter your hourly wage: '))
    total = caluclateWeeklyWages(hours, wage)
    print('The wages for {hours} hours at ${wage:.2f} per hr are ${total:.2f}'
          .format(**()))

main()