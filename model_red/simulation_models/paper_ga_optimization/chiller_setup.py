##This script contains helper functions to communicate with the chiller model 

##This function converts the decision variables into readable form for the chiller model 
def chiller_convert_variables (decision_variables, twb):
    
    ##decision_variables    --- input from the GA level 
    ##twb                   --- the thermodynamic wetbulb temperature (deg C)
    
    chiller_decision_variables = {}
    ##chiller_decision_variables['chiller_evap_return_temperature']                 --- the evaporator return temperature to all chillers
    ##chiller_decision_variables['chiller_cond_inlet_temperature']                  --- the condenser inlet temperature to all chillers
    
    ##chiller_decision_variables['chiller1_onoff']                                  --- a variable to determine if the chiller is on or off
    ##chiller_decision_variables['chiller1_mevap']                                  --- the evaporator flowrate through the chiller 1
    ##chiller_decision_variables['chiller1_evap_delt']                              --- the evaporator temperature difference for chiller 1
    ##chiller_decision_variables['chiller1_mcond']                                  --- the condenser flowrate through the chiller 1

    ##chiller_decision_variables['chiller2_onoff']                                  --- a variable to determine if the chiller is on or off
    ##chiller_decision_variables['chiller2_mevap']                                  --- the evaporator flowrate through the chiller 2
    ##chiller_decision_variables['chiller2_evap_delt']                              --- the evaporator temperature difference for chiller 2
    ##chiller_decision_variables['chiller2_mcond']                                  --- the condenser flowrate through the chiller 2
    
    ##chiller_decision_variables['chiller3_onoff']                                  --- a variable to determine if the chiller is on or off
    ##chiller_decision_variables['chiller3_mevap']                                  --- the evaporator flowrate through the chiller 3
    ##chiller_decision_variables['chiller3_evap_delt']                              --- the evaporator temperature difference for chiller 3
    ##chiller_decision_variables['chiller3_mcond']                                  --- the condenser flowrate through the chiller 3 
    
    cooling_tower_range = 5
    cooling_tower_min_approach = 5
    
    
    chiller_decision_variables['chiller_evap_return_temperature'] = decision_variables[0] - 273.15
    chiller_decision_variables['chiller_cond_inlet_temperature'] = ((decision_variables[1] / 100) * cooling_tower_min_approach) + (twb + cooling_tower_range)
    
    chiller_decision_variables['chiller1_onoff'] = decision_variables[2]
    chiller_decision_variables['chiller1_mevap'] = decision_variables[3]
    chiller_decision_variables['chiller1_evap_delt'] = ((decision_variables[4] / 100) * (decision_variables[0] - 274.15)) 

    if chiller_decision_variables['chiller1_onoff'] == 1: 
        chiller_decision_variables['chiller1_mcond'] = 407 
   
    chiller_decision_variables['chiller2_onoff'] = decision_variables[5]
    chiller_decision_variables['chiller2_mevap'] = decision_variables[6]
    chiller_decision_variables['chiller2_evap_delt'] = ((decision_variables[7] / 100) * (decision_variables[0] - 274.15)) 

    if chiller_decision_variables['chiller2_onoff'] == 1: 
        chiller_decision_variables['chiller2_mcond'] = 1476     
    
    chiller_decision_variables['chiller3_onoff'] = decision_variables[8]
    chiller_decision_variables['chiller3_mevap'] = decision_variables[9]
    chiller_decision_variables['chiller3_evap_delt'] = ((decision_variables[10] / 100) * (decision_variables[0] - 274.15)) 

    if chiller_decision_variables['chiller3_onoff'] == 1: 
        chiller_decision_variables['chiller3_mcond'] = 1476      
        
    return chiller_decision_variables

###################################################################################################################################################################################################
##This function takes in the processed chiller decision variables and interacts with the chiller model 
def chiller_setup (chiller_decision_variables):
    
    ##chiller_decision_variables --- a dataframe containing the decision variables 
    
    ##chiller_decision_variables['chiller_evap_return_temperature']                 --- the evaporator return temperature to all chillers
    ##chiller_decision_variables['chiller_cond_inlet_temperature']                  --- the condenser inlet temperature to all chillers
    
    ##chiller_decision_variables['chiller1_onoff']                                  --- a variable to determine if the chiller is on or off
    ##chiller_decision_variables['chiller1_evap_delt']                              --- the evaporator temperature difference for chiller 1
    ##chiller_decision_variables['chiller1_mevap']                                  --- the evaporator flowrate through the chiller 1
    ##chiller_decision_variables[chiller1_mcond]                                    --- the condenser flowrate through the chiller 1

    ##chiller_decision_variables['chiller2_onoff']                                  --- a variable to determine if the chiller is on or off
    ##chiller_decision_variables['chiller2_evap_delt']                              --- the evaporator temperature difference for chiller 2
    ##chiller_decision_variables['chiller2_mevap']                                  --- the evaporator flowrate through the chiller 2
    ##chiller_decision_variables[chiller2_mcond]                                    --- the condenser flowrate through the chiller 2

    ##chiller_decision_variables['chiller3_onoff']                                  --- a variable to determine if the chiller is on or off
    ##chiller_decision_variables['chiller3_evap_delt']                              --- the evaporator temperature difference for chiller 3
    ##chiller_decision_variables['chiller3_mevap']                                  --- the evaporator flowrate through the chiller 3
    ##chiller_decision_variables[chiller3_mcond]                                    --- the condenser flowrate through the chiller 3      
    
    import pandas as pd 
    
    ##Importing the chiller model 
    from chiller_model import chiller_gnu

    ##Defining chiller parameters 
    small_chiller_reg_cst = [0.123020043325872, 1044.79734873891, 0.0204660495029597]
    small_chiller_qc_coeff = 1.09866273284186
    small_chiller_Qe_max = 2000
    big_chiller_reg_cst = [1.35049420632748, -134.853705222833, 0.00430128306723068]
    big_chiller_qc_coeff = 1.10348067074030
    big_chiller_Qe_max = 7330
    
    ##Converting main values
    tin_evap = chiller_decision_variables['chiller_evap_return_temperature'] 
    tin_cond = chiller_decision_variables['chiller_cond_inlet_temperature'] 
    
    ##Converting onoff values 
    ch1_onoff = chiller_decision_variables['chiller1_onoff']
    ch2_onoff = chiller_decision_variables['chiller2_onoff']
    ch3_onoff = chiller_decision_variables['chiller3_onoff']
    
    ##Running chiller 1 model 
    if ch1_onoff == 1:
        ch1_tout_evap = tin_evap - chiller_decision_variables['chiller1_evap_delt']
        ch1_mevap = chiller_decision_variables['chiller1_mevap']
        ch1_mcond = chiller_decision_variables['chiller1_mcond']
        chiller1_calculated_values, chiller1_calculated_values_df = chiller_gnu (small_chiller_reg_cst, small_chiller_qc_coeff, tin_evap, ch1_tout_evap, tin_cond, ch1_mevap, ch1_mcond, 
                                                                                 small_chiller_Qe_max)
        chiller1_econs = chiller1_calculated_values['Electricity_consumption'] 
        chiller1_tout_cond = chiller1_calculated_values['Tout_cond']
        chiller1_load_violation = 0
    else:
        chiller1_econs = 0
        chiller1_tout_cond = chiller_decision_variables['chiller_cond_inlet_temperature']
        chiller1_load_violation = 0
        
    ##Running chiller 2 model
    if ch2_onoff == 1:
        ch2_tout_evap = tin_evap - chiller_decision_variables['chiller2_evap_delt']
        ch2_mevap = chiller_decision_variables['chiller2_mevap']
        ch2_mcond = chiller_decision_variables['chiller2_mcond']
        chiller2_calculated_values, chiller2_calculated_values_df = chiller_gnu (big_chiller_reg_cst, big_chiller_qc_coeff, tin_evap, ch2_tout_evap, tin_cond, ch2_mevap, ch2_mcond, 
                                                                                 big_chiller_Qe_max)    
        chiller2_econs = chiller2_calculated_values['Electricity_consumption'] 
        chiller2_tout_cond = chiller2_calculated_values['Tout_cond']
        chiller2_load_violation = 0
    else:
        chiller2_econs = 0
        chiller2_tout_cond = chiller_decision_variables['chiller_cond_inlet_temperature']
        chiller2_load_violation = 0
        
    ##Running chiller 3 model 
    if ch3_onoff == 1:    
        ch3_tout_evap = tin_evap - chiller_decision_variables['chiller3_evap_delt']
        ch3_mevap = chiller_decision_variables['chiller3_mevap']
        ch3_mcond = chiller_decision_variables['chiller3_mcond']
        chiller3_calculated_values, chiller3_calculated_values_df = chiller_gnu (big_chiller_reg_cst, big_chiller_qc_coeff, tin_evap, ch3_tout_evap, tin_cond, ch3_mevap, ch3_mcond, 
                                                                                 big_chiller_Qe_max)
        chiller3_econs = chiller3_calculated_values['Electricity_consumption'] 
        chiller3_tout_cond = chiller3_calculated_values['Tout_cond']
        chiller3_load_violation = 0

    else:
        chiller3_econs = 0
        chiller3_tout_cond = chiller_decision_variables['chiller_cond_inlet_temperature']
        chiller3_load_violation = 0
        
    ##Consolidating the condenser outlet temperatures 
    temp_data = [['chiller_1_tout_cond', chiller1_tout_cond], 
                 ['chiller_2_tout_cond', chiller2_tout_cond], 
                 ['chiller_3_tout_cond', chiller3_tout_cond]]
    chiller_t_out_cond = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])
            
    ##Consolidating the output values for the objective function  
    temp_data = [['chiller_1_e_cons', chiller1_econs], 
                 ['chiller_2_e_cons', chiller2_econs], 
                 ['chiller_3_e_cons', chiller3_econs]]    
    obj_func = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])
    
    ##Consolidating the load violation from the chiller 
    temp_data = [['chiller_1_load_violation', chiller1_load_violation], 
                 ['chiller_2_load_violation', chiller2_load_violation], 
                 ['chiller_3_load_violation', chiller3_load_violation]] 
    chiller_load_violation = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])
    
    return obj_func, chiller_t_out_cond, chiller_load_violation 