##This script will activate the master-slave optimization excercise

import sys
sys.path.append('C:\\Optimization_zlc\\master_level\\')
sys.path.append('C:\\Optimization_zlc\\slave_level_models\\glpk_v1\\')
from multi_objective_master_backend import multi_objective_master_backend
#from lin_prog_run import lin_prog_run


##Directory of filed 
mdv = 'C:\\Optimization_zlc\\input_data\\nsgaII_glpk_v1\\master_decision_variables.csv'
wd = 'C:\\Optimization_zlc\\input_data\\nsgaII_glpk_v1\\weather_data_day_170816.csv'
dd = 'C:\\Optimization_zlc\\input_data\\nsgaII_glpk_v1\\la_marina_demand_day_170816.csv'


##Define the input considerations 
multi_time = 1

multi_objective_master_backend(multi_time, mdv, wd, dd)

##Running the slave optimization only

#obj_value, util = lin_prog_run()

#print(obj_value)
#print(util)
#print(master_slave_var)
#print(allm_var)


