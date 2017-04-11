import re
from datetime import datetime,date


class PropAddrHistEvent:

    def __init__(self):
        self.prop_addr_id = ''
        self.event_date = date.today()
        self.event = ''
        self.price = 0
        self.price_sqft = 0

    def set_price(self, val_str):
        self.price = PropAddrHistEvent.__extract_number__(val_str)

    def set_event(self, val_str):
        if str(val_str).lower() == 'sold':
            self.event = 'Sold'
        else:
            self.event = 'Listed'

    def to_string(self):
        return (str(self.prop_addr_id) + '|' + str(self.event_date) + '|' + self.event +
                '|' + str(self.price))

    @staticmethod
    def __extract_number__(val_str):
        num_str = val_str.replace(',','')
        float_lst = re.findall(r'[-+]?\d*\.\d+|\d+', num_str)
        if not float_lst:
            return None
        else:
            return round(float(float_lst[0]), 2)
