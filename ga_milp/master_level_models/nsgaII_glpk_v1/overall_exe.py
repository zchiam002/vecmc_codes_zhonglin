##This is the function for evaluating the values of the optimization problem 

def ecoenergies_opt(x,V):
    ##V is the number of decision variables (total)
    ##x contains the total number of decision variables
    import sys
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\\glpk_v1\\')
    #sys.path.append('C:\\Users\\zhonglin.chiam\\AppData\\Local\\Continuum\\Anaconda3\\lib\\site-packages\\pandas\\') #__init__.py')
    import pandas as pd 
    from network_model import network_model 
    from master_to_slave import master_to_slave
    from lin_prog_run import lin_prog_run
    from mapping_variables import mapping_variables
    
    sub_station_tinlim = 278.15
    sub_station_toutlim = 287.15
    
    objective_function = 0
    decision_variables = pd.read_csv('C:\\Optimization_zlc\\input_data\\nsgaII_glpk_v1\\master_decision_variables.csv')
    weather_param = pd.read_csv('C:\\Optimization_zlc\\input_data\\nsgaII_glpk_v1\\weather_data_day_170816.csv')
    demand = pd.read_csv('C:\\Optimization_zlc\\input_data\\nsgaII_glpk_v1\\la_marina_demand_day_170816.csv')
    dim_decision_variables = decision_variables.shape
    num_dv = dim_decision_variables[0]
    num_time_step = int(len(x)/num_dv)
    
    index = 0   
    for i in range (0,num_time_step):
        infeasibility = 0
        all_var = []
        ##Prepare the input variables
        for j in range(index, index+num_dv):
            all_var.append(x[j])

        all_var = mapping_variables(all_var)
        nwk_pump_power = network_model(all_var)

        if nwk_pump_power < 0:
            infeasibility = infeasibility + 2
        else:
            ##Continue with the linear optimization phase 
            ##Create the slave parameters csv
            input_demand_time = [demand['ss_gv2_demand'][i], demand['ss_hsb_demand'][i], demand['ss_pfa_demand'][i], demand['ss_ser_demand'][i], demand['ss_fir_demand'][i]]
            demand_time = pd.DataFrame(data = [input_demand_time], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
            master_to_slave(all_var, sub_station_tinlim, sub_station_toutlim, demand_time, weather_param['T_WB'][i])
            ##run the linear program 
            obj_value, unit_utilization = lin_prog_run()
            print(obj_value)
            #print(obj_value)
            if obj_value < 0:
                infeasibility = infeasibility + 1
            else:
                power = nwk_pump_power + obj_value
        index = index + num_dv
        if infeasibility == 0:
            objective_function = objective_function + power[0]
        else:
            objective_function = objective_function + (infeasibility*10000)
    
    #print(objective_function)

    return objective_function
    
    