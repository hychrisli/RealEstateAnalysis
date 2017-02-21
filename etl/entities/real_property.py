import re


class RealProperty:
    ONE_ACRE = 43560.0
    CITY_SIZE = 15000.0

    def __init__(self, json_item):
        self.mls_id = str(json_item['MLSNumber'])
        self.zipcode = str(json_item['postalCode'])
        self.city = str(json_item['cityPostalName']).capitalize()
        self.addr = str(json_item['filteredAddress'])
        self.beds = RealProperty.__extract_int__(json_item['beds'])
        (self.full_baths,  self.part_baths) = RealProperty.__extract_bath_num__(json_item['baths'])
        self.struct_sqft = RealProperty.__extract_float__(json_item['structureSqFt'])
        (self.lot_size, self.lot_size_unit) = RealProperty.__process_lot_size__(json_item['lotSizeArea'])
        self.year_built = RealProperty.__extract_int__(json_item['yearBuilt'])
        self.list_price = float(json_item['listSalePrice'])
        self.list_status = str(json_item['listingStatus'])
        self.url = str(json_item['siteMapDetailUrlPath'])

    def print_details(self):
        print(self.mls_id)
        print(self.addr + ", " + self.city + ", " + self.zipcode)
        print("price: $" + str(self.list_price) + " | built: " + str(self.year_built))
        print(str(self.beds) + " beds | "
              + str(self.full_baths) + " full baths | "
              + str(self.part_baths) + " part baths ")
        print("structure: " + str(self.struct_sqft) + " sqft | lot: "
              + str(self.lot_size) + " " + self.lot_size_unit + "\n")

    @staticmethod
    def __extract_int__(json_value):
        val_str = str(json_value).replace(',', '')
        int_str = re.sub('[^0-9]', '', val_str)
        # print ("int: " + str(json_value))
        # print (int_str)
        if not int_str:
            return None
        else:
            return int(int_str)

    @staticmethod
    def __extract_float__(json_value):
        val_str = str(json_value).replace(',', '')
        float_lst = re.findall(r'[-+]?\d*\.\d+|\d+', val_str)
        # print ("float: " + str(json_value))
        # print (float_lst)
        if not float_lst:
            return float('NAN')
        else:
            return float(float_lst[0])

    @staticmethod
    def __extract_bath_num__(json_value):
        val_lst = str(json_value).lower().split('/')
        full_bath_num = None
        part_bath_num = 0
        if len(val_lst) > 0:
            if 'full' in val_lst[0]:
                full_bath_num = RealProperty.__extract_int__(val_lst[0])
                if len(val_lst) > 1:
                    part_bath_num = RealProperty.__extract_int__(val_lst[1])
            else:
                part_bath_num = RealProperty.__extract_int__(val_lst[0])
        return full_bath_num, part_bath_num

    @staticmethod
    def __process_lot_size__(json_value):
        var_str = str(json_value).lower()
        lot_size = RealProperty.__extract_float__(json_value)
        lot_size_unit = "sqft"
        if "acre" in var_str:
            lot_size_unit = "acres"
            if lot_size > RealProperty.CITY_SIZE: # Wrong Input Unit
                lot_size_correct = lot_size / RealProperty.ONE_ACRE
                lot_size = lot_size_correct
        elif lot_size > RealProperty.ONE_ACRE:
            lot_size_acre = lot_size / RealProperty.ONE_ACRE
            lot_size = round(lot_size_acre, 2)
            lot_size_unit = "acres"

        return lot_size, lot_size_unit
