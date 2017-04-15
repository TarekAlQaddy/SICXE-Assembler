import binascii


class Pass2:
    def __init__(self):
        self.SYMTAB = {}
        self.table = []
        self.opcode = {}
        self.reg_num = {'a': 0, 'x': 1, 'l': 2, 'pc': 8, 'sw': 9, 'b': 3, 's': 4, 't': 5, 'f': 6}

    def start(self, table, SYMTAB, txtfile):
        with open(txtfile) as f:
            for line in f:
                (key, val) = line.split()
                self.opcode[key] = val

        self.SYMTAB = SYMTAB
        self.table = table
        self.parse()

    def getInstructionIndex(self, str):
        for i in range(len(self.opcode)):
            if self.opcode[i]["memonic"] == str:
                return i
        return -1

    def hexa_to_binary_conv(self, num, length):
        my_hexdata = num
        scale = 16  ## equals to hexadecimal
        return bin(int(my_hexdata, scale))[2:].zfill(length)

    def parse(self):

        for index, inst in enumerate(self.table):
            temp_object_code = ''
            hex_object_code = 0
            print(temp_object_code)
            if inst['is_dir']:
                # handle
                continue
            temp = inst['opcode']
            if temp[0] == '+':
                temp = temp[1:]
            temp_object_code += self.hexa_to_binary_conv(str(self.opcode.get(temp)), 8)
            if inst['type'] == 1:
                continue
            if inst['type'] == 2:
                operand = inst['operand']
                if operand.find(",") == -1:
                    # TODO:
                    # FIX: case of type2 => if only one operand it's in the first 4 bits then add 4 zeros
                    # FIX: remove all these strings and use hexa instead (hex_object_code instead of temp_object_code)
                    temp_object_code += '0000'
                    if self.reg_num.get(operand):
                        print(self.reg_num.get(operand))
                        temp_object_code += self.hexa_to_binary_conv(self.reg_num.get(operand), 4)
                        print(inst["opcode"])
                        print(temp_object_code)
                        continue
                    else:
                        temp_object_code += self.hexa_to_binary_conv(operand, 8)
                        print(temp_object_code)
                        continue
                else:
                    string = operand.split(",")

                    print(temp_object_code)
                    temp_object_code += self.hexa_to_binary_conv(repr(self.reg_num.get(string[0])), 4)

                    temp_object_code += self.hexa_to_binary_conv(repr(self.reg_num.get(string[1])), 4)
                    print(temp_object_code + "\n")
                    continue

            if inst['type'] == 3:
                hex_object_code = 0x000000

                opcode = int('0x' + self.opcode[inst['opcode']], 0)
                hex_object_code |= (opcode << 16)

                operand = inst['operand']
                locctr = inst['locctr']

                if (operand.find(',') != -1) and (operand[-1] == 'x'):
                    hex_object_code |= 0x008000
                    operand = operand[:len(operand)-2]

                if inst['operand'][0] == '@':
                    hex_object_code |= 0x020000
                    try:
                        operand_address = self.SYMTAB[operand[1:]]
                    except KeyError:
                        print("{} label not defined !".format(operand[1:]))
                        continue

                    if -2048 <= operand_address - locctr - 3 <= 2047:
                        hex_object_code |= 0x002000
                        hex_object_code |= (operand_address - locctr - 3)
                    elif 0 <= operand_address - locctr <= 4095:
                        hex_object_code |= 0x004000
                        # TODO:handle if base relative (operand_address - base)
                    else:
                        print('operand is out of range of PC and Base relative')
                        # TODO:throw exception
                        continue

                elif inst['operand'][0] == '#':
                    hex_object_code |= 0x010000
                    imm = 0
                    imm_flag = True
                    try:
                        imm = int(operand[1:])
                    except():
                        imm_flag = False
                        print('not numerical imm')

                    if imm_flag:
                        hex_object_code |= 0x006000
                        if -2048 <= imm <= 2047:
                            hex_object_code |= imm
                        else:
                            print('immediate is too big for format 3')
                            continue
                            # TODO: throw exception
                    else:
                        try:
                            operand_address = self.SYMTAB[operand[1:]]
                        except KeyError:
                            print('{} label not defined'.format(operand[1:]))
                            continue

                        if -2048 <= operand_address - locctr - 3 <= 2047:
                            hex_object_code |= 0x002000
                            hex_object_code |= (operand_address - locctr - 3)
                        elif 0 <= operand_address - locctr <= 4095:
                            hex_object_code |= 0x004000
                            # TODO:handle if base relative (operand_address - base)
                        else:
                            print('operand is out of range of PC and Base relative')
                            continue

                else:
                    hex_object_code |= 0x030000
                    try:
                        operand_address = self.SYMTAB[operand]
                    except KeyError:
                        print('{} label not defined!'.format(operand))
                        continue

                    if -2048 <= operand_address - locctr - 3 <= 2047:
                        hex_object_code |= 0x002000
                        hex_object_code |= (operand_address - locctr - 3)
                    elif 0 <= operand_address - locctr <= 4095:
                        hex_object_code |= 0x004000
                        # TODO:handle if base relative (operand_address - base)
                    else:
                        print('operand is out of range of PC and Base relative')
                        continue

            if inst['type'] == 4:
                hex_object_code = 0x00000000
                opcode = int('0x' + self.opcode[inst['opcode'][1:]], 0)
                hex_object_code |= (opcode << 24)

                hex_object_code |= 0x00600000  # always not pc nor base relative
                operand = inst['operand']

                if (operand.find(',') != -1) and (operand[-1] == 'x'):
                    hex_object_code |= 0x00800000  # x is set
                    operand = operand[:-1]

                if operand[0] == '@':
                    hex_object_code |= 0x02000000  # n is set
                    operand_address = 0
                    try:
                        operand_address = self.SYMTAB[operand[1:]]
                    except KeyError:
                        print('{} label not defined!'.format(operand[1:]))
                        continue

                    hex_object_code |= operand_address

                elif operand[0] == '#':
                    hex_object_code |= 0x01000000  # i is set

                    operand_address = 0
                    operand = operand[1:]
                    imm_flag = True

                    try:
                        operand_address = int(operand)
                    except ValueError:
                        imm_flag = False

                    if imm_flag:
                        if -524288 <= operand_address <= 524287:
                            hex_object_code |= operand_address
                        else:
                            print('immediate too big for format 4 ')
                            continue
                    else:
                        try:
                            operand_address = self.SYMTAB[operand]
                        except KeyError:
                            print('{} label not defined!'.format(operand))
                            continue
                        hex_object_code |= operand_address

                else:
                    hex_object_code |= 0x03000000
                    try:
                        operand_address = self.SYMTAB[operand]
                    except KeyError:
                        print('{} label not defined!'.format(operand))
                        continue

                    hex_object_code |= operand_address

            print(hex(hex_object_code))
