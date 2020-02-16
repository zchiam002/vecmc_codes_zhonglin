##This function determines the chiller's electricity consumption 

def determine_chiller_elect (dt):
    import numpy as np 
    import pandas as pd 
    import sys
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from chiller_models import chiller_gnu_stepwise_cop_lprelax
    
    steps = 4
    bilinear_pieces = 20
    
    ##Importing chiller information 
    data_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\final_processed_values.csv'
    chiller_data = pd.read_csv(data_loc)
    
    ##Deterimining chiller on-off status 
    chiller_on_off_data = pd.DataFrame(columns = ['Chiller_1', 'Chiller_2', 'Chiller_3'])
    dim_chiller_data = chiller_data.shape 
    
    for i in range (0, dim_chiller_data[0]):
        data1 = []
        if chiller_data['ch1_4nc_evap_m_perc'][i] <= 0.0001:
            data1.append(0)
        else:
            data1.append(1)            
    
        if chiller_data['ch2_4nc_evap_m_perc'][i] <= 0.0001:
            data1.append(0)
        else:
            data1.append(1)         

        if chiller_data['ch3_4nc_evap_m_perc'][i] <= 0.0001:
            data1.append(0)
        else:
            data1.append(1)  
        
        temp_df = pd.DataFrame(data = [data1], columns = ['Chiller_1', 'Chiller_2', 'Chiller_3'])
        chiller_on_off_data = chiller_on_off_data.append(temp_df, ignore_index = True)

    save_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\chiller_on_off.csv'
    chiller_on_off_data.to_csv(save_loc)
    
    #Determining master decision variables 
    master_dv_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\ga_results_current_store\\' + dt + '_load\\ts_' 
    
    ##Determining weather conditions
    weather_data_loc = 'C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\' + dt + '_load' + '\\' + dt + '_demand_weather.csv'
    weather_data = pd.read_csv(weather_data_loc)

    ##Preparing return data 
    return_chiller_elect = pd.DataFrame(columns = ['Chiller_1', 'Chiller_2', 'Chiller_3'])
    
    for i in range (0, 24):
        
        print(i)
        elect_data = []
        
        ##Determining master decision variables 
        master_values_loc = master_dv_loc + str(i) + '\\best_agent_movement.csv'
        master_data = np.genfromtxt(master_values_loc, delimiter = ',')
        master_tret = master_data[30,0] 
        master_evap_flow = master_data[30,1]
        master_values = [master_tret, master_evap_flow]        
        
        ##Determining wet bulb temperature 
        twb_curr = weather_data['T_WB'][i]
        
        ##Determining which chiller is switched on
        if chiller_on_off_data['Chiller_1'][i] == 1:
            reg_cst = [0.123020043325872, 1044.79734873891, 0.0204660495029597]
            qc_coeff = 1.09866273284186
            Tin_evap = master_tret - 273.15
            Tout_evap = chiller_data['ch1_4nc_evap_t_out'][i] - 273.149
            Tin_cond = twb_curr + 5
            mevap = chiller_data['ch1_4nc_evap_m_perc'][i]
            mcond = 407
            Qe_max = 2000
            mevap_t = master_evap_flow
            mcond_t = 410
            r1, r1_df = chiller_gnu_stepwise_cop_lprelax (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max, steps, bilinear_pieces, mevap_t, mcond_t, twb_curr)
            elect_data.append(r1_df['Value'][0])
        else:
            elect_data.append(0)
            
        if chiller_on_off_data['Chiller_2'][i] == 1:
            reg_cst = [1.35049420632748, -134.853705222833, 0.00430128306723068]
            qc_coeff = 1.10348067074030
            Tin_evap = master_tret - 273.15
            Tout_evap = chiller_data['ch2_4nc_evap_t_out'][i] - 273.15
            Tin_cond = twb_curr + 5
            mevap = chiller_data['ch2_4nc_evap_m_perc'][i]
            mcond = 1476
            Qe_max = 7330
            mevap_t = master_evap_flow
            mcond_t = 1485
            r2, r2_df = chiller_gnu_stepwise_cop_lprelax (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max, steps, bilinear_pieces, mevap_t, mcond_t, twb_curr)
            elect_data.append(r2_df['Value'][0])
        else:
            elect_data.append(0)        

        if chiller_on_off_data['Chiller_3'][i] == 1:
            reg_cst = [1.35049420632748, -134.853705222833, 0.00430128306723068]
            qc_coeff = 1.10348067074030
            Tin_evap = master_tret - 273.15
            Tout_evap = chiller_data['ch3_4nc_evap_t_out'][i] - 273.15
            Tin_cond = twb_curr + 5
            mevap = chiller_data['ch3_4nc_evap_m_perc'][i]
            mcond = 1476
            Qe_max = 7330
            mevap_t = master_evap_flow
            mcond_t = 1485
            r3, r3_df = chiller_gnu_stepwise_cop_lprelax (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max, steps, bilinear_pieces, mevap_t, mcond_t, twb_curr)
            elect_data.append(r3_df['Value'][0])
        else:
            elect_data.append(0)      
        
        temp_df = pd.DataFrame(data = [elect_data], columns = ['Chiller_1', 'Chiller_2', 'Chiller_3'])
        return_chiller_elect = return_chiller_elect.append(temp_df, ignore_index = True)
        
        save_loc_elec = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\chiller_elec.csv' 
        return_chiller_elect.to_csv(save_loc_elec)
    return 

#########################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    dt = 'low'
    determine_chiller_elect (dt)