import os
current_directory = os.path.dirname(__file__)[:-108] + '//' 
import sys
sys.path.append(current_directory + 'master_level_models\\\chiller_optimization_dist_nwk_pg_master_level_models\\add_ons\\')
from convert_to_quadratic import convert_to_quadratic 
from solve_quad_simul_eqns import solve_quad_simul_eqns
from sklearn import linear_model 
import numpy as np
import matplotlib.pyplot as plt 

##Pump parameters, regarding pressure-drop
pumpaf1_c0 = -0.0001266405
pumpaf1_c1 = 0.0112272822
pumpaf1_c2 = 12.3463827922

##Pump parameters, regarding electricity consumption at the maximum rpm 
pumpaf1_e_c0 = -0.0000003355
pumpaf1_e_c1 = 0.0001014045
pumpaf1_e_c2 = 0.0053863673
pumpaf1_e_c3 = 3.8221779914

##Network parameters 
evap_network_A_val = 1.66667E-05
ch1_evap_A_val = 0.000246472 + evap_network_A_val

##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
ch1_evap_x2_coeff, ch1_evap_x_coeff = convert_to_quadratic(ch1_evap_A_val)
##ch1_eflow_max[0] - maximum flowrate for this given combination 
ch1_eflow_max = solve_quad_simul_eqns([ch1_evap_x2_coeff, ch1_evap_x_coeff, 0], [pumpaf1_c0, pumpaf1_c1, pumpaf1_c2])
##The corresponding electricity consumption at the maximum flowrate and rpm is 
ch1_e_max = pumpaf1_e_c0*pow(ch1_eflow_max[0], 3) + pumpaf1_e_c1*pow(ch1_eflow_max[0], 2) + pumpaf1_e_c2*ch1_eflow_max[0] + pumpaf1_e_c3
##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
delp_interval = 20 
flowrate_interval = 50
flowrate_step = ch1_eflow_max[0] / flowrate_interval 
##Initiate a matrix to hold all the values 
##Column 1 will be flowrate 
##Column 2 will be pressure drop 
##Column 3 will be electricity consumed 
ch1_value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
ch1_value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

for i in range (0, flowrate_interval+1):
    ##current flowrate 
    c_fr = i * flowrate_step 
    ##minimum pressure drop comes from the system curve 
    min_p = ch1_evap_x2_coeff*pow(c_fr, 2) + ch1_evap_x_coeff*c_fr
    ##maximum pressure drop comes from the pump curve 
    max_p = pumpaf1_c0*pow(c_fr, 2) + pumpaf1_c1*c_fr + pumpaf1_c2
    ##minimum electricity consumption comes from the linear assumption curve 
    min_e = c_fr * (ch1_e_max / ch1_eflow_max[0])
    ##maximum electricity consumption comes from the electricity curve 
    max_e = pumpaf1_e_c0*pow(c_fr, 3) + pumpaf1_e_c1*pow(c_fr, 2) + pumpaf1_e_c2*c_fr + pumpaf1_e_c3
    ##recording the maximum and minimums 
    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

    for j in range (0, delp_interval):
        ch1_value_table_X[i*delp_interval+j, 0] = c_fr
        ch1_value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
        ch1_value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]

##Performing regression analysis
clf = linear_model.LinearRegression(fit_intercept = True)
clf.fit(ch1_value_table_X, ch1_value_table_Y)
result = clf.score(ch1_value_table_X, ch1_value_table_Y, sample_weight=None)
lin_coeff = clf.coef_
int_lin = clf.intercept_  
  
print(result)
##print(lin_coeff)
##print(int_lin)

##Evaluating the electricity consumption using linear combination model 
calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
for i in range (0, flowrate_interval+1):
    calc_Y[i,0] = lin_coeff[0,0]*ch1_value_table_X[i,0] + lin_coeff[0,1]*ch1_value_table_X[i,1] + int_lin

print(calc_Y.shape)
print(ch1_value_table_Y.shape)

##Plotting the pressure drop and flowrate area
plt.plot(ch1_value_table_X[:, 0], ch1_value_table_X[:, 1], 'o')
plt.show()
##Plotting the electricity consumption and flowrate area
plt.plot(ch1_value_table_X[:, 0], ch1_value_table_Y[:, 0], 'o')
plt.show()
##Plotting actual values and predicted values 
plt.plot(calc_Y, ch1_value_table_Y, 'o')
plt.show()
plt.plot(ch1_value_table_X[:, 0], calc_Y, 'o')
plt.show()