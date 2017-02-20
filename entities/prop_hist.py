import re


class PropHist:

    def __init__(self):
        self.date = ''
        self.event = ''
        self.price = 0
        self.price_sqft = 0

    def set_price(self, val_str):
        self.price = PropHist.__extract_number__(val_str)

    def set_price_sqft(self, val_str):
        self.price_sqft = PropHist.__extract_number__(val_str)

    def print_hist(self):
        print (self.date + " | " + self.event + " | " + str(self.price) + " | " + str(self.price_sqft))

    @staticmethod
    def __extract_number__(val_str):
        num_str = val_str.replace(',','')
        float_lst = re.findall(r'[-+]?\d*\.\d+|\d+', num_str)
        if not float_lst:
            return float('NAN')
        else:
            return round(float(float_lst[0]), 2)
