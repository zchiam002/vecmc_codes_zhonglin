##This function prepares the look-up table for evaporator and condenser pump system linearized parameters 

def prepare_evap_cond_pump_lin_coeff ():
    
    import os
    current_directory = os.path.dirname(__file__)[:-76] + '//' 
    import pandas as pd 
    from evap_cond_pump_model import evap_pump_ch1
    from evap_cond_pump_model import evap_pump_ch2
    from evap_cond_pump_model import evap_pump_ch3
    from evap_cond_pump_model import cond_pump_ch1
    from evap_cond_pump_model import cond_pump_ch2
    from evap_cond_pump_model import cond_pump_ch3
    
    ##Savefile directory
    save_dir = current_directory + 'master_level_models\\chiller_optimization_dist_nwk_ga_nb_master_level_models\\look_up_tables\\'
    
    ##Initialize a dataframe to hold the values 
    evap_cond_lin_values = pd.DataFrame(columns = ['Name', 'm_coeff', 'p_coeff', 'cst', 'max_flow', 'max_pressure','r2_value'])
    
    ##Dealing with the evaporator pumps
    ##The return values are m_coeff, p_coeff, cst, max_flow, regression coefficient 
    
    ch1_evap_pump_values = evap_pump_ch1()
    name_ch1_evap = 'ch1_evap_pump_values'
    data_ch1_evap = [name_ch1_evap, ch1_evap_pump_values[0,0], ch1_evap_pump_values[1,0], ch1_evap_pump_values[2,0], ch1_evap_pump_values[3,0], ch1_evap_pump_values[4,0], ch1_evap_pump_values[5,0]]
    data_ch1_evap_df = pd.DataFrame(data = [data_ch1_evap], columns = ['Name', 'm_coeff', 'p_coeff', 'cst', 'max_flow', 'max_pressure', 'r2_value'])
    evap_cond_lin_values = evap_cond_lin_values.append(data_ch1_evap_df, ignore_index=True)
    
    ch2_evap_pump_values = evap_pump_ch2()
    name_ch2_evap = 'ch2_evap_pump_values'
    data_ch2_evap = [name_ch2_evap, ch2_evap_pump_values[0,0], ch2_evap_pump_values[1,0], ch2_evap_pump_values[2,0], ch2_evap_pump_values[3,0], ch2_evap_pump_values[4,0], ch2_evap_pump_values[5,0]]
    data_ch2_evap_df = pd.DataFrame(data = [data_ch2_evap], columns = ['Name', 'm_coeff', 'p_coeff', 'cst', 'max_flow', 'max_pressure', 'r2_value'])
    evap_cond_lin_values = evap_cond_lin_values.append(data_ch2_evap_df, ignore_index=True)
    
    ch3_evap_pump_values = evap_pump_ch3()
    name_ch3_evap = 'ch3_evap_pump_values'
    data_ch3_evap = [name_ch3_evap, ch3_evap_pump_values[0,0], ch3_evap_pump_values[1,0], ch3_evap_pump_values[2,0], ch3_evap_pump_values[3,0], ch3_evap_pump_values[4,0], ch3_evap_pump_values[5,0]]
    data_ch3_evap_df = pd.DataFrame(data = [data_ch3_evap], columns = ['Name', 'm_coeff', 'p_coeff', 'cst', 'max_flow', 'max_pressure', 'r2_value'])
    evap_cond_lin_values = evap_cond_lin_values.append(data_ch3_evap_df, ignore_index=True)
    
    ##Dealing with the condensation pumps
    ##The return values are m_coeff, p_coeff, cst, max_flow, regression coefficient\
    
    ch1_cond_pump_values = cond_pump_ch1()
    name_ch1_cond = 'ch1_cond_pump_values'
    data_ch1_cond = [name_ch1_cond, ch1_cond_pump_values[0,0], ch1_cond_pump_values[1,0], ch1_cond_pump_values[2,0], ch1_cond_pump_values[3,0], ch1_cond_pump_values[4,0], ch1_cond_pump_values[5,0]]
    data_ch1_cond_df = pd.DataFrame(data = [data_ch1_cond], columns = ['Name', 'm_coeff', 'p_coeff', 'cst', 'max_flow', 'max_pressure', 'r2_value'])
    evap_cond_lin_values = evap_cond_lin_values.append(data_ch1_cond_df, ignore_index=True)
    
    ch2_cond_pump_values = cond_pump_ch2()
    name_ch2_cond = 'ch2_cond_pump_values'
    data_ch2_cond = [name_ch2_cond, ch2_cond_pump_values[0,0], ch2_cond_pump_values[1,0], ch2_cond_pump_values[2,0], ch2_cond_pump_values[3,0], ch2_cond_pump_values[4,0], ch2_cond_pump_values[5,0]]
    data_ch2_cond_df = pd.DataFrame(data = [data_ch2_cond], columns = ['Name', 'm_coeff', 'p_coeff', 'cst', 'max_flow', 'max_pressure', 'r2_value'])
    evap_cond_lin_values = evap_cond_lin_values.append(data_ch2_cond_df, ignore_index=True)
    
    ch3_cond_pump_values = cond_pump_ch3()
    name_ch3_cond = 'ch3_cond_pump_values'
    data_ch3_cond = [name_ch3_cond, ch3_cond_pump_values[0,0], ch3_cond_pump_values[1,0], ch3_cond_pump_values[2,0], ch3_cond_pump_values[3,0], ch3_cond_pump_values[4,0], ch3_cond_pump_values[5,0]]
    data_ch3_cond_df = pd.DataFrame(data = [data_ch3_cond], columns = ['Name', 'm_coeff', 'p_coeff', 'cst', 'max_flow', 'max_pressure', 'r2_value'])
    evap_cond_lin_values = evap_cond_lin_values.append(data_ch3_cond_df, ignore_index=True)
    
    evap_cond_lin_values.to_csv(save_dir + 'evap_cond_pump_lincoeff.csv')
    
    return 

#####################################################################################################################################################################################################

###Running the extraction algorithm  
#if __name__ == '__main__':
#    prepare_evap_cond_pump_lin_coeff ()
    