##This is a script to check the intersection point between the pump and the system curve 
import os
current_directory = os.path.dirname(__file__)[:-111] + '//' 
import sys 
sys.path.append(current_directory + 'master_level_models\\\chiller_optimization_dist_nwk_ga_nb_master_level_models\\add_ons\\')
from convert_to_quadratic import convert_to_quadratic 
from solve_quad_simul_eqns import solve_quad_simul_eqns
import matplotlib.pyplot as plt
import numpy as np 

##The end-point flowrate 
flow_end_evap = 700 #m3h
flow_end_cond = 2000 #m3/h

##Evaporator pumps
pumpaf1_c0 = -0.0001266405
pumpaf1_c1 = 0.0112272822
pumpaf1_c2 = 12.3463827922

pumpaf2_c0 = -0.0000136254
pumpaf2_c1 = 0.0001647403
pumpaf2_c2 = 21.4327511013

##Condenser pumps 
pumpar1_c0 = -0.0000552287
pumpar1_c1 = 0.0127459461
pumpar1_c2 = 28.8570326545

pumpar2_c0 = -0.0000090818
pumpar2_c1 = 0.0029568794
pumpar2_c2 = 45.1880038403

evap_network_A_val = 1.66667E-05
cond_network_A_val = 6.62983E-07

ch1_evap_A_val = 0.000246472 + evap_network_A_val
ch1_cond_A_val = 0.000133743 + cond_network_A_val

ch2_evap_A_val = 3.07492E-05 + evap_network_A_val
ch2_cond_A_val = 1.78251E-05 + cond_network_A_val

ch1_evap_x2_coeff, ch1_evap_x_coeff = convert_to_quadratic(ch1_evap_A_val)
ch1_cond_x2_coeff, ch1_cond_x_coeff = convert_to_quadratic(ch1_cond_A_val)

ch2_evap_x2_coeff, ch2_evap_x_coeff = convert_to_quadratic(ch2_evap_A_val)
ch2_cond_x2_coeff, ch2_cond_x_coeff = convert_to_quadratic(ch2_cond_A_val)


flow_evap = np.linspace(0, flow_end_evap, flow_end_evap, endpoint = True)
flow_cond = np.linspace(0, flow_end_cond, flow_end_cond, endpoint = True)

##Chiller 1
pumpaf1_curve = pumpaf1_c0*np.power(flow_evap,2) + pumpaf1_c1*flow_evap + pumpaf1_c2
evap_sys_ch1 = ch1_evap_x2_coeff*np.power(flow_evap,2) + ch1_evap_x_coeff*flow_evap 
pumpar1_curve = pumpar1_c0*np.power(flow_cond,2) + pumpar1_c1*flow_cond + pumpar1_c2
cond_sys_ch1 = ch1_cond_x2_coeff*np.power(flow_cond,2) + ch1_cond_x_coeff*flow_cond

#Chiller 2
pumpaf2_curve = pumpaf2_c0*np.power(flow_evap,2) + pumpaf2_c1*flow_evap + pumpaf2_c2
evap_sys_ch2 = ch2_evap_x2_coeff*np.power(flow_evap,2) + ch2_evap_x_coeff*flow_evap 
pumpar2_curve = pumpar2_c0*np.power(flow_cond,2) + pumpar2_c1*flow_cond + pumpar2_c2
cond_sys_ch2 = ch2_cond_x2_coeff*np.power(flow_cond,2) + ch2_cond_x_coeff*flow_cond

##Finding the maximum flowrate points 
ch1_eflow_max = solve_quad_simul_eqns([ch1_evap_x2_coeff, ch1_evap_x_coeff, 0], [pumpaf1_c0, pumpaf1_c1, pumpaf1_c2])
ch1_cflow_max = solve_quad_simul_eqns([ch1_cond_x2_coeff, ch1_cond_x_coeff, 0], [pumpar1_c0, pumpar1_c1, pumpar1_c2])
ch2_eflow_max = solve_quad_simul_eqns([ch2_evap_x2_coeff, ch2_evap_x_coeff, 0], [pumpaf2_c0, pumpaf2_c1, pumpaf2_c2])
ch2_cflow_max = solve_quad_simul_eqns([ch2_cond_x2_coeff, ch2_cond_x_coeff, 0], [pumpar2_c0, pumpar2_c1, pumpar2_c2])

##Plotting Chiller 1
plt.plot(flow_evap, pumpaf1_curve)
plt.plot(flow_evap, evap_sys_ch1)
plt.title('Ch1_Evaporator')
plt.xlabel('Evaporator_flowrate m3/h')
plt.ylabel('Delta_P mH2O')
plt.show()
print('Ch1_evap_max_flow = ' + str(ch1_eflow_max[0]))

plt.plot(flow_cond, pumpar1_curve)
plt.plot(flow_cond, cond_sys_ch1)
plt.title('Ch1_Condenser')
plt.xlabel('Condenser_flowrate m3/h')
plt.ylabel('Delta_P mH2O')
plt.show()
print('Ch1_cond_max_flow = ' + str(ch1_cflow_max[0]))

##Plotting Chiller 2
plt.plot(flow_evap, pumpaf2_curve)
plt.plot(flow_evap, evap_sys_ch2)
plt.title('Ch2_Evaporator')
plt.xlabel('Evaporator_flowrate m3/h')
plt.ylabel('Delta_P mH2O')
plt.show()
print('Ch2_evap_max_flow = ' + str(ch2_eflow_max[0]))

plt.plot(flow_cond, pumpar2_curve)
plt.plot(flow_cond, cond_sys_ch2)
plt.title('Ch2_Condenser')
plt.xlabel('Condenser_flowrate m3/h')
plt.ylabel('Delta_P mH2O')
plt.show()
print('Ch2_cond_max_flow = ' + str(ch2_cflow_max[0]))
