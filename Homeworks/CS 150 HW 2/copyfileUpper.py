file = input('Enter a file name: ')
outfile = open(file, 'r')
contents = outfile.read()
outfile.close()


file = 'upper' + fileNew
outfile = open(file, 'w')
outfile.write(contents.upper())
outfile.close()



