##This function takes in the master_variables and converts them into input parameters for the slave optimization 

def master_to_slave(all_var, sub_station_tinlim, sub_station_toutlim, demand_time, wet_bulb_temp):
    import pandas as pd

    m2s_param = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    ##1
    temp_ph = {}
    temp_ph['Name'] = 'chiller1_em'
    temp_ph['Value'] = all_var[0]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##2
    temp_ph = {}
    temp_ph['Name'] = 'chiller1_etret'
    temp_ph['Value'] = all_var[14]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##3
    temp_ph = {}
    temp_ph['Name'] = 'chiller1_cm'
    temp_ph['Value'] = all_var[1]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##4
    temp_ph = {}
    temp_ph['Name'] = 'chiller1_ctin'
    temp_ph['Value'] = all_var[12]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##5
    temp_ph = {}
    temp_ph['Name'] = 'chiller1_tenwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##6
    temp_ph = {}
    temp_ph['Name'] = 'chiller1_tcnwkflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##7
    temp_ph = {}
    temp_ph['Name'] = 'chiller2_em'
    temp_ph['Value'] = all_var[2]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##8
    temp_ph = {}
    temp_ph['Name'] = 'chiller2_etret'
    temp_ph['Value'] = all_var[14]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##9
    temp_ph = {}
    temp_ph['Name'] = 'chiller2_cm'
    temp_ph['Value'] = all_var[3]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##10
    temp_ph = {}
    temp_ph['Name'] = 'chiller2_ctin'
    temp_ph['Value'] = all_var[12]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##11
    temp_ph = {}
    temp_ph['Name'] = 'chiller2_tenwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##12
    temp_ph = {}
    temp_ph['Name'] = 'chiller2_tcnwkflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)

    ##13
    temp_ph = {}
    temp_ph['Name'] = 'chiller3_em'
    temp_ph['Value'] = all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##14
    temp_ph = {}
    temp_ph['Name'] = 'chiller3_etret'
    temp_ph['Value'] = all_var[14]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##15
    temp_ph = {}
    temp_ph['Name'] = 'chiller3_cm'
    temp_ph['Value'] = all_var[5]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##16
    temp_ph = {}
    temp_ph['Name'] = 'chiller3_ctin'
    temp_ph['Value'] = all_var[12]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##17
    temp_ph = {}
    temp_ph['Name'] = 'chiller3_tenwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##18
    temp_ph = {}
    temp_ph['Name'] = 'chiller3_tcnwkflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)

    ##19
    temp_ph = {}
    temp_ph['Name'] = 'substation_cp_inflow'
    temp_ph['Value'] = all_var[6] * (all_var[0] + all_var[2] + all_var[4])
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##20
    temp_ph = {}
    temp_ph['Name'] = 'substation_cp_tnwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)

    ##21
    temp_ph = {}
    temp_ph['Name'] = 'substation_gv2_inflow'
    temp_ph['Value'] = all_var[7] * (all_var[0] + all_var[2] + all_var[4])
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##22
    temp_ph = {}
    temp_ph['Name'] = 'substation_gv2_tnwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##23
    temp_ph = {}
    temp_ph['Name'] = 'substation_gv2_tinlim'
    temp_ph['Value'] = sub_station_tinlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##24
    temp_ph = {}
    temp_ph['Name'] = 'substation_gv2_toutlim'
    temp_ph['Value'] = sub_station_toutlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##25
    temp_ph = {}
    temp_ph['Name'] = 'substation_gv2_demand'
    temp_ph['Value'] = demand_time['ss_gv2_demand'][0]
    temp_ph['Unit'] = 'kWh'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)

    ##26
    temp_ph = {}
    temp_ph['Name'] = 'substation_hsb_inflow'
    temp_ph['Value'] = all_var[8] * (all_var[0] + all_var[2] + all_var[4])
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##27
    temp_ph = {}
    temp_ph['Name'] = 'substation_hsb_tnwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##28
    temp_ph = {}
    temp_ph['Name'] = 'substation_hsb_tinlim'
    temp_ph['Value'] = sub_station_tinlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##29
    temp_ph = {}
    temp_ph['Name'] = 'substation_hsb_toutlim'
    temp_ph['Value'] = sub_station_toutlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##30
    temp_ph = {}
    temp_ph['Name'] = 'substation_hsb_demand'
    temp_ph['Value'] = demand_time['ss_hsb_demand'][0]
    temp_ph['Unit'] = 'kWh'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)

    ##31
    temp_ph = {}
    temp_ph['Name'] = 'substation_pfa_inflow'
    temp_ph['Value'] = all_var[9] * (all_var[0] + all_var[2] + all_var[4])
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##32
    temp_ph = {}
    temp_ph['Name'] = 'substation_pfa_tnwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##33
    temp_ph = {}
    temp_ph['Name'] = 'substation_pfa_tinlim'
    temp_ph['Value'] = sub_station_tinlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##34
    temp_ph = {}
    temp_ph['Name'] = 'substation_pfa_toutlim'
    temp_ph['Value'] = sub_station_toutlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##35
    temp_ph = {}
    temp_ph['Name'] = 'substation_pfa_demand'
    temp_ph['Value'] = demand_time['ss_pfa_demand'][0]
    temp_ph['Unit'] = 'kWh'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)

    ##36
    temp_ph = {}
    temp_ph['Name'] = 'substation_ser_inflow'
    temp_ph['Value'] = all_var[10] * (all_var[0] + all_var[2] + all_var[4])
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##37
    temp_ph = {}
    temp_ph['Name'] = 'substation_ser_tnwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##38
    temp_ph = {}
    temp_ph['Name'] = 'substation_ser_tinlim'
    temp_ph['Value'] = sub_station_tinlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##39
    temp_ph = {}
    temp_ph['Name'] = 'substation_ser_toutlim'
    temp_ph['Value'] = sub_station_toutlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##40
    temp_ph = {}
    temp_ph['Name'] = 'substation_ser_demand'
    temp_ph['Value'] = demand_time['ss_ser_demand'][0]
    temp_ph['Unit'] = 'kWh'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##41
    temp_ph = {}
    temp_ph['Name'] = 'substation_fir_inflow'
    temp_ph['Value'] = all_var[11] * (all_var[0] + all_var[2] + all_var[4])
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##42
    temp_ph = {}
    temp_ph['Name'] = 'substation_fir_tnwkflow'
    temp_ph['Value'] = all_var[0] + all_var[2] + all_var[4]
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##43
    temp_ph = {}
    temp_ph['Name'] = 'substation_fir_tinlim'
    temp_ph['Value'] = sub_station_tinlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##44
    temp_ph = {}
    temp_ph['Name'] = 'substation_fir_toutlim'
    temp_ph['Value'] = sub_station_toutlim
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##45
    temp_ph = {}
    temp_ph['Name'] = 'substation_fir_demand'
    temp_ph['Value'] = demand_time['ss_fir_demand'][0]
    temp_ph['Unit'] = 'kWh'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##46
    temp_ph = {}
    temp_ph['Name'] = 'chiller1_ret_etret'
    temp_ph['Value'] = all_var[14]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##47
    temp_ph = {}
    temp_ph['Name'] = 'chiller2_ret_etret'
    temp_ph['Value'] = all_var[14]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##48
    temp_ph = {}
    temp_ph['Name'] = 'chiller3_ret_etret'
    temp_ph['Value'] = all_var[14]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True) 
    
    ##49
    temp_ph = {}
    temp_ph['Name'] = 'splitter3_tin'
    temp_ph['Value'] = all_var[13] + all_var[12]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)     
    
    ##50
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower_ret'
    temp_ph['Value'] = all_var[12]
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)    
    
    ##51
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower1_tin'
    temp_ph['Value'] = all_var[12] + all_var[13]                                                ##Adding the predefined Tin to the predefined Tout of the cooling tower configuration
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##52
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower1_totalconfigflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]                                                
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
    
    ##53
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower1_twb'
    temp_ph['Value'] = wet_bulb_temp                                                
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)
      
    ##54
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower2_tin'
    temp_ph['Value'] = all_var[12] + all_var[13]                                                ##Adding the predefined Tin to the predefined Tout of the cooling tower configuration
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##55
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower2_totalconfigflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]                                                
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)

    ##56
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower2_twb'
    temp_ph['Value'] = wet_bulb_temp                                                
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)        
    
    ##57
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower3_tin'
    temp_ph['Value'] = all_var[12] + all_var[13]                                                ##Adding the predefined Tin to the predefined Tout of the cooling tower configuration
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##58
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower3_totalconfigflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]                                                
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##59
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower3_twb'
    temp_ph['Value'] = wet_bulb_temp                                                
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  

    ##60
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower4_tin'
    temp_ph['Value'] = all_var[12] + all_var[13]                                                ##Adding the predefined Tin to the predefined Tout of the cooling tower configuration
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##61
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower4_totalconfigflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]                                                
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)      
    
    ##62
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower4_twb'
    temp_ph['Value'] = wet_bulb_temp                                                
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##63
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower5_tin'
    temp_ph['Value'] = all_var[12] + all_var[13]                                                ##Adding the predefined Tin to the predefined Tout of the cooling tower configuration
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##64
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower5_totalconfigflow'
    temp_ph['Value'] = all_var[1] + all_var[3] + all_var[5]                                                
    temp_ph['Unit'] = 'm3/h'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    ##65
    temp_ph = {}
    temp_ph['Name'] = 'cooling_tower5_twb'
    temp_ph['Value'] = wet_bulb_temp                                                
    temp_ph['Unit'] = 'K'
    
    input_data = [temp_ph['Name'], temp_ph['Value'], temp_ph['Unit']]
    inputdf = pd.DataFrame(data = [input_data], columns = ['Name', 'Value', 'Unit'])
    m2s_param = m2s_param.append(inputdf, ignore_index=True)  
    
    m2s_param.to_csv('C:\\Optimization_zlc\\master_level\\master-slave_var.csv', sep=',', encoding='utf-8')
    
    return