age = int(input('Enter your age: '))
usResidency = int(input('Enter how long you have been a U.S. citizen: '))
#Input user data for age and living time in the US

if age >= 30 and usResidency >= 9:
    print('You are able to run for both House and Senate. ')
#If the age is greater than 30 and US residency is longer than 9, they are able to run for both.

elif age >= 35 and usResidency >= 7:
    print('You are only able to run for the House. ')
#If the age is greater than 35 and US residency is longer than 7, you can only run for the House.

else:
    print('You are not able to run for either the House or Senate. ')

