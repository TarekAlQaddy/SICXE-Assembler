class Pass2:
    def __init__(self):
        self.SYMTAB = {}
        self.table = []
        self.opcode = {}
        self.reg_num = {'a': 0x00, 'x': 0x01, 'l': 0x02, 'pc': 0x08, 'sw': 0x09, 'b': 0x03, 's': 0x04, 't': 0x05,
                        'f': 0x06}
        self.base_flag = False
        self.base_reg = None

    def start(self, table, SYMTAB, txtfile):
        with open(txtfile) as f:
            for line in f:
                (key, val) = line.split()
                self.opcode[key] = val
        self.SYMTAB = SYMTAB
        self.table = table
        self.parse()

    def parse(self):

        for index, inst in enumerate(self.table):
            temp_object_code = ''
            hex_object_code = 0
            temp = inst['opcode']
            if temp == 'base':
                self.base_flag = True
            if temp == 'nobase':
                self.base_flag = False
            if temp == 'ldb':
                self.base_reg = inst['operand']
            else:
                print('ERROR!!! base loaded without reference')
            if inst['is_dir']:

                if temp == 'resw' or 'resw':  # --------------- 7anefsel el HTME record
                    continue

                if temp == 'word':
                    hex_object_code = 0x000000
                    hex_object_code &= inst['operand']
                    print(hex(hex_object_code))
                    continue

                if temp == 'byte':
                    hex_object_code = 0x00
                    value = operand.partition("'")[-1].rpartition("'")[0]
                    temp = len(value)
                    if inst[operand[0]].lower() == 'x':
                        if temp % 2 == 0:
                            hex_object_code &= value

                        else:
                            hex_object_code &= value >> 1

                    elif operand[0].lower() == 'c':
                        hex_object_code &= format(ord(value), "x")

                    else:
                        hex_object_code &= hex(value)
                    continue

            if temp[0] == '+':
                temp = temp[1:]

            if inst['type'] == 1:
                hex_object_code = 0x00
                hex_object_code &= self.opcode.get(temp)
                print(hex(hex_object_code))
                continue

            if inst['type'] == 2:
                hex_object_code = 0x0000
                opcode = int('0x' + self.opcode[inst['opcode']], 0)
                hex_object_code |= (opcode << 8)
                operand = inst['operand']
                if operand.find(",") == -1:
                    if self.reg_num.get(operand):
                        try:
                            hex_object_code &= self.reg_num.get(operand)
                        except KeyError:
                            print("Register not found!")
                        continue
                        # aw yenfa3 mesh 3aref momken ykoon masalan rakam aw 7aga??------------elly howa law mafesh operand register momken ykon rakam?

                else:
                    string = operand.split(",")
                    hex_object_code |= self.reg_num.get(string[0]) << 4
                    hex_object_code |= self.reg_num.get(string[1])
                    print(hex(hex_object_code))
                    continue

            if inst['type'] == 3:
                hex_object_code = 0x000000

                opcode = int('0x' + self.opcode[inst['opcode']], 0)
                hex_object_code |= (opcode << 16)
                operand = inst['operand']
                locctr = inst['locctr']

                if (operand.find(',') != -1) and (operand[-1] == 'x'):
                    hex_object_code |= 0x008000
                    operand = operand[:len(operand) - 2]

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
                        if self.base_flag and self.base_reg:
                            hex_object_code |= 0x004000
                            hex_object_code |= (operand_address - self.base_reg)

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
                            if self.base_flag and self.base_reg:
                                hex_object_code |= 0x004000
                                hex_object_code |= (operand_address - self.base_reg)
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
