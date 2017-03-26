def start_handle(str):
    """
    returns the address of the first line in program
    """
    if str[9:14].lower() == 'START':
        start_add = str[17:34]
        start_add = start_add.strip()
        return int(start_add, 16)
    else:
        #TODO: handle error end the program
        print("No START at begin of the program")

#TODO: add format handling function