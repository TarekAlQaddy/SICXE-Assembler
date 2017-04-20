from pass1 import Pass1
from pass2 import Pass2

tab = {}

with open('optab.txt') as f:
    for line in f:
        (key, val) = line.split()
        tab[key] = val

pass1 = Pass1(tab)

pass1.start('test2.txt')


for i in pass1.final:
    print(i)

pass2 = Pass2()

pass2.start(pass1.final, pass1.SYMTAB, tab, pass1.start_address, pass1.prog_len, pass1.first_exec, pass1.name)

pass2.write_to_htme('HTME.txt')

#TODO: make errors array here and append in each pass error, line no
