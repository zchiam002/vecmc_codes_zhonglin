##This script computes the error between the abstracted model and the original model 

def dist_nwk_abstracted_vs_org_error ():
    
    import pandas as pd 
    
    ##Hyper parameters 
    pwl_pieces = 4
    #bilinear_pieces = 12
    
    ##Importing the linear function 
    
    ##This function prepares the csv file for referencing the linear coefficients for the linearized model 
    from prepare_dist_nwk_lin_coeff_pwl import prepare_dist_nwk_lin_coeff_pwl
    prepare_dist_nwk_lin_coeff_pwl (pwl_pieces)
    
    ##Based on a selected pump and network configuration, we range the flow from the max flow and min/max pressure 
    #nwk_select = 3
    pump_select = 37                       ##for only choose 34-40
    
    ##Determining the lowest pressure drop curves 
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\')
    from dist_nwk_lower_limits_model import dist_nwk_lower_limits_model  
    lowest_limit_info = dist_nwk_lower_limits_model()
    ##Since we are only interested in the final case 
    sys_curve = [lowest_limit_info['x2_coeff'][7], lowest_limit_info['x_coeff'][7], 0]
    
    ##Determining the pump curve 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from dist_network_models_sub import dist_nwk_pump_select
    pump_related_data = dist_nwk_pump_select(pump_select)
    
    ##Enumerating through the entire range 
        ##Hyper parameters 
    delp_interval = 10
    flowrate_interval = 20
        ##Determine the maximum flowrate for the given configuration 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\add_on_functions\\')
    from golden_section import golden_section_dist 
    max_flow = 2300
    max_sys_flow = golden_section_dist(pump_sys_int_dist, [0, max_flow], sys_curve, pump_related_data['ice_tro_fir_branch_pump_delp'])
    flow_step = (max_sys_flow-5) / flowrate_interval 
        ##Creating a dataframe for collecting the data 
    elect_results = pd.DataFrame(columns = ['flow', 'org_model_elect_cons', 'pwl_lin_model_elect_cons', 'error_2', 'error_mae'])
        ##Counter for RMSE
    counter = 0
    
    for i in range (0, flowrate_interval+1):
        curr_flow = i * flow_step 
        p_0 = pump_related_data['ice_tro_fir_branch_pump_delp'][0]
        p_1 = pump_related_data['ice_tro_fir_branch_pump_delp'][1]
        p_2 = pump_related_data['ice_tro_fir_branch_pump_delp'][2]
        s_0 = sys_curve[0]
        s_1 = sys_curve[1]
        s_2 = sys_curve[2]
        max_pressure = (p_0 * curr_flow) + (p_1 * curr_flow) + p_2
        min_pressure = (s_0 * curr_flow) + (s_1 * curr_flow) + s_2
        diff_pressure = max_pressure - min_pressure 
        press_step = diff_pressure / delp_interval
        
        for j in range (0, delp_interval+1):
            curr_pressure = min_pressure + (j * press_step)
            ##evaluating using the original model 
            pump_curve = pump_related_data['ice_tro_fir_branch_pump_delp']
            elect_curve = pump_related_data['ice_tro_fir_branch_pump_elect']
            elect_cons_om = dist_nwk_pump_nwk (pump_curve, sys_curve, elect_curve, curr_pressure, curr_flow)

            elect_cons_pwl = dist_nwk_pwl_elect (curr_flow, curr_pressure, pwl_pieces, pump_select+1)

            
            counter = counter + 1
            if elect_cons_om != 0:
                error_2 = pow((((elect_cons_om - elect_cons_pwl)/elect_cons_om)*100), 2)
                error_mae =  100*(abs(elect_cons_om - elect_cons_pwl)/elect_cons_om)
            else:
                error_2 = 0
                error_mae = 0
                
            temp_data = [curr_flow, elect_cons_om, elect_cons_pwl, error_2, error_mae]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['flow', 'org_model_elect_cons', 'pwl_lin_model_elect_cons', 'error_2', 'error_mae'])
            elect_results = elect_results.append(temp_df, ignore_index = True)
            
    ##Calculating the RMSE
    total_error = sum(elect_results['error_2'][:])
    total_error = total_error / counter 
    RMSE = pow(total_error, 0.5)
    
    ##Calculating the MAE
    total_mae = sum(elect_results['error_mae'][:])
    mae = total_mae/counter
    
    print(mae)
    print(RMSE)
    
    ##Plotting the results 
    import matplotlib.pyplot as plt
    import numpy as np
    

#    plt.scatter(elect_results['flow'][:], elect_results['org_model_elect_cons'][:], color = 'blue')    
    plt.scatter(elect_results['org_model_elect_cons'][:], elect_results['pwl_lin_model_elect_cons'][:], color = 'blue', marker = '.')
    plt.show()
    
    
    
    
    
    return 

###################################################################################################################################################################################
##Additional functions
    
##This is the pwl pump model used for determining the electricity consumption, only the final 7 choices 
def dist_nwk_pwl_elect (flow, pressure, pwl, pump_select):
    
    import pandas as pd 
    
    ##flow --- the current flowrate 
    ##pressure --- the current pressure drop 
    ##pwl --- the number of piecewise pieces
    ##pump_select --- the selected pump-network configuration
    
    ##Import the dataframe from the location 
    lin_coeff_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_nwk_testing\\dist_pump_lincoeff.csv')
    
    ##Determine the maximum flowrate for the current configuration 
    key = 'p1_max_m_' + str(pwl - 1)
    max_flow_config = lin_coeff_data[key][pump_select] 
    if (flow > max_flow_config):
        max_flow_config = flow
    
    
    ##Searching through the linear pieces 
    flow_step = max_flow_config / pwl
    
    not_in_range = 0
    for i in range (0, pwl):
        curr_min = i * flow_step 
        curr_max = (i + 1) * flow_step
        ##Checking for 0 flow case
        if flow == 0:
            elect_cons = 0
            not_in_range = 1
            break 
        elif (flow > curr_min) and (flow <= curr_max):
            c_1 = lin_coeff_data['p1_m_coeff_' + str(i)][pump_select]
            c_2 = lin_coeff_data['p1_p_coeff_' + str(i)][pump_select]
            c_3 = lin_coeff_data['p1_cst_' + str(i)][pump_select]
            elect_cons = (c_1 * flow) + (c_2 * pressure) + c_3
            not_in_range = 1
            break   
        
    return elect_cons

##This is a generic pump function to emulate reading from a graph, the objective of this function is to return the electricity consumption for a given pump-network configuration 
def dist_nwk_pump_nwk (pump_curve, sys_curve, elect_curve, pressure, flow):
    
    import pandas as pd 
    
    ##pump_curve --- the associated pump curve in quadratic form
    ##sys_coeff --- the associated coefficient of system curve in the quadratic form  
    ##elect_curve --- the electricity consumption at nominal speeds
    ##pressure --- the operating pressure 
    ##flow --- the operating flow 
    
    ##Step 1: determine the intersection point of the pump curve and the system curve, which is needed to determine the maximum flow  
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\add_on_functions\\')
    from golden_section import golden_section_dist
    
    max_flow = 2300
    max_sys_flow = golden_section_dist(pump_sys_int_dist, [0, max_flow], sys_curve, pump_curve)
    
    ##Step 2: determine the maximum and minimum electricity consumption which is needed for interpolation 
    sys_max_elect_cons = (elect_curve[0] * pow(max_sys_flow, 3)) + (elect_curve[1] * pow(max_sys_flow, 2)) + (elect_curve[2] * max_sys_flow) + elect_curve[3]
    max_elect_cons = (elect_curve[0] * pow(flow, 3)) + (elect_curve[1] * pow(flow, 2)) + (elect_curve[2] * flow) + elect_curve[3]
    min_elect_cons = flow * (sys_max_elect_cons / max_sys_flow)
    
    ##Step 3: determine the pressure ratio between the min and max for the electricity interpolation 
    max_curr_pressure = (pump_curve[0] * pow(flow, 2)) + (pump_curve[1] * flow) + pump_curve[2]
    min_curr_pressure = (sys_curve[0] * pow(flow, 2)) + (sys_curve[1] * flow) + sys_curve[2]
    pressure_ratio = (pressure - min_curr_pressure) / (max_curr_pressure - min_curr_pressure) 
    
    ##Step 4: determine the electricity consumption
    if flow != 0:
        elect_cons = (pressure_ratio * (max_elect_cons - min_elect_cons)) + min_elect_cons
    else:
        elect_cons = 0
    
    return elect_cons

##Function to calculate the deviation between the pump and system curves, this function is to be used  
def pump_sys_int_dist (sys_coeffs, pump_coeffs, flow):
    ##sys_coeffs --- the single coefficient of the system curve 
    ##pump_coeffs[0] --- x2 coefficient 
    ##pump_coeffs[1] --- x coefficient
    ##pump_coeffs[2] --- constant term 
    ##flow --- the flowrate which the intersection point may be 
    
    sys_curve_value = (sys_coeffs[0] * pow(flow, 2)) + (sys_coeffs[1] * flow) + sys_coeffs[2]
    pump_curve_value = (pump_coeffs[0] * pow(flow, 2)) + (pump_coeffs[1] * flow) + pump_coeffs[2]
    ret_value = abs(pump_curve_value - sys_curve_value)
    ##print(sys_curve_value)
    ##print(pump_curve_value)
    
    return ret_value
###################################################################################################################################################################################
##Running the script 
if __name__ == '__main__':

    dist_nwk_abstracted_vs_org_error ()