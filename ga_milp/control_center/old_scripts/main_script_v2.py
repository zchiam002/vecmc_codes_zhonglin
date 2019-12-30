##This script will activate the master-slave optimization excercise
##VERSION 2

import sys
sys.path.append('C:\\Optimization_zlc\\master_level\\')
sys.path.append('C:\\Optimization_zlc\\slave_level_models\\slave_convex_v1\\')
from multi_objective_master_backend_v2 import multi_objective_master_backend_v2


##Directory of filed 
mdv = 'C:\\Optimization_zlc\\input_data\\master_decision_v1\\master_decision_variables.csv'
wd = 'C:\\Optimization_zlc\\input_data\\master_decision_v1\\weather_data_day_170816.csv'
dd = 'C:\\Optimization_zlc\\input_data\\master_decision_v1\\la_marina_demand_day_170816.csv'


##Define the input considerations 
multi_time = 1

multi_objective_master_backend_v2(multi_time, mdv, wd, dd)

##Running the slave optimization only

#obj_value, util = lin_prog_run()

#print(obj_value)
#print(util)
#print(master_slave_var)
#print(allm_var)


