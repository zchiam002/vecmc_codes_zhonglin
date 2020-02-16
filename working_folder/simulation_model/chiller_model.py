##This is the Gordon-Ng Universal chiller model

def chiller_gnu (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max):
    
    import pandas as pd
    
    ##reg_cst[0] --- b0
    ##reg_cst[1] --- b1
    ##reg_cst[2] --- b2
    ##qc_coeff --- link between the Qe and Qc
    ##Tin_evap --- evaporator return temperature (deg C)
    ##Tout_evap --- evaporator set point temperature (deg C) 
    ##Tin_cond --- condenser inlet temperature (deg C)
    ##mevap --- flowrate through the evaporator (m3/h)
    ##mcond --- flowrate through the condenser (m3/h)
    ##Qe_max --- maximum capacity of the chiller (kWh)
    
    ##Dealing with the regression coefficients 
    b0 = reg_cst[0]
    b1 = reg_cst[1]
    b2 = reg_cst[2]

    ##Converting all the temperature values 
    Tin_evap = Tin_evap + 273.15
    Tout_evap = Tout_evap + 273.15
    Tin_cond = Tin_cond + 273.15
    
    ##Converting volume flowrate (m3/h) to (kg/s)
    mevap = mevap * 998.2 / 3600
    mcond = mcond * 998.2 / 3600
    
    ##Determining the values of Qe
    Qe = mevap * 4.2 * (Tin_evap - Tout_evap)
    
    if Qe > 0:
        a_1 = (b0 * Tin_evap) / Qe
        a_2 = b1 * ((Tin_cond - Tin_evap) / (Tin_cond * Qe))
        a_3 = Tin_evap / Tin_cond
        a_4 = (b2 * Qe) / Tin_cond
        
        temp = (((a_1 + a_2 + 1) / (a_3 - a_4)) - 1)
        COP = pow(temp, -1)
        
        ##Computing the return side values of the condenser side 
        Qc = qc_coeff * (Qe + (Qe / COP))
        if mcond != 0:
            Tout_cond = (Tin_cond + (Qc / (mcond * 4.2))) - 273.15
        else:
            Tout_cond = float('inf')
            
        ##Computing the electricity consumption 
        if (COP > 0) and (Qe < Qe_max):
            E = Qe / COP
            load_violation = 0
        else:
            E = float('inf') 
            load_violation = abs(Qe - Qe_max) / Qe_max
    
    else:
        E = 0
        COP = 0
        Tout_cond = Tin_cond
        Qc = 0
        load_violation = 0
    
    ##Assembling the return values 
    return_values = {}
    return_values['Electricity_consumption'] = E
    return_values['Coefficient_of_performance'] = COP 
    return_values['Cooling_load'] = Qe
    return_values['Tout_cond'] = Tout_cond
    return_values['Heat_rejected'] = Qc
    return_values['Load_violation'] = load_violation 

    ##Putting it in a dataframe for easy viewing 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_data = ['Electricity_consumption', return_values['Electricity_consumption'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Coefficient_of_performance', return_values['Coefficient_of_performance'], '-']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Cooling_load', return_values['Cooling_load'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Tout_cond', return_values['Tout_cond'], 'K']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Heat_rejected', return_values['Heat_rejected'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)   
    
    temp_data = ['Load_violation', return_values['Load_violation'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)  
    
    return return_values, return_values_df  