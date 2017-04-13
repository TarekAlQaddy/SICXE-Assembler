class Pass2:

    def __init__(self):
        self.SYMTAB = {}
        self.instructions = []

    def start(self, inst, SYMTAB):
        self.SYMTAB = SYMTAB
        self.instructions = inst

        self.parse()

    def parse(self):
        file = open("HTME.txt", "w")

        file.write("testing..")

        #loop here

        file.close()
