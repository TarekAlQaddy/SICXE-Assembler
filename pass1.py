from math import log2, ceil


class Pass1:

    def __init__(self, optab):
        self.SYMTAB = {}
        self.OPTAB = optab
        self.LOCCTR = 0
        self.start_address = 0
        self.end_address = 0
        self.line_no = 0
        self.prog_len = 0
        self.instructions = []
        self.errors = []
        self.registers = ['a', 'l', 'pc', 'sw', 'b', 's', 't', 'f']
        self.final = []
        self.baseflag = False

    def start(self, file_name):
        file = open(file_name, 'r')
        str1 = file.read()
        self.instructions = str1.split('\n')
        self.start_address = self.start_handle(self.instructions[0])
        self.LOCCTR = self.start_address
        if len(self.errors) > 0:
            print(self.errors[0])
            return
        self.parse()
        self.print_errors()

    def start_handle(self, start_inst):
        """
        returns the address of the first line in program
        """
        if start_inst[9:14].lower().strip() == 'start':
            start_add = start_inst[17:34]
            start_add = start_add.strip()
            return int(start_add, 16)
        else:
            self.errors.append("No START at begin of the program")

    def is_reg(self, str):
        if str in self.registers:
            return True
        return False

    def end_handle(self, opcode):
        if opcode == 'end':
            self.end_address = self.LOCCTR
            self.prog_len = self.calc_prog_len()
        else:
            self.errors.append("Error: No end instruction found in your code!")

    def calc_prog_len(self):
        return self.end_address-self.start_address

    def parse(self):
        for index, inst in enumerate(self.instructions[1:]):
            # case of comment
            if inst[0].strip() == '.':
                print(inst)
                continue

            label = inst[0:7].strip().lower()
            opcode = inst[9:14].strip().lower()
            operand = inst[17:34].strip().lower()

            # label handling
            label_flag = None
            if label != "":
                if not self.SYMTAB.get(label):
                    label_flag = True
                    self.SYMTAB[label] = self.LOCCTR
                else:
                    label_flag = False
                    self.errors.append("Error: Label defined more than once")

            #end handling
            if index == len(self.instructions)-2:
                self.end_handle(opcode)
                self.print_line(inst)
                return
            if opcode == "end":
                print("Error: End found in middle of instructions")
                return

            # opcode handling if not in OPTAB
            temp = opcode
            if temp[0] == '+':
                temp = temp[1:]
            if not self.OPTAB.get(temp):
                self.errors.append("Error: No such opcode")
                continue

            self.print_line(inst)

            temp_dict = {}
            temp_dict["opcode"] = opcode
            temp_dict["operand"] = operand
            if label_flag:
                temp_dict["label"] = label
            else:
                temp_dict["label"] = None
            temp_dict["locctr"] = self.LOCCTR

            f_type = Pass1.locctr_increamenter(opcode, operand)
            temp_dict["type"] = f_type[0]
            temp_dict["is_dir"] = f_type[1]

            self.final.append(temp_dict)

            self.LOCCTR += f_type[0]
            self.line_no += 1

    @staticmethod
    def locctr_increamenter(opcode, operand):
        """
        returns the number of bytes to be increamented by LOCCTR and if the opcode is assembler directive or not
        :return: [no_of_bytes, is_directive?]
        """
        if opcode =="base":
            return [0,True]
        if opcode == "resw":
            temp = int(operand) * 3
            return [temp, True]
        if opcode == "word":
            return [3, True]
        if opcode == "byte":
            value = operand.partition("'")[-1].rpartition("'")[0]
            temp = len(value)
            if operand[0].lower() == 'x':
                if temp % 2 == 0:
                    return [temp // 2, True]
                else:
                    return [(temp + 1) // 2, True]
            elif operand[0].lower() == 'c':
                return [temp, True]
            else:
                no_of_bits = ceil(log2(int(operand)))
                bytes = ceil(no_of_bits/8)
                return [bytes, True]
        if opcode == "resb":
            value = int(operand)
            return [value, True]
        if opcode.find('+') != -1:
            return [4, False]
        if operand.find(",") != -1:
            str = operand.split(",")
            if str[1].lower() == 'x':
                return [3, False]
            return [2, False]
        if opcode == 'clear' or opcode == 'svc' or opcode == 'tixr':
            return [2, False]
        if operand.isspace():
            return [1, False]

        return [3, False]

    def print_line(self, inst):
        print(self.line_no, ' ', hex(self.LOCCTR), ' ', inst)
        for i in self.errors:
            print(i)
        self.errors = []

    def print_errors(self):
        if len(self.errors) >= 1:
            for error in self.errors:
                print(error)
