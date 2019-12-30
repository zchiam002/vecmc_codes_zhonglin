##Interface for linear optimiaztion 

##The process is as follows 
    ##Take in values from the master optimization 
        ##Passes in a list of master variables with the respective tag names to act as constants for the linear programming phase 
    ##Linear programming phase 
        ##A master list
        ##Models 
        ##Script to arrange into standard form for the GLPK solver 
        ##Script to extract the answers from the solver 
        ##Returning the objective function values to the master solver 

def lin_prog_run():
    import sys
    sys.path.append('C:\\Optimization_zlc\\glpk_handlers')
    from glpk_backend import glpk_backend
    import pandas as pd
    
    files = pd.DataFrame(columns = ['Filename'])
    
    inputmodel = pd.DataFrame(data = ['layers'], columns = ['Filename'])                    ##File number 1
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['chiller1'], columns = ['Filename'])                  ##File number 2
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['chiller2'], columns = ['Filename'])                  ##File number 3
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['chiller3'], columns = ['Filename'])                  ##File number 4
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['splitter1'], columns = ['Filename'])                 ##File number 5
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['substation_cp'], columns = ['Filename'])             ##File number 6
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['substation_gv2'], columns = ['Filename'])             ##File number 7
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['substation_hsb'], columns = ['Filename'])             ##File number 8
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['substation_pfa'], columns = ['Filename'])             ##File number 9
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['substation_ser'], columns = ['Filename'])             ##File number 10
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['substation_fir'], columns = ['Filename'])             ##File number 11
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['splitter2'], columns = ['Filename'])                  ##File number 12
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['chiller1_ret'], columns = ['Filename'])               ##File number 13
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['chiller2_ret'], columns = ['Filename'])               ##File number 14
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['chiller3_ret'], columns = ['Filename'])               ##File number 15
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['splitter3'], columns = ['Filename'])                  ##File number 16
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['cooling_tower1'], columns = ['Filename'])             ##File number 17
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['cooling_tower2'], columns = ['Filename'])             ##File number 17
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['cooling_tower3'], columns = ['Filename'])             ##File number 17
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['cooling_tower4'], columns = ['Filename'])             ##File number 17
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['cooling_tower5'], columns = ['Filename'])             ##File number 17
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['cooling_tower_ret'], columns = ['Filename'])          ##File number 17
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['water_supply'], columns = ['Filename'])          ##File number 17
    files = files.append(inputmodel, ignore_index=True)
    
    ##Multi-time problem definition
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
    
    obj_value, util = glpk_backend(files, multi_time, obj_func)
    #print(obj_value)
    #print(obj_value)
    #print(util)
        
    return obj_value, util









