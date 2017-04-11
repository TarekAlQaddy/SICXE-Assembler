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
        self.registers =['a','l','pc','sw','b','s','t','f']

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

    def is_reg(self,str):
        if(str in self.registers):
            return True
        return False

    def end_handle(self,opcode):
        if opcode=='end':
            self.end_address=self.LOCCTR
            self.prog_len=self.calc_prog_len()
        else:
            self.errors.append("Error: No end instruction found in your code!")


    def calc_prog_len(self):
        return self.end_address-self.start_address




    def parse(self):
        for inst in self.instructions[1:]:
            # case of comment
            if inst[0].strip() == '.':
                print(inst)
                continue

            label = inst[0:7].strip().lower()
            opcode = inst[9:14].strip().upper()
            operand = inst[17:34].strip().lower()

            # label handling
            if label != "":
                if not self.SYMTAB.get(label):
                    self.SYMTAB[label] = self.LOCCTR
                else:
                    self.errors.append("Error: Label defined more than once")

            # opcode handling if not in OPTAB
            if not self.OPTAB.get(opcode):
                self.errors.append("Error: No such opcode")
                continue

            self.print_line(inst)
            if self.instructions.index(inst)==len(self.instructions):
                self.end_handle(opcode)
                return
            if opcode =="end":
                self.errors.append("End found ")
                return

            self.LOCCTR += self.locctr_increamenter(opcode, operand)
            #handle end bta3 nbreak
            self.line_no += 1


    def locctr_increamenter(self,opcode, operand):
        # if opcode=='end':
        #     self.end_address=self.LOCCTR
        #     return  0
        # elif:
        #     self.errors.append("Error: No end instruction found in your code!")

        if opcode.lower() == "resw":
            temp = int(operand) * 3
            return temp
        if opcode.lower() == "word":

         return 3
        if opcode.lower() == "byte":
            value = operand.partition("'")[-1].rpartition("'")[0]
            temp = len(value)
            if operand[0].lower() == 'x':
                if temp % 2 == 0:
                    return temp // 2
                else:
                    return (temp + 1) // 2
            elif operand[0].lower() == 'c':
                return temp
        if opcode.lower() == "resb":
            value = int(operand)
            return value
        if opcode.lower() == "end":
            return 0
        if opcode.find('+') != -1:
            return 4
        if operand.find(",") != -1:
            str = operand.split(",")
            if str[1].lower() == 'x':
                return 3
            return 2
        if operand.isspace():
            return 1
        else:
            return 3

    def print_line(self, inst):
        print(inst)
        for i in self.errors:
            print(i)
        self.errors = []
