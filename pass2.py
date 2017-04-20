class Pass2:
    def __init__(self):
        self.SYMTAB = {}
        self.table = []
        self.opcode = {}
        self.reg_num = {'a': 0x00, 'x': 0x01, 'l': 0x02, 'pc': 0x08, 'sw': 0x09, 'b': 0x03, 's': 0x04, 't': 0x05,
                        'f': 0x06}
        self.base_flag = False
        self.base_reg = None
        self.prog_len = 0
        self.start_add = 0
        self.first_exec = ''
        self.name = ''
        self.final = []

    def start(self, table, SYMTAB, tab, start_add, prog_len, first_exec, name):
        self.opcode = tab
        self.SYMTAB = SYMTAB
        self.table = table
        self.prog_len = prog_len
        self.start_add = start_add
        self.first_exec = first_exec
        self.name = name

        self.parse()

    def convert_to_ascii(self, text):
        return "".join("{:02x}".format(ord(c)) for c in text)

    def modify_final(self):
        """
        modifies self.final array to have the HTME record
        :return:
        """
        temp_len = 60
        length_list1 = []

        # pre fill length_list1 with T lengths that will be put in HTME
        for inst in self.table:
            if temp_len - len(inst['objcode']) < 0 or inst['opcode'] == 'resw' or inst['opcode'] == 'resb':
                length_list1.append((60-temp_len) // 2)
                temp_len = 60
                if not (inst['opcode'] == 'resw' or inst['opcode'] == 'resb'):
                    temp_len -= len(inst['objcode'])
            else:
                temp_len -= len(inst['objcode'])
        length_list1.append((60 - temp_len) // 2)

        # remove zeros
        length_list = []
        for i in length_list1:
            if i == 0:
                continue
            length_list.append(i)

        self.final.append('H ' + self.name + ' ' + hex(self.start_add)[2:] + ' ' + hex(self.prog_len)[2:] + '\n')
        self.final.append('T ' + hex(self.start_add)[2:].zfill(6) + ' ' + hex(length_list[0])[2:].zfill(2) + ' ')

        temp_len = 60
        index = 1
        flag = False
        for inst in self.table:
            if inst['opcode'] == 'resw' or inst['opcode'] == 'resb':
                if self.final[-1] == 'T ':
                    continue
                self.final.append('\n')
                self.final.append('T ')
                flag = True
                continue
            if temp_len - len(inst['objcode']) < 0:
                self.final.append('\n')
                self.final.append('T ' + hex(inst['locctr'])[2:].zfill(6) + ' ' + hex(length_list[index])[2:].zfill(2) + ' ')
                index += 1
                temp_len = 60

            if flag:
                self.final.append(hex(inst['locctr'])[2:].zfill(6) + ' ' + hex(length_list[index])[2:].zfill(2) + ' ')
                index += 1
                temp_len = 60

            self.final.append(inst['objcode'] + ' ')
            temp_len -= len(inst['objcode'])
            flag = False

        self.final.append('\n')

        # TODO: add Modification records


        first_ex = 0
        try:
            first_ex = hex(int(self.SYMTAB[self.first_exec]))[2:]
            self.final.append('E ' + first_ex)
        except KeyError:
            print("label of first excecutable instruction is not pre defined !")
            self.final.append('E ' + hex(self.start_add)[2:])

    def write_to_htme(self, filename):
        file = open(filename, 'w')

        for str in self.final:
            file.write(str)

    def parse(self):

        for index, inst in enumerate(self.table):
            hex_object_code = 0
            str_object_code = ''

            temp = inst['opcode']
            if temp == 'ldb':
                self.base_flag = True
            if temp == 'base' and self.base_flag:
                try:
                    self.base_reg = self.SYMTAB[inst['operand']]
                except KeyError:
                    print("{} Label not defined!".format(inst['operand']))

            if inst['is_dir']:
                if temp == 'resw' or temp == 'resb':
                    self.table[index]['objcode'] = ''
                    continue

                if inst['opcode'] == 'word':
                    str_object_code = hex(int(inst['operand']))[2:].zfill(6)

                elif temp == 'byte':
                    if inst['operand'][0] == 'x':
                        value = inst['operand'].partition("'")[-1].rpartition("'")[0]
                        len_temp = len(value)
                        if len_temp % 2 == 0:
                            str_object_code = value
                        else:
                            str_object_code = value.zfill(len_temp + 1)
                    elif inst['operand'][0] == 'c':
                        value = inst['operand'].partition("'")[-1].rpartition("'")[0]
                        str_object_code = self.convert_to_ascii(value)

                    else:
                        str_object_code = hex(int(inst['operand']))[2:]
                        if len(str_object_code) % 2 == 1:
                            str_object_code = str_object_code.zfill(len(str_object_code) + 1)
                self.table[index]['objcode'] = str_object_code

            elif inst['type'] == 1:
                hex_object_code = self.opcode.get(temp)
                self.table[index]['objcode'] = hex(hex_object_code)[2:].zfill(2)

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
                self.table[index]['objcode'] = hex(hex_object_code)[2:].zfill(4)

            elif inst['type'] == 3:
                hex_object_code = 0x000000

                opcode = int('0x' + self.opcode[inst['opcode']], 0)
                hex_object_code = (hex_object_code | opcode) << 16
                operand = inst['operand']
                locctr = inst['locctr']

                if (operand.find(',') != -1) and (operand[-1] == 'x'):
                    hex_object_code |= 0x008000
                    operand = operand[:len(operand) - 2]
                if inst['opcode'] == 'rsub':
                    hex_object_code = 0x4F0000
                elif inst['operand'][0] == '@':
                    hex_object_code |= 0x020000
                    try:
                        operand_address = self.SYMTAB[operand[1:]]
                    except KeyError:
                        print("{} label not defined !".format(operand[1:]))
                        continue

                    if -2048 <= operand_address - locctr - 3 <= 2047:
                        hex_object_code |= 0x002000
                        if operand_address >= locctr + 3:
                            hex_object_code |= (operand_address - locctr - 3)
                        else:
                            tows_comp = operand_address - locctr - 3 + 0xfff + 1
                            hex_object_code |= tows_comp
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
                    except ValueError:
                        imm_flag = False

                    if imm_flag:
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
                            if operand_address >= locctr + 3:
                                hex_object_code |= (operand_address - locctr - 3)
                            else:
                                tows_comp = operand_address - locctr - 3 + 0xfff + 1
                                hex_object_code |= tows_comp
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
                        if operand_address >= locctr + 3:
                            hex_object_code |= (operand_address - locctr - 3)
                        else:
                            tows_comp = operand_address - locctr - 3 + 0xfff + 1
                            hex_object_code |= tows_comp
                    elif 0 <= operand_address - self.base_reg <= 4095:
                        if self.base_flag and self.base_reg:
                            hex_object_code |= 0x004000
                            hex_object_code |= (operand_address - self.base_reg)
                    else:
                        print('operand is out of range of PC and Base relative')
                        continue
                self.table[index]['objcode'] = hex(hex_object_code)[2:].zfill(6)

            elif inst['type'] == 4:
                hex_object_code = 0x00000000
                opcode = int('0x' + self.opcode[inst['opcode'][1:]], 0)
                hex_object_code |= (opcode << 24)

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
                self.table[index]['objcode'] = hex(hex_object_code)[2:].zfill(8)
        self.modify_final()
