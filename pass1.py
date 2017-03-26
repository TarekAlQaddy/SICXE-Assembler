import sys
import vars
import helpers

def main(file_name):
    """
    pass1 of the assembler to make the LOCCTR, vars.SYMTAB and output the program
    """

    error_str = []

    file = open(file_name, 'r')
    str = file.read()
    instructions = str.split('\n')

    vars.start_address = helpers.start_handle(instructions[0], error_str)
    vars.LOCCTR = vars.start_address

    #if START not found in the first instruction
    if len(error_str) ==1:
        print(error_str[0])
        return

    for inst in instructions[1:]:

        #case of comment
        if inst[0].strip() == '.':
            print(inst)
            continue

        label = inst[0:7].strip().lower()
        opcode = inst[9:14].strip().lower()
        operand = inst[17:34].strip().lower()

        #label handling
        if label != "":
            if vars.SYMTAB.get(label) != None:
                vars.SYMTAB[label] = vars.LOCCTR
            else:
                error_str.append("Error: Label defined more than once")

        #opcode handling if not in vars.OPTAB

        if vars.OPTAB.get(opcode) == None:
            error_str.append("Error: No such opcode")

        vars.LOCCTR += helpers.locctr_increamenter(opcode, operand)

        vars.line_no += 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('test.txt')
