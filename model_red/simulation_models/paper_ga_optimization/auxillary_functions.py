##This script contains auxillary functions for the GA only approach

def check_balance_temperature_balance (final_obj_value, decision_variables, dist_nwk_outlet_temperature, ct_delt, twb, cond_nwk_outlet_temp):
    
    ##final_obj_value                       --- the current objective function value which is to be appended to if needed 
    ##decision_variables                    --- list of decision variables from the genetic algorithm 
    ##dist_nwk_outlet_temperature           --- the outlet temperature from the distribution network 
    ##ct_delt                               --- a dataframe of the delta ts of the cooling network 
    ##twb                                   --- the thermodynamic wetbulb temperature (deg C)
    ##cond_nwk_outlet_temp                  --- the outlet temperature of the condenser network 
    
    penalty = 20000
    cooling_tower_range = 5
    cooling_tower_min_approach = 5
    
    ##Checking the return temperature to the chiller evaporator
    if decision_variables[0] != dist_nwk_outlet_temperature:
        perc_difference = abs(decision_variables[0] - dist_nwk_outlet_temperature) / 10
        final_obj_value = final_obj_value + (perc_difference * penalty)
        
    ##Checking the return temperature to the chiller condenser 
        ##Determining the condenser inlet temperature 
    cond_inlet_temp = ((decision_variables[1] / 100) * cooling_tower_min_approach) + (twb + cooling_tower_range)
        ##Calculating the average delta t of the cooling towers 
    dim_ct_delt = ct_delt.shape 
    total_delt = sum(ct_delt['Value'][:])
    ave_delt = total_delt / dim_ct_delt[0]
    
    ##To avoid the case where all the chillers are turn off
    if cond_nwk_outlet_temp != 'Undefined':
        cooling_tower_outlet_temp = cond_nwk_outlet_temp - ave_delt
        
        if cooling_tower_outlet_temp != cond_inlet_temp:
            perc_difference = abs(cond_inlet_temp - cooling_tower_outlet_temp) / 10
            final_obj_value = final_obj_value + (perc_difference * penalty)
    
    return final_obj_value

########################################################################################################################################################################
########################################################################################################################################################################
##This function calculates the temperature difference at each substation and makes sure that it is not violated. If it is, the objective function is appended accordingly
def check_delt_substation (final_obj_value, customer_delts, max_delt_substation):
    
    ##final_obj_value           ---the current objective function value which is to be appeneded to if needed
    ##customer_delts            --- a list of substation temperature differences
    ##max_delt_substation       --- a dictionary of maximum delt values 
    
    penalty = 20000
    
    if customer_delts[0] > max_delt_substation['gv2_delt_max']:
        final_obj_value = final_obj_value + (penalty * (customer_delts[0] - max_delt_substation['gv2_delt_max']))
    
    if customer_delts[1] > max_delt_substation['hsb_delt_max']:
        final_obj_value = final_obj_value + (penalty * (customer_delts[1] - max_delt_substation['hsb_delt_max'])) 
        
    if customer_delts[2] > max_delt_substation['pfa_delt_max']:
        final_obj_value = final_obj_value + (penalty * (customer_delts[2] - max_delt_substation['pfa_delt_max'])) 
        
    if customer_delts[3] > max_delt_substation['ser_delt_max']:
        final_obj_value = final_obj_value + (penalty * (customer_delts[3] - max_delt_substation['ser_delt_max']))
    
    return final_obj_value

########################################################################################################################################################################
########################################################################################################################################################################
##This function calculates the objective function 
def calc_obj_func (chiller_obj_func, evap_nwk_obj_func, dist_nwk_obj_func, cond_nwk_obj_func, cooling_tower_obj_func, chiller_load_violation, dist_nwk_flow_violation):
    
    ##chiller_obj_func          --- dataframe of the electricity consumption from the various chillers 
    ##evap_nwk_obj_func         --- dataframe of the electricity consumption from the various evaporator network pumps
    ##dist_nwk_obj_func         --- dataframe of the electricity consumption from the various distribution network pumps 
    ##cond_nwk_obj_func         --- dataframe of the electricity consumption from the various condenser network pumps
    ##cooling_tower_obj_func    --- dataframe of the electricity consumption from the various cooling towers
    ##chiller_load_violation    --- the percentage to which the cooling load exceeds the maximum value 
    ##dist_nwk_flow_violation   --- the percentage to which the flowrate in the distribution network has to be reduced
    
    ##This is the objective function placeholder 
    final_obj_value = 0
    
    ##Defining penalties 
    penalty = 20000
    
    ##Computing the chiller_objective_function 
    dim_chiller_obj_func = chiller_obj_func.shape
    
    for i in range (0, dim_chiller_obj_func[0]):
        if chiller_obj_func['Value'][i] != float('inf'):
            final_obj_value = final_obj_value + chiller_obj_func['Value'][i]
        else:
            final_obj_value = final_obj_value + (penalty * chiller_load_violation['Value'][i])
    
    ##Computing the evap_nwk_obj_func 
    dim_evap_nwk_obj_func = evap_nwk_obj_func.shape 
    
    for i in range (0, dim_evap_nwk_obj_func[0]):
        final_obj_value = final_obj_value + evap_nwk_obj_func['Value'][i]
        
    ##Computing the dist_nwk_obj_func 
    dim_dist_nwk_obj_func = dist_nwk_obj_func.shape 
    
    for i in range (0, dim_dist_nwk_obj_func[0]):
        if dist_nwk_obj_func['Value'][i] != float('inf'):
            final_obj_value = final_obj_value + dist_nwk_obj_func['Value'][i]
        else:
            final_obj_value = final_obj_value + (penalty * dist_nwk_flow_violation)              
        
    ##Computing the cond_nwk_obj_func 
    dim_cond_nwk_obj_func = cond_nwk_obj_func.shape
    
    for i in range (0, dim_cond_nwk_obj_func[0]):
        final_obj_value = final_obj_value + cond_nwk_obj_func['Value'][i]
        
    ##Computing the cooling_tower_obj_func 
    dim_cooling_tower_obj_func = cooling_tower_obj_func.shape 
    
    for i in range (0, dim_cooling_tower_obj_func[0]):
        final_obj_value = final_obj_value + cooling_tower_obj_func['Value'][i]
    
    return final_obj_value

########################################################################################################################################################################
########################################################################################################################################################################

##Function to calculate the deviation between the pump and system curves, this function is to be used  
def pump_sys_int_dist (sys_coeff, pump_coeffs, flow):
    ##pump_coeffs[0] --- x2 coefficient 
    ##pump_coeffs[1] --- x coefficient
    ##pump_coeffs[2] --- constant term 
    ##flow --- the flowrate which the intersection point may be 
    
    sys_curve_value = (sys_coeff*pow(flow, 1.852))
    pump_curve_value = (pump_coeffs[0] * pow(flow, 2)) + (pump_coeffs[1] * flow) + pump_coeffs[2]
    ret_value = abs(pump_curve_value - sys_curve_value)
    ##print(sys_curve_value)
    ##print(pump_curve_value)
    #print(sys_curve_value, pump_curve_value, ret_value)
    
    return ret_value

########################################################################################################################################################################
########################################################################################################################################################################
##Function to calculate the deviation between the pump and system curves, this function is to be used  
def pump_sys_int_evap_cond (sys_coeff, pump_coeffs, sys_offset, flow):
    ##sys_coeff --- the single coefficient of the system curve 
    ##pump_coeffs[0] --- x2 coefficient 
    ##pump_coeffs[1] --- x coefficient
    ##pump_coeffs[2] --- constant term 
    ##flow --- the flowrate which the intersection point may be 
    
    sys_curve_value = (sys_coeff*pow(flow, 1.852)) + sys_offset
    pump_curve_value = (pump_coeffs[0] * pow(flow, 2)) + (pump_coeffs[1] * flow) + pump_coeffs[2]
    ret_value = abs(pump_curve_value - sys_curve_value)
    ##print(sys_curve_value)
    ##print(pump_curve_value)
    #print(sys_curve_value, pump_curve_value, ret_value)
    
    return ret_value

