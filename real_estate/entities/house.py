

class House:

    def __init__(self):
        self.addr = ''
        self.price = 0
        self.type = ''
        self.beds = 0
        self.baths = 0
        self.sqft = 0
        self.sqftlot = 0

    def print_details(self):
        print(self.addr)
        print(self.price)
        print(str(self.type) + " | " + str(self.beds) + " beds | " + str(self.baths) + "baths")
        print(str(self.sqft) + " sqft | " + str(self.sqftlot) + " lotsqft\n")
