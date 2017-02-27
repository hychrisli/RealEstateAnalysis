import re
from datetime import datetime


class PropAddrHistEvent:

    def __init__(self):
        self.prop_addr_id = ''
        self.event_date = ''
        self.event = ''
        self.price = 0
        self.price_sqft = 0

    def set_price(self, val_str):
        self.price = PropAddrHistEvent.__extract_number__(val_str)

    def set_price_sqft(self, val_str):
        self.price_sqft = PropAddrHistEvent.__extract_number__(val_str)

    def set_date(self, val_str):
        self.event_date = datetime.strptime(val_str, '%m/%d/%Y').date()

    def print_hist(self):
        print (str(self.prop_addr_id) + ' | ' + str(self.event_date) + " | " + self.event +
               " | " + str(self.price) + " | " + str(self.price_sqft))

    @staticmethod
    def __extract_number__(val_str):
        num_str = val_str.replace(',','')
        float_lst = re.findall(r'[-+]?\d*\.\d+|\d+', num_str)
        if not float_lst:
            return None
        else:
            return round(float(float_lst[0]), 2)
