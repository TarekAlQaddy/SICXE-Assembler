from pass1 import Pass1
from pass2 import Pass2

tab = {}

f = open('optab.txt', 'r')
str1 = f.read()
ops = str1.split('\n')

for i in ops:
    t = i.split(' ')
    tab[t[0].lower()] = int(t[1], 16)

pass1 = Pass1(tab)

pass1.start('test.txt')


for i in pass1.final:
    print(i)

print(pass1.SYMTAB)
pass2 = Pass2()

pass2.start(pass1.final, pass1.SYMTAB, 'optab.txt')