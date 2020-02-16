##This is the script for setting up the multi-objective optimization 
def MOOSetUp ():
    
    import pandas as pd
    from nsga_2 import nsga_2

    allm_var = pd.DataFrame(columns = ['Name', 'Value', 'Unit', 'LB', 'UB', 'Type'])
    
    activate_parallel = 'no'
    obj_func_plot = 'yes'
    num_cores = 4
    ##Crossover pool percentage (size of the parent_pool) (best to keep above 0.2 and less than 0.6)
    crossover_perc = 0.3
    
    ##Mutation percentage (variation, not corrpution, best to keep between 0.05 and 0.1)
    mutation_perc = 0.1

    v1 = ['x1','continuous',-100,100,3,'-']
    v2 = ['x2','continuous',-100,100,3,'-']
    
    t11 = pd.DataFrame(data = [v1],columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec', 'Steps'])
    t12 = pd.DataFrame(data = [v2],columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec', 'Steps'])

    allm_var = allm_var.append(t11,ignore_index = True)
    allm_var = allm_var.append(t12,ignore_index = True)
    
    input_v = {}
    
    ##These are parameters for the genetic algorithm to work
    dim_allm_var = [2]
    
    input_v['population'] = 100
    input_v['generations'] = 50
    input_v['number_of_objectives'] = 2
    input_v['number_of_decision_variables'] = dim_allm_var[0]

    ##List of objective functions values 
    
    obj_v = pd.DataFrame(columns = ['Value'])
    
    ##1
    add_obj_v = {}
    add_obj_v['Value'] = 0
    
    input_add_obj_v = [add_obj_v['Value']]
    input_add_obj_vdf = pd.DataFrame(data = [input_add_obj_v], columns = ['Value'])
    obj_v = obj_v.append(input_add_obj_vdf, ignore_index=True)
    
    ##2
    add_obj_v = {}
    add_obj_v['Value'] = 0
    
    input_add_obj_v = [add_obj_v['Value']]
    input_add_obj_vdf = pd.DataFrame(data = [input_add_obj_v], columns = ['Value'])
    obj_v = obj_v.append(input_add_obj_vdf, ignore_index=True)
    
    input_v['obj_func_values'] = obj_v
    
    ##List of decision variables and their respective ranges 
    
    dv = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec', 'Steps'])
    
    for i in range (0,dim_allm_var[0]):
        add_dv = {}
        add_dv['Name'] = allm_var['Name'][i]
        add_dv['Type'] = allm_var['Type'][i]
        add_dv['Lower_bound'] = allm_var['Lower_bound'][i]
        add_dv['Upper_bound'] = allm_var['Upper_bound'][i]
        add_dv['Bin_dec_prec'] = allm_var['Bin_dec_prec'][i]
        add_dv['Steps'] = allm_var['Steps'][i]

        input_add_dv = [add_dv['Name'], add_dv['Type'], add_dv['Lower_bound'], add_dv['Upper_bound'], add_dv['Bin_dec_prec'], add_dv['Steps']]
        input_add_dvdf = pd.DataFrame(data = [input_add_dv], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec', 'Steps'])
        dv = dv.append(input_add_dvdf, ignore_index=True)
    
    input_v['range_of_decision_variables'] = dv
    
    ##Input the data into NSGA=II
    
    nsga_2(input_v,activate_parallel,num_cores,crossover_perc,mutation_perc,obj_func_plot)
    
    return
    
#####################################################################################################################################################
if __name__ == '__main__':
    import timing
    MOOSetUp ()