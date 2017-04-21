from pass1 import Pass1
from pass2 import Pass2

tab = {}
errors = []

# insert op-table as a text file (already made)
with open('optab.txt') as f:
    for line in f:
        (key, val) = line.split()
        tab[key] = val

pass1 = Pass1(tab, errors)

pass1.start('test2.txt')

pass2 = Pass2(errors)

pass2.start(pass1.final, pass1.SYMTAB, tab, pass1.start_address, pass1.prog_len, pass1.first_exec, pass1.name)

# type file name to write the HTME record

pass2.write_to_htme('HTME.txt')
