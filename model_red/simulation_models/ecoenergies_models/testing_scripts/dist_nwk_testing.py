##This is the testing script for the network models 
def dist_pump_elect_cons (a1, s1, s2, s3, s4, s5):
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from dist_network_models import dist_nwk_org
    from dist_network_models import dist_nwk_piecewise_pressure
    from dist_network_models import dist_nwk_piecewise_pressure_reg_pumpnwk
    from dist_network_models import dist_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp
    import pandas as pd 
    
    gv2_demand = 1000
    hsb_demand = 400
    pfa_demand = 500
    ser_demand = 900
    fir_demand = 1000
    
    consumer_demand = [gv2_demand, hsb_demand, pfa_demand, ser_demand, fir_demand]
    
    total_nwk_flow = a1
    
    gv2_split = s1		
    hsb_split = s2
    pfa_split = s3
    ser_split = s4
    fir_split = s5
    
    perc_split = [gv2_split, hsb_split, pfa_split, ser_split, fir_split]
    
    nwk_pump_select = 37
    
    tin_dist_nwk = 273.15 + 6
    
    steps = 4
    
    tin_dist_nwk_max = 273.15 + 20
    
    bilinear_pieces = 20
    
    return_values_1, return_values_df_1 = dist_nwk_org(consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk)
    return_values_2, return_values_df_2 = dist_nwk_piecewise_pressure (consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, steps)
    return_values_3, return_values_df_3 = dist_nwk_piecewise_pressure_reg_pumpnwk (consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, steps)
    #return_values_4, return_values_df_4 = dist_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp(consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, steps, tin_dist_nwk_max, bilinear_pieces)
    
    
    #print(return_values_df_1)
    #print(return_values_df_2)
    print(return_values_df_3)
    #print(return_values_df_4)
    
    return return_values_df_3['Value'][2]
###########################################################################################################################################################
if __name__ == '__main__':
    
    import pandas as pd
    
    dt = 'mid'
    data_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\simulation_results\\simul_' + dt + '\\'
    data_name = 'dist_nwk_split.csv'
    
    data_req = pd.read_csv(data_loc + data_name)
    
    dim_data_req = data_req.shape 
    
    return_data = pd.DataFrame(columns = ['dist_pump'])
    
    for i in range (0, dim_data_req[0]):
        a1 = data_req['total'][i]
        s1 = data_req['gv2'][i]
        s2 = data_req['hsb'][i] 
        s3 = data_req['pfa'][i] 
        s4 = data_req['ser'][i] 
        s5 = 0
        print(i)
        elect_cons = dist_pump_elect_cons (a1, s1, s2, s3, s4, s5)
        temp_data = [elect_cons]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['dist_pump'])  
        return_data = return_data.append(temp_df, ignore_index = True)
    
    return_data.to_csv(data_loc + 'dist_pump.csv')
    
    
        
    