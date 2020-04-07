##This script contains all the chiller models, the input and output of all the models should be the same 
##The entire model is built based on 

##Model 1: Gordon-ng chiller model 
##Model 2: The effect of step-wise linearization on the model 
##Model 3: The effect of LP relaxation of bilinear terms on the model 

###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################

##Model 1: Gordon-ng chiller model 
def chiller_gnu (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max):
    
    ##reg_cst[0] --- b0
    ##reg_cst[1] --- b1
    ##reg_cst[2] --- b2
    ##qc_coeff --- link between the Qe and Qc
    ##Tin_evap --- evaporator return temperature (deg C)
    ##Tout_evap --- evaporator set point temperature (deg C) 
    ##Tin_cond --- condenser inlet temperature (deg C)
    ##mevap --- flowrate through the evaporator (m3/h)
    ##mcond --- flowrate through the condenser (m3/h)
    ##Qe_max --- maximum capacity of the chiller (kWh)
    
    import pandas as pd
    
    ##Dealing with the regression coefficients 
    b0 = reg_cst[0]
    b1 = reg_cst[1]
    b2 = reg_cst[2]

    ##Converting all the temperature values 
    Tin_evap = Tin_evap + 273.15
    Tout_evap = Tout_evap + 273.15
    Tin_cond = Tin_cond + 273.15
    
    ##Converting volume flowrate (m3/h) to (kg/s)
    mevap = mevap * 998.2 / 3600
    mcond = mcond * 998.2 / 3600
    
    ##Determining the values of Qe
    Qe = mevap * 4.2 * (Tin_evap - Tout_evap)
    
    a_1 = (b0 * Tin_evap) / Qe
    a_2 = b1 * ((Tin_cond - Tin_evap) / (Tin_cond * Qe))
    a_3 = Tin_evap / Tin_cond
    a_4 = (b2 * Qe) / Tin_cond
    
    temp = (((a_1 + a_2 + 1) / (a_3 - a_4)) - 1)
    COP = pow(temp, -1)
    
    ##Computing the return side values of the condenser side 
    Qc = qc_coeff * (Qe + (Qe / COP))
    if mcond != 0:
        Tout_cond = (Tin_cond + (Qc / (mcond * 4.2))) - 273.15
    else:
        Tout_cond = float('inf')
        
    ##Computing the electricity consumption 
    if COP > 0:
        E = Qe / COP
    else:
        E = float('inf') 
    
    ##Assembling the return values 
    return_values = {}
    return_values['Electricity_consumption'] = E
    return_values['Coefficient_of_performance'] = COP 
    return_values['Cooling_load'] = Qe
    return_values['Tout_cond'] = Tout_cond
    return_values['Heat_rejected'] = Qc

    ##Putting it in a dataframe for easy viewing 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_data = ['Electricity_consumption', return_values['Electricity_consumption'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Coefficient_of_performance', return_values['Coefficient_of_performance'], '-']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Cooling_load', return_values['Cooling_load'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Tout_cond', return_values['Tout_cond'], 'K']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Heat_rejected', return_values['Heat_rejected'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)    
    
    return return_values, return_values_df    
    
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################

##Model 2: The effect of step-wise linearization of COP 
def chiller_gnu_stepwise_cop (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max, steps):

    ##reg_cst[0] --- b0
    ##reg_cst[1] --- b1
    ##reg_cst[2] --- b2
    ##qc_coeff --- link between the Qe and Qc
    ##Tin_evap --- evaporator return temperature (K)
    ##Tout_evap --- evaporator set point temperature (K) 
    ##Tin_cond --- condenser inlet temperature (K)
    ##mevap --- flowrate through the evaporator (m3/h)
    ##mcond --- flowrate through the condenser (m3/h)
    ##Qe_max --- maximum capacity of the chiller (kWh)
    ##steps --- the number of stepwise COP pieces

    import pandas as pd
    
    ##Based on the fixed evaporator temperatures, we would like to determine the maximum flowrate though which the load is maximized 
    mevap_max = Qe_max / (4.2 * (Tin_evap - Tout_evap))
    mevap_max = (mevap_max * 3600) / 998.2
    mevap_step = mevap_max / steps 
    
    ##Building a reference table for the various pieces, for which the lb and ub values are based on the flowrates
    stepwise_info = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    for i in range (0, steps):
        mevap_curr_lb = i * mevap_step
        mevap_curr_ub = (i + 1) * mevap_step
            
        ##Determining the electricity consumption of the chiller at the upper and lower bounds 
        if i == 0:
            result_lb, result_lb_df = chiller_gnu(reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, 0.001, mcond, Qe_max)
        else:
            result_lb, result_lb_df = chiller_gnu(reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap_curr_lb, mcond, Qe_max)
        result_ub, result_ub_df = chiller_gnu(reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap_curr_ub, mcond, Qe_max)
                   
        elect_lb = result_lb['Electricity_consumption']
        elect_ub = result_ub['Electricity_consumption']
        
        grad = (elect_ub - elect_lb) / (mevap_curr_ub - mevap_curr_lb)
        intercept  = elect_ub - (grad * mevap_curr_ub)
        
        data_temp = [mevap_curr_lb, mevap_curr_ub, grad, intercept]
        stepwise_info_temp = pd.DataFrame(data = [data_temp], columns = ['lb', 'ub', 'grad', 'int'])
        stepwise_info = stepwise_info.append(stepwise_info_temp, ignore_index = True)
        
    ##With the bounds established, we would like to check the electricity consumption based on matching the stepwise pieces
    for i in range (0, steps):
        if (mevap >= stepwise_info['lb'][i]) and (mevap <= stepwise_info['ub'][i]):
            elect_cons = (mevap * stepwise_info['grad'][i]) + stepwise_info['int'][i]
            break
    
    Qe = ((mevap * 998.2) / 3600) * 4.2 * (Tin_evap - Tout_evap)
    COP = Qe / elect_cons 
    
    ##Computing the return side values of the condenser side 
    ##Converting all the temperature values 
    Tin_evap = Tin_evap + 273.15
    Tout_evap = Tout_evap + 273.15
    Tin_cond = Tin_cond + 273.15
    
    ##Converting volume flowrate (m3/h) to (kg/s)
    mevap = mevap * 998.2 / 3600
    mcond = mcond * 998.2 / 3600
    
    Qc = qc_coeff * (Qe + (Qe / COP))
    if mcond != 0:
        Tout_cond = Tin_cond + (Qc / (mcond * 4.2)) - 273.15
    else:
        Tout_cond = float('inf') 
        
    ##Assembling the return values 
    return_values = {}
    return_values['Electricity_consumption'] = elect_cons
    return_values['Coefficient_of_performance'] = COP 
    return_values['Cooling_load'] = Qe
    return_values['Tout_cond'] = Tout_cond    
    return_values['Heat_rejected'] = Qc   
       
    ##Putting it in a dataframe for easy viewing 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_data = ['Electricity_consumption', return_values['Electricity_consumption'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Coefficient_of_performance', return_values['Coefficient_of_performance'], '-']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Cooling_load', return_values['Cooling_load'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Tout_cond', return_values['Tout_cond'], 'K']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Heat_rejected', return_values['Heat_rejected'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)    
    
    return return_values, return_values_df    
    
###########################################################################################################################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################    

##Model 3: The effect of LP relaxation of bilinear terms on the model 
def chiller_gnu_stepwise_cop_lprelax (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max, steps, bilinear_pieces, mevap_t, mcond_t, twb):
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\' 
    import sys 
    sys.path.append(current_path + 'sub_scripts\\')
    sys.path.append(current_path + 'C:\Optimization_zlc\glpk_handlers\simulation_output_extractor\\')
    sys.path.append('C:\\Optimization_zlc\\glpk_handlers\\')
    import pandas as pd
    from optimaluv_chiller_cond_gen_script_lpformat import optimaluv_chiller_cond_gen_script_lpformat
    from glpk_runscript import glpk_runscript
    from glpk_output_extractor_chiller_cond_bilin import glpk_output_extractor_chiller_cond_bilin
    
    ##reg_cst[0] --- b0
    ##reg_cst[1] --- b1
    ##reg_cst[2] --- b2
    ##qc_coeff --- link between the Qe and Qc
    ##Tin_evap --- evaporator return temperature (K)
    ##Tout_evap --- evaporator set point temperature (K) 
    ##Tin_cond --- condenser inlet temperature (K)
    ##mevap --- flowrate through the evaporator (m3/h)
    ##mcond --- flowrate through the condenser (m3/h)
    ##Qe_max --- maximum capacity of the chiller (kWh)
    ##steps --- the number of stepwise COP pieces
    ##bilinear_pieces --- the number of stepwise pieces to deal with bilinear terms in the equation 
    
    ##Need to create an estimate for Qe first, the bilinear term is mevap * Tout_evap 
    ##Creating the number of bilinear pieces based on predefined bounds 
    Tout_evap_min = 1 + 273.15
    Tout_evap_max = Tin_evap + 273.15
    mevap_perc_min = 0
    mevap_perc_max = 1

    ##Generating the bilinear reference table for evaporator 
    u_table_evap, v_table_evap = gen_bilinear_pieces (mevap_perc_min, mevap_perc_max, Tout_evap_min, Tout_evap_max, bilinear_pieces)
            
    ##Need to create an estimate for Qc next, the bilinear term is mcond * Tout_cond
    Tout_cond_min = twb + 273.15
    Tout_cond_max = twb + 8 + 273.15
    mcond_perc_min = 0
    mcond_perc_max = 1   
    
    ##Generating the bilinear reference table for the condenser 
    u_table_cond, v_table_cond = gen_bilinear_pieces (mcond_perc_min, mcond_perc_max, Tout_cond_min, Tout_cond_max, bilinear_pieces)
        
    ##Since the list is established, need to check for the which of the bilinear pieces will it fall into for the evaporator side 
    mevap_perc_actual = mevap / mevap_t
    
    bilin_est_evap = search_bilin_table_for_values (u_table_evap, v_table_evap, mevap_perc_actual, (Tout_evap + 273.15))

    ##Now we can estimate the value of Qe 
    mevap_conv = (mevap * 998.2) / 3600
    mevap_t_conv = (mevap_t * 998.2) / 3600
    Qe = (mevap_conv * 4.2 * (Tin_evap + 273.15)) - (mevap_t_conv * 4.2 * bilin_est_evap)
    
    ##Using the stepwise linear model, we can estimate the elctricity consumption, however we need to take into consideration how to represent the part load 
    rep_tout_evap = 1
    rep_mevap = Qe / (4.2 * (Tin_evap - rep_tout_evap))
    rep_mevap = (rep_mevap / 998.2) * 3600
    
    ##Using model 2 we generate the relevant values 
    result, result_df = chiller_gnu_stepwise_cop (reg_cst, qc_coeff, Tin_evap, rep_tout_evap, Tin_cond, rep_mevap, mcond, Qe_max, steps)
    elect_cons = result['Electricity_consumption']
    COP = result['Coefficient_of_performance']

    ##We also need to determine the condenser outlet temperature, to do that we need to fix Qc first 
    Qc = qc_coeff * (Qe + (Qe / COP))
    
    ##Checking which of the bilinear pieces it will fall identifying the u and v, this is an optimization problem 
    bilin_pieces_list_cond = combine_u_v_table (u_table_cond, v_table_cond)
    data_org_bounds = [mcond_perc_min, mcond_perc_max, Tout_cond_min, Tout_cond_max]
    org_var_bounds = pd.DataFrame(data = [data_org_bounds], columns = ['mcond_perc_min', 'mcond_perc_max', 'Tout_cond_min', 'Tout_cond_max'])
    var_list = optimaluv_chiller_cond_gen_script_lpformat(Qc, bilin_pieces_list_cond, Tin_cond, mcond, mcond_t, org_var_bounds)
    
    ##Using the GLPK to solve the reverse problem 
    input_dir = 'C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\sub_scripts\\result_holder\\chiller_cond_bilin.lp'
    output_dir = 'C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\sub_scripts\\result_holder\\glpk_chiller_cond_bilin_out.txt'
    file_format = '--lp'
    
    output = glpk_runscript(input_dir, output_dir, file_format)
    convergence = output[1]

    if convergence == 1:
        obj_value, var_rec = glpk_output_extractor_chiller_cond_bilin(output_dir, var_list)
        dim_var_rec = var_rec.shape
        for i in range (0, dim_var_rec[0]):
            if ('_y' not in var_rec['var_name'][i]) and (var_rec['var_value'][i] > 0) and ('Tcond' in var_rec['var_name'][i]):
                Tcond_out = var_rec['var_value'][i] - 273.15
                break
    
    else:
        print('error')
    
    
    ##Assembling the return values 
    return_values = {}
    return_values['Electricity_consumption'] = elect_cons
    return_values['Coefficient_of_performance'] = COP 
    return_values['Cooling_load'] = Qe
    return_values['Tout_cond'] = Tcond_out    
    return_values['Heat_rejected'] = Qc
    
    ##Putting it in a dataframe for easy viewing 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_data = ['Electricity_consumption', return_values['Electricity_consumption'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Coefficient_of_performance', return_values['Coefficient_of_performance'], '-']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Cooling_load', return_values['Cooling_load'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Tout_cond', return_values['Tout_cond'], 'K']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)

    temp_data = ['Heat_rejected', return_values['Heat_rejected'], 'kWh']
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(temp_df, ignore_index = True)    
    
    return return_values, return_values_df    

################################################################################################################################################################
################################################################################################################################################################
##Add-on functions

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
    
##A function to assemble combine u_table and v_table, stupid function 
def combine_u_v_table (u_table, v_table):
    import pandas as pd 
    dim_u_table = u_table.shape
    combined_table = pd.DataFrame(columns = ['u_min' , 'u_max', 'u_grad', 'u_int', 'v_min', 'v_max', 'v_grad', 'v_int'])
    
    for i in range (0, dim_u_table[0]):
        data_temp = [u_table['lb'][i], u_table['ub'][i], u_table['grad'][i], u_table['int'][i], v_table['lb'][i], v_table['ub'][i], v_table['grad'][i], v_table['int'][i]]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['u_min' , 'u_max', 'u_grad', 'u_int', 'v_min', 'v_max', 'v_grad', 'v_int'])
        combined_table = combined_table.append(temp_df, ignore_index = True)

    return combined_table

import os 
current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'  

print(current_path)