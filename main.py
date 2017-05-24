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
file = open('HTME.txt','w')
pass1.start('test.txt')

print(pass1.table3)
try:
    pass2 = Pass2(errors)
    print(pass1.SYMTAB)
    pass2.start(pass1.table1, pass1.SYMTAB, tab, pass1.start_address, pass1.table1[-1]['locctr'], pass1.first_exec, pass1.name)
    pass2.write_to_htme('HTME.txt')
    pass2.extdef=[]
    pass2.extref=[]
    pass2.start(pass1.table2, pass1.SYMTAB, tab, pass1.start_address, pass1.table2[-1]['locctr'], pass1.first_exec, pass1.name)
    pass2.write_to_htme('HTME.txt')
    pass2.extdef=[]
    pass2.extref=[]
    pass2.start(pass1.table3, pass1.SYMTAB, tab, pass1.start_address,pass1.table3[-1]['locctr'], pass1.first_exec, pass1.name)
    pass2.write_to_htme('HTME.txt')

except IndexError:
    pass
    