##This script is to test the chiller output performance for different evaporator return temperature 

def chiller_testing_performance():
    
    import matplotlib.pyplot as plt
    import pandas as pd 
    
    reg_cst = [0.123020043325872, 1044.79734873891, 0.0204660495029597]
    qc_coeff = 1.09866273284186
    Tin_evap = 278.2361877 - 273.15
    Tin_cond = 289.2806598 - 273.15
    
    max_qe = 2000
    iterations = 100
    qe_step = max_qe / iterations - 1
    
    ##Initialize a storage dataframe 
    ret_values = pd.DataFrame(columns = ['Qe', 'Elect'])
    
    for i in range (0, iterations):
        
        if i == 0:
            Qe = 0.0001
        else:
            Qe = (i * qe_step)    
            return_values, return_values_df = chiller_gnu_basic (reg_cst, qc_coeff, Tin_evap, Tin_cond, Qe)
            temp_data = [Qe, return_values['Electricity_consumption']]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Qe', 'Elect'])
            ret_values = ret_values.append(temp_df, ignore_index = True)
            
    ##Plotting Qe values 
    plt.plot(ret_values['Qe'][:], ret_values['Elect'][:], color='yellow') 
    plt.xlabel('Qe')
    plt.ylabel('Elect')
    plt.show()
    
    return 

##Model 1: Gordon-ng chiller model 
def chiller_gnu_basic (reg_cst, qc_coeff, Tin_evap, Tin_cond, Qe):
    
    import pandas as pd
    
    ##reg_cst[0] --- b0
    ##reg_cst[1] --- b1
    ##reg_cst[2] --- b2
    ##qc_coeff --- link between the Qe and Qc
    ##Tin_evap --- evaporator return temperature (deg C)
    ##Tin_cond --- condenser inlet temperature (deg C)
    ##Qe --- Chiller load (kWh)
    
    ##Dealing with the regression coefficients 
    b0 = reg_cst[0]
    b1 = reg_cst[1]
    b2 = reg_cst[2]

    ##Converting all the temperature values 
    Tin_evap = Tin_evap + 273.15
    Tin_cond = Tin_cond + 273.15
    
    a_1 = (b0 * Tin_evap) / Qe
    a_2 = b1 * ((Tin_cond - Tin_evap) / (Tin_cond * Qe))
    a_3 = Tin_evap / Tin_cond
    a_4 = (b2 * Qe) / Tin_cond
    
    temp = (((a_1 + a_2 + 1) / (a_3 - a_4)) - 1)
    COP = pow(temp, -1)
    
    ##Computing the return side values of the condenser side 
    Qc = qc_coeff * (Qe + (Qe / COP))
        
    ##Computing the electricity consumption 
    if COP > 0:
        E = Qe / COP
    else:
        E = float('inf') 
    
    ##Assembling the return values 
    return_values = {}
    return_values['Electricity_consumption'] = E
    return_values['Coefficient_of_performance'] = COP 
    return_values['Heat_rejected'] = Qc

    ##Putting it in a dataframe for easy viewing 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_data = ['Electricity_consumption', return_values['Electricity_consumption'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Coefficient_of_performance', return_values['Coefficient_of_performance'], '-']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Heat_rejected', return_values['Heat_rejected'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)    
    
    return return_values, return_values_df    

#########################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    chiller_testing_performance()