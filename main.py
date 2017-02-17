from controllers.mls_controller import CrawlRunner
from db_ops.mysql_dao.mls_type_dao import MlsTypeDao
from db_ops.etl.property_etl import PropertyEtl


etl_cnx = PropertyEtl()
etl_cnx.call_sp_property_incr_insert()

runner = CrawlRunner()
runner.run()

etl_cnx.call_sp_prop_del_mls_excld()
# cnx = MlsTypeDao()
# res = cnx.get_prop_types()
# print (res)
