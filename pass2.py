import binascii
class Pass2:

    def __init__(self):
        self.SYMTAB = {}
        self.Table= []
        self.Opcode={}
        self.RegNum={'a':0,'x':1,'l':2,'pc':8,'sw':9,'b':3,'s':4,'t':5,'f':6}

    def start(self, table, SYMTAB , txtfile):
        with open(txtfile) as f:
            for line in f:
                (key, val) = line.split()
                self.Opcode[key] = val



        self.SYMTAB = SYMTAB
        self.Table = table
        self.parse()


    def getInstructionIndex(self,str):
        for i in range(len(self.Opcode)):
            if self.Opcode[i]["memonic"]== str:
                return i
        return -1

    def hexaToBinaryConversion(self,num,length):
        my_hexdata = num
        scale = 16  ## equals to hexadecimal
        return bin(int(my_hexdata, scale))[2:].zfill(length)

    def parse(self):

        for i in range(len(self.Table)):
            temp_object_code = ''
            print(temp_object_code)
            if self.Table[i]['opcode'] == 'byte' or self.Table[i]['opcode'] == 'word' or self.Table[i][
                'opcode'] == 'resw' or self.Table[i]['opcode'] == 'resb':
                # handle
                continue
            temp_object_code += self.hexaToBinaryConversion(str(self.Opcode.get(self.Table[i]["opcode"])), 8)
            if self.Table[i]['type']==1:
                continue
            if self.Table[i]['type']==2:
                operand = self.Table[i]['operand']
                if self.Table[i]["operand"].find(",")==-1:
                    temp_object_code+='0000'
                    if(self.RegNum.get(operand)):
                        print(self.RegNum.get(operand))
                        temp_object_code+=self.hexaToBinaryConversion(self.RegNum.get(operand),4)
                        print(self.Table[i]["opcode"])
                        print(temp_object_code)
                        continue
                    else:

                        temp_object_code+=self.hexaToBinaryConversion((operand),8)
                        print(temp_object_code)
                        continue
                else:
                    string = operand.split(",")

                    print(temp_object_code)
                    temp_object_code+=self.hexaToBinaryConversion(repr(self.RegNum.get(string[0])), 4)

                    temp_object_code+=self.hexaToBinaryConversion(repr(self.RegNum.get(string[1])), 4)
                    print(temp_object_code +"\n")
                    continue
                #fadel format 3 w 4




