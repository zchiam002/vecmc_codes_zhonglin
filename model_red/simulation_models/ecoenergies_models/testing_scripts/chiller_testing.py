##This section tests the outputs of the various relaxed forms of the chiller models
from datetime import datetime
startTime = datetime.now() 
import sys 
sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
from chiller_models import chiller_gnu 
from chiller_models import chiller_gnu_stepwise_cop
from chiller_models import chiller_gnu_stepwise_cop_lprelax
import matplotlib.pyplot as plt

##Importing raw_data

##Testing section 
max_cap_1 = 2000
b0_1 = 0.123020043325872
b1_1 = 1044.79734873891
b2_1 = 0.0204660495029597
reg_cst_1 = [b0_1, b1_1, b2_1]
qc_coeff_1 = 0.8814766772

#max_cap_1 = 7330
#b0_1 = 1.35049420632748
#b1_1 = -134.853705222833
#b2_1 = 0.00430128306723068
#reg_cst_1 = [b0_1, b1_1, b2_1]
#qc_coeff_1 = 1.10348067074030

##Variables 
mevap = 217.3903135
mcond = 1050
Tin_evap_1 = 6.92196897
Tout_evap_1 = 5
Tin_cond_1 = 23.44221012 + 5

##Testing model 1
result_1, result_1_df = chiller_gnu(reg_cst_1, qc_coeff_1, Tin_evap_1, Tout_evap_1, Tin_cond_1, mevap, mcond, max_cap_1)
##Testing model 2
steps = 4
result_2, result_2_df = chiller_gnu_stepwise_cop(reg_cst_1, qc_coeff_1, Tin_evap_1, Tout_evap_1, Tin_cond_1, mevap, mcond, max_cap_1, steps)
##Testing model 3
bilin_pieces = 20
mevap_t = 633.6169025
mcond_t = 1050
twb = 30

result_3, result_3_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_1, qc_coeff_1, Tin_evap_1, Tout_evap_1, Tin_cond_1, mevap, mcond, max_cap_1, steps, bilin_pieces, mevap_t, mcond_t, twb)


##Printing values 
print('Model 1: \n', result_1_df)
print('Model 2: \n', result_2_df)
print('Model 3: \n', result_3_df)

print(datetime.now() - startTime)