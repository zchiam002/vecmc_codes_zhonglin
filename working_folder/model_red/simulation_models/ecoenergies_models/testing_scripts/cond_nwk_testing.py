##This is the testing script for the network models 

import sys 
sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
from cond_network_models import cond_nwk_org
from cond_network_models import cond_nwk_piecewise_pressure
from cond_network_models import cond_nwk_piecewise_pressure_reg_pumpnwk
from cond_network_models import cond_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp
import pandas as pd 

ch1_flow = 0                                         ##(m3/h)
ch1_temp = 35 + 273.15                                       ##(K)
ch2_flow = 1476                                              ##(m3/h)
ch2_temp = 35 + 273.15                                       ##(K)
ch3_flow = 1476                                              ##(m3/h)
ch3_temp = 35 + 273.15                                       ##(K)
split_to_dist_nwk = 70                                      ##(%)
split_to_common_pipe = 100 - split_to_dist_nwk              ##(%)

##Processing data into input form 
chiller_input = pd.DataFrame(columns = ['Name', 'Value'])
data_temp = ['chiller_1_flow', ch1_flow]
temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
chiller_input = chiller_input.append(temp_df, ignore_index = True)
data_temp = ['chiller_1_supply_temperature', ch1_temp]
temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
chiller_input = chiller_input.append(temp_df, ignore_index = True)
data_temp = ['chiller_2_flow', ch2_flow]
temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
chiller_input = chiller_input.append(temp_df, ignore_index = True)
data_temp = ['chiller_2_supply_temperature', ch2_temp]
temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
chiller_input = chiller_input.append(temp_df, ignore_index = True)
data_temp = ['chiller_3_flow', ch3_flow]
temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
chiller_input = chiller_input.append(temp_df, ignore_index = True)
data_temp = ['chiller_3_supply_temperature', ch3_temp]
temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
chiller_input = chiller_input.append(temp_df, ignore_index = True)

num_cooling_towers = 5
steps = 4
bilinear_pieces = 50
tcond_in = 45 + 273.15                                                          ##It is temporary used as the upper limit of tevap_out

##Calling the original model 
#return_values_1_dict, return_values_1_df = cond_nwk_org(chiller_input, num_cooling_towers)

##Calling the pwl model 
#return_values_2_dict, return_values_2_df = cond_nwk_piecewise_pressure(chiller_input, num_cooling_towers, steps)

##Calling pwl and regression model 
return_values_3_dict, return_values_3_df = cond_nwk_piecewise_pressure_reg_pumpnwk(chiller_input, num_cooling_towers, steps)

##Calling the pwl and regression and bilinear model 
#return_values_4_dict, return_values_4_df = cond_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp(chiller_input, num_cooling_towers, steps, tcond_in, bilinear_pieces)

#print(return_values_1_df)
#print(return_values_2_df)
print(return_values_3_df)
#print(return_values_4_df)