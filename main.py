from pass1 import Pass1
from pass2 import Pass2

tab = {}

f = open('optab.txt', 'r')
str1 = f.read()
ops = str1.split('\n')

for i in ops:
    t = i.split(' ')
    tab[t[0].lower()] = int(t[1], 16)

p = Pass1(tab)

p.start('test.txt')

print(p.LOCCTR, p.SYMTAB, "\n\n")

for i in p.final:
    print(i)


p2 = Pass2()

p2.start(p.final, p.SYMTAB)