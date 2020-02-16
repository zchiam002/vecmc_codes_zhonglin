##This is the revised cooling tower model 


def cooling_tower_uem_revised (perc_fan, total_water_flow_config, tw_in, twb):
    
    import pandas as pd 
    
    ##perc_fan --- the percentage at which the cooling tower 1's fan is operated (0 - 100 %)
    ##total_water_flow_config --- the total flowrate of water into the configuration 
    ##tw_in --- the temperature of water into the cooling tower configuration 
    ##twb --- the ambient wet_bulb temperature 
    
    ##Cooling tower regression derived coefficients 
    b0 = 0.14029549639345207	
    b1 = 0.600266127023157	
    b2 = -0.0211475692653011	
    b3 = 0.2792094538127389	
    b4 = 9.294683422723725*pow(10, -4)
    b5 = 0.16052557022400754
    
    make_up_water_correct_coeff = 2.3294122
    
    ct_reg_coeff = [b0, b1, b2, b3, b4, b5]
    towers_in_config = 1
    flow_rate_to_each_tower = total_water_flow_config / towers_in_config 
    del_t_max = tw_in - twb+1
    
    ##Deriving the flowrate of air
    min_air_flow = 0            ##kg/h
    max_air_flow = 369117       ##kg/h
    ##Maximum electricity consumption by fan 
    elect_max_fan = 22          ##kWh
    
    return_values = {}
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_values = pd.DataFrame(columns = ['Name', 'Value'])
    

    ct_id = 'ct' + str(i + 1)
    flow_ma_temp = perc_fan[i] * (max_air_flow - min_air_flow)
    constants_temp = [flow_rate_to_each_tower, twb]
    del_t_temp = delT_calc (ct_reg_coeff, flow_ma_temp, tw_in, constants_temp)
    if del_t_temp > del_t_max: 
        del_t_temp = del_t_max
    
    ##Calculating exit water temperature of unit 
    name_temp = ct_id + '_t_out'
    value = tw_in - del_t_temp
    data_temp = [name_temp, value]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    temp_values = temp_values.append(temp_df, ignore_index = True)
    
    ##Calculating the electricity consumption of the fan 
    name_temp = ct_id + '_elect_fan'
    value = perc_fan[i] * elect_max_fan 
    data_temp = [name_temp, value]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    temp_values = temp_values.append(temp_df, ignore_index = True)
    
    ##Calculating the make up water needed 
    name_temp = ct_id + '_water_cons'     
    value = (0.0027 + (0.01 * (del_t_temp/5.6))) * flow_rate_to_each_tower * make_up_water_correct_coeff
    data_temp = [name_temp, value]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    temp_values = temp_values.append(temp_df, ignore_index = True)

    ##Writing values in a dictionary  
    return_values[temp_values['Name'][(i * 3) + 0]] = temp_values['Value'][(i * 3) + 0]
    return_values[temp_values['Name'][(i * 3) + 1]] = temp_values['Value'][(i * 3) + 1]
    return_values[temp_values['Name'][(i * 3) + 2]] = temp_values['Value'][(i * 3) + 2]
    ##Writing values in a dataframe 
    data_temp = [temp_values['Name'][(i * 3) + 0], temp_values['Value'][(i * 3) + 0], 'K']
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
    return_values_df = return_values_df.append(temp_df, ignore_index = True)
    
    data_temp = [temp_values['Name'][(i * 3) + 1], temp_values['Value'][(i * 3) + 1], 'kWh']
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
    return_values_df = return_values_df.append(temp_df, ignore_index = True)
    
    data_temp = [temp_values['Name'][(i * 3) + 2], temp_values['Value'][(i * 3) + 2], 'm3/h']
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
    return_values_df = return_values_df.append(temp_df, ignore_index = True)
            
    return return_values, return_values_df