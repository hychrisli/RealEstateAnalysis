from etl.dao.prop_addr_dao import PropAddrDao
from crawlers.selnms.prop_addr_url_selnm import PropAddrUrlSelnm

url_selnm = PropAddrUrlSelnm()
url_selnm.upd_urls()

# 2017-02-21
# addr_cnx = PropAddrDao()
# addr_cnx.init_cleanup()
# addr_cnx.add_addrs()
