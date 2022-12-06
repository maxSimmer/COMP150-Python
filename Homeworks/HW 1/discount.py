''' Prompt the user for an original price and for a discount
percentage and prints out the new price to the nearest cent.'''

originalPrice = float(input('Enter an original price: ')) # float rather than int as we percentages include decimals.
discountPercentage = float(input('Enter a discount %: '))
discountPercentage = discountPercentage * .01

newPrice =  originalPrice - (originalPrice * discountPercentage)
newPrice = format(newPrice, '.2f')

print('The price after adding the discount is: ', newPrice, '.')



