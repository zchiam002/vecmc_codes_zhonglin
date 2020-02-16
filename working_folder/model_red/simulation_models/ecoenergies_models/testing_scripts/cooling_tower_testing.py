 ##The main script for the cooling tower testing 

def main_cooling_tower_script ():
    
    import numpy as np
    import pandas as pd
    
    ##Import the TWB data 
    weather_hl = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\high_load\\high_demand_weather.csv')
    weather_ml = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\mid_load\\mid_demand_weather.csv')    
    weather_ll = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\low_load\\low_demand_weather.csv')  
    
    dim_weather_hl = weather_hl.shape
    dim_weather_ml = weather_ml.shape
    dim_weather_ll = weather_ll.shape

    twb_array_hl = [20.72]
    twb_array_ml = []
    twb_array_ll = []
    
#    for i in range (0, dim_weather_hl[0]):
#        twb_array_hl.append(weather_hl['T_WB'][i])
#        twb_array_ml.append(weather_ml['T_WB'][i])    
#        twb_array_ll.append(weather_ll['T_WB'][i])
            
    flow = [1476+1476]#407, 1476, 407+1476, 1476+1476, 407+1476+1476]    
    max_dt = 12
    steps = 2
    bilinear_pieces = 12
    
    ##The reference dataframe 
    
    
    
    
    
    alliter = len(flow)
    check = 0
    while check == 0:
        check2 = 0
        for k in range (0, alliter):
            
            hl_csv = pd.DataFrame(columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb'])
            ml_csv = pd.DataFrame(columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb'])
            ll_csv = pd.DataFrame(columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb'])   
            
            
            iterations = len(twb_array_hl)   
            for i in range (0, iterations):
            
                twb = twb_array_hl[i]
                print_dataframe_hl, del_t_coeff_temp = testing_one_cooling_tower (twb, max_dt, flow[k], steps, bilinear_pieces)
                hl_csv = hl_csv.append(print_dataframe_hl, ignore_index = True)
                str1 = str(k) + ' of ' + str(iterations)
                print(i, str1)
                print(del_t_coeff_temp)
            
            for i in range (0, pow((steps+1),2)):
                if hl_csv['ct1_water_cons'][i] < 0:
                    print(k)
                    check2 = check2 + 1                    
                    
            filename = 'hl_' + str(k) + '_1.csv'  
            hl_csv.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_analysis\\' + filename) 
            np.savetxt('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_analysis\\coeff_' + filename , del_t_coeff_temp)
            
        if check2 > 0:
            twb_array_hl[0] = twb_array_hl[0] + 0.01
        else:
            print(twb_array_hl[0])
            check = 1      
        
#        
#        iterations = len(twb_array_ml)
#        for i in range (0, iterations):
#        
#            twb = twb_array_ml[i]
#            print_dataframe_ml = testing_one_cooling_tower (twb, max_dt, flow[k], steps, bilinear_pieces)    
#            ml_csv = ml_csv.append(print_dataframe_ml, ignore_index = True)
#            str1 = str(k) + ' of ' + str(iterations)
#            print(i, str1)
#
#        filename = 'ml_' + str(k) + '_1.csv'          
#        ml_csv.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_analysis\\' + filename)   
#
#
#
#        iterations = len(twb_array_ll)
#        for i in range (0, iterations):
#                
#            twb = twb_array_ll[i]
#            print_dataframe_ll = testing_one_cooling_tower (twb, max_dt, flow[k], steps, bilinear_pieces) 
#            ll_csv = ll_csv.append(print_dataframe_ll, ignore_index = True)        
#            str1 = str(k) + ' of ' + str(iterations)
#            print(i, str1)       
#            
#        filename = 'll_' + str(k) + '_1.csv'          
#        ll_csv.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_analysis\\' + filename)     

        
    return 

###########################################################################################################################################################
##Additional functions 

##To test the performance of cooling tower 
def testing_one_cooling_tower (twb, max_dt, flow, steps, bilinear_pieces):
    
    import pandas as pd 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import cooling_tower_uem
    from cooling_tower_models import cooling_tower_uem_reg 
    from cooling_tower_models import cooling_tower_uem_reg_lprelax 
    
    ##Assembling the return dataframe 
    print_dataframe = pd.DataFrame(columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb']) 
    
    for i in range (0, steps+1):
        ##Determining the step size for the fan
        fan_min = 0.05
        fan_max = 1
        fan_perc_ct1 = (i * (1/steps) * (fan_max - fan_min)) + fan_min
        
        for j in range (0, steps+1):
            ##Determining the step size for tin
            
            if twb > 15:
                tin_min = twb + 3
                tin_max = tin_min + max_dt 
                tin_curr = ((i * (1/steps) * (tin_max - tin_min)) + tin_min) + 273.15
                
                twi_min = 273.15 + tin_min       ##(Sensitive parameters, need to be taken care off...)
                twi_max = 273.15 + tin_max
            
            else:
                tin_min = 18 
                tin_max = 35 
                tin_curr = ((i * (1/steps) * (tin_max - tin_min)) + tin_min) + 273.15  
                
                twi_min = 273.15 + tin_min       ##(Sensitive parameters, need to be taken care off...)
                twi_max = 273.15 + tin_max
                
            perc_fan = [fan_perc_ct1, 0, 0, 0, 0]
            total_water_flow = flow
            twb1 = 273.15 + twb
        
            #return_values_1, return_values_df_1 = cooling_tower_uem (perc_fan, total_water_flow, tin_curr, twb1)
            #return_values_3, return_values_df_3, del_t_coeff_temp = cooling_tower_uem_reg(perc_fan, total_water_flow, tin_curr, twb1, twi_min, twi_max)
            return_values_3, return_values_df_3, del_t_coeff_temp = cooling_tower_uem_reg_lprelax (perc_fan, total_water_flow, tin_curr, twb1, twi_min, twi_max, bilinear_pieces)
        
            #print(return_values_df_1)
            #print(return_values_df_2)
            #print(return_values_df_3)

            temp_data = [fan_perc_ct1, tin_curr - 273.15, return_values_df_3['Value'][0] - 273.15, return_values_df_3['Value'][1], return_values_df_3['Value'][2], twb1-273.15]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb'])
            print_dataframe = print_dataframe.append(temp_df, ignore_index = True)
   
    return print_dataframe, del_t_coeff_temp


###########################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    main_cooling_tower_script ()
