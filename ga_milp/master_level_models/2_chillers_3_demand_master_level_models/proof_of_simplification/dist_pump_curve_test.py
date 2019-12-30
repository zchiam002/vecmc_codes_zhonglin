##This is a test script for the intersection points and the description 
#Finally, this is proof that the linear estimation actually makes sense

import sys 
sys.path.append('C:\\Optimization_zlc\\master_level_models\\2_chillers_3_demand_master_level_models\\proof_of_simplification\\')
sys.path.append('C:\\Optimization_zlc\\master_level_models\\2_chillers_3_demand_master_level_models\\add_ons\\')
import matplotlib.pyplot as plt
import numpy as np 
from sklearn import linear_model 
from dist_nwk import dist_nwk_system_bounds 
from solve_quad_simul_eqns import solve_quad_simul_eqns
##Selected pump data 

##AF2.1

#p_2 = -0.0000151451
#p_1 = 0.0119236210
#p_cst = 58.2250275059

##AF3.1

p_2 = -0.0001095722
p_1 = 0.0228923489
p_cst = 35.2618445622

#Distribution network 

#Getting the quadratic coefficients of the lower and upper bounds of the system curve  
Cl_2, Cl_1, Cu_2, Cu_1 = dist_nwk_system_bounds()

##Finding the intersection points between the bounds and the pump curve 

##The pump curve 
pump_coeff = []
pump_coeff.append(p_2)
pump_coeff.append(p_1)
pump_coeff.append(p_cst)

##The upper limit system curve 
sys_u = []
sys_u.append(Cu_2)
sys_u.append(Cu_1)
sys_u.append(0)

##The lower limit system curve 
sys_l = []
sys_l.append(Cl_2)
sys_l.append(Cl_1)
sys_l.append(0)

int_pt_u = solve_quad_simul_eqns(pump_coeff, sys_u)                             ##What if the flowrate is higher than max pump flow 
int_pt_l = solve_quad_simul_eqns(pump_coeff, sys_l)                             ##There is a need to deal with that situation 

print(int_pt_l)

##Identifying the critical flowrate of the curve combination
critical_flow = int_pt_u[0]
##Identifying the maximum flowrate of the curve combination 
max_flow = int_pt_l[0]

#Electricity curve AF2.1
#e_2 = -0.0000055276
#e_1 = 0.0771653808
#e_cst = 106.7867892025

#Electricity curve AF3.1
e_2 = -0.0000372609
e_1 = 0.0745145187
e_cst = 13.8059958033

##Identifying the maximum electricity at the 2 defined flowrates 

e_max_critical_flow = e_2*critical_flow + e_1*critical_flow + e_cst 
e_max_max_flow = e_2*pow(max_flow,2) + e_1*max_flow + e_cst 

##Assuming linear relationship between when the pump changes speed, we want to map the delta p and the flowrate to the electricity 
##consumption 

##The key is to split the data into before the critical point and after the critical point 

##Before the critical point 
##We consider 10 flowrates intervals and correspondingly 10 different delta p values with their 10 electricity consumption values 

flow_before_c_f = np.linspace(0, critical_flow, 10, endpoint = True )
data_before_c_f = np.zeros((100,3))
e_l_bound_grad_bcf = e_max_max_flow / max_flow
e_u_bound_grad_bcf = e_max_critical_flow / critical_flow

for i in range (0, 10):
    min_p = Cl_2*pow(flow_before_c_f[i], 2) + Cl_1*flow_before_c_f[i]
    max_p = Cu_2*pow(flow_before_c_f[i], 2) + Cu_1*flow_before_c_f[i]
    p_record_temp = np.linspace(min_p, max_p, 10, endpoint = True)              ##10 temporary records of the pressure  
    min_e = e_l_bound_grad_bcf*flow_before_c_f[i]
    max_e = e_u_bound_grad_bcf*flow_before_c_f[i]
    e_record_temp = np.linspace(min_e, max_e, 10, endpoint = True)              ##10 temporary records of electricity
    
    for j in range (0, 10):
        data_before_c_f[i*10+j, 0] = flow_before_c_f[i]
        data_before_c_f[i*10+j, 1] = p_record_temp[j]
        data_before_c_f[i*10+j, 2] = e_record_temp[j]

##After the critical point and before the maximum flow 
##We consider 10 flowrates intervals and corresponding 10 different delta p values with their 10 electricty consumption values 

flow_after_c_f = np.linspace(critical_flow, max_flow, 10, endpoint = True)
data_after_c_f = np.zeros((100,3))
e_l_bound_grad_acf = e_max_max_flow / max_flow

for i in range (0, 10):
    min_p = Cl_2*pow(flow_after_c_f[i], 2) + Cl_1*flow_after_c_f[i]
    max_p = p_2*pow(flow_after_c_f[i], 2) + p_1*flow_after_c_f[i] + p_cst
    p_record_temp = np.linspace(min_p, max_p, 10, endpoint = True)
    min_e = e_l_bound_grad_bcf*flow_after_c_f[i]
    max_e = e_2*pow(flow_after_c_f[i], 2) + e_1*flow_after_c_f[i] + e_cst
    e_record_temp = np.linspace(min_e, max_e, 10, endpoint = True)
    
    for j in range (0, 10):
        data_after_c_f[i*10+j, 0] = flow_after_c_f[i]
        data_after_c_f[i*10+j, 1] = p_record_temp[j]
        data_after_c_f[i*10+j, 2] = e_record_temp[j]        

print(data_before_c_f)
print(data_after_c_f)
print(e_max_critical_flow, e_max_max_flow)
print(int_pt_u)
print(int_pt_l)

##Finding the correlations between the flow, pressure and electricity before and after the cirtical flow


X_include_all_bcf = np.zeros((100, 5))
#m_2, p_2, mp, m, p
for i in range (0, 100):
    X_include_all_bcf[i, 0] = pow(data_before_c_f[i, 0], 2)
    X_include_all_bcf[i, 1] = pow(data_before_c_f[i, 1], 2)
    X_include_all_bcf[i, 2] = data_before_c_f[i, 0] * data_before_c_f[i, 1]
    X_include_all_bcf[i, 3] = data_before_c_f[i, 0]
    X_include_all_bcf[i, 4] = data_before_c_f[i, 1]

clf = linear_model.LinearRegression(fit_intercept = True)
clf.fit(X_include_all_bcf, data_before_c_f[:,2])
result_1 = clf.score(X_include_all_bcf, data_before_c_f[:,2], sample_weight=None)
quad_coeff_1 = clf.coef_
int_1 = clf.intercept_

print(result_1)
print(quad_coeff_1)
print(int_1)

X_include_all_acf = np.zeros((100, 5))
#m_2, p_2, mp, m, p
for i in range (0, 100):
    X_include_all_acf[i, 0] = pow(data_after_c_f[i, 0], 2)
    X_include_all_acf[i, 1] = pow(data_after_c_f[i, 1], 2)
    X_include_all_acf[i, 2] = data_after_c_f[i, 0] * data_after_c_f[i, 1]
    X_include_all_acf[i, 3] = data_after_c_f[i, 0]
    X_include_all_acf[i, 4] = data_after_c_f[i, 1]

clf1 = linear_model.LinearRegression(fit_intercept = True)
clf1.fit(X_include_all_acf, data_after_c_f[:,2])
result_2 = clf1.score(X_include_all_acf, data_after_c_f[:,2], sample_weight=None)
quad_coeff_2 = clf1.coef_
int_2 = clf1.intercept_

print(result_2)
print(quad_coeff_2)
print(int_2)

X_v1_bcf = np.zeros((100,2))
#m, p only
for i in range (0, 100):
    X_v1_bcf[i, 0] = data_before_c_f[i, 0]
    X_v1_bcf[i, 1] = data_before_c_f[i, 1]

clf2 = linear_model.LinearRegression(fit_intercept = True)
clf2.fit(X_v1_bcf, data_before_c_f[:,2])
result_3 = clf2.score(X_v1_bcf, data_before_c_f[:,2], sample_weight=None)
quad_coeff_3 = clf2.coef_   
int_3 = clf2.intercept_

print(result_3)
print(quad_coeff_3)
print(int_3)

X_v1_acf = np.zeros((100,2))
#m, p only
for i in range (0, 100):
    X_v1_acf[i, 0] = data_after_c_f[i, 0]
    X_v1_acf[i, 1] = data_after_c_f[i, 1]

clf3 = linear_model.LinearRegression(fit_intercept = True)
clf3.fit(X_v1_acf, data_after_c_f[:,2])
result_4 = clf3.score(X_v1_acf, data_after_c_f[:,2], sample_weight=None)
quad_coeff_4 = clf3.coef_   
int_4 = clf3.intercept_

print(result_4)
print(quad_coeff_4)
print(int_4)

##Plotting the m + p correlation with the original values 
estimated_elec_bcf = np.zeros((100,1))
estimated_elec_acf = np.zeros((100,1))

for i in range (0, 100):
    estimated_elec_bcf[i, 0] = quad_coeff_3[0]*data_before_c_f[i,0] + quad_coeff_3[1]*data_before_c_f[i,1] + int_3

for i in range (0, 100):
    estimated_elec_acf[i, 0] = quad_coeff_4[0]*data_after_c_f[i,0] + quad_coeff_4[1]*data_after_c_f[i,1] + int_4

X1 = np.linspace(0, 28, 6, endpoint = True)
X = np.linspace(0, 600, 1200, endpoint = True)
Y1 = Cl_2*np.power(X, 2) + Cl_1*X
Y2 = Cu_2*np.power(X1, 2) + Cu_1*X1
Y3 = p_2*np.power(X, 2) + p_1*X + p_cst

X_E1 = np.linspace(0, 36, 10, endpoint = True)
X_E2 = np.linspace(0, 600, 100, endpoint = True)
X_E3 = np.linspace(0, 600, 200, endpoint = True)
Y_E1 = e_u_bound_grad_bcf * X_E1
Y_E2 = e_l_bound_grad_bcf * X_E2
Y_E3 = e_2*np.power(X_E3, 2) + e_1*X_E3 + e_cst

plt.plot(X, Y1)
plt.plot(X1, Y2)
plt.plot(X, Y3)
plt.plot(data_before_c_f[:,0], data_before_c_f[:,1], 'o')
plt.plot(data_after_c_f[:,0], data_after_c_f[:,1], 'o')
plt.show()

plt.plot(data_before_c_f[:,0], data_before_c_f[:,2], 'o')
plt.plot(data_after_c_f[:,0], data_after_c_f[:,2], 'o')
plt.plot(X_E1, Y_E1)
plt.plot(X_E2, Y_E2)
plt.plot(X_E3, Y_E3)
plt.show()

plt.plot(data_before_c_f[:,2], estimated_elec_bcf, 'o')
plt.show()
plt.plot(data_after_c_f[:,2], estimated_elec_acf, 'o')
plt.show()

##For the model of m + p, display the maximum error estimate 
error_bcf = []
error_acf = []

for i in range (0, 100):
    error_bcf.append(np.fabs((data_before_c_f[i,2] - estimated_elec_bcf[i,0])))
    error_acf.append(np.fabs((data_after_c_f[i,2] - estimated_elec_acf[i,0])))
    
print(error_bcf)
print(error_acf)
    
plt.hist(error_bcf, 50, normed=1, facecolor='g', alpha=0.75)
plt.show()
plt.hist(error_acf, 50, normed=1, facecolor='g', alpha=0.75)
