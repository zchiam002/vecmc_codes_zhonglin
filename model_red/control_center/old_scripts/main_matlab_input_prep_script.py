##This script will prepare the inputs for matlab optimizers

import sys
sys.path.append('C:\\Optimization_zlc\\master_level\\Matlab_Optimizers\\Fmincon\\')
from fmincon_prep_values import fmincon_prep_values
#from lin_prog_run import lin_prog_run


##Directory of filed 
mdv = 'C:\\Optimization_zlc\\input_data\\master_decision_variables.csv'
wd = 'C:\\Optimization_zlc\\input_data\\weather_data_day_170816.csv'
dd = 'C:\\Optimization_zlc\\input_data\\la_marina_demand_day_170816.csv'


##Define the input considerations 
multi_time = 1

fmincon_prep_values(multi_time, mdv, wd, dd)

##Running the slave optimization only

#obj_value, util = lin_prog_run()

#print(obj_value)
#print(util)
#print(master_slave_var)
#print(allm_var)