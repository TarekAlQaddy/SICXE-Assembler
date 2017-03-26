def start_handle(str, errors):
    """
    returns the address of the first line in program
    """
    if str[9:14].lower().strip() == 'start':
        start_add = str[17:34]
        start_add = start_add.strip()
        return int(start_add, 16)
    else:
        errors.append("No START at begin of the program")


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
        elif operand[0].lower() =='c':
            return hex(temp)
        #TODO: return No of bytes needed for decimal numbers
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
