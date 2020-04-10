##This function processes the output textfile from GLPK and extracts the relevant values 

def glpk_output_extractor(obj_func, units, util):
    import pandas as pd
    
    output_file = 'C:\\Optimization_zlc\\glpk_handlers\\input_output\\glpk_output.txt'
    
    ##Determining the objective function text 
    dim_obj_func = len(obj_func)
    name_obj_func = ''
    for i in range (0, dim_obj_func):
        name_obj_func = name_obj_func + obj_func[i]
        if i != dim_obj_func-1:
            name_obj_func = name_obj_func + '_'

    ##Extracting the objective function 
    with open(output_file) as fo:
        for rec in fo:
            if 'Objective:  ' + name_obj_func in rec:
                obj = rec.split(' ')
                break
        obj_value = float(obj[4])

    ##Extracting the utilization rates of associated units
    with open(output_file) as fo:
        for rec in fo:
            for i in range (0, len(units)):
                if 'u_rate['+units[i]+']' in rec:
                    if len(units[i]) <= 4:
                        u_all = rec.split(' ')
                        dim_u_all = len(u_all)
                        count = 0
                        for j in range (0, dim_u_all):
                            if u_all[j] != '':
                                count = count + 1
                                if count == 3:
                                    u = u_all[j]
                                    u_data = [units[i], u]
                                    udf = pd.DataFrame(data = [u_data], columns = ['Unit', 'Utilization'])
                                    util = util.append(udf, ignore_index=True)
                                    break
    
                    else:
                        u_all = next(fo).split(' ')
                        dim_u_all = len(u_all)
                        count = 0
                        for j in range (0, dim_u_all):
                            if u_all[j] != '':
                                count = count + 1
                                if count == 1:
                                    u = u_all[j]
                                    u_data = [units[i], u]
                                    udf = pd.DataFrame(data = [u_data], columns = ['Unit', 'Utilization'])
                                    util = util.append(udf, ignore_index=True)
                                    break
                                
    return obj_value, util
