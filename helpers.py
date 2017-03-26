def start_handle(str):
    """
    returns the address of the first line in program
    """
    if str[9:14].lower() == 'start':
        start_add = str[17:34]
        start_add = start_add.strip()
        return int(start_add, 16)
    else:
        # TODO: handle error end the program
        print("No START at begin of the program")

        # TODO: add format handling function


def locctr_increamenter(opcode, operand):
    if opcode.lower() == "resw":
        temp = int(operand) * 3
        return hex(temp)
    if opcode.lower() == "word":
        return 3
    if opcode.lower() == "byte":
        value = operand.partition("'")[-1].rpartition("'")[0]
        temp = len(value)
        if operand[0].lower() == 'x':
            if temp % 2 == 0:
                return hex(temp / 2)
            else:
                return hex(temp + 1 / 2)
        if operand[0].lower() =='c':
            return hex(temp)
    if opcode.lower() == "resb":
        value = hex(int(operand))
        return value
    if opcode.lower() == "end":
        return 0
    if opcode.find('+'):
        return 4
    if operand.find(","):
        return 2
    if operand.isspace() | operand.isnull():
        return 1
    else:
        return 3
