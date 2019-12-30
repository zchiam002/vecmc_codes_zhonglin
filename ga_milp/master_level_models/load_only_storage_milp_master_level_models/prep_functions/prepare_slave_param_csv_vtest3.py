##This function writes the parameters and master decision variables into a csv file for the slave to read
##Version 3 has multi-time handling capabilities 

def prepare_slave_param_csv_vtest3 (var, demand, weather, elect_tariff, piecewise_steps, time_steps):
    
    import pandas as pd 
    
    ##var --- the master decision variables for this given MILP iteration 
    ##demand --- the given demand profile to be fulfilled 
    ##elect_tariff --- the pricing structure for electricity 
    ##piecewise_steps --- the number of piecewise steps 
    ##time_steps --- the number of hourly time steps 
    
    mdv_slave_param = fill_in_values_for_multi_time (var, demand, weather, elect_tariff, piecewise_steps, time_steps)
    
    return mdv_slave_param

############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
##Additional functions 

##This function appends the related values for a multi-time MILP problem 
def fill_in_values_for_multi_time (var, demand, weather, elect_tariff, piecewise_steps, time_steps):
    
    import pandas as pd

    ##var --- the master decision variables for this given MILP iteration 
    ##demand --- the given demand profile to be fulfilled 
    ##elect_tariff --- the pricing structure for electricity 
    ##piecewise_steps --- the number of piecewise steps 
    ##time_steps --- the number of hourly time steps 

    ##Creating an empty dataframe to be filled
    column_header = ['Name', 'Unit']
    
    for i in range (0, time_steps):
        entry_1 = 'Value_' + str(i)
        column_header.append(entry_1)
        
    mdv_slave_param = pd.DataFrame (columns = [column_header])
    
    ###########################################################################
    ##Chiller1     
    ###########################################################################
    
    input_value = {}                                                        
    input_value['Name'] = 'chiller1_wet_bulb_temp' 
    input_value['Unit'] = 'deg C'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(weather['T_WB'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'chiller1_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)                  
    

    input_value = {}
    input_value['Name'] = 'chiller1_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ###########################################################################
    ##Chiller2
    ###########################################################################    

    input_value = {}                                                        
    input_value['Name'] = 'chiller2_wet_bulb_temp' 
    input_value['Unit'] = 'deg C'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(weather['T_WB'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'chiller2_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)                  
    

    input_value = {}
    input_value['Name'] = 'chiller2_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ###########################################################################
    ##Chiller3
    ###########################################################################    

    input_value = {}                                                        
    input_value['Name'] = 'chiller3_wet_bulb_temp' 
    input_value['Unit'] = 'deg C'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(weather['T_WB'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'chiller3_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)                  
    

    input_value = {}
    input_value['Name'] = 'chiller3_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ###########################################################################
    ##Combined_substation
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'combined_substation_gv2_demand' 
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(demand['ss_gv2_demand'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 


    input_value = {}
    input_value['Name'] = 'combined_substation_hsb_demand' 
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(demand['ss_hsb_demand'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
    
    
    input_value = {}
    input_value['Name'] = 'combined_substation_pfa_demand' 
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(demand['ss_pfa_demand'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    
    input_value = {}
    input_value['Name'] = 'combined_substation_ser_demand' 
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(demand['ss_ser_demand'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ###########################################################################
    ##Cond_nwk
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'cond_nwk_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ###########################################################################
    ##Cond_pump1
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'cond_pump1_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'cond_pump1_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ###########################################################################
    ##Cond_pump2
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'cond_pump2_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'cond_pump2_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
    
    ###########################################################################
    ##Cond_pump3
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'cond_pump3_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'cond_pump3_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ###########################################################################
    ##Cooling_towers
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'cooling_towers_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ###########################################################################
    ##Dist_nwk_pump
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    

    ###########################################################################
    ##Evap_nwk
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'evap_nwk_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ###########################################################################
    ##Evap_pump1
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'evap_pump1_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'evap_pump1_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ###########################################################################
    ##Evap_pump2
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'evap_pump2_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'evap_pump2_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
    
    ###########################################################################
    ##Evap_pump3
    ###########################################################################

    input_value = {}
    input_value['Name'] = 'evap_pump3_steps' 
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(piecewise_steps)
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)


    input_value = {}
    input_value['Name'] = 'evap_pump3_time_dependent_elect_tariff' 
    input_value['Unit'] = 'euro/kWh'
    
    temp_values = [input_value['Name'], input_value['Unit']]
    
    ##Appending multi-time data 
    for i in range (0, time_steps):
        temp_values.append(elect_tariff['Price'][i])
    
    temp_df = pd.DataFrame(data = [temp_values], columns = column_header)
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    return mdv_slave_param

