##This script contains functions which need to be manually edited for the solver to run 

##This function takes in manual inputs from the used to build the parameters for the MILP solver 
def mrs_manual_edit_milp_param (cooling_load_data, weather_condition, ga_inputs, piecewise_linear_steps):
    
    ##cooling_load_data                 --- the associated cooling load data 
    ##weather_condition                 --- the associated weather condition
    ##ga_inputs                         --- inputs from the genetic algorithm
    ##piecewise_linear_steps            --- the number of pieces used to linearize the models 

    import pandas as pd 
    
    ##Manually some input parameters  
    cond_temp = weather_condition['T_WB'][0] + 5 + 273.15                   ##Just an assumption for the condenser temperature 
    
    ##Initiate a dataframe to hold values 
    milp_param = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    ##############################################################################################################
    ##chiller_evap_flow_consol    
    input_value = {}
    input_value['Name'] = 'chiller_evap_flow_consol_tenwkflow'                      ##Name of the parameter format = <model name>_<parameter name>
    input_value['Value'] = ga_inputs['evap_flow'][0]                                ##Value of the parameter
    input_value['Unit'] = 'm3/h'                                                    ##Units of the parameter
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)       
    
    ##############################################################################################################    
    ##chiller_ret
    input_value = {}
    input_value['Name'] = 'chiller_ret_etret' 
    input_value['Value'] = ga_inputs['tin_evap'][0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)  
       
    ##############################################################################################################
    ##chiller1_evap    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_etret' 
    input_value['Value'] = ga_inputs['tin_evap'][0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_ctin' 
    input_value['Value'] = cond_temp
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)   
    
    ##############################################################################################################    
    ##chiller1_evap_nwk
    input_value = {}
    input_value['Name'] = 'chiller1_evap_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller1_evap_nwk_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)

    ##############################################################################################################
    ##chiller1_evap_pump       
    input_value = {}
    input_value['Name'] = 'chiller1_evap_pump_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)    

    ##############################################################################################################    
    ##chiller2_evap
    input_value = {}
    input_value['Name'] = 'chiller2_evap_etret' 
    input_value['Value'] = ga_inputs['tin_evap'][0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller2_evap_ctin' 
    input_value['Value'] = cond_temp
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller2_evap_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller2_evap_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    ##############################################################################################################    
    ##chiller2_evap_nwk
    input_value = {}
    input_value['Name'] = 'chiller2_evap_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller2_evap_nwk_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################
    ##chiller2_evap_pump       
    input_value = {}
    input_value['Name'] = 'chiller2_evap_pump_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##cp_nwk    
    input_value = {}
    input_value['Name'] = 'cp_nwk_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)   
    
    ##############################################################################################################
    ##dist_nwk_pump  
    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_choice'              ##There are 2 pumps to choose from pump 0 and pump 1
    input_value['Value'] = 0
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)       
    
    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)  
    
    ##############################################################################################################
    ##gv2_nwk   
    input_value = {}
    input_value['Name'] = 'gv2_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'gv2_nwk_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##gv2_substation
    input_value = {}
    input_value['Name'] = 'gv2_substation_demand' 
    input_value['Value'] = cooling_load_data['gv2_ss'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'gv2_substation_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##hsb_nwk 
    input_value = {}
    input_value['Name'] = 'hsb_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'hsb_nwk_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)      
    
    ##############################################################################################################
    ##hsb_substation  
    input_value = {}
    input_value['Name'] = 'hsb_substation_demand' 
    input_value['Value'] = cooling_load_data['hsb_ss'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'hsb_substation_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    ##############################################################################################################
    ##ice_nwk 
    input_value = {}
    input_value['Name'] = 'ice_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_linear_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'ice_nwk_tenwkflow' 
    input_value['Value'] = ga_inputs['evap_flow'][0]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    milp_param = milp_param.append(temp_df, ignore_index=True) 

    return milp_param