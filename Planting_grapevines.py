r = int(input('Enter the length of the row(in feet): '))
e = int(input('Enter the amount of space used by an end-port assembly(in feet): '))
s = int(input('Enter the amount of space between the vines(in feet): '))
v = (r - (2 * e))/s
print('The number of vines that will fit in the row are: ', v, 'vines')
