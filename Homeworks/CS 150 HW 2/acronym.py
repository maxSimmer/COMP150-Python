acronym = input('Enter an acronym here: ')
acronym = acronym.upper()
acronym = acronym.split()

letter = []
for i in acronym:
    letter.append(i[0])
letter = ''.join(letter)
print(letter)





