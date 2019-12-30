##This is a test script of the universal cooling tower model 

import numpy as np
from sklearn import linear_model 
import matplotlib.pyplot as plt 
#################################################################################################################################################################
#################################################################################################################################################################
##################################################################### FUNCTION WRITING AREA #####################################################################
#################################################################################################################################################################
#################################################################################################################################################################

##Letting Twi-Two be delT, we want to find the relationship between delT, ma, Twi 

def delT_calc (ma, Twi, constants):
    ##Constants
    mw = constants[0]                      ##mw (m3/h)
    Twb = constants[1]                     ##Twb (K)
    Two = constants[2]                     ##Two (K), quite irrelevant actually 
    
    ##Converting mw to kg/h
    mw = mw * 998.2    

    ##Calculated coefficients 
    b0 = 0.14029549639345207	
    b1 = 0.600266127023157	
    b2 = -0.0211475692653011	
    b3 = 0.2792094538127389	
    b4 = 9.294683422723725E-4
    b5 = 0.16052557022400754 
    
    term1 = b0 * (Twi - Twb)
    term2 = b1 * (ma / mw) * (Twi - Twb)
    term3 = b2 * pow((Twi - Twb), 2)
    term4 = b3 * pow((ma / mw), 2) * (Twi - Twb)
    term5 = b4 * pow((Twi - Twb), 3)
    term6 = b5 * (ma / mw) * pow((Twi - Twb), 2)
    
    delT_overall = term1 + term2 + term3 + term4 + term5 + term6

    return delT_overall
    
#################################################################################################################################################################
#################################################################################################################################################################
############################################################################## TESTING AREA #####################################################################
#################################################################################################################################################################
#################################################################################################################################################################

ma_min = 0
ma_max = 369117 ##in kg/hr
steps_ma = 100

Twi_min = 15 
Twi_max = 50
steps_Twi = 100 

##Constants 
mw = 100
Twb = 15
Two = Twb + 1

##Conversion 
Twi_min = Twi_min + 273.15
Twi_max = Twi_max + 273.15
Twb = Twb + 273.15
Two = Two + 273.15

constants = [mw, Twb, Two]

##Calculations Delta t linear sum

valuesX = np.zeros(((steps_ma*steps_Twi),2))
valuesY = np.zeros(((steps_ma*steps_Twi),1))
ma_increment = (ma_max - ma_min) / steps_ma
Twi_increment = (Twi_max - Twi_min) / steps_Twi
 
row = 0
for i in range (0, steps_ma):
    for j in range (0, steps_Twi):
        valuesX[row, 0] = ma_min + (i * ma_increment)
        valuesX[row, 1] = Twi_min + (j * Twi_increment)
        valuesY[row, 0] = delT_calc(valuesX[row, 0],  valuesX[row, 1], constants)
        row = row + 1
        
clf = linear_model.LinearRegression(fit_intercept = True)
clf.fit(valuesX, valuesY)
result_1 = clf.score(valuesX, valuesY, sample_weight=None)
lin_coeff_1 = clf.coef_
int_1 = clf.intercept_

print(result_1)
print(lin_coeff_1[0,1])
print(int_1)

regY = np.zeros(((steps_ma*steps_Twi), 1))
for i in range (0, (steps_ma*steps_Twi)):
    regY[i,0] = lin_coeff_1[0,0]*valuesX[i, 0] + lin_coeff_1[0,1]*valuesX[i, 1] + int_1

plt.plot(valuesY, regY)
plt.show()

plt.plot(valuesX[:, 0], valuesY, 'o')
plt.title('DelT vs ma')
plt.xlabel('ma')
plt.ylabel('DelT')
plt.show()

plt.plot(valuesX[:, 1], valuesY, 'o')
plt.title('DelT vs Twi')
plt.xlabel('Twi')
plt.ylabel('DelT')
plt.show()

##Calculations Delta t quad sum 

valuesX = np.zeros(((steps_ma*steps_Twi),5))
valuesY = np.zeros(((steps_ma*steps_Twi),1))
ma_increment = (ma_max - ma_min) / steps_ma
Twi_increment = (Twi_max - Twi_min) / steps_Twi
 
row = 0
for i in range (0, steps_ma):
    for j in range (0, steps_Twi):
        valuesX[row, 0] = 0 #pow(ma_min + (i * ma_increment),2)
        valuesX[row, 1] = ma_min + (i * ma_increment)
        valuesX[row, 2] = 0 #pow(Twi_min + (j * Twi_increment), 2)
        valuesX[row, 3] = Twi_min + (j * Twi_increment)
        valuesX[row, 4] = (ma_min + (i * ma_increment)) * (Twi_min + (j * Twi_increment))
        valuesY[row, 0] = delT_calc(valuesX[row, 1],  valuesX[row, 3], constants)
        row = row + 1

clf = linear_model.LinearRegression(fit_intercept = True)
clf.fit(valuesX, valuesY)
result_1 = clf.score(valuesX, valuesY, sample_weight=None)
lin_coeff_1 = clf.coef_
int_1 = clf.intercept_

print(result_1)
print(lin_coeff_1)
print(int_1)

regY = np.zeros(((steps_ma*steps_Twi), 1))
for i in range (0, (steps_ma*steps_Twi)):
    regY[i,0] = lin_coeff_1[0,0]*valuesX[i, 0] + lin_coeff_1[0,1]*valuesX[i, 1] + lin_coeff_1[0,2]*valuesX[i, 2] + lin_coeff_1[0,3]*valuesX[i, 3] + lin_coeff_1[0,4]*valuesX[i, 4] + int_1

plt.plot(valuesY, regY, 'o')
plt.show()

plt.plot(valuesX[:, 1], valuesY, 'o')
plt.title('DelT vs ma')
plt.xlabel('ma')
plt.ylabel('DelT')
plt.show()

plt.plot(valuesX[:, 3], valuesY, 'o')
plt.title('DelT vs Twi')
plt.xlabel('Twi')
plt.ylabel('DelT')
plt.show()
