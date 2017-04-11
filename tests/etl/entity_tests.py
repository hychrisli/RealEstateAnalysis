from tests.abstr_tests import AbstrTest
from etl.routines.addr_verf_etl import AddrVerfEtl
from etl.entities.prop_addr_incr_lst import PropAddrIncrLst
from pyusps.address_information import OrderedDict


class EntityTests(AbstrTest):
    def test_prop_addr_incr_lst(self):

        sel_rows = [
            ('BE40776509', '132', '1327 Gwerder Ct', 'Tracy', 'CA', 'http://www.mlslistings.com/property/be40776509/'),
            ('ML81579690', '96', '230 Forrester RD', 'Los Gatos', 'CA',
             'http://www.mlslistings.com/property/ml81579690/')]

        test_addr_dict_lst = [dict([
            ('address', '1327 Gwerder Ct'),
            ('city', 'Tracy'),
            ('state', 'CA'),
        ]), dict([
            ('address', '230 Forrester RD'),
            ('city', 'Los Gatos'),
            ('state', 'CA'),
        ])]

        test_incr_inserts = \
            [{'url': 'http://www.mlslistings.com/property/be40776509/', 'area_id': '132', 'mls_id': 'BE40776509',
              'addr': '1327 GWERDER CT'},
             {'url': 'http://www.mlslistings.com/property/ml81579690/', 'area_id': '96', 'mls_id': 'ML81579690',
              'addr': '230 FORRESTER RD'}]

        prop_addr_incr_lst = PropAddrIncrLst()
        prop_addr_incr_lst.parse(sel_rows)
        try:
            incr_inserts = prop_addr_incr_lst.get_incr_inserts()
            self.assertEqual(incr_inserts, test_incr_inserts)
            self.success(prop_addr_incr_lst.get_incr_inserts.__name__)
        except AssertionError:
            self.failure(prop_addr_incr_lst.get_incr_inserts.__name__)

