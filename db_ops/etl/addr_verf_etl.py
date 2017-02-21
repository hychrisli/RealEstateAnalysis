from pyusps import address_information
import os


class AddrVerfEtl:
    def __init__(self):
        self.usps_id = os.environ['USPS_ID']

    def verify(self, addrs):
        res = address_information.verify(self.usps_id, *addrs)
        return res

