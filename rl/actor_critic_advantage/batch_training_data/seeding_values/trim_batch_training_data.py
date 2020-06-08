##This function trims the batch training data 
def trim_batch_training_data ():
    
    import pandas as pd 
    import os 
    current_directory = os.path.dirname(__file__)[:-84] + '//'
    
    ##Importing the training data 
    org_training_data = pd.read_csv(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//batch_training_data//seeding_values//fully_prepared_norm.csv')
    
    return_df = pd.DataFrame(columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'T_WB', 'return_obj', 'temp_error'])
    
    dim_org_training_data = org_training_data.shape 
    
    for i in range (0, dim_org_training_data[0]):
        if (org_training_data['return_obj'][i] < 5000) and (org_training_data['temp_error'][i] < 5000):
            temp_data = [org_training_data['T_evap_in'][i], org_training_data['evap_flow'][i], org_training_data['ss_gv2_demand'][i], org_training_data['ss_hsb_demand'][i], 
                         org_training_data['ss_pfa_demand'][i], org_training_data['ss_ser_demand'][i], org_training_data['T_WB'][i], org_training_data['return_obj'][i], 
                         org_training_data['temp_error'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'T_WB', 
                                                                  'return_obj', 'temp_error'])
            return_df = return_df.append(temp_df, ignore_index = True)
    
    ##Saving the new dataframe 
    return_df.to_csv(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//batch_training_data//seeding_values//cleansed_norm.csv')
    
    return

#################################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    trim_batch_training_data()