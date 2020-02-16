##Cooling tower test model 
##This is a test script for identifying the relationship between flowrate, delta t and electricity consumption of a cooling tower 

import sys 
sys.path.append('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\')
import numpy as np 
import matplotlib.pyplot as plt


##Weather information data 
t_wb = 30                           ##The thermodynamic wetbulb temperature in degrees celcius  

##Input information 
t_w_in = 35                         ##The inlet water temperature in degrees celcius

##Finding the effect of flowrate on the maximum delta t
##Note that the maximum delta t is achieved when the maximum flowrate of air is delivered 

max_flow = 407/5                 ##m3/h
min_flow = 0                    ##m3/h
iterations = 1000

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

##Changing the inputs into the correct units 
t_wb = t_wb + 273.15                ##Changing the units into degree kelvin 
t_w_in = t_w_in + 273.15            ##Changing the units into degree kelvin 

##Constants 

##Cooling tower derived constants 
c0 = 0.140295496
c1 = 0.600266127
c2 = -0.021147569
c3 = 0.279209454
c4 = 0.000929468
c5 = 0.16052557

##Cooling tower maximum electricity consumption 
E_max = 22                          ##The units are in kWh 

##Cooling tower maximum air flow 
G_max  = 301320                     ##The units are in m3/h

##Cooling tower linear fan coefficient 
cta_fan_coeff = E_max / (G_max * 1.225)

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

##Setting up the search for the relationship between delta-t_max and the flowrate for different temperatures 
A1 = t_w_in - ((t_w_in - t_wb) * (c0 + c2*(t_w_in - t_wb) + c4*(pow((t_w_in - t_wb), 2))))
A2 = -(t_w_in - t_wb)*(c1 + c5*(t_w_in - t_wb))
A3 = -(t_w_in - t_wb)*c3

min_flow = min_flow * 998.2
max_flow = max_flow * 998.2

flow_step_size = (max_flow - min_flow) / iterations 
current_flow = min_flow

##Initiate a matrix to hold the values 
dt_max_flow_rs = np.zeros((iterations, 2))

for i in range (0, iterations):
    if current_flow == 0:
        ratio = 0
    else:
        ratio = G_max / current_flow 
    
    t_w_out = A3*pow(ratio, 2) + A2*ratio + A1
    if t_w_out <= t_wb:
        t_w_out = t_wb
        
    delta_t_max = t_w_in - t_w_out 
    
    dt_max_flow_rs[i,0] = current_flow / 998.2
    dt_max_flow_rs[i,1] = delta_t_max

    current_flow = current_flow + flow_step_size
    
##Step-wise linearization of the Delta-T_max relationship with the flowrate for fixed vlues of T-in and T-wb 

##Finding the flowrate where Delta-T = maximum
max_delta_t = t_w_in - t_wb
B1 = c3                                                                         ##ratio ^2 term
B2 = c1 + c5*(t_w_in - t_wb)                                                    ##ratio term 
B3 = c0 + c2*(t_w_in - t_wb) + c4*(pow((t_w_in - t_wb), 2)) - (1)               ##cst term 

x1 = (-B2 + pow(pow(B2,2) - 4*B1*B3, 0.5)) / (2*B1)

critical_flow = (G_max / x1) / 998.2
print('critical flow = ' + str(critical_flow) + ' m3/h')

##1 step to account for no flow conditions 
##1 step to account for max_delta t conditions 
##4 steps to account till the rest till the maximum flowrate possible 

num_steps = 4
s_size = (max_flow/998.2 - critical_flow) / num_steps
limit1 = critical_flow + s_size
limit2 = limit1 + s_size
limit3 = limit2 + s_size 
limit4 = limit3 + s_size

##For each step ather are 2 terms, 1 corresponding to the gradient and the other the constant 

##Step 1
##Occurs for flowrate 0 < flow < 0.01 m3/h
delta_t_max_1_1 = 0
delta_t_max_1_2 = 0

##Step 2 
##Occurs for flowrate 0.01 < flow < critical flow m3/h
delta_t_max_2_1 = 0
delta_t_max_2_2 = max_delta_t

##Step 3
y1_3 =  max_delta_t
x1_3 = critical_flow 
y2_3 = t_w_in - (A3*pow(G_max / (limit1*998.2), 2) + A2*(G_max / (limit1*998.2)) + A1)
x2_3 = limit1

delta_t_max_3_1 = (y2_3 - y1_3)/ (x2_3 - x1_3)
delta_t_max_3_2 = y2_3 - delta_t_max_3_1*x2_3

##Step 4
y1_4 = t_w_in - (A3*pow(G_max / (limit1*998.2), 2) + A2*(G_max / (limit1*998.2)) + A1)
x1_4 = limit1 
y2_4 = t_w_in - (A3*pow(G_max / (limit2*998.2), 2) + A2*(G_max / (limit2*998.2)) + A1)
x2_4 = limit2

delta_t_max_4_1 = (y2_4 - y1_4)/ (x2_4 - x1_4)
delta_t_max_4_2 = y2_4 - delta_t_max_4_1*x2_4

##Step 5
y1_5 = t_w_in - (A3*pow(G_max / (limit2*998.2), 2) + A2*(G_max / (limit2*998.2)) + A1)
x1_5 = limit2
y2_5 = t_w_in - (A3*pow(G_max / (limit3*998.2), 2) + A2*(G_max / (limit3*998.2)) + A1)
x2_5 = limit3

delta_t_max_5_1 = (y2_5 - y1_5)/ (x2_5 - x1_5)
delta_t_max_5_2 = y2_5 - delta_t_max_5_1*x2_5

##Step 6
y1_6 = t_w_in - (A3*pow(G_max / (limit3*998.2), 2) + A2*(G_max / (limit3*998.2)) + A1)
x1_6 = limit3
y2_6 = t_w_in - (A3*pow(G_max / (limit4*998.2), 2) + A2*(G_max / (limit4*998.2)) + A1)
x2_6 = limit4

delta_t_max_6_1 = (y2_6 - y1_6)/ (x2_6 - x1_6)
delta_t_max_6_2 = y2_6 - delta_t_max_6_1*x2_6

##Initiate a matrix to hold the values for plotting the stepwise functions 
sw_holder = np.zeros((600,6))

row = 0
min_flow1 = 0
max_flow1 = 0.01 
flow1_step = (max_flow1 - min_flow1) / 100
c_flow = min_flow1

for i in range (0, 100):
    sw_holder[row,0] = c_flow 
    sw_holder[row,1] = (delta_t_max_1_1 * c_flow) + delta_t_max_1_2
    row = row + 1
    c_flow = c_flow + flow1_step

min_flow2 = 0.01
max_flow2 = critical_flow 
flow2_step = (max_flow2 - min_flow2) / 100
c_flow = min_flow2

for i in range (0, 100):
    sw_holder[row,0] = c_flow 
    sw_holder[row,1] = (delta_t_max_2_1 * c_flow) + delta_t_max_2_2
    row = row + 1
    c_flow = c_flow + flow2_step

min_flow3 = critical_flow 
max_flow3 = limit1 
flow3_step = (max_flow3 - min_flow3) / 100
c_flow = min_flow3

for i in range (0, 100):
    sw_holder[row,0] = c_flow 
    sw_holder[row,1] = (delta_t_max_3_1 * c_flow) + delta_t_max_3_2
    row = row + 1
    c_flow = c_flow + flow3_step
    
min_flow4 = limit1 
max_flow4 = limit2 
flow4_step = (max_flow4 - min_flow4) / 100
c_flow = min_flow4

for i in range (0, 100):
    sw_holder[row,0] = c_flow 
    sw_holder[row,1] = (delta_t_max_4_1 * c_flow) + delta_t_max_4_2
    row = row + 1
    c_flow = c_flow + flow4_step

min_flow5 = limit2 
max_flow5 = limit3 
flow5_step = (max_flow5 - min_flow5) / 100
c_flow = min_flow5

for i in range (0, 100):
    sw_holder[row,0] = c_flow 
    sw_holder[row,1] = (delta_t_max_5_1 * c_flow) + delta_t_max_5_2
    row = row + 1
    c_flow = c_flow + flow5_step

min_flow6 = limit3 
max_flow6 = limit4 
flow6_step = (max_flow6 - min_flow6) / 100
c_flow = min_flow6

for i in range (0, 100):
    sw_holder[row,0] = c_flow 
    sw_holder[row,1] = (delta_t_max_6_1 * c_flow) + delta_t_max_6_2
    row = row + 1
    c_flow = c_flow + flow6_step
 
    
plt.plot(dt_max_flow_rs[:,0], dt_max_flow_rs[:,1])
plt.plot(sw_holder[:,0], sw_holder[:,1])
plt.xlabel('Flowrate (m3/h)')
plt.ylabel('Delta-T_max (K)')
plt.show()

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

##This section generates the relationship between E cons, mass_flowrate and delta t


