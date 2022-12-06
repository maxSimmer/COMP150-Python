'''annual interest rate is .04'''

initialBalance = float(input('Enter your initial balance: ')) #beginning balance
interestRate = float(input('Enter the annual interest rate: ')) #interest rate yearly
desiredBalance = float(input('Enter the desired final balance: ')) #final account total

annualBalance = initialBalance #sets the final annual balance to be the initial balance

timeinYears = 1
print('Beginning balance: %.2f' %(initialBalance))

while(annualBalance <= desiredBalance):
    annualBalance = annualBalance+(annualBalance * interestRate)
print('Year: %d \t Balance: %.2f' %(timeinYears, annualBalance))





