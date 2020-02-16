##This function redesigns the cooling tower model based on the universal cooling tower engineering model 

def ct_prepare_coefficients ():
    
    import pandas as pd 
    
    ##Preparing the cooling tower raw data, unsorted as of now
    raw_data = prepare_cooling_tower_data ()
    ret_coeff = pure_regression_ct_uem (raw_data)
    
    ##Inputs 
    bilinear_pieces = 20
    steps = 3
    hl_data = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\high_load\\high_demand_weather.csv')
    ml_data = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\mid_load\\mid_demand_weather.csv')
    ll_data = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\low_load\\low_demand_weather.csv')
    
    
    ##Analysis of the cooling tower model performance 
    
    flowrate = 420
    twb = 12
    #uem_twi_ma_delt_analysis (ret_coeff, flowrate, twb)
    
    ##Checking the outputs of uem and reduced regression and the lp relax format    
#    delt_uem = uem_model (ret_coeff, flowrate, twb, twi, ma)    
#    ct_calc, delt_reg_output = uem_model_reduced_coeff (ret_coeff, flowrate, twb, twi, ma)
#    del_t_lprelax = uem_model_reduced_coeff_lprelax (twb, twi, ma, bilinear_pieces, ct_calc)
#    
#    print(delt_uem)
#    print(delt_reg_output)
#    print(del_t_lprelax)

    ##Checking all iterations for consistency of performance across the uem, reg and bilinear model 
#    check_input_data_output (hl_data, ml_data, ll_data, ret_coeff, bilinear_pieces, steps)
    
    

    ##This function is used to prepare the coefficients for different flowrates     IT NEEDS TO BE RUN BEFORE ANY OPTIMIZATION IS TO TAKE PLACE
    prepare_cooling_tower_coefficients (ret_coeff, hl_data, ml_data, ll_data)
    
    
    #check_generated_coefficients_thorough (hl_data, ml_data, ll_data, steps)
    return 

###################################################################################################################################################################
##Additional functions 

##This function checks the output of the calculated coefficients
def check_generated_coefficients_thorough (hl_data, ml_data, ll_data, steps):
    import pandas as pd 
    
    flowrate = [407, 1476, 407+1476, 1476+1476, 407+1476+1476]
    flow_iterations = len(flowrate)

    ##Handling high load data first 
        ##Loading the precomputed coefficients 
    hl_reg_coeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_hl_coeff.csv')    
    
    for i in range (0, flow_iterations):
        demand_iterations = hl_data.shape
        hl_all_iterations = pd.DataFrame(columns = ['ma', 'Twi', 'Twb', 'delt_reg'])
        for j in range (0, demand_iterations[0]):
            twb_curr = hl_data['T_WB'][j]
            
            ##Loading the coefficients 
            c0 = hl_reg_coeff['f' + str(i) + '_c0'][j]
            c1 = hl_reg_coeff['f' + str(i) + '_c1'][j]
            c2 = hl_reg_coeff['f' + str(i) + '_c2'][j]
            c3 = hl_reg_coeff['f' + str(i) + '_c3'][j]

            
            ##Handling the parameters
            ma_min = 0.05
            ma_max = 1
            
            if twb_curr < 17:
                twi_min = 18
                twi_max = twi_min + 10
            else:
                twi_min = twb_curr + 1
                twi_max = twi_min + 10
                
            ma_step = (ma_max - ma_min) / (steps - 1)
            twi_step = (twi_max - twi_min) / (steps - 1)
            
            for k in range (0, steps):      ##Vary Twi first 
                twi_curr = twi_min + (k * twi_step)                
                ##Vary ma next  
                for l in range (0, steps):
                    print('flow: ', i, 'time_step: ', j, 'twi_step: ', k, 'ma_step: ', l)
                    ma_curr = ((l * ma_step) + ma_min)
                    
                    delt = (c0 * ma_curr * 369117) + (c1 * (twi_curr + 273.15)) + (c2 * (twi_curr + 273.15) * (ma_curr * 369117)) + c3
        
                    temp_data = [ma_curr, twi_curr, twb_curr, delt]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['ma', 'Twi', 'Twb','delt_reg'])
                    hl_all_iterations = hl_all_iterations.append(temp_df, ignore_index = True)
        
        save_name = 'hl_results_' + str(i) + '.csv'
        hl_all_iterations.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\test_coeff_ct\\' + save_name)
    


    ##Handling mid load data next 
        ##Loading the precomputed coefficients 
    ml_reg_coeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ml_coeff.csv')    
    
    for i in range (0, flow_iterations):
        demand_iterations = ml_data.shape
        ml_all_iterations = pd.DataFrame(columns = ['ma', 'Twi', 'Twb', 'delt_reg'])
        for j in range (0, demand_iterations[0]):
            twb_curr = ml_data['T_WB'][j]
            
            ##Loading the coefficients 
            c0 = ml_reg_coeff['f' + str(i) + '_c0'][j]
            c1 = ml_reg_coeff['f' + str(i) + '_c1'][j]
            c2 = ml_reg_coeff['f' + str(i) + '_c2'][j]
            c3 = ml_reg_coeff['f' + str(i) + '_c3'][j]

            
            ##Handling the parameters
            ma_min = 0.05
            ma_max = 1
            
            if twb_curr < 17:
                twi_min = 18
                twi_max = twi_min + 10
            else:
                twi_min = twb_curr + 1
                twi_max = twi_min + 10
                
            ma_step = (ma_max - ma_min) / (steps - 1)
            twi_step = (twi_max - twi_min) / (steps - 1)
            
            for k in range (0, steps):      ##Vary Twi first 
                twi_curr = twi_min + (k * twi_step)                
                ##Vary ma next  
                for l in range (0, steps):
                    print('flow: ', i, 'time_step: ', j, 'twi_step: ', k, 'ma_step: ', l)
                    ma_curr = ((l * ma_step) + ma_min)
                    
                    delt = (c0 * ma_curr * 369117) + (c1 * (twi_curr + 273.15)) + (c2 * (twi_curr + 273.15) * (ma_curr * 369117)) + c3
        
                    temp_data = [ma_curr, twi_curr, twb_curr, delt]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['ma', 'Twi', 'Twb','delt_reg'])
                    ml_all_iterations = ml_all_iterations.append(temp_df, ignore_index = True)
        
        save_name = 'ml_results_' + str(i) + '.csv'
        ml_all_iterations.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\test_coeff_ct\\' + save_name)



    ##Handling low load data next 
        ##Loading the precomputed coefficients 
    ll_reg_coeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ll_coeff.csv')    
    
    for i in range (0, flow_iterations):
        demand_iterations = ll_data.shape
        ll_all_iterations = pd.DataFrame(columns = ['ma', 'Twi', 'Twb', 'delt_reg'])
        for j in range (0, demand_iterations[0]):
            twb_curr = ll_data['T_WB'][j]
            ##Loading the coefficients 
            c0 = ll_reg_coeff['f' + str(i) + '_c0'][j]
            c1 = ll_reg_coeff['f' + str(i) + '_c1'][j]
            c2 = ll_reg_coeff['f' + str(i) + '_c2'][j]
            c3 = ll_reg_coeff['f' + str(i) + '_c3'][j]

            
            ##Handling the parameters
            ma_min = 0.05
            ma_max = 1
            
            if twb_curr < 17:
                twi_min = 18
                twi_max = twi_min + 10
            else:
                twi_min = twb_curr + 1
                twi_max = twi_min + 10
                
            ma_step = (ma_max - ma_min) / (steps - 1)
            twi_step = (twi_max - twi_min) / (steps - 1)
            
            for k in range (0, steps):      ##Vary Twi first 
                twi_curr = twi_min + (k * twi_step)                
                ##Vary ma next  
                for l in range (0, steps):
                    print('flow: ', i, 'time_step: ', j, 'twi_step: ', k, 'ma_step: ', l)
                    ma_curr = ((l * ma_step) + ma_min)
                    
                    delt = (c0 * ma_curr * 369117) + (c1 * (twi_curr + 273.15)) + (c2 * (twi_curr + 273.15) * (ma_curr * 369117)) + c3
        
                    temp_data = [ma_curr, twi_curr, twb_curr, delt]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['ma', 'Twi', 'Twb','delt_reg'])
                    ll_all_iterations = ll_all_iterations.append(temp_df, ignore_index = True)
        
        save_name = 'll_results_' + str(i) + '.csv'
        ll_all_iterations.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\test_coeff_ct\\' + save_name)    
    return 


##This function is used to prepare the coefficients for different flowrates and different wetblub temperature combinations 
def prepare_cooling_tower_coefficients (ret_coeff, hl_data, ml_data, ll_data):
    
    import pandas as pd
    
    flowrate = [407, 1476, 407+1476, 1476+1476, 407+1476+1476]
    flow_iterations = len(flowrate)
    
    ##Handling the high load data first 
    hl_data_with_coefficients = pd.DataFrame(columns = ['T_DB', 'T_WB', 
                                                        'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 
                                                        'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3',
                                                        'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3',
                                                        'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3',
                                                        'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3',])
    dim_hl_data = hl_data.shape 
    for i in range (0, dim_hl_data[0]):
        temp_data = []
        temp_data.append(hl_data['T_DB'][i])
        temp_data.append(hl_data['T_WB'][i])

        for j in range (0, flow_iterations):    
            print('hl', i, j)
            ct_calc = uem_model_reduced_coeff_return_coeff_only (ret_coeff, flowrate[j], hl_data['T_WB'][i])
            temp_data.append(ct_calc[0,0])
            temp_data.append(ct_calc[1,0])
            temp_data.append(ct_calc[2,0])
            temp_data.append(ct_calc[3,0])
        
        temp_df = pd.DataFrame(data = [temp_data], columns = ['T_DB', 'T_WB', 
                                                            'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 
                                                            'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3',
                                                            'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3',
                                                            'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3',
                                                            'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3',])
        
        hl_data_with_coefficients = hl_data_with_coefficients.append(temp_df, ignore_index = True)
        
    hl_data_with_coefficients.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_hl_coeff.csv')
    
    ##Handling the mid load data first 
    ml_data_with_coefficients = pd.DataFrame(columns = ['T_DB', 'T_WB', 
                                                        'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 
                                                        'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3',
                                                        'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3',
                                                        'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3',
                                                        'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3',])
    dim_ml_data = ml_data.shape 
    for i in range (0, dim_ml_data[0]):
        temp_data = []
        temp_data.append(ml_data['T_DB'][i])
        temp_data.append(ml_data['T_WB'][i])

        for j in range (0, flow_iterations):    
            print('ml', i, j)
            ct_calc = uem_model_reduced_coeff_return_coeff_only (ret_coeff, flowrate[j], ml_data['T_WB'][i])
            temp_data.append(ct_calc[0,0])
            temp_data.append(ct_calc[1,0])
            temp_data.append(ct_calc[2,0])
            temp_data.append(ct_calc[3,0])
        
        temp_df = pd.DataFrame(data = [temp_data], columns = ['T_DB', 'T_WB', 
                                                            'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 
                                                            'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3',
                                                            'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3',
                                                            'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3',
                                                            'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3',])
        
        ml_data_with_coefficients = ml_data_with_coefficients.append(temp_df, ignore_index = True)
        
    ml_data_with_coefficients.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ml_coeff.csv')   
    
    ##Handling the low load data first 
    ll_data_with_coefficients = pd.DataFrame(columns = ['T_DB', 'T_WB', 
                                                        'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 
                                                        'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3',
                                                        'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3',
                                                        'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3',
                                                        'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3',])
    dim_ll_data = ll_data.shape 
    for i in range (0, dim_ll_data[0]):
        temp_data = []
        temp_data.append(ll_data['T_DB'][i])
        temp_data.append(ll_data['T_WB'][i])

        for j in range (0, flow_iterations):    
            print('ll', i, j)
            ct_calc = uem_model_reduced_coeff_return_coeff_only (ret_coeff, flowrate[j], ll_data['T_WB'][i])
            temp_data.append(ct_calc[0,0])
            temp_data.append(ct_calc[1,0])
            temp_data.append(ct_calc[2,0])
            temp_data.append(ct_calc[3,0])
        
        temp_df = pd.DataFrame(data = [temp_data], columns = ['T_DB', 'T_WB', 
                                                            'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 
                                                            'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3',
                                                            'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3',
                                                            'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3',
                                                            'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3',])
        
        ll_data_with_coefficients = ll_data_with_coefficients.append(temp_df, ignore_index = True)
        
    ll_data_with_coefficients.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ll_coeff.csv') 
    return 

##This model creates a regression based model to return coefficients only  
def uem_model_reduced_coeff_return_coeff_only (ret_coeff, flowrate, twb):
    
    import numpy as np 
    import pandas as pd 
    from sklearn import linear_model 
    
    ##Finding out the min and max of each to create a regression table 
    ma_min = 0.05
    ma_max = 1

    if twb < 17:
        twi_min = 18
        twi_max = twi_min + 10
    else:
        twi_min = twb + 1
        twi_max = twi_min + 10    

    steps = 100
    ma_step = (ma_max - ma_min) / (steps - 1)
    twi_step = (twi_max - twi_min) / (steps - 1)
    
    reg_data = pd.DataFrame(columns = ['Twi', 'ma', 'delT'])
    
    ##Vary Twi first
    for i in range (0, steps):
        twi_curr = twi_min + (i * twi_step)
        ##Vary ma next 
        for j in range (0, steps):
            ma_curr = ((j * ma_step) + ma_min)
            delt = uem_model (ret_coeff, flowrate, twb, twi_curr, ma_curr)
            temp_data = [twi_curr + 273.15, ma_curr * 369117, delt]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Twi', 'ma', 'delT'])
            reg_data = reg_data.append(temp_df, ignore_index = True)
    
    #Performing regression 
    dim_reg_data = reg_data.shape
    
    reg_data_expanded_X = np.zeros((dim_reg_data[0],3))
    target_Y = np.zeros((dim_reg_data[0],1))
    
    for i in range (0, dim_reg_data[0]):
        reg_data_expanded_X[i, 0] = reg_data['ma'][i]
        reg_data_expanded_X[i, 1] = reg_data['Twi'][i]
        reg_data_expanded_X[i, 2] = reg_data['ma'][i] * reg_data['Twi'][i]
        target_Y[i, 0] = reg_data['delT'][i]   
        
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(reg_data_expanded_X, target_Y)
    result_1 = clf.score(reg_data_expanded_X, target_Y, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_    
        
    ##Since the idea is to express delta T as a function of Twi, ma and Twi * ma 
    ma_coeff = lin_coeff_1[0,0]
    twi_coeff = lin_coeff_1[0,1]
    matwi_coeff = lin_coeff_1[0,2]
    cst_term = int_1        
        
    ##Initiating a matrix to hold the return values 
    
    ct_calc = np.zeros((4,1))
    
    ct_calc[0,0] = ma_coeff
    ct_calc[1,0] = twi_coeff
    ct_calc[2,0] = matwi_coeff
    ct_calc[3,0] = cst_term      
    
    return ct_calc

##This function checks for every input data combination (twb and flow) through all possible combinations twi and ma the corresponding delta t 
def check_input_data_output (hl_data, ml_data, ll_data, ret_coeff, bilinear_pieces, steps):
    
    import pandas as pd 
    
    flowrate = [407, 1476, 407+1476, 1476+1476, 407+1476+1476]
    flow_iterations = len(flowrate)

    ##Handling high load data first 
    for i in range (0, flow_iterations):
        flow_curr = flowrate[i]
        demand_iterations = hl_data.shape
        hl_all_iterations = pd.DataFrame(columns = ['ma', 'Twi', 'Twb', 'delt_uem', 'delt_reg', 'delt_lp_relax'])
        for j in range (0, demand_iterations[0]):
            twb_curr = hl_data['T_WB'][j]
            
            ##Handling the parameters
            ma_min = 0.05
            ma_max = 1
            
            if twb_curr < 17:
                twi_min = 18
                twi_max = twi_min + 10
            else:
                twi_min = twb_curr + 1
                twi_max = twi_min + 10
                
            ma_step = (ma_max - ma_min) / (steps - 1)
            twi_step = (twi_max - twi_min) / (steps - 1)
            
            for k in range (0, steps):      ##Vary Twi first 
                twi_curr = twi_min + (k * twi_step)                
                ##Vary ma next  
                for l in range (0, steps):
                    print('flow: ', i, 'time_step: ', j, 'twi_step: ', k, 'ma_step: ', l)
                    ma_curr = ((l * ma_step) + ma_min)
                    delt = uem_model (ret_coeff, flow_curr, twb_curr, twi_curr, ma_curr)
                    ct_calc, delt_reg_output = uem_model_reduced_coeff (ret_coeff, flow_curr, twb_curr, twi_curr, ma_curr)
                    del_t_lprelax = uem_model_reduced_coeff_lprelax (twb_curr, twi_curr, ma_curr, bilinear_pieces, ct_calc)
                    
                    temp_data = [ma_curr, twi_curr, twb_curr, delt, delt_reg_output[0], del_t_lprelax]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['ma', 'Twi', 'Twb', 'delt_uem', 'delt_reg', 'delt_lp_relax'])
                    hl_all_iterations = hl_all_iterations.append(temp_df, ignore_index = True)
        
        save_name = 'hl_results_' + str(i) + '.csv'
        hl_all_iterations.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\proof_of_simplification\\rough_work\\' + save_name)
                    
    ##Handling mid load data next 
    for i in range (0, flow_iterations):
        flow_curr = flowrate[i]
        demand_iterations = ml_data.shape
        ml_all_iterations = pd.DataFrame(columns = ['ma', 'Twi', 'Twb', 'delt_uem', 'delt_reg', 'delt_lp_relax'])
        for j in range (0, demand_iterations[0]):
            twb_curr = ml_data['T_WB'][j]
            
            ##Handling the parameters
            ma_min = 0.05
            ma_max = 1
            
            if twb_curr < 17:
                twi_min = 18
                twi_max = twi_min + 10
            else:
                twi_min = twb_curr + 1
                twi_max = twi_min + 10
                
            ma_step = (ma_max - ma_min) / (steps - 1)
            twi_step = (twi_max - twi_min) / (steps - 1)
            
            for k in range (0, steps):      ##Vary Twi first 
                twi_curr = twi_min + (k * twi_step)                
                ##Vary ma next  
                for l in range (0, steps):
                    print('flow: ', i, 'time_step: ', j, 'twi_step: ', k, 'ma_step: ', l)
                    ma_curr = ((l * ma_step) + ma_min)
                    delt = uem_model (ret_coeff, flow_curr, twb_curr, twi_curr, ma_curr)
                    ct_calc, delt_reg_output = uem_model_reduced_coeff (ret_coeff, flow_curr, twb_curr, twi_curr, ma_curr)
                    del_t_lprelax = uem_model_reduced_coeff_lprelax (twb_curr, twi_curr, ma_curr, bilinear_pieces, ct_calc)
                    
                    temp_data = [ma_curr, twi_curr, twb_curr, delt, delt_reg_output[0], del_t_lprelax]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['ma', 'Twi', 'Twb', 'delt_uem', 'delt_reg', 'delt_lp_relax'])
                    ml_all_iterations = ml_all_iterations.append(temp_df, ignore_index = True)
        
        save_name = 'ml_results_' + str(i) + '.csv'
        ml_all_iterations.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\proof_of_simplification\\rough_work\\' + save_name)            
    
    ##Handling low load data last 
    for i in range (0, flow_iterations):
        flow_curr = flowrate[i]
        demand_iterations = ll_data.shape
        ll_all_iterations = pd.DataFrame(columns = ['ma', 'Twi', 'Twb', 'delt_uem', 'delt_reg', 'delt_lp_relax'])
        for j in range (0, demand_iterations[0]):
            twb_curr = ll_data['T_WB'][j]
            
            ##Handling the parameters
            ma_min = 0.05
            ma_max = 1
            
            if twb_curr < 17:
                twi_min = 18
                twi_max = twi_min + 10
            else:
                twi_min = twb_curr + 1
                twi_max = twi_min + 10
                
            ma_step = (ma_max - ma_min) / (steps - 1)
            twi_step = (twi_max - twi_min) / (steps - 1)
            
            for k in range (0, steps):      ##Vary Twi first 
                twi_curr = twi_min + (k * twi_step)                
                ##Vary ma next  
                for l in range (0, steps):
                    print('flow: ', i, 'time_step: ', j, 'twi_step: ', k, 'ma_step: ', l)
                    ma_curr = ((l * ma_step) + ma_min)
                    delt = uem_model (ret_coeff, flow_curr, twb_curr, twi_curr, ma_curr)
                    ct_calc, delt_reg_output = uem_model_reduced_coeff (ret_coeff, flow_curr, twb_curr, twi_curr, ma_curr)
                    del_t_lprelax = uem_model_reduced_coeff_lprelax (twb_curr, twi_curr, ma_curr, bilinear_pieces, ct_calc)
                    
                    temp_data = [ma_curr, twi_curr, twb_curr, delt, delt_reg_output[0], del_t_lprelax]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['ma', 'Twi', 'Twb', 'delt_uem', 'delt_reg', 'delt_lp_relax'])
                    ll_all_iterations = ll_all_iterations.append(temp_df, ignore_index = True)
        
        save_name = 'll_results_' + str(i) + '.csv'
        ll_all_iterations.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\proof_of_simplification\\rough_work\\' + save_name)            

    return 

##This model is the lp relaxed model of uem_model_reduced_coeff
def uem_model_reduced_coeff_lprelax (twb, twi, ma, bilinear_pieces, ct_calc):
    
    ma_min = 0.05 * 369117 
    ma_max = 1 * 369117
    
    if twb < 17:
        twi_min = 18
        twi_max = twi_min + 10
    else:
        twi_min = twb + 1
        twi_max = twi_min + 10   
    
    ##Creating a look up table for the bilinear pieces
    ma_table, twi_table = gen_bilinear_pieces (ma_min, ma_max, twi_min + 273.15, twi_max + 273.15, bilinear_pieces)
    bilin_est = search_bilin_table_for_values (ma_table, twi_table, ma * 369117, twi + 273.15)
    del_t_lprelax = (ct_calc[0,0] * ma * 369117) + (ct_calc[1,0] * (twi + 273.15)) + (ct_calc[2,0] * bilin_est) + ct_calc[3,0]
    
    return del_t_lprelax

##This model creates a regression model based on reduced coefficients 
def uem_model_reduced_coeff (ret_coeff, flowrate, twb, twi, ma):
    
    import numpy as np 
    import pandas as pd 
    from sklearn import linear_model 
    
    ##Finding out the min and max of each to create a regression table 
    ma_min = 0.05
    ma_max = 1

    if twb < 17:
        twi_min = 18
        twi_max = twi_min + 10
    else:
        twi_min = twb + 1
        twi_max = twi_min + 10    

    steps = 100
    ma_step = (ma_max - ma_min) / (steps - 1)
    twi_step = (twi_max - twi_min) / (steps - 1)
    
    reg_data = pd.DataFrame(columns = ['Twi', 'ma', 'delT'])
    
    ##Vary Twi first
    for i in range (0, steps):
        twi_curr = twi_min + (i * twi_step)
        ##Vary ma next 
        for j in range (0, steps):
            ma_curr = ((j * ma_step) + ma_min)
            delt = uem_model (ret_coeff, flowrate, twb, twi_curr, ma_curr)
            temp_data = [twi_curr + 273.15, ma_curr * 369117, delt]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Twi', 'ma', 'delT'])
            reg_data = reg_data.append(temp_df, ignore_index = True)
    
    #Performing regression 
    dim_reg_data = reg_data.shape
    
    reg_data_expanded_X = np.zeros((dim_reg_data[0],3))
    target_Y = np.zeros((dim_reg_data[0],1))
    
    for i in range (0, dim_reg_data[0]):
        reg_data_expanded_X[i, 0] = reg_data['ma'][i]
        reg_data_expanded_X[i, 1] = reg_data['Twi'][i]
        reg_data_expanded_X[i, 2] = reg_data['ma'][i] * reg_data['Twi'][i]
        target_Y[i, 0] = reg_data['delT'][i]   
        
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(reg_data_expanded_X, target_Y)
    result_1 = clf.score(reg_data_expanded_X, target_Y, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_    
        
    ##Since the idea is to express delta T as a function of Twi, ma and Twi * ma 
    ma_coeff = lin_coeff_1[0,0]
    twi_coeff = lin_coeff_1[0,1]
    matwi_coeff = lin_coeff_1[0,2]
    cst_term = int_1        
        
    ##Initiating a matrix to hold the return values 
    
    ct_calc = np.zeros((4,1))
    
    ct_calc[0,0] = ma_coeff
    ct_calc[1,0] = twi_coeff
    ct_calc[2,0] = matwi_coeff
    ct_calc[3,0] = cst_term
    
    ##Calculating the delta t
    twi_reg_input = twi + 273.15
    ma_reg_input = ma * 369117
    
    x0 = ma_coeff * ma_reg_input
    x1 = twi_coeff * twi_reg_input
    x2 = matwi_coeff * ma_reg_input * twi_reg_input
    x3 = cst_term
    
    delt_reg_output = x0 + x1 + x2 + x3
      
    
    return ct_calc, delt_reg_output

##This model takes in values twi and ma with fixed flowrate and twb, returning the delta t estimated
def uem_model (ret_coeff, flowrate, twb, twi, ma):
    
    ##Sorting out the units of flowrate and twb 
    flowrate_used = (flowrate * 998.2) / 5
    twb_used = twb + 273.15    
    twi_used = twi + 273.15
    ma_curr = ma * 369117
     
    twi_curr = twi_used
    
    x0 = ret_coeff[0,0] * (ma_curr / flowrate_used) 
    x1 = ret_coeff[1,0] * (twi_curr - twb_used)
    x2 = ret_coeff[2,0] * pow((ma_curr / flowrate_used), 2)
    x3 = ret_coeff[3,0] * pow((twi_curr - twb_used), 2)
    x4 = ret_coeff[4,0] * (ma_curr / flowrate_used) * (twi_curr - twb_used)
    
    denom_term = (twi_curr - twb_used)
    
    delt_uem = (x0 + x1 + x2 + x3 + x4 + ret_coeff[5,0]) * denom_term   
    
    return delt_uem

##This function analyzes the relationship between DeltaT, twi and ma for a fixed flowrate and wetbulb temperature using the ct UEM only 
def uem_twi_ma_delt_analysis (ret_coeff, flowrate, twb):
    
    import matplotlib.pyplot as plt     
    import pandas as pd
    
    ##Sorting out the units of flowrate and twb 
    flowrate_used = (flowrate * 998.2) / 5
    twb_used = twb + 273.15
    
    ##Determining the range of twi_min
    if twb < 17:
        twi_min = 18
        twi_max = twi_min + 10
    else:
        twi_min = twb + 1
        twi_max = twi_min + 10
        
    twi_steps = 5
    
    ##Determining the twi array 
    twi_step = (twi_max - twi_min) / (twi_steps - 1)
    twi_used = []
    
    for i in range (0, twi_steps):
        twi_used.append(twi_min + (i*twi_step))
    
    plot_data_1 = pd.DataFrame(columns = ['twi', 'ma', 'delt'])
    plot_data_2 = pd.DataFrame(columns = ['twi', 'ma', 'delt'])
    plot_data_3 = pd.DataFrame(columns = ['twi', 'ma', 'delt'])
    plot_data_4 = pd.DataFrame(columns = ['twi', 'ma', 'delt'])
    plot_data_5 = pd.DataFrame(columns = ['twi', 'ma', 'delt'])
    
    ma_steps = 100
    ma_min = 0.05
    ma_max = 1
    ma_step = (ma_max - ma_min) / (ma_steps - 1)
    
    ##Appending dataframe 1
    for i in range (0, ma_steps):
        
        twi_curr = twi_used[0] + 273.15
        ma_curr = ((i * ma_step) + ma_min) * 369117
        
        x0 = ret_coeff[0,0] * (ma_curr / flowrate_used) 
        x1 = ret_coeff[1,0] * (twi_curr - twb_used)
        x2 = ret_coeff[2,0] * pow((ma_curr / flowrate_used), 2)
        x3 = ret_coeff[3,0] * pow((twi_curr - twb_used), 2)
        x4 = ret_coeff[4,0] * (ma_curr / flowrate_used) * (twi_curr - twb_used)
        
        denom_term = (twi_curr - twb_used)
        
        delt_curr = (x0 + x1 + x2 + x3 + x4 + ret_coeff[5,0]) * denom_term
        
        temp_data = [twi_curr, ma_curr, delt_curr]  
        temp_df = pd.DataFrame(data = [temp_data], columns = ['twi', 'ma', 'delt'])
        plot_data_1 = plot_data_1.append(temp_df, ignore_index = True) 

    ##Appending dataframe 2
    for i in range (0, ma_steps):
        
        twi_curr = twi_used[1] + 273.15
        ma_curr = ((i * ma_step) + ma_min) * 369117
        
        x0 = ret_coeff[0,0] * (ma_curr / flowrate_used) 
        x1 = ret_coeff[1,0] * (twi_curr - twb_used)
        x2 = ret_coeff[2,0] * pow((ma_curr / flowrate_used), 2)
        x3 = ret_coeff[3,0] * pow((twi_curr - twb_used), 2)
        x4 = ret_coeff[4,0] * (ma_curr / flowrate_used) * (twi_curr - twb_used)
        
        denom_term = (twi_curr - twb_used)
        
        delt_curr = (x0 + x1 + x2 + x3 + x4 + ret_coeff[5,0]) * denom_term
        
        temp_data = [twi_curr, ma_curr, delt_curr]  
        temp_df = pd.DataFrame(data = [temp_data], columns = ['twi', 'ma', 'delt'])
        plot_data_2 = plot_data_2.append(temp_df, ignore_index = True) 
        
    ##Appending dataframe 3
    for i in range (0, ma_steps):
        
        twi_curr = twi_used[2] + 273.15
        ma_curr = ((i * ma_step) + ma_min) * 369117
        
        x0 = ret_coeff[0,0] * (ma_curr / flowrate_used) 
        x1 = ret_coeff[1,0] * (twi_curr - twb_used)
        x2 = ret_coeff[2,0] * pow((ma_curr / flowrate_used), 2)
        x3 = ret_coeff[3,0] * pow((twi_curr - twb_used), 2)
        x4 = ret_coeff[4,0] * (ma_curr / flowrate_used) * (twi_curr - twb_used)
        
        denom_term = (twi_curr - twb_used)
        
        delt_curr = (x0 + x1 + x2 + x3 + x4 + ret_coeff[5,0]) * denom_term
        
        temp_data = [twi_curr, ma_curr, delt_curr]  
        temp_df = pd.DataFrame(data = [temp_data], columns = ['twi', 'ma', 'delt'])
        plot_data_3 = plot_data_3.append(temp_df, ignore_index = True) 
        
    ##Appending dataframe 4
    for i in range (0, ma_steps):
        
        twi_curr = twi_used[3] + 273.15
        ma_curr = ((i * ma_step) + ma_min) * 369117
        
        x0 = ret_coeff[0,0] * (ma_curr / flowrate_used) 
        x1 = ret_coeff[1,0] * (twi_curr - twb_used)
        x2 = ret_coeff[2,0] * pow((ma_curr / flowrate_used), 2)
        x3 = ret_coeff[3,0] * pow((twi_curr - twb_used), 2)
        x4 = ret_coeff[4,0] * (ma_curr / flowrate_used) * (twi_curr - twb_used)
        
        denom_term = (twi_curr - twb_used)
        
        delt_curr = (x0 + x1 + x2 + x3 + x4 + ret_coeff[5,0]) * denom_term
        
        temp_data = [twi_curr, ma_curr, delt_curr]  
        temp_df = pd.DataFrame(data = [temp_data], columns = ['twi', 'ma', 'delt'])
        plot_data_4 = plot_data_4.append(temp_df, ignore_index = True) 
        
    ##Appending dataframe 5
    for i in range (0, ma_steps):
        
        twi_curr = twi_used[4] + 273.15
        ma_curr = ((i * ma_step) + ma_min) * 369117
        
        x0 = ret_coeff[0,0] * (ma_curr / flowrate_used) 
        x1 = ret_coeff[1,0] * (twi_curr - twb_used)
        x2 = ret_coeff[2,0] * pow((ma_curr / flowrate_used), 2)
        x3 = ret_coeff[3,0] * pow((twi_curr - twb_used), 2)
        x4 = ret_coeff[4,0] * (ma_curr / flowrate_used) * (twi_curr - twb_used)
        
        denom_term = (twi_curr - twb_used)
        
        delt_curr = (x0 + x1 + x2 + x3 + x4 + ret_coeff[5,0]) * denom_term
        
        temp_data = [twi_curr, ma_curr, delt_curr]  
        temp_df = pd.DataFrame(data = [temp_data], columns = ['twi', 'ma', 'delt'])
        plot_data_5 = plot_data_5.append(temp_df, ignore_index = True) 
        
    plt.plot(plot_data_1['ma'][:]/369117, plot_data_1['delt'][:], 'o', color = 'blue')
    plt.plot(plot_data_2['ma'][:]/369117, plot_data_2['delt'][:], 'o', color = 'red')
    plt.plot(plot_data_3['ma'][:]/369117, plot_data_3['delt'][:], 'o', color = 'green')
    plt.plot(plot_data_4['ma'][:]/369117, plot_data_4['delt'][:], 'o', color = 'purple')
    plt.plot(plot_data_5['ma'][:]/369117, plot_data_5['delt'][:], 'o', color = 'orange')
    plt.show()
    
    return 

##This function performs the typical regression and finds the regression derived coefficients 
def pure_regression_ct_uem (raw_data):
    
    import numpy as np
    import pandas as pd
    from sklearn import linear_model 
    
    dim_raw_data = raw_data.shape
    
    ##To perform multivariate regression amongst the variables 
    valuesX = np.zeros((dim_raw_data[0], 5))
    valuesY = np.zeros((dim_raw_data[0], 1))
    
    for i in range (0, dim_raw_data[0]):
        
        valuesX[i, 0] = (raw_data['ma'][i] / raw_data['mw'][i])
        valuesX[i, 1] = (raw_data['Tin'][i] - raw_data['Twb'][i])    
        valuesX[i, 2] = (pow((raw_data['ma'][i] / raw_data['mw'][i]), 2))
        valuesX[i, 3] = (pow((raw_data['Tin'][i] - raw_data['Twb'][i]), 2))
        valuesX[i, 4] = ((raw_data['ma'][i] / raw_data['mw'][i]) * (raw_data['Tin'][i] - raw_data['Twb'][i]) )
        
        valuesY[i, 0] = (raw_data['Tin'][i] - raw_data['Tout'][i]) / (raw_data['Tin'][i] - raw_data['Twb'][i])
    
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(valuesX, valuesY)
    result_1 = clf.score(valuesX, valuesY, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_
    
#    print(result_1)
#    print(lin_coeff_1)
#    print(int_1)

    ret_coeff = np.zeros((6,1))
    
    ret_coeff[0,0] = lin_coeff_1[0,0]
    ret_coeff[1,0] = lin_coeff_1[0,1]
    ret_coeff[2,0] = lin_coeff_1[0,2]
    ret_coeff[3,0] = lin_coeff_1[0,3]
    ret_coeff[4,0] = lin_coeff_1[0,4]
    ret_coeff[5,0] = int_1[0]
    
    return ret_coeff


##This function separates the cooling tower data into separate flowrates
def prepare_cooling_tower_data ():
    
    import pandas as pd 
    
    ##Importing the raw data
    raw_data = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\proof_of_simplification\\cooling_tower_raw_data\\raw_data.csv')
    dim_raw_data = raw_data.shape 
    
    
    ##Changing the units of the raw data
#    raw_data_changed_units = pd.DataFrame(columns = ['Tin', 'Tout', 'Twb', 'E', 'mw', 'ma'])
#    
#    for i in range(0, dim_raw_data[0]):
#        tin_curr = raw_data['Tin'][i] - 273.15
#        tout_curr = raw_data['Tout'][i] - 273.15
#        twb_curr = raw_data['Twb'][i] - 273.15
#        mw_curr = raw_data['mw'][i] / 998.2
#        ma_curr = raw_data['ma'][i]
#        
#        temp_data = [tin_curr, tout_curr, twb_curr, raw_data['E'][i], mw_curr, ma_curr]
#        temp_df = pd.DataFrame(data = [temp_data], columns = ['Tin', 'Tout', 'Twb', 'E', 'mw', 'ma'])
#        raw_data_changed_units = raw_data_changed_units.append(temp_df, ignore_index = True)
    
    ##Discovering the number of flow categories 
    #discover_flow_categories (raw_data_changed_units)
    
    ##Saving the raw data into csv format 
    #raw_data_changed_units.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\proof_of_simplification\\cooling_tower_raw_data\\raw_data_changed_units.csv')
    
    ##This function is stopped here due to poor data quality insufficient data points 
    return raw_data

##This function studies the number of flowrate categories which the raw data falls into 
def discover_flow_categories (raw_data_changed_units):
    
    import pandas as pd 
    import matplotlib.pyplot as plt 
    
    ##Plotting the flowrate instances according to the flow 
    dim_raw_data_changed_units = raw_data_changed_units.shape 
    
    x_data = []
    ##Fixing the iterations axis 
    for i in range (0, dim_raw_data_changed_units[0]):
        x_data.append(i)
        
    ##Plotting 
    plt.plot(x_data, raw_data_changed_units['mw'][:], 'o')
    plt.show()
    
    return 

##A function to generate a lookup table of bilinear pieces 
def gen_bilinear_pieces (x_min, x_max, y_min, y_max, bilinear_pieces):
    import pandas as pd 
    u_table = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    v_table = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int']) 
    
    ##u_bounds 
    u_overall_min = x_min + y_min 
    u_overall_max = x_max + y_max
    ##y_bounds 
    v_overall_min = x_min - y_max
    v_overall_max = x_max - y_min 
    ##step_increment 
    u_step = (u_overall_max - u_overall_min) / bilinear_pieces
    v_step = (v_overall_max - v_overall_min) / bilinear_pieces

    for i in range (0, bilinear_pieces):
        ##Handling u values first 
        u_min = (i * u_step) + u_overall_min
        u_max = ((i + 1) * u_step) + u_overall_min
        fu_min = 0.25 * pow(u_min, 2)
        fu_max = 0.25 * pow(u_max, 2)
        u_grad = (fu_max - fu_min) / (u_max - u_min)
        u_int = fu_max - (u_grad * u_max)
        u_data = [u_min, u_max, u_grad, u_int]
        u_df = pd.DataFrame(data = [u_data], columns = ['lb', 'ub', 'grad', 'int'])
        u_table = u_table.append(u_df, ignore_index = True)
        ##Handling v values next 
        v_min = (i * v_step) + v_overall_min
        v_max = ((i + 1) * v_step) + v_overall_min
        fv_min = 0.25 * pow(v_min, 2)
        fv_max = 0.25 * pow(v_max, 2)
        v_grad = (fv_max - fv_min) / (v_max - v_min)
        v_int = fv_max - (v_grad * v_max)
        v_data = [v_min, v_max, v_grad, v_int]
        v_df = pd.DataFrame(data = [v_data], columns = ['lb', 'ub', 'grad', 'int'])
        v_table = v_table.append(v_df, ignore_index = True)        
        
    return u_table, v_table 
    
##A function to determine the estimated values of using bilinear pieces 
def search_bilin_table_for_values (u_table, v_table, x_actual, y_actual):
    
    ##Computing the actual values 
    u_actual = x_actual + y_actual 
    v_actual = x_actual - y_actual 
    ##Computing the number of iterations 
    dim_u_table = u_table.shape 
    dim_v_table = v_table.shape 
    
    for i in range (0, dim_u_table[0]):
        if (u_actual >= u_table['lb'][i]) and (u_actual <= u_table['ub'][i]):
            fu_calc = (u_actual * u_table['grad'][i]) + u_table['int'][i]
            break
    for i in range (0, dim_v_table[0]):
         if (v_actual >= v_table['lb'][i]) and (v_actual <= v_table['ub'][i]):
            fv_calc = (v_actual * v_table['grad'][i]) + v_table['int'][i]
            break       
        
    bilin_est = fu_calc - fv_calc

    return bilin_est

###########################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    ct_prepare_coefficients ()
