import helpers

def pass1(file_name):
    """
    pass1 of the assembler to make the LOCCTR, SYMTAB and output the program
    """

    SYMTAB = {}
    OPTAB = {}
    LOCCTR = 0
    start_address = 0
    line_no =0
    prog_len = 0
    error_str = ''
    operand =''

    file = open(file_name, 'r')
    str = file.read()
    instructions = str.split('\n')

    start_address = helpers.start_handle(str[1])
    LOCCTR = start_address

    for inst in instructions[1:]:

        #case of comment
        if inst[0] == '.':
            print(inst)
            continue

        #label handling
        label = inst[0:7].strip().lower()
        if label != "":
            if SYMTAB.get(label) != None:
                SYMTAB[label] = LOCCTR
            else:
                #handle error
                print("Error: Label defined more than once")

        #opcode handling if not in OPTAB
        opcode = inst[9:14].strip().lower()
        if OPTAB.get(opcode) == None:
            #handle error
            print("Error: No such opcode")

        #TODO: add No of bytes LOCCTR increaments(helper function) & printing at the end
        operand =inst[17:34]
        LOCCTR += helpers.locctr_increamenter(opcode,operand)


#TODO: we need a better way to handle the errors
#       think of better way to keep the variables as we need them in pass2