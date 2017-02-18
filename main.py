from controllers.mls_controller import ApiSearchRunner
from controllers.mls_controller import PropPageRunner
from db_ops.etl.property_etl import PropertyEtl

import os

pid = os.fork()
if pid == 0:
    print ("api_search_runner")
    api_search_runner = ApiSearchRunner()
    api_search_runner.run()
    os._exit(0)

os.waitpid(pid, 0)
print ("Main: " + str(os.getpid()))

print ("call_sp_property_incr_insert")
etl_cnx = PropertyEtl()
etl_cnx.call_sp_property_incr_insert()


print ("prop_page_runner")
prop_page_runner = PropPageRunner()
prop_page_runner.run()

etl_cnx.call_sp_prop_del_mls_excld()
print ("call_sp_prop_del_mls_excld")
etl_cnx.call_sp_property_fact_insert()
print ("call_sp_property_fact_insert")
etl_cnx.call_sp_property_dim_upd()
print ("call_sp_property_dim_upd")
