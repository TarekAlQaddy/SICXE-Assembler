from pass1 import Pass1
from pass2 import Pass2

tab = {}

f = open('optab.txt', 'r')
#eh str1 dah?
str1 = f.read()
#eh ops deh?
ops = str1.split('\n')

for i in ops:
    t = i.split(' ')
    tab[t[0].lower()] = int(t[1], 16)

pass1 = Pass1(tab)

pass1.start('test.txt')

# print(pass1.LOCCTR, pass1.SYMTAB, "\n\n")
#
for i in pass1.final:
    print(i)

print(pass1.SYMTAB)
pass2 = Pass2()

pass2.start(pass1.final, pass1.SYMTAB, 'optab.txt')