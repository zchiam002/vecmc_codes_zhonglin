##This section validates the outputs of the various relaxed forms of the chiller models 
import pandas as pd
import sys 
sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
from chiller_models import chiller_gnu 
from chiller_models import chiller_gnu_stepwise_cop
from chiller_models import chiller_gnu_stepwise_cop_lprelax
import matplotlib.pyplot as plt

##Validation for chiller 1 (2000kWh)

##Setting parameters
max_cap_1 = 2000
b0_1 = 0.123020043325872
b1_1 = 1044.79734873891
b2_1 = 0.0204660495029597
reg_cst_1 = [b0_1, b1_1, b2_1]
qc_coeff_1 = 1.09866273284186
steps = 4
bilinear_pieces = 12

##Loading the raw data 
chiller1_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\cleansed_data\\ch1_data_weather.csv')
dim_chiller1_data = chiller1_data.shape

##Initiating a DataFrame to hold output values 
output_values = pd.DataFrame(columns = ['Qe_org', 'Qe_m1', 'Qe_m2', 'Qe_m3', 'COP_org', 'COP_m1', 'COP_m2', 'COP_m3', 'E_org', 'E_m1', 'E_m2', 'E_m3', 
                                        'Tout_cond_org', 'Tout_cond_m1', 'Tout_cond_m2', 'Tout_cond_m3', 'instance_no'])
perc_difference = pd.DataFrame(columns = ['Qe_m1_%', 'Qe_m2_%', 'Qe_m3_%', 'COP_m1_%', 'COP_m2_%', 'COP_m3_%', 'E_m1_%', 'E_m2_%', 'E_m3_%',
                                          'Tout_cond_m1_%', 'Tout_cond_m2_%', 'Tout_cond_m3_%', 'instance_no'])

sum_e_m1_error = 0
sum_e_m2_error = 0
sum_e_m3_error = 0

for i in range(0, dim_chiller1_data[0]):
    
    perc_complete = i/dim_chiller1_data[0] * 100
    print('Processing... ' + str(perc_complete) + '%')
    
    ##Preparing values 
    Tin_evap_1 = chiller1_data['Tin_evap'][i] - 273.15
    Tout_evap_1 = chiller1_data['Tout_evap'][i] - 273.15
    Tin_cond_1 = chiller1_data['Tin_cond'][i] - 273.15
    mevap_1 = chiller1_data['mevap'][i]
    mcond_1 = chiller1_data['mcond'][i]
    mevap_t = 500
    mcond_t = 500
    twb = chiller1_data['T_WB'][i]

    ##Handling the original data 
    results_org = {}
    results_org['Cooling_load'] = chiller1_data['Qe'][i]
    results_org['Electricity_consumption'] = chiller1_data['E'][i]
    results_org['Tout_cond'] = chiller1_data['Tout_cond'][i]
    results_org['Coefficient_of_performance'] = chiller1_data['Qe'][i] / chiller1_data['E'][i]
    
    results_m1, results_m1_df = chiller_gnu(reg_cst_1, qc_coeff_1, Tin_evap_1, Tout_evap_1, Tin_cond_1, mevap_1, mcond_1, max_cap_1)
    results_m2, results_m2_df = chiller_gnu_stepwise_cop(reg_cst_1, qc_coeff_1, Tin_evap_1, Tout_evap_1, Tin_cond_1, mevap_1, mcond_1, max_cap_1, steps)
    results_m3, results_m3_df = chiller_gnu_stepwise_cop_lprelax(reg_cst_1, qc_coeff_1, Tin_evap_1, Tout_evap_1, Tin_cond_1, mevap_1, mcond_1, max_cap_1, steps, bilinear_pieces, mevap_t, mcond_t, twb)

    data_temp = [results_org['Cooling_load'], results_m1['Cooling_load'], results_m2['Cooling_load'], results_m3['Cooling_load'],
                 results_org['Coefficient_of_performance'], results_m1['Coefficient_of_performance'], results_m2['Coefficient_of_performance'], results_m3['Coefficient_of_performance'],
                 results_org['Electricity_consumption'], results_m1['Electricity_consumption'], results_m2['Electricity_consumption'], results_m3['Electricity_consumption'],
                 results_org['Tout_cond'], results_m1['Tout_cond'] + 273.15, results_m2['Tout_cond'] + 273.15, results_m3['Tout_cond'],
                 i]
    
    output_values_temp = pd.DataFrame(data = [data_temp], columns = ['Qe_org', 'Qe_m1', 'Qe_m2', 'Qe_m3', 'COP_org', 'COP_m1', 'COP_m2', 'COP_m3', 'E_org', 'E_m1', 'E_m2', 'E_m3', 
                                                                     'Tout_cond_org', 'Tout_cond_m1', 'Tout_cond_m2', 'Tout_cond_m3', 'instance_no'])
    output_values = output_values.append(output_values_temp, ignore_index = True)
    
    Qe_m1_perc = (results_m1['Cooling_load'] - results_org['Cooling_load']) / results_org['Cooling_load'] * 100
    Qe_m2_perc = (results_m2['Cooling_load'] - results_org['Cooling_load']) / results_org['Cooling_load'] * 100
    Qe_m3_perc = (results_m3['Cooling_load'] - results_org['Cooling_load']) / results_org['Cooling_load'] * 100
    COP_m1_perc = (results_m1['Coefficient_of_performance'] - results_org['Coefficient_of_performance']) / results_org['Coefficient_of_performance'] * 100
    COP_m2_perc = (results_m2['Coefficient_of_performance'] - results_org['Coefficient_of_performance']) / results_org['Coefficient_of_performance'] * 100 
    COP_m3_perc = (results_m3['Coefficient_of_performance'] - results_org['Coefficient_of_performance']) / results_org['Coefficient_of_performance'] * 100
    E_m1_perc = abs(results_m1['Electricity_consumption'] - results_org['Electricity_consumption']) / results_org['Electricity_consumption'] * 100
    E_m2_perc = abs(results_m2['Electricity_consumption'] - results_org['Electricity_consumption']) / results_org['Electricity_consumption'] * 100
    E_m3_perc = abs(results_m3['Electricity_consumption'] - results_org['Electricity_consumption']) / results_org['Electricity_consumption'] * 100
    Tout_cond_m1_perc = ((results_m1['Tout_cond'] + 273.15) - results_org['Tout_cond']) / results_org['Tout_cond'] * 100
    Tout_cond_m2_perc = ((results_m2['Tout_cond'] + 273.15) - results_org['Tout_cond']) / results_org['Tout_cond'] * 100
    Tout_cond_m3_perc = 'NaN'

    sum_e_m1_error = sum_e_m1_error + pow(E_m1_perc, 2)
    sum_e_m2_error = sum_e_m2_error + pow(E_m2_perc, 2)
    sum_e_m3_error = sum_e_m3_error + pow(E_m3_perc, 2)

    data_temp = [Qe_m1_perc, Qe_m2_perc, Qe_m3_perc, COP_m1_perc, COP_m2_perc, COP_m3_perc, E_m1_perc, E_m2_perc, E_m3_perc, Tout_cond_m1_perc,
                 Tout_cond_m2_perc, Tout_cond_m3_perc, i]
                 
    perc_difference_temp = pd.DataFrame(data = [data_temp], columns = ['Qe_m1_%', 'Qe_m2_%', 'Qe_m3_%', 'COP_m1_%', 'COP_m2_%', 'COP_m3_%', 'E_m1_%', 'E_m2_%', 'E_m3_%',
                                                                       'Tout_cond_m1_%', 'Tout_cond_m2_%', 'Tout_cond_m3_%', 'instance_no'])
    
    perc_difference = perc_difference.append(perc_difference_temp, ignore_index = True)
    
output_values.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_csv_files\\chiller1_models_output.csv')
perc_difference.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_csv_files\\chiller1_models_perc_diff.csv')

##processing RMSE
rmse_m1_e = sum_e_m1_error / dim_chiller1_data[0]
rmse_m1_e = pow(rmse_m1_e, 0.5)
rmse_m2_e = sum_e_m2_error / dim_chiller1_data[0]
rmse_m2_e = pow(rmse_m2_e, 0.5)
rmse_m3_e = sum_e_m3_error / dim_chiller1_data[0]
rmse_m3_e = pow(rmse_m3_e, 0.5)

print(rmse_m1_e, rmse_m2_e, rmse_m3_e)
sys.exit()

##Plotting graphs 

##Plotting Qe values 
plt.plot(output_values['instance_no'], output_values['Qe_org'], color='blue') 
plt.plot(output_values['instance_no'], output_values['Qe_m1'], color='green')
plt.plot(output_values['instance_no'], output_values['Qe_m2'], color='black')
plt.plot(output_values['instance_no'], output_values['Qe_m3'], color='red')
plt.xlabel('Instance')
plt.ylabel('Cooling Load (kWh)')
plt.show()

##Plotting individual Qe values 
plt.plot(output_values['instance_no'], output_values['Qe_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['Qe_m1'], color='green', label = 'Model 1')
plt.xlabel('Instance')
plt.ylabel('Cooling Load (kWh)')
plt.show()

plt.plot(output_values['instance_no'], output_values['Qe_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['Qe_m2'], color='black', label = 'Model 2')
plt.xlabel('Instance')
plt.ylabel('Cooling Load (kWh)')
plt.show()

plt.plot(output_values['instance_no'], output_values['Qe_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['Qe_m3'], color='red', label = 'Model 3')
plt.xlabel('Instance')
plt.ylabel('Cooling Load (kWh)')
plt.show()

##Plotting Qe percentage difference 
plt.plot(perc_difference['instance_no'], perc_difference['Qe_m1_%'], color='green')
plt.xlabel('Instance')
plt.ylabel('Model 1: Cooling Load % diff')
plt.show()
print('Model 1 mean = ' + str(perc_difference['Qe_m1_%'].mean()))

plt.plot(perc_difference['instance_no'], perc_difference['Qe_m2_%'], color='black')
plt.xlabel('Instance')
plt.ylabel('Model 2: Cooling Load % diff')
plt.show()
print('Model 2 mean = ' + str(perc_difference['Qe_m2_%'].mean()))

plt.plot(perc_difference['instance_no'], perc_difference['Qe_m3_%'], color='red')
plt.xlabel('Instance')
plt.ylabel('Model 3: Cooling Load % diff')
plt.show()
print('Model 3 mean = ' + str(perc_difference['Qe_m3_%'].mean()))
         
##Plotting COP values 
plt.plot(output_values['instance_no'], output_values['COP_org'], color='blue') 
plt.plot(output_values['instance_no'], output_values['COP_m1'], color='green')
plt.plot(output_values['instance_no'], output_values['COP_m2'], color='black')
plt.plot(output_values['instance_no'], output_values['COP_m3'], color='red')
plt.xlabel('Instance')
plt.ylabel('COP')
plt.show()

##Plotting individual COP values 
plt.plot(output_values['instance_no'], output_values['COP_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['COP_m1'], color='green', label = 'Model 1')
plt.xlabel('Instance')
plt.ylabel('COP')
plt.show()

plt.plot(output_values['instance_no'], output_values['COP_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['COP_m2'], color='black', label = 'Model 2')
plt.xlabel('Instance')
plt.ylabel('COP')
plt.show()

plt.plot(output_values['instance_no'], output_values['COP_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['COP_m3'], color='red', label = 'Model 3')
plt.xlabel('Instance')
plt.ylabel('COP')
plt.show()

##Plotting COP percentage difference 
plt.plot(perc_difference['instance_no'], perc_difference['COP_m1_%'], color='green')
plt.xlabel('Instance')
plt.ylabel('Model 1: COP % diff')
plt.show()
print('Model 1 mean = ' + str(perc_difference['COP_m1_%'].mean()))

plt.plot(perc_difference['instance_no'], perc_difference['COP_m2_%'], color='black')
plt.xlabel('Instance')
plt.ylabel('Model 2: COP % diff')
plt.show()
print('Model 2 mean = ' + str(perc_difference['COP_m2_%'].mean()))

plt.plot(perc_difference['instance_no'], perc_difference['COP_m3_%'], color='red')
plt.xlabel('Instance')
plt.ylabel('Model 3: COP % diff')
plt.show()
print('Model 3 mean = ' + str(perc_difference['COP_m3_%'].mean()))

##Plotting E values 
plt.plot(output_values['instance_no'], output_values['E_org'], color='blue') 
plt.plot(output_values['instance_no'], output_values['E_m1'], color='green')
plt.plot(output_values['instance_no'], output_values['E_m2'], color='black')
plt.plot(output_values['instance_no'], output_values['E_m3'], color='red')
plt.xlabel('Instance')
plt.ylabel('E (kWh)')
plt.show()

##Plotting individual E values 
plt.plot(output_values['instance_no'], output_values['E_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['E_m1'], color='green', label = 'Model 1')
plt.xlabel('Instance')
plt.ylabel('E (kWh)')
plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_images\\E_M1.png', dpi = 1000)
plt.show()

plt.plot(output_values['instance_no'], output_values['E_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['E_m2'], color='black', label = 'Model 2')
plt.xlabel('Instance')
plt.ylabel('E (kWh)')
plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_images\\E_M2.png', dpi = 1000)
plt.show()

plt.plot(output_values['instance_no'], output_values['E_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['E_m3'], color='red', label = 'Model 3')
plt.xlabel('Instance')
plt.ylabel('E (kWh)')
plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_images\\E_M3.png', dpi = 1000)
plt.show()

##Plotting E percentage difference 
plt.plot(perc_difference['instance_no'], perc_difference['E_m1_%'], color='green')
plt.xlabel('Instance')
plt.ylabel('Model 1: E % diff')
plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_images\\E_%M1.png', dpi = 1000)
plt.show()
print('Model 1 mean = ' + str(perc_difference['E_m1_%'].mean()))

plt.plot(perc_difference['instance_no'], perc_difference['E_m2_%'], color='black')
plt.xlabel('Instance')
plt.ylabel('Model 2: E % diff')
plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_images\\E_%M2.png', dpi = 1000)
plt.show()
print('Model 2 mean = ' + str(perc_difference['E_m2_%'].mean()))

plt.plot(perc_difference['instance_no'], perc_difference['E_m3_%'], color='red')
plt.xlabel('Instance')
plt.ylabel('Model 3: E % diff')
plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_images\\E_%M3.png', dpi = 1000)
plt.show()
print('Model 3 mean = ' + str(perc_difference['E_m3_%'].mean()))

##Plotting Tout_cond values 
plt.plot(output_values['instance_no'], output_values['Tout_cond_org'], color='blue') 
plt.plot(output_values['instance_no'], output_values['Tout_cond_m1'], color='green')
plt.plot(output_values['instance_no'], output_values['Tout_cond_m2'], color='black')
#plt.plot(output_values['instance_no'], output_values['Tout_cond_m3'], color='red')
plt.xlabel('Instance')
plt.ylabel('Tcond_out (K)')
plt.show()

##Plotting individual Tout_cond values 
plt.plot(output_values['instance_no'], output_values['Tout_cond_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['Tout_cond_m1'], color='green', label = 'Model 1')
plt.xlabel('Instance')
plt.ylabel('Tcond_out (K)')
plt.show()

plt.plot(output_values['instance_no'], output_values['Tout_cond_org'], color='blue', label = 'Original') 
plt.plot(output_values['instance_no'], output_values['Tout_cond_m2'], color='black', label = 'Model 2')
plt.xlabel('Instance')
plt.ylabel('Tcond_out (K)')
plt.show()

#plt.plot(output_values['instance_no'], output_values['Tout_cond_org'], color='blue', label = 'Original') 
#plt.plot(output_values['instance_no'], output_values['Tout_cond_m3'], color='red', label = 'Model 3')
#plt.xlabel('Instance')
#plt.ylabel('Tcond_out (K)')
#plt.show()

##Plotting Tout_cond percentage difference 
plt.plot(perc_difference['instance_no'], perc_difference['Tout_cond_m1_%'], color='green')
plt.xlabel('Instance')
plt.ylabel('Model 1: Tcond_out % diff')
plt.show()
print('Model 1 mean = ' + str(perc_difference['Tout_cond_m1_%'].mean()))

plt.plot(perc_difference['instance_no'], perc_difference['Tout_cond_m2_%'], color='black')
plt.xlabel('Instance')
plt.ylabel('Model 2: Tcond_out % diff')
plt.show()
print('Model 2 mean = ' + str(perc_difference['Tout_cond_m2_%'].mean()))

#plt.plot(perc_difference['instance_no'], perc_difference['E_m3_%'], color='red')
#plt.xlabel('Instance')
#plt.ylabel('Model 3: E % diff')
#plt.show()