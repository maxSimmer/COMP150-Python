file = input('Enter file name: ')
outfile = open(file, 'r')
contents = outfile.read()
print(contents.upper()) 