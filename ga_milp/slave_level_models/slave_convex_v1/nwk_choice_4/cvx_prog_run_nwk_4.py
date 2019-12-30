##Interface for convex optimization with/without relaxations

##The process is as follows 
    ##Take in values from the master optimization 
        ##Passes in a list of master variables with the respective tag names to act as constants for the quadratic programming phase 
    ##Convex programming phase 
        ##A master list
        ##Models 
        ##Script to arrange into standard lp form 
        ##Script to extract the answers from the solver 
        ##Returning the objective function values to the master solver

def cvx_prog_run_nwk_4(parallel_thread_num):
        
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\')
    from slave_convex_backend import slave_convex_backend
    import pandas as pd 
    
    slave_models_location = 'C:\\Optimization_zlc\\slave_level_models\\slave_convex_v1\\nwk_choice_4\\'
    ##Bilinear pieces
    bilinear_pieces = 5
    
    package_name = 'nwk_choice_4'
    files = pd.DataFrame(columns = ['Filename'])
    
    ##Auxillary files 
    
    ##File 1
    inputmodel = pd.DataFrame(data = ['layers'], columns = ['Filename'])                        ##The layers model 
    files = files.append(inputmodel, ignore_index=True)
    
    ##Chiller models 
        
    ##File 2
    inputmodel = pd.DataFrame(data = ['chiller1'], columns = ['Filename'])                      ##Chiller 1 model 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 3
    inputmodel = pd.DataFrame(data = ['chiller2'], columns = ['Filename'])                      ##Chiller 2 model 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 4
    inputmodel = pd.DataFrame(data = ['chiller3'], columns = ['Filename'])                      ##Chiller 3 model
    files = files.append(inputmodel, ignore_index=True)
    
    ##Chiller evaporator side 
    
    ##File 5
    inputmodel = pd.DataFrame(data = ['ch1_evap_pump'], columns = ['Filename'])                 ##Chiller 1 evaporator pump 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 6
    inputmodel = pd.DataFrame(data = ['ch2_evap_pump'], columns = ['Filename'])                 ##Chiller 2 evaporator pump 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 7
    inputmodel = pd.DataFrame(data = ['ch3_evap_pump'], columns = ['Filename'])                 ##Chiller 3 evaporator pump
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 8
    inputmodel = pd.DataFrame(data = ['splitter1_temp'], columns = ['Filename'])                ##A model to consoliate the outlet temperatures of each chiller
    files = files.append(inputmodel, ignore_index=True)                                         ##and splits them into 6 streams for the each of the parallel network branches
    
    ##File 9
    inputmodel = pd.DataFrame(data = ['chiller_evap_flow_consol'], columns = ['Filename'])      ##A model to make sure that the total flowrate matches the master
    files = files.append(inputmodel, ignore_index=True)                                         ##decision input
    
    ##File 10
    inputmodel = pd.DataFrame(data = ['chiller1_evap_nwk'], columns = ['Filename'])             ##The pressure drop which chiller 1 evaporator pump has to face 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 11
    inputmodel = pd.DataFrame(data = ['chiller2_evap_nwk'], columns = ['Filename'])             ##The pressure drop which chiller 2 evaporator pump has to face 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 12
    inputmodel = pd.DataFrame(data = ['chiller3_evap_nwk'], columns = ['Filename'])             ##The pressure drop which chiller 3 evaporator pump has to face 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 13
    inputmodel = pd.DataFrame(data = ['splitter2_temp'], columns = ['Filename'])                ##A model to consolidate the outlet temperatures of each substation
    files = files.append(inputmodel, ignore_index=True)                                         ##and splits them into 3 return streams to the 3 chillers
    
    ##File 14
    inputmodel = pd.DataFrame(data = ['chiller1_ret'], columns = ['Filename'])                  ##A model to make sure that the return temperature of this chiller is 
    files = files.append(inputmodel, ignore_index=True)                                         ##that specified by the master decision input
    
    ##File 15
    inputmodel = pd.DataFrame(data = ['chiller2_ret'], columns = ['Filename'])                  ##A model to make sure that the return temperature of this chiller is 
    files = files.append(inputmodel, ignore_index=True)                                         ##that specified by the master decision input
    
    ##File 16
    inputmodel = pd.DataFrame(data = ['chiller3_ret'], columns = ['Filename'])                  ##A model to make sure that the return temperature of this chiller is 
    files = files.append(inputmodel, ignore_index=True)                                         ##that specified by the master decision input
    
    ##Chiller condenser side 
    
    ##File 17
    inputmodel = pd.DataFrame(data = ['ch1_cond_pump'], columns = ['Filename'])                 ##Chiller 1 condenser pump
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 18
    inputmodel = pd.DataFrame(data = ['ch2_cond_pump'], columns = ['Filename'])                 ##Chiller 2 condenser pump
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 19
    inputmodel = pd.DataFrame(data = ['ch3_cond_pump'], columns = ['Filename'])                 ##Chiller 3 condenser pump
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 20
    inputmodel = pd.DataFrame(data = ['chiller_cond_ret_mflow'], columns = ['Filename'])        ##A model to make sure that the total flowrate matches the master 
    files = files.append(inputmodel, ignore_index=True)                                         ##decision input
    
    ##File 21
    inputmodel = pd.DataFrame(data = ['splitter3_temp'], columns = ['Filename'])                ##A model to consolidate the temperatures of the chiller condensers
    files = files.append(inputmodel, ignore_index=True)                                         ##and splits them into individual streams for the cooling towers
    
    ##File 22
    inputmodel = pd.DataFrame(data = ['chiller1_cond_nwk'], columns = ['Filename'])             ##The pressure drop which chiller 1 condenser pump has to face
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 23
    inputmodel = pd.DataFrame(data = ['chiller2_cond_nwk'], columns = ['Filename'])             ##The pressure drop which chiller 2 condenser pump has to face 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 24
    inputmodel = pd.DataFrame(data = ['chiller3_cond_nwk'], columns = ['Filename'])             ##The pressure drop which chiller 3 condenser pump has to face 
    files = files.append(inputmodel, ignore_index=True)
    
    ##Network models 
    
    ##File 25
    inputmodel = pd.DataFrame(data = ['cp_network'], columns = ['Filename'])                    ##The common pipe network, to copy the temperature and flowrate
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 26
    inputmodel = pd.DataFrame(data = ['ice_network'], columns = ['Filename'])                   ##The ice network model, to calculate the pressure drop 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 27
    inputmodel = pd.DataFrame(data = ['gv2_network'], columns = ['Filename'])                   ##The gv2 network model, to calculate the pressure drop 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 28
    inputmodel = pd.DataFrame(data = ['hsb_network'], columns = ['Filename'])                   ##The hsb network model, to calculate the pressure drop 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 29
    inputmodel = pd.DataFrame(data = ['tro_network'], columns = ['Filename'])                   ##The troncal network model, to calculate the pressure drop
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 30
    inputmodel = pd.DataFrame(data = ['pfa_network'], columns = ['Filename'])                   ##The pfa network model, to calculate the pressure drop
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 31
    inputmodel = pd.DataFrame(data = ['ser_network'], columns = ['Filename'])                   ##The sertram network model, to calculate the pressure drop
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 32
    inputmodel = pd.DataFrame(data = ['fir_network'], columns = ['Filename'])                   ##The firal network model, to calculate the pressure drop
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 33
    inputmodel = pd.DataFrame(data = ['dist_nwk_consol'], columns = ['Filename'])               ##A model to consolidate the pressure drops of all parallel distribution
    files = files.append(inputmodel, ignore_index=True)                                         ##networks
    
    ##File 34
    inputmodel = pd.DataFrame(data = ['dist_pump1'], columns = ['Filename'])                     ##The selected distribution pump which is selected to serve the distribution
    files = files.append(inputmodel, ignore_index=True)                                         ##network
    
    ##Substation models
    
    ##File 35
    inputmodel = pd.DataFrame(data = ['gv2_substation'], columns = ['Filename'])                ##The gv2 substation model which calculates the delta t, based on a fixed flowrate
    files = files.append(inputmodel, ignore_index=True)                                         ##and a predetermined demand
    
    ##File 36
    inputmodel = pd.DataFrame(data = ['hsb_substation'], columns = ['Filename'])                ##The hsb substation model which calculates the delta t, based on a fixed flowrate
    files = files.append(inputmodel, ignore_index=True)                                         ##and a predetermined demand
    
    ##File 37
    inputmodel = pd.DataFrame(data = ['pfa_substation'], columns = ['Filename'])                ##The pfa substation model which calculates the delta t, based on a fixed flowrate 
    files = files.append(inputmodel, ignore_index=True)                                         ##and a predetermined demand
    
    ##File 38
    inputmodel = pd.DataFrame(data = ['ser_substation'], columns = ['Filename'])                ##The ser substation model which calculates the delta t, based on a fixed flowrate 
    files = files.append(inputmodel, ignore_index=True)                                         ##and a predetermined demand
    
    ##File 39
    inputmodel = pd.DataFrame(data = ['fir_substation'], columns = ['Filename'])                ##The fir substation model which calculates the delta t, based on a fixed flowrate
    files = files.append(inputmodel, ignore_index=True)                                         ##and a predetermined demand
    
    ##Cooling tower models 
    
    ##File 40
    inputmodel = pd.DataFrame(data = ['cooling_tower1'], columns = ['Filename'])                ##The cooling tower 1 model 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 41
    inputmodel = pd.DataFrame(data = ['cooling_tower2'], columns = ['Filename'])                ##The cooling tower 2 model 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 42
    inputmodel = pd.DataFrame(data = ['cooling_tower3'], columns = ['Filename'])                ##The cooling tower 3 model 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 43
    inputmodel = pd.DataFrame(data = ['cooling_tower4'], columns = ['Filename'])                ##The cooling tower 4 model
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 44
    inputmodel = pd.DataFrame(data = ['cooling_tower5'], columns = ['Filename'])                ##The cooling tower 5 model
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 45
    inputmodel = pd.DataFrame(data = ['cooling_tower_ret'], columns = ['Filename'])             ##The cooling tower return temperature model, to make sure that the outlet temperature 
    files = files.append(inputmodel, ignore_index=True)                                         ##matches that of the master decision input
    
    ##Multi-time problem definition
    ##By multi-time, this means that the multi-time problem is transferred to the slave
    ##If the multi-time part is handled by the master optimizer, multi-time should be 0
    ##The values can only be 1(yes) or 0(no)
    multi_time = 0
    
    ##Objective function definition 
    ##The values can be either of the following 
    ##1. 'investment_cost'
    ##2. 'operation_cost'
    ##3. 'power'
    ##4. 'impact'
    
    #Put them in a list
    obj_func = ['power']
    
    ##Relaxation applications
    ##The values can only be 1(yes) or 0(no)
    ##If the value is 1, the link to the python file has to be specified
    
    ##Preferred solver 
    ##Available solvers: GLPK, Gurobi
    
    #obj_value, util = 
    x = slave_convex_backend(files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces)
    
    
    return x
