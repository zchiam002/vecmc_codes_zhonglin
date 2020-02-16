##This script contains helper functions to communicate with the distribution network model 

##This function converts the decision variables into readable form for the distribution network model 
def dist_nwk_convert_variables (decision_variables, consumer_demand_df, tin_from_evap_nwk):
    
    ##decision_variables        --- input from the GA level 
    
    
    dist_nwk_decision_variables = {}
    ##dist_nwk_decision_variables['dist_nwk_gv2_split_perc']
    ##dist_nwk_decision_variables['dist_nwk_hsb_split_perc']
    ##dist_nwk_decision_variables['dist_nwk_pfa_split_perc']
    ##dist_nwk_decision_variables['dist_nwk_ser_split_perc']
    ##dist_nwk_decision_variables['total_evap_nwk_flowrate']
    ##dist_nwk_decision_variables['dist_nwk_cp_split'] 
    ##dist_nwk_decision_variables['nwk_pump_select'] 

    dist_nwk_decision_variables['dist_nwk_gv2_split_perc'] = decision_variables[13] / 100
    dist_nwk_decision_variables['dist_nwk_hsb_split_perc'] = decision_variables[14] / 100
    dist_nwk_decision_variables['dist_nwk_pfa_split_perc'] = decision_variables[15] / 100
    dist_nwk_decision_variables['dist_nwk_ser_split_perc'] = decision_variables[16] / 100
    
    dist_nwk_decision_variables['total_evap_nwk_flowrate'] = decision_variables[3] + decision_variables[6] + decision_variables[9]
    
    dist_nwk_decision_variables['dist_nwk_cp_split'] = decision_variables[11] / 100
    
    dist_nwk_decision_variables['nwk_pump_select'] = decision_variables[12] + 33
    
    
    consumer_demand = {}
    ##consumer_demand['gv2_demand']
    ##consumer_demand['hsb_demand']
    ##consumer_demand['pfa_demand']
    ##consumer_demand['ser_demand'] 

    consumer_demand['gv2_demand'] = consumer_demand_df['ss_gv2_demand'][0]
    consumer_demand['hsb_demand'] = consumer_demand_df['ss_hsb_demand'][0]
    consumer_demand['pfa_demand'] = consumer_demand_df['ss_pfa_demand'][0]
    consumer_demand['ser_demand'] = consumer_demand_df['ss_ser_demand'][0]
    
    
    outputs_from_other_models = {}
    ##outputs_from_other_models['tin_dist_nwk']
    
    outputs_from_other_models['tin_dist_nwk'] = tin_from_evap_nwk
         
    return dist_nwk_decision_variables, consumer_demand, outputs_from_other_models


###################################################################################################################################################################################################
##This function takes in the processed chiller decision variables and interacts with the distribution network model 
def dist_nwk_setup (dist_nwk_decision_variables, consumer_demand, outputs_from_other_models):
    
    ##dist_nwk_decision_variables['dist_nwk_gv2_split_perc']
    ##dist_nwk_decision_variables['dist_nwk_hsb_split_perc']
    ##dist_nwk_decision_variables['dist_nwk_pfa_split_perc']
    ##dist_nwk_decision_variables['dist_nwk_ser_split_perc']
    ##dist_nwk_decision_variables['total_evap_nwk_flowrate']
    ##dist_nwk_decision_variables['dist_nwk_cp_split'] 
    ##dist_nwk_decision_variables['nwk_pump_select'] 
    
    ##consumer_demand['gv2_demand']
    ##consumer_demand['hsb_demand']
    ##consumer_demand['pfa_demand']
    ##consumer_demand['ser_demand'] 
    
    ##outputs_from_other_models['tin_dist_nwk']
    
    import pandas as pd
    
    ##Organizing the values into the format for the dist_nwk_org model
    consumer_demand = [consumer_demand['gv2_demand'], consumer_demand['hsb_demand'], consumer_demand['pfa_demand'], consumer_demand['ser_demand']]
    m_total = dist_nwk_decision_variables['total_evap_nwk_flowrate'] * (1 - dist_nwk_decision_variables['dist_nwk_cp_split'])
    perc_split = [dist_nwk_decision_variables['dist_nwk_gv2_split_perc'], dist_nwk_decision_variables['dist_nwk_hsb_split_perc'], dist_nwk_decision_variables['dist_nwk_pfa_split_perc'],
                  dist_nwk_decision_variables['dist_nwk_ser_split_perc']]
    nwk_pump_select = dist_nwk_decision_variables['nwk_pump_select']
    tin_dist_nwk = outputs_from_other_models['tin_dist_nwk']
    
    ##Importing the distribution network model 
    from dist_nwk_model import dist_nwk_org
    dist_nwk_calculated, dist_nwk_calculated_df = dist_nwk_org(consumer_demand, m_total, perc_split, nwk_pump_select, tin_dist_nwk)
    
    ##Calculating the objective function 
    temp_data = ['dist_pump_elect_cons', dist_nwk_calculated['ice_tro_fir_elect_cons']]
    obj_func = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])

    ##Determining the outlet temperature of the evaporator network
    outlet_temperature = dist_nwk_calculated['tout_dist_nwk']
    
    ##Determining the temperature difference of each branch 
    gv2_delt = dist_nwk_calculated['gv2_tout'] - outputs_from_other_models['tin_dist_nwk']
    hsb_delt = dist_nwk_calculated['hsb_tout'] - outputs_from_other_models['tin_dist_nwk']
    pfa_delt = dist_nwk_calculated['pfa_tout'] - outputs_from_other_models['tin_dist_nwk']
    ser_delt = dist_nwk_calculated['ser_tout'] - outputs_from_other_models['tin_dist_nwk']
    
    customer_delts = [gv2_delt, hsb_delt, pfa_delt, ser_delt]
    
    ##Flow violation 
    flow_violation = dist_nwk_calculated['flow_violation']
    
    return obj_func, outlet_temperature, customer_delts, flow_violation