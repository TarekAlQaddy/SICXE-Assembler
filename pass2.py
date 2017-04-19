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

    def convert_to_ascii(self,text):
        return "".join("{:02x}".format(ord(c)) for c in text)

    def parse(self):

        for index, inst in enumerate(self.table):
            hex_object_code = 0
            temp = inst['opcode']
            if temp == 'ldb':
                self.base_flag = True
            if temp == 'base' and self.base_flag:
                try:
                    self.base_reg = self.SYMTAB[inst['operand'][1:]]
                except KeyError:
                    print("{} Label not defined!".format(inst['operand'][1:]))

            if inst['is_dir']:
                if temp == 'resw' or temp == 'resb':  # --------------- 7anefsel el HTME record
                    continue


                if inst['opcode'] == 'word':
                    hex_object_code = 0x000000
                    hex_object_code |= (int(inst['operand']))
                    print(str(hex_object_code).zfill(6))

                elif temp == 'byte':
                    if inst['operand'][0] == 'x':
                        value = inst['operand'].partition("'")[-1].rpartition("'")[0]
                        temp = len(value)
                        if temp % 2 == 0:
                            hex_object_code = int(value)
                        else:
                            hex_object_code = int(value.zfill(temp+1))
                    elif inst['operand'][0] == 'c':
                        value = inst['operand'].partition("'")[-1].rpartition("'")[0]
                        temprar = self.convert_to_ascii(value)
                        hex_object_code |= int(temprar,16)

                    else:
                        hex_object_code |= int(inst['operand'])
                        print(str(hex(hex_object_code))[2:].zfill(6))

            elif inst['type'] == 1:
                hex_object_code = 0x00
                hex_object_code |= self.opcode.get(temp)

            elif inst['type'] == 2:
                hex_object_code = 0x0000
                opcode = int('0x' + self.opcode[inst['opcode']], 0)
                hex_object_code |= (opcode << 8)
                operand = inst['operand']
                if operand.find(",") == -1:
                    if self.reg_num.get(operand):
                        hex_object_code |= (self.reg_num.get(operand) << 4)
                else:
                    string = operand.split(",")
                    hex_object_code |= self.reg_num.get(string[0]) << 4
                    hex_object_code |= self.reg_num.get(string[1])

            elif inst['type'] == 3:
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
                    elif 0 <= operand_address - self.base_reg <= 4095:
                        if self.base_flag and self.base_reg:
                            hex_object_code |= 0x004000
                            hex_object_code |= (operand_address - self.base_reg)

                    else:
                        print('operand is out of range of PC and Base relative')
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
                    elif 0 <= operand_address - self.base_reg <= 4095:
                        if self.base_flag and self.base_reg:
                            hex_object_code |= 0x004000
                            hex_object_code |= (operand_address - self.base_reg)
                    else:
                        print('operand is out of range of PC and Base relative')
                        continue

            elif inst['type'] == 4:
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
