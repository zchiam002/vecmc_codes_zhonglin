##This script contains helper functions to communicate with the cooling tower model 

##This function converts the decision variables into readable form for the cooling tower model 
def cooling_tower_convert_variables (decision_variables, twb, cond_flow, tin):
    
    ##decision_variables        --- input from the GA level 
    ##twb                       --- the wetbubl temperature
    ##cond_flow_in              --- condenser flowrate 
    ##tin                       --- exit temperature from the condenser network 

    cooling_tower_decision_variables = {}
    ##cooling_tower_decision_variables['cooling_tower_1_air']    
    ##cooling_tower_decision_variables['cooling_tower_2_air']   
    ##cooling_tower_decision_variables['cooling_tower_3_air']  
    ##cooling_tower_decision_variables['cooling_tower_4_air']  
    ##cooling_tower_decision_variables['cooling_tower_5_air']
    
    max_air_flow = 369117
    num_cooling_towers = 5
    
    cooling_tower_decision_variables['cooling_tower_1_air'] = (decision_variables[17] / 100) * max_air_flow
    cooling_tower_decision_variables['cooling_tower_2_air'] = (decision_variables[18] / 100) * max_air_flow
    cooling_tower_decision_variables['cooling_tower_3_air'] = (decision_variables[19] / 100) * max_air_flow
    cooling_tower_decision_variables['cooling_tower_4_air'] = (decision_variables[20] / 100) * max_air_flow
    cooling_tower_decision_variables['cooling_tower_5_air'] = (decision_variables[21] / 100) * max_air_flow    
    
    cooling_tower_decision_variables['twb'] = twb
    cooling_tower_decision_variables['m_ct'] = cond_flow / num_cooling_towers
    cooling_tower_decision_variables['tin'] = tin
    
    return cooling_tower_decision_variables 

###################################################################################################################################################################################################
##This function takes in the processed chiller decision variables and interacts with the chiller model 
def cooling_tower_setup (cooling_tower_decision_variables):
    

    ##cooling_tower_decision_variables['cooling_tower_1_air']    
    ##cooling_tower_decision_variables['cooling_tower_2_air']   
    ##cooling_tower_decision_variables['cooling_tower_3_air']  
    ##cooling_tower_decision_variables['cooling_tower_4_air']  
    ##cooling_tower_decision_variables['cooling_tower_5_air']
    
    ##cooling_tower_decision_variables['twb']
    ##cooling_tower_decision_variables['m_ct']
    ##cooling_tower_decision_variables['tin']    
      
    from cooling_tower_model import ct_uem_original
    import pandas as pd
    
    twb = cooling_tower_decision_variables['twb']
    m_ct = cooling_tower_decision_variables['m_ct']
    t_in = cooling_tower_decision_variables['tin'] 
    
    ct1_m_air = cooling_tower_decision_variables['cooling_tower_1_air'] 
    ct1_dt, ct1_e_cons = ct_uem_original (twb, m_ct, ct1_m_air, t_in)
    
    ct2_m_air = cooling_tower_decision_variables['cooling_tower_2_air'] 
    ct2_dt, ct2_e_cons = ct_uem_original (twb, m_ct, ct2_m_air, t_in)    
    
    ct3_m_air = cooling_tower_decision_variables['cooling_tower_3_air'] 
    ct3_dt, ct3_e_cons = ct_uem_original (twb, m_ct, ct3_m_air, t_in)     

    ct4_m_air = cooling_tower_decision_variables['cooling_tower_4_air'] 
    ct4_dt, ct4_e_cons = ct_uem_original (twb, m_ct, ct4_m_air, t_in)  

    ct5_m_air = cooling_tower_decision_variables['cooling_tower_5_air'] 
    ct5_dt, ct5_e_cons = ct_uem_original (twb, m_ct, ct5_m_air, t_in)    
    
    temp_data = [['ct1_e_cons', ct1_e_cons],
                 ['ct2_e_cons', ct2_e_cons],
                 ['ct3_e_cons', ct3_e_cons],
                 ['ct4_e_cons', ct4_e_cons],
                 ['ct5_e_cons', ct5_e_cons]]
    obj_func = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])
    
    temp_data = [['ct1_dt', ct1_dt],
                 ['ct2_dt', ct2_dt],
                 ['ct3_dt', ct3_dt],
                 ['ct4_dt', ct4_dt],
                 ['ct5_dt', ct5_dt]]
    ct_delt = pd.DataFrame(data = temp_data, columns = ['Name', 'Value'])
      
    return obj_func, ct_delt