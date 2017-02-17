from controllers.mls_controller import CrawlRunner
from db_ops.mysql_dao.mls_type_dao import MlsTypeDao
from db_ops.etl.property_etl import PropertyEtl


etl_cnx = PropertyEtl()
fdbk_incr = etl_cnx.call_sp_property_incr_insert()
print (fdbk_incr)

runner = CrawlRunner()
runner.run()

fdbk_del = etl_cnx.call_sp_prop_del_mls_excld()
print (fdbk_del)
fdbk_fact = etl_cnx.call_sp_property_fact_insert()
print (fdbk_fact)
# cnx = MlsTypeDao()
# res = cnx.get_prop_types()
# print (res)
