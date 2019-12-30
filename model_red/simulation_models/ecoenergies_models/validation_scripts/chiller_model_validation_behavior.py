##This script validates the behavior of the chiller models 

def chiller1(Tout_evap, Qe, mevap, Tin_cond, mcond, Qe_max):
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\') 
    from chiller_models import chiller_gnu
    
    b0_1 = 0.123020043325872
    b1_1 = 1044.79734873891
    b2_1 = 0.0204660495029597
    reg_cst = [b0_1, b1_1, b2_1]
    qc_coeff = 1.09866273284186
    
    Tin_evap = (Qe / (4.2 * mevap)) + Tout_evap
    
    return_values, return_values_df = chiller_gnu (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max)
    

    COP = return_values['Coefficient_of_performance']
    E = return_values['Electricity_consumption']
    return COP, E

def chiller2and3(Tout_evap, Qe, mevap, Tin_cond, mcond, Qe_max):
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\') 
    from chiller_models import chiller_gnu
    
    b0_1 = 0.123020043325872
    b1_1 = 1044.79734873891
    b2_1 = 0.0204660495029597
    reg_cst = [b0_1, b1_1, b2_1]
    qc_coeff = 1.09866273284186
    
    Tin_evap = (Qe / (4.2 * mevap)) + Tout_evap
    
    return_values, return_values_df = chiller_gnu (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max)
    

    COP = return_values['Coefficient_of_performance']
    E = return_values['Electricity_consumption']
    return COP, E


import numpy as np
import matplotlib.pyplot as plt

##Testing conditions 
##Number of variables = 5
    ##1. Tout_evap
    ##2. mevap
    ##3. Qe
    ##4. Tin_cond
    ##5. mcond 

####################################################################################################################################################
#####################################################################################################################################################    
##Test 1: Vary Tout_evap

##Fixed parameters
mevap_1 = 190.8
Qe_1 = 1000
Tin_cond_1 = 30
mcond_1 = 406.8
Qe_max_1 = 2000

mevap_2 = 698.4
Qe_2 = 3665
Tin_cond_2 = 30
mcond_2 = 1476
Qe_max_2 = 7330

##Determine the range of Tout_evap
Tout_evap_min = 1
Tout_evap_max = 10

iterations = 100
##Determine the range of outlet temperatures
x = np.linspace(Tout_evap_min, Tout_evap_max, num=iterations)
##Initiate a matrix to hold return values 
COP_1 = np.zeros((iterations, 1))
E_1 = np.zeros((iterations, 1))
COP_2 = np.zeros((iterations, 1))
E_2 = np.zeros((iterations, 1))

for i in range (0, iterations):
    COP_1[i, 0], E_1[i, 0] = chiller1(x[i], Qe_1, mevap_1, Tin_cond_1, mcond_1, Qe_max_1)
    COP_2[i, 0], E_2[i, 0] = chiller2and3(x[i], Qe_2, mevap_2, Tin_cond_2, mcond_2, Qe_max_2)

##Percentage change within range
COP_1change = (((COP_1[iterations -1, 0] - COP_1[0, 0]) / 2) / COP_1[int(iterations/2) -1, 0]) * 100
E_1change = (((E_1[iterations -1, 0] - E_1[0, 0]) / 2) / E_1[int(iterations/2) -1, 0]) * 100
COP_2change = (((COP_2[iterations -1, 0] - COP_2[0, 0]) / 2) / COP_2[int(iterations/2) -1, 0]) * 100
E_2change = (((E_2[iterations -1, 0] - E_2[0, 0]) / 2) / E_2[int(iterations/2) -1, 0]) * 100

print(COP_1change, E_1change)
print(COP_2change, E_2change)


##Plotting the data 

#plt.plot(x, COP_1, color='blue') 
#plt.title('Chiller 1')
#plt.xlabel('Tout_evap (C)')
#plt.ylabel('COP')
#plt.show()
#
#plt.plot(x, E_1, color='blue')
#plt.title('Chiller 1') 
#plt.xlabel('Tout_evap (C)')
#plt.ylabel('E (kWh)')
#plt.show()
#
#plt.plot(x, COP_2, color='red') 
#plt.title('Chiller 2&3')
#plt.xlabel('Tout_evap (C)')
#plt.ylabel('COP')
#plt.show()
#
#plt.plot(x, E_2, color='red')
#plt.title('Chiller 2&3') 
#plt.xlabel('Tout_evap (C)')
#plt.ylabel('E (kWh)')
#plt.show()

####################################################################################################################################################
####################################################################################################################################################
##Test 2: Vary mevap

##Fixed parameters
Tout_evap_1 = 5
Qe_1 = 1000
Tin_cond_1 = 30
mcond_1 = 406.8
Qe_max_1 = 2000

Tout_evap_2 = 5
Qe_2 = 3665
Tin_cond_2 = 30
mcond_2 = 1476
Qe_max_2 = 7330

##Determine the range of Tout_evap
mevap_1_min = 30
mevap_1_max = 300
mevap_2_min = 100
mevap_2_max = 1000

iterations = 100
##Determine the range of outlet temperatures
x_1 = np.linspace(mevap_1_min, mevap_1_max, num=iterations)
x_2 = np.linspace(mevap_2_min, mevap_2_max, num=iterations)
##Initiate a matrix to hold return values 
COP_1 = np.zeros((iterations, 1))
E_1 = np.zeros((iterations, 1))
COP_2 = np.zeros((iterations, 1))
E_2 = np.zeros((iterations, 1))

for i in range (0, iterations):
    COP_1[i, 0], E_1[i, 0] = chiller1(Tout_evap_1, Qe_1, x_1[i], Tin_cond_1, mcond_1, Qe_max_1)
    COP_2[i, 0], E_2[i, 0] = chiller2and3(Tout_evap_2, Qe_2, x_2[i], Tin_cond_2, mcond_2, Qe_max_2)

##Percentage change within range
COP_1change = (((COP_1[iterations -1, 0] - COP_1[0, 0]) / 2) / COP_1[int(iterations/2) -1, 0]) * 100
E_1change = (((E_1[iterations -1, 0] - E_1[0, 0]) / 2) / E_1[int(iterations/2) -1, 0]) * 100
COP_2change = (((COP_2[iterations -1, 0] - COP_2[0, 0]) / 2) / COP_2[int(iterations/2) -1, 0]) * 100
E_2change = (((E_2[iterations -1, 0] - E_2[0, 0]) / 2) / E_2[int(iterations/2) -1, 0]) * 100

print(COP_1change, E_1change)
print(COP_2change, E_2change)

###Plotting the data 
#plt.plot(x_1, COP_1, color='blue') 
#plt.title('Chiller 1')
#plt.xlabel('mevap (m3/h)')
#plt.ylabel('COP')
#plt.show()
#
#plt.plot(x_1, E_1, color='blue')
#plt.title('Chiller 1') 
#plt.xlabel('mevap (m3/h)')
#plt.ylabel('E (kWh)')
#plt.show()
#
#plt.plot(x_2, COP_2, color='red') 
#plt.title('Chiller 2&3')
#plt.xlabel('mevap (m3/h)')
#plt.ylabel('COP')
#plt.show()
#
#plt.plot(x_2, E_2, color='red')
#plt.title('Chiller 2&3') 
#plt.xlabel('mevap (m3/h)')
#plt.ylabel('E (kWh)')
#plt.show()

######################################################################################################################################################
##Test 3: Vary Qe
##Fixed parameters
mevap_1 = 190.8
Tout_evap_1 = 5
Tin_cond_1 = 30
mcond_1 = 406.8
Qe_max_1 = 2000

mevap_2 = 698.4
Tout_evap_2 = 5
Tin_cond_2 = 30
mcond_2 = 1476
Qe_max_2 = 7330

##Determine the range of Tout_evap
Qe_1_min = 200
Qe_1_max = 2000
Qe_2_min = 733
Qe_2_max = 7330

iterations = 100
##Determine the range of outlet temperatures
x_1 = np.linspace(Qe_1_min, Qe_1_max, num=iterations)
x_2 = np.linspace(Qe_2_min, Qe_2_max, num=iterations)
##Initiate a matrix to hold return values 
COP_1 = np.zeros((iterations, 1))
E_1 = np.zeros((iterations, 1))
COP_2 = np.zeros((iterations, 1))
E_2 = np.zeros((iterations, 1))

COP_3 = np.zeros((iterations, 1))
E_3 = np.zeros((iterations, 1))

COP_4 = np.zeros((iterations, 1))
E_4 = np.zeros((iterations, 1))

COP_5 = np.zeros((iterations, 1))
E_5 = np.zeros((iterations, 1))

COP_6 = np.zeros((iterations, 1))
E_6 = np.zeros((iterations, 1))

for i in range (0, iterations):
    COP_1[i, 0], E_1[i, 0] = chiller1(Tout_evap_1, x_1[i], mevap_1, Tin_cond_1, mcond_1, Qe_max_1)
    COP_2[i, 0], E_2[i, 0] = chiller2and3(Tout_evap_2, x_2[i], mevap_2, Tin_cond_2, mcond_2, Qe_max_2)
    COP_3[i, 0], E_3[i, 0] = chiller2and3(Tout_evap_2-2, x_2[i], mevap_2, Tin_cond_2, mcond_2, Qe_max_2)
    COP_4[i, 0], E_4[i, 0] = chiller2and3(Tout_evap_2-4, x_2[i], mevap_2, Tin_cond_2, mcond_2, Qe_max_2)
    
    COP_5[i, 0], E_5[i, 0] = chiller2and3(Tout_evap_2, x_2[i], mevap_2, Tin_cond_2+4, mcond_2, Qe_max_2)
    COP_6[i, 0], E_6[i, 0] = chiller2and3(Tout_evap_2, x_2[i], mevap_2, Tin_cond_2+8, mcond_2, Qe_max_2)    
##Percentage change within range
COP_1change = (((COP_1[iterations -1, 0] - COP_1[0, 0]) / 2) / COP_1[int(iterations/2) -1, 0]) * 100
E_1change = (((E_1[iterations -1, 0] - E_1[0, 0]) / 2) / E_1[int(iterations/2) -1, 0]) * 100
COP_2change = (((COP_2[iterations -1, 0] - COP_2[0, 0]) / 2) / COP_2[int(iterations/2) -1, 0]) * 100
E_2change = (((E_2[iterations -1, 0] - E_2[0, 0]) / 2) / E_2[int(iterations/2) -1, 0]) * 100

print(COP_1change, E_1change)
print(COP_2change, E_2change)

##Plotting the data 
#plt.plot(x_1, COP_1, color='blue') 
#plt.title('Chiller 1')
#plt.xlabel('Qe (kWh)')
#plt.ylabel('COP')
#plt.show()
#
#plt.plot(x_1, E_1, color='blue')
#plt.title('Chiller 1') 
#plt.xlabel('Qe (kWh)')
#plt.ylabel('E (kWh)')
#plt.show()

#plt.plot(x_2, COP_2, color='blue', label = r'$T^{in}_{cond, 1}$')
#plt.plot(x_2, COP_5, color='red', label = r'$T^{in}_{cond, 2}$')
#plt.plot(x_2, COP_6, color='green', label = r'$T^{in}_{cond, 3}$')
##plt.title('Chiller 2&3')
#plt.xlabel('Qe (kWh)')
#plt.ylabel('COP')
#plt.legend(loc='best')
#plt.axes().get_xaxis().set_ticks([])
#plt.axes().get_yaxis().set_ticks([])
#plt.savefig('C:\\Optimization_zlc\\reports\\qe_report\\workspace\\chiller_cop_tcond_in.png', dpi=1000, bbox_inches='tight')
#plt.show()

##Scale factor = 1.7
scale = 1.7
mag_red = 1000
relative = scale /mag_red

from matplotlib.ticker import FormatStrFormatter

fig, ax = plt.subplots()

ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))

#plt.plot(relative * x_2, scale * COP_2, color='blue', label = r'$T^{out}_{evap, 1}$')
#plt.plot(relative * x_2, scale * COP_3, color='red', label = r'$T^{out}_{evap, 2}$')
#plt.plot(relative * x_2, scale * COP_4, color='green', label = r'$T^{out}_{evap, 3}$')
##plt.title('Chiller 2&3')
##plt.xlabel('Qe ' + r'$\times 10^{3}$'+ ' (kWh)')
#plt.xlabel('Qe (kWh)')
#plt.ylabel('COP')
#plt.legend(loc='best')
#plt.axes().get_xaxis().set_ticks([])
#plt.axes().get_yaxis().set_ticks([])
#
#
#plt.savefig('C:\\Optimization_zlc\\reports\\qe_report\\workspace\\chiller_cop.png', dpi=1000, bbox_inches='tight')
#plt.show()

#plt.plot(x_2, E_2, color='red')
#plt.title('Chiller 2&3') 
#plt.xlabel('Qe (kWh)')
#plt.ylabel('E (kWh)')
#plt.show()

#####################################################################################################################################################
##Test 4: Vary Tcond_in
##Fixed parameters
mevap_1 = 190.8
Tout_evap_1 = 5
Qe_1 = 1000
mcond_1 = 406.8
Qe_max_1 = 2000

mevap_2 = 698.4
Tout_evap_2 = 5
Qe_2 = 3665 
Tin_cond_2 = 30
mcond_2 = 1476
Qe_max_2 = 7330

##Determine the range of Tout_evap
Tcond_in_min = 20
Tcond_in_max = 35

iterations = 100
##Determine the range of outlet temperatures
x = np.linspace(Tcond_in_min, Tcond_in_max, num=iterations)
##Initiate a matrix to hold return values 
COP_1 = np.zeros((iterations, 1))
E_1 = np.zeros((iterations, 1))
COP_2 = np.zeros((iterations, 1))
E_2 = np.zeros((iterations, 1))

for i in range (0, iterations):
    COP_1[i, 0], E_1[i, 0] = chiller1(Tout_evap_1, Qe_1, mevap_1, x[i], mcond_1, Qe_max_1)
    COP_2[i, 0], E_2[i, 0] = chiller2and3(Tout_evap_2, Qe_2, mevap_2, x[i], mcond_2, Qe_max_2)

##Percentage change within range
COP_1change = (((COP_1[iterations -1, 0] - COP_1[0, 0]) / 2) / COP_1[int(iterations/2) -1, 0]) * 100
E_1change = (((E_1[iterations -1, 0] - E_1[0, 0]) / 2) / E_1[int(iterations/2) -1, 0]) * 100
COP_2change = (((COP_2[iterations -1, 0] - COP_2[0, 0]) / 2) / COP_2[int(iterations/2) -1, 0]) * 100
E_2change = (((E_2[iterations -1, 0] - E_2[0, 0]) / 2) / E_2[int(iterations/2) -1, 0]) * 100

print(COP_1change, E_1change)
print(COP_2change, E_2change)

##Plotting the data 
plt.plot(x, COP_1, color='blue') 
plt.title('Chiller 1')
plt.xlabel('Tcond_in (C)')
plt.ylabel('COP')
plt.show()

#plt.plot(x, E_1, color='blue')
#plt.title('Chiller 1') 
#plt.xlabel('Tcond_in (C)')
#plt.ylabel('E (kWh)')
#plt.show()

fig = plt.figure()
plt.plot(x, COP_2, color='red') 
plt.title('Chiller 2&3')
plt.xlabel('Tcond_in (C)')
plt.ylabel('COP')
plt.show()
#
#fig= plt.figure()
#plt.plot(x, E_2, color='red')
#plt.title('Chiller 2&3') 
#plt.xlabel('Tcond_in (C)')
#plt.ylabel('E (kWh)')
#plt.show()

####################################################################################################################################################
##Test 5: Vary mcond
##Fixed parameters
Tin_cond_1 = 30
mevap_1 = 190.8
Tout_evap_1 = 5
Qe_1 = 1000
Qe_max_1 = 2000

Tin_cond_2 = 30
mevap_2 = 698.4
Tout_evap_2 = 5
Qe_2 = 3665 
Tin_cond_2 = 30
Qe_max_2 = 7330

##Determine the range of Tout_evap
mcond_1_min = 70
mcond_1_max = 700
mcond_2_min = 200
mcond_2_max = 2000

iterations = 100
##Determine the range of outlet temperatures
x_1 = np.linspace(mcond_1_min, mcond_1_max, num=iterations)
x_2 = np.linspace(mcond_2_min, mcond_2_max, num=iterations)

##Initiate a matrix to hold return values 
COP_1 = np.zeros((iterations, 1))
E_1 = np.zeros((iterations, 1))
COP_2 = np.zeros((iterations, 1))
E_2 = np.zeros((iterations, 1))

for i in range (0, iterations):
    COP_1[i, 0], E_1[i, 0] = chiller1(Tout_evap_1, Qe_1, mevap_1, Tin_cond_1, x_1[i], Qe_max_1)
    COP_2[i, 0], E_2[i, 0] = chiller2and3(Tout_evap_2, Qe_2, mevap_2, Tin_cond_2, x_2[i], Qe_max_2)

##Percentage change within range
COP_1change = (((COP_1[iterations -1, 0] - COP_1[0, 0]) / 2) / COP_1[int(iterations/2) -1, 0]) * 100
E_1change = (((E_1[iterations -1, 0] - E_1[0, 0]) / 2) / E_1[int(iterations/2) -1, 0]) * 100
COP_2change = (((COP_2[iterations -1, 0] - COP_2[0, 0]) / 2) / COP_2[int(iterations/2) -1, 0]) * 100
E_2change = (((E_2[iterations -1, 0] - E_2[0, 0]) / 2) / E_2[int(iterations/2) -1, 0]) * 100

print(COP_1change, E_1change)
print(COP_2change, E_2change)

##Plotting the data 
#plt.plot(x_1, COP_1, color='blue') 
#plt.title('Chiller 1')
#plt.xlabel('mcond (kWh)')
#plt.ylabel('COP')
#plt.show()
#
#plt.plot(x_1, E_1, color='blue')
#plt.title('Chiller 1') 
#plt.xlabel('mcond (kWh)')
#plt.ylabel('E (kWh)')
#plt.show()
#
#plt.plot(x_2, COP_2, color='red') 
#plt.title('Chiller 2&3')
#plt.xlabel('mcond (kWh)')
#plt.ylabel('COP')
#plt.show()
#
#plt.plot(x_2, E_2, color='red')
#plt.title('Chiller 2&3') 
#plt.xlabel('mcond (kWh)')
#plt.ylabel('E (kWh)')
#plt.show()