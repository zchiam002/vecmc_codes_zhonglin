##This function processes the output textfile from GLPK and extracts the relevant values 

def glpk_output_extractor_chiller_cond_bilin(output_file, var_list):
    import pandas as pd            
    
    dim_var_list = var_list.shape
    
    ##Extracting the objective function 
    with open(output_file) as fo:
        for rec in fo:
            if 'Objective:  obj' in rec:
                obj = rec.split(' ')
                break
        obj_value = float(obj[4])
    
    ##Creating a DataFrame to store the results 
    results = pd.DataFrame(columns = ['var_name', 'var_value'])
        
    ##Extracting the values of variables in the output file
    written_var = []                                                                ##To avoid writing already written variables 
    with open(output_file) as fo:
        for rec in fo:
            for i in range (0, dim_var_list[0]):
                checking = 0
                if var_list['var_name'][i] in rec:
                    if i not in written_var:
                        if len(var_list['var_name'][i]) <= 12:                      ##The var_name limit to which the value will be on the same line
                            u_all = rec.split(' ')
                            dim_u_all = len(u_all)
                            count = 0
                            for j in range (0, dim_u_all):
                                if u_all[j] != '':
                                    count = count + 1
                                    if count == 3:                                  ##This is where the value exists 
                                        u = u_all[j]
                                        u_data = [var_list['var_name'][i], float(u)]
                                        udf = pd.DataFrame(data = [u_data], columns = ['var_name', 'var_value'])
                                        results = results.append(udf, ignore_index=True)
                                        checking = 1
                                        written_var.append(i)
                                        break
                        else:                                                           ##The values will be on the next line 
                            u_all = next(fo).split(' ')
                            dim_u_all = len(u_all)
                            count = 0
                            for j in range (0, dim_u_all):
                                if u_all[j] != '':
                                    count = count + 1
                                    if '_y' not in var_list['var_name'][i]:
                                        if count == 1:                                      ##This is where the value should exist
                                            u = u_all[j]
                                            u_data = [var_list['var_name'][i], float(u)]
                                            udf = pd.DataFrame(data = [u_data], columns = ['var_name', 'var_value'])
                                            results = results.append(udf, ignore_index=True)
                                            checking = 1
                                            written_var.append(i)
                                            break
                                    else:
                                        if count == 2:                                      ##This is where the value should exist
                                            u = u_all[j]
                                            u_data = [var_list['var_name'][i], float(u)]
                                            udf = pd.DataFrame(data = [u_data], columns = ['var_name', 'var_value'])
                                            results = results.append(udf, ignore_index=True)
                                            checking = 1
                                            written_var.append(i)
                                            break
                    if checking != 0:
                        break
    return obj_value, results