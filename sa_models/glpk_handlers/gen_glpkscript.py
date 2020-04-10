##This function creates the script for GLPK

def gen_glpkscript(layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms, obj_func):
    import pandas as pd
    
    ##The definition and data will be handled together

    temp_holding_dir = 'C:\\Optimization_zlc\\glpk_handlers\\input_output\\'
    
    data_name = 'data_set.txt'
    
    data_dir = temp_holding_dir + data_name                                 ##Data directory
    
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################    
    
    ##Problem definition section
    
    f_data_set = open(data_dir,'w')
    
#######################################################################################################################################
    
    ##Writing utilities and processes sets

    f_data_set.write('set UNIT_TYPES; \n')
    f_data_set.write('set UNITS_ALL; \n')
    f_data_set.write('set UNIT{h in UNIT_TYPES} within UNITS_ALL; \n')
    
    f_data_set.write('\n')
    
#######################################################################################################################################    

    ##Writing layers sets

    f_data_set.write('set LAYER_TYPES; \n')
    f_data_set.write('set LAYERS_ALL; \n')
    f_data_set.write('set LAYERS{h in LAYER_TYPES} within LAYERS_ALL; \n')
    f_data_set.write('set LAYERS_DIR_IN{h in LAYERS_ALL} within UNITS_ALL; \n')
    f_data_set.write('set LAYERS_DIR_OUT{h in LAYERS_ALL} within UNITS_ALL; \n')
    f_data_set.write('set LAYERS_DIR; \n')
    
    f_data_set.write('\n')
    
#######################################################################################################################################
    
    ##Writing additional constraints sets
    
    if cons_eqns.empty == False:
        f_data_set.write('set ADD_CONS_TYPE; \n')
        f_data_set.write('set ADD_CONS_SIGN; \n')
        f_data_set.write('set ADD_CONS_ALL; \n')  
        
        all_add_cons_sign = cons_eqns['Sign']
        all_add_cons_sign = set(all_add_cons_sign)
        all_add_cons_sign = list(set(all_add_cons_sign))
        
        seen = set()
        unique_add_cons_sign = []
        for add_cons_sign in all_add_cons_sign:
            if add_cons_sign not in seen:
                seen.add(add_cons_sign)
                unique_add_cons_sign.append(add_cons_sign)
        
        if 'less_than_equal_to' in unique_add_cons_sign:
            f_data_set.write('set ADD_CONS_LESS_THAN_EQUAL_TO{h in ADD_CONS_TYPE} within ADD_CONS_ALL; \n') 
        if 'greater_than_equal_to' in unique_add_cons_sign:
            f_data_set.write('set ADD_CONS_GREATER_THAN_EQUAL_TO{h in ADD_CONS_TYPE} within ADD_CONS_ALL; \n') 
        if 'equal_to' in unique_add_cons_sign:
            f_data_set.write('set ADD_CONS_EQUAL_TO{h in ADD_CONS_TYPE} within ADD_CONS_ALL; \n') 
        
        f_data_set.write('set ADD_TERMS_PARENT{h in ADD_CONS_TYPE} within UNITS_ALL; \n')
        f_data_set.write('set ADD_TERMS{h in ADD_CONS_ALL} within UNITS_ALL; \n')
        
        f_data_set.write('\n')  
        
#######################################################################################################################################

    ##Writing objective function sets
    
    f_data_set.write('set OBJ_FUNC_TYPES; \n')
    f_data_set.write('set OBJ_FUNC{h in OBJ_FUNC_TYPES} within UNITS_ALL; \n')

    f_data_set.write('\n')
    
#######################################################################################################################################
#######################################################################################################################################

    ##Writing parameters 
    
    f_data_set.write('##Parameter definition \n')
    f_data_set.write('\n')    
    
#######################################################################################################################################    

    ##Writing objective function parameters
    
    f_data_set.write('param fmin{h in UNITS_ALL}; \n')
    f_data_set.write('param fmax{h in UNITS_ALL}; \n')
    f_data_set.write('param obj1{g in OBJ_FUNC_TYPES, h in UNITS_ALL}; \n')
    f_data_set.write('param obj2{n in OBJ_FUNC_TYPES, i in UNITS_ALL}; \n')
    
    f_data_set.write('\n')

#######################################################################################################################################          

    ##Writing layers parameters 
    
    f_data_set.write('param layers_const{g in LAYER_TYPES, h in LAYERS_ALL, i in LAYERS_DIR, j in UNITS_ALL}; \n')
    f_data_set.write('param layers_grad{g in LAYER_TYPES, h in LAYERS_ALL, i in LAYERS_DIR, j in UNITS_ALL}; \n')
    
    f_data_set.write('\n')

#######################################################################################################################################
    
    ##Writing additional constraints parameters 

    if cons_eqns.empty == False:
                
        dim_cons_eqns = cons_eqns.shape                                             ##Ensuring there is no duplicate constraint type 
        all_add_cons_types = cons_eqns['Type']
        all_add_cons_types = set(all_add_cons_types)
        all_add_cons_types = list(set(all_add_cons_types))
        
        seen = set()
        unique_cons_eqns_types = []
        for add_cons_type in all_add_cons_types:
            if add_cons_type not in seen:
                seen.add(add_cons_type)
                unique_cons_eqns_types.append(add_cons_type)
        
        if 'stream_limit' in unique_cons_eqns_types:
            f_data_set.write('param add_terms_streams_const{h in ADD_CONS_LESS_THAN_EQUAL_TO[\'stream_limit\']}; \n')
            f_data_set.write('param add_terms_streams_grad{h in ADD_CONS_LESS_THAN_EQUAL_TO[\'stream_limit\']}; \n')
        
        f_data_set.write('\n')        
        
        if 'less_than_equal_to' in unique_add_cons_sign:
            if 'unit_binary' in unique_cons_eqns_types:
                f_data_set.write('param less_than_equal_to_unit_binary{h in ADD_CONS_LESS_THAN_EQUAL_TO[\'unit_binary\']}; \n')
                f_data_set.write('param less_than_equal_to_unit_binary_terms_coeff{h in ADD_TERMS_PARENT[\'unit_binary\']}; \n')
            if 'stream_limit' in unique_cons_eqns_types:
                f_data_set.write('param less_than_equal_to_stream_limit{h in ADD_CONS_LESS_THAN_EQUAL_TO[\'stream_limit\']}; \n')

        if 'greater_than_equal_to' in unique_add_cons_sign:
            if 'unit_binary' in unique_cons_eqns_types:
                f_data_set.write('param greater_than_equal_to_unit_binary{h in ADD_CONS_GREATER_THAN_EQUAL_TO[\'unit_binary\']}; \n')
                f_data_set.write('param greater_than_equal_to_unit_binary_terms_coeff{h in ADD_TERMS_PARENT[\'unit_binary\']}; \n')
            if 'stream_limit' in unique_cons_eqns_types:
                f_data_set.write('param greater_than_equal_to_stream_limit{h in ADD_CONS_GREATER_THAN_EQUAL_TO[\'stream_limit\']}; \n')
                
        if 'equal_to' in unique_add_cons_sign:
            if 'unit_binary' in unique_cons_eqns_types:
                f_data_set.write('param equal_to_unit_binary{h in ADD_CONS_EQUAL_TO[\'unit_binary\']}; \n')
                f_data_set.write('param equal_to_unit_binary_terms_coeff{h in ADD_TERMS_PARENT[\'unit_binary\']}; \n')
            if 'stream_limit' in unique_cons_eqns_types:
                f_data_set.write('param equal_to_stream_limit{h in ADD_CONS_EQUAL_TO[\'stream_limit\']}; \n')
        
        f_data_set.write('\n')
            
#######################################################################################################################################
#######################################################################################################################################
    
    ##Writing variables 
    
    f_data_set.write('##Variable definition \n')
    f_data_set.write('\n')
    
    f_data_set.write('var u_rate{h in UNITS_ALL}, >= 0, <= 1000; \n')
    f_data_set.write('var y_onoff{i in UNITS_ALL}, integer, >= 0, <= 1; \n')
    
    f_data_set.write('\n')
    
#######################################################################################################################################
#######################################################################################################################################

    ##Writing constraints 
    
    f_data_set.write('##Constraint definition \n')
    f_data_set.write('\n')
    
#######################################################################################################################################

    ##Writing variable constraints 
    
    f_data_set.write('s.t. y_onoff_proc{h in UNIT[\'process\']}: y_onoff[h] = 1; \n')
    f_data_set.write('s.t. u_lb_util{h in UNITS_ALL}: y_onoff[h]*fmin[h] - u_rate[h] <= 0; \n')
    f_data_set.write('s.t. u_ub_util{h in UNITS_ALL}: u_rate[h] - y_onoff[h]*fmax[h] <= 0; \n')
    f_data_set.write('\n')

#######################################################################################################################################

    ##Writing layers constraints 

    f_data_set.write('s.t. layer_balance{g in LAYER_TYPES, h in LAYERS[g]}: \n') 
    f_data_set.write('(sum{i in LAYERS_DIR_IN[h]} (layers_const[g,h,\'in\',i]*y_onoff[i] + layers_grad[g,h,\'in\',i]*u_rate[i])) -  \n')
    f_data_set.write('(sum{j in LAYERS_DIR_OUT[h]} (layers_const[g,h,\'out\',j]*y_onoff[j] + layers_grad[g,h,\'out\',j]*u_rate[j])) \n') 
    f_data_set.write('= 0; \n')        
    f_data_set.write('\n')
    
#######################################################################################################################################

    #Writing additional constraints 
    
    if cons_eqns.empty == False:
        
        if 'less_than_equal_to' in unique_add_cons_sign:
            if 'unit_binary' in unique_cons_eqns_types:
                f_data_set.write('s.t. add_cons_ltet_ub{g in ADD_CONS_LESS_THAN_EQUAL_TO[\'unit_binary\']}: \n')
                f_data_set.write('(sum{h in ADD_TERMS[g]} (y_onoff[h]*less_than_equal_to_unit_binary_terms_coeff[h])) -  \n')
                f_data_set.write('less_than_equal_to_unit_binary[g] <= 0; \n')
                f_data_set.write('\n')
            if 'stream_limit' in unique_cons_eqns_types:
                f_data_set.write('s.t. add_cons_ltet_sl{g in ADD_CONS_LESS_THAN_EQUAL_TO[\'stream_limit\'], h in ADD_TERMS[g]}: \n')
                f_data_set.write('add_terms_streams_const[g]*y_onoff[h] + add_terms_streams_grad[g]*u_rate[h] - \n')
                f_data_set.write('less_than_equal_to_stream_limit[g] <= 0; \n')
                f_data_set.write('\n')
                
        if 'greater_than_equal_to' in unique_add_cons_sign:
            if 'unit_binary' in unique_cons_eqns_types:
                f_data_set.write('s.t. add_cons_gtet_ub{g in ADD_CONS_GREATER_THAN_EQUAL_TO[\'unit_binary\']}: \n')
                f_data_set.write('(sum{h in ADD_TERMS[g]} (y_onoff[h]*greater_than_equal_to_unit_binary_terms_coeff[h])) -  \n')
                f_data_set.write('greater_than_equal_to_unit_binary[g] >= 0; \n')
                f_data_set.write('\n')
            if 'stream_limit' in unique_cons_eqns_types:
                f_data_set.write('s.t. add_cons_gtet_sl{g in ADD_CONS_GREATER_THAN_EQUAL_TO[\'stream_limit\'], h in ADD_TERMS[g]}: \n')
                f_data_set.write('add_terms_streams_const[g]*y_onoff[h] + add_terms_streams_grad[g]*u_rate[h] - \n')
                f_data_set.write('greater_than_equal_to_stream_limit[g] >= 0; \n')   
                f_data_set.write('\n')
                
        if 'equal_to' in unique_add_cons_sign:
            if 'unit_binary' in unique_cons_eqns_types:
                f_data_set.write('s.t. add_cons_et_ub{g in ADD_CONS_EQUAL_TO[\'unit_binary\']}: \n')
                f_data_set.write('(sum{h in ADD_TERMS[g]} (y_onoff[h]*equal_to_unit_binary_terms_coeff[h])) -  \n')
                f_data_set.write('equal_to_unit_binary[g] = 0; \n')
                f_data_set.write('\n')
            if 'stream_limit' in unique_cons_eqns_types:
                f_data_set.write('s.t. add_cons_et_sl{g in ADD_CONS_EQUAL_TO[\'stream_limit\'], h in ADD_TERMS[g]}: \n')
                f_data_set.write('add_terms_streams_const[g]*y_onoff[h] + add_terms_streams_grad[g]*u_rate[h] - \n')
                f_data_set.write('equal_to_stream_limit[g] = 0; \n')
                f_data_set.write('\n')            
       
#######################################################################################################################################
#######################################################################################################################################

    ##Writing objective function
    
    f_data_set.write('##Objective function definition \n') 
    f_data_set.write('\n')

    dim_obj_func = len(obj_func)
    
    name_obj_func = ''
    for i in range (0, dim_obj_func):
        name_obj_func = name_obj_func + obj_func[i]
        if i != dim_obj_func-1:
            name_obj_func = name_obj_func + '_'
    
    f_data_set.write('minimize ' + name_obj_func + ': \n')
    f_data_set.write('sum{g in OBJ_FUNC_TYPES, h in OBJ_FUNC[g]} (y_onoff[h]*obj1[g,h] + u_rate[h]*obj2[g,h]); \n')
    f_data_set.write('\n')
    
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################    
    
    ##Data section
     
    ##Writing the utilities and processes
    
    units = ''                                                                  ##Printing the utilities and processes
    units_u = ''
    units_p = ''
    unit_type = ''
    
    if utilitylist.empty == False: 
        dim_utilitylist = utilitylist.shape
        unit_type = unit_type + 'utility '
        
        for i in range (0, dim_utilitylist[0]):
            units = units + utilitylist['Name'][i] + ' '
            units_u = units_u + utilitylist['Name'][i] + ' '       

    if processlist.empty == False:
        dim_processlist = processlist.shape    
        unit_type = unit_type + 'process '
        
        for i in range (0, dim_processlist[0]):
            units = units + processlist['Name'][i] + ' '
            units_p = units_p + processlist['Name'][i] + ' '
        
    f_data_set.write('data ; \n')
    f_data_set.write('\n')
    f_data_set.write('set UNIT_TYPES := ' + unit_type + '; \n')
    f_data_set.write('set UNITS_ALL := ' + units + '; \n')
    f_data_set.write('\n')
    
    if utilitylist.empty == False: 
        f_data_set.write('set UNIT[utility] := ' + units_u + '; \n')
    if processlist.empty == False:
        f_data_set.write('set UNIT[process] := ' + units_p + '; \n')
    
#######################################################################################################################################    
    
    ##Writing the layers 

    layer_types = ''                                                            ##Printing the layers 
    
    dim_layerslist = layerslist.shape                                           ##Ensuring no duplicate layer type 
    all_type_instance = layerslist['Type']
    all_type_instance = set(all_type_instance)
    all_type_instance = list(set(all_type_instance))

    seen = set()
    unique_layer_types = []
    for layer in all_type_instance:
        if layer not in seen:
            seen.add(layer)
            unique_layer_types.append(layer)                                    ##unique_layer_types will now hold the list of unique layers
    
    dim_unique_layer_types = len(unique_layer_types)
    
    for i in range (0,dim_unique_layer_types):
        layer_types = layer_types +  unique_layer_types[i] + ' '

    f_data_set.write('set LAYER_TYPES := ' + layer_types + '; \n')
    
    layers = ''
    for i in range (0, dim_layerslist[0]):
        layers = layers + layerslist['Name'][i] + ' ' 
    
    f_data_set.write('set LAYERS_ALL := ' + layers + '; \n')
    
    if 'balancing_only' in unique_layer_types:
        balancing_only_layers = ''
        
        for i in range (0,dim_layerslist[0]):
            if layerslist['Type'][i] == 'balancing_only':
                balancing_only_layers = balancing_only_layers + layerslist['Name'][i] + ' ' 
    
        f_data_set.write('set LAYERS[balancing_only] := ' + balancing_only_layers + '; \n')
        
        f_data_set.write('\n')
    
    dim_streams = streams.shape
    for i in range (0,dim_layerslist[0]):
        units_in = ''
        units_out = ''
        for j in range (0,dim_streams[0]):
            if streams['Layer'][j] == layerslist['Name'][i]:
                if streams['InOut'][j] == 'out':
                    units_in = units_in + streams['Parent'][j] + ' '
                elif streams['InOut'][j] == 'in':
                    units_out = units_out + streams['Parent'][j] + ' '
        f_data_set.write('set LAYERS_DIR_IN[' + layerslist['Name'][i] + '] := ' + units_in + '; \n')
        f_data_set.write('set LAYERS_DIR_OUT[' + layerslist['Name'][i] + '] := ' + units_out + '; \n')
        
    f_data_set.write('\n')
    f_data_set.write('set LAYERS_DIR := in out; \n')
    f_data_set.write('\n')
    
#######################################################################################################################################    
    
    ##Writing the additional constraints 

    if cons_eqns.empty == False:
        
        add_cons_types = ''
        
        dim_unique_cons_eqns_types = len(unique_cons_eqns_types)
        
        for i in range (0, dim_unique_cons_eqns_types):
            add_cons_types = add_cons_types + unique_cons_eqns_types[i] + ' '
    
        f_data_set.write('set ADD_CONS_TYPE := ' + add_cons_types + '; \n')
        
        add_cons_signs = ''
        
        dim_unique_add_cons_sign = len(unique_add_cons_sign)
        
        for i in range (0, dim_unique_add_cons_sign):
            add_cons_signs = add_cons_signs + unique_add_cons_sign[i] + ' '
    
        f_data_set.write('set ADD_CONS_SIGN := ' + add_cons_signs + '; \n')
        
        add_cons_name = ''
        for i in range (0, dim_cons_eqns[0]):
            add_cons_name = add_cons_name + cons_eqns['Name'][i] + ' '
        
        f_data_set.write('set ADD_CONS_ALL := ' + add_cons_name + '; \n')
        f_data_set.write('\n')   
        
        if 'less_than_equal_to' in unique_add_cons_sign:
            for i in range (0, dim_unique_cons_eqns_types):
                add_cons_name_by_type = '' 
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Type'][j] == unique_cons_eqns_types[i]) and (cons_eqns['Sign'][j] == 'less_than_equal_to'):
                        add_cons_name_by_type = add_cons_name_by_type + cons_eqns['Name'][j] + ' '
                
                f_data_set.write('set ADD_CONS_LESS_THAN_EQUAL_TO[' + unique_cons_eqns_types[i] + '] := ' + add_cons_name_by_type + '; \n')   
        
        elif 'greater_than_equal_to' in unique_add_cons_sign: 
            for i in range (0, dim_unique_cons_eqns_types):
                add_cons_name_by_type = '' 
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Type'][j] == unique_cons_eqns_types[i]) and (cons_eqns['Sign'][j] == 'greater_than_equal_to'):
                        add_cons_name_by_type = add_cons_name_by_type + cons_eqns['Name'][j] + ' '
                
                f_data_set.write('set ADD_CONS_GREATER_THAN_EQUAL_TO[' + unique_cons_eqns_types[i] + '] := ' + add_cons_name_by_type + '; \n')
        
        elif 'equal_to' in unique_add_cons_sign: 
            for i in range (0, dim_unique_cons_eqns_types):
                add_cons_name_by_type = '' 
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Type'][j] == unique_cons_eqns_types[i]) and (cons_eqns['Sign'][j] == 'equal_to'):
                        add_cons_name_by_type = add_cons_name_by_type + cons_eqns['Name'][j] + ' '
                
                f_data_set.write('set ADD_CONS_EQUAL_TO[' + unique_cons_eqns_types[i] + '] := ' + add_cons_name_by_type + '; \n')
                            
        f_data_set.write('\n')
        
        dim_cons_eqns_terms = cons_eqns_terms.shape                                 ##Unique list of parent_units 
        pu_pe_et_rs = pd.DataFrame(columns = ['Parent_unit', 'Parent_eqn', 'Type'])
    
        for i in range (0, dim_cons_eqns_terms[0]):
            pu = cons_eqns_terms['Parent_unit'][i]
            pe = cons_eqns_terms['Parent_eqn'][i]
            for j in range (0,  dim_cons_eqns_terms[0]):
                if cons_eqns_terms['Parent_eqn'][i] == cons_eqns['Name'][j]:
                    et = cons_eqns['Type'][j]
                    break
            temp_ph = [pu, pe, et]
            temp_df = pd.DataFrame(data = [temp_ph], columns = ['Parent_unit', 'Parent_eqn', 'Type'])
            pu_pe_et_rs = pu_pe_et_rs.append(temp_df, ignore_index=True) 
        
        dim_pu_pe_et_rs = pu_pe_et_rs.shape
        
        temp_dict = {}
    
        for i in range (0, dim_unique_cons_eqns_types):
            temp_h = []
            for j in range (0, dim_pu_pe_et_rs[0]):
                if pu_pe_et_rs['Type'][j] == unique_cons_eqns_types[i]:
                    temp_h.append(pu_pe_et_rs['Parent_unit'][j])
            temp_dict[unique_cons_eqns_types[i]] = temp_h
    
        for i in range (0, dim_unique_cons_eqns_types):
            et_pu = temp_dict[unique_cons_eqns_types[i]]
            et_pu = set(et_pu)
            et_pu = list(set(et_pu))
            
            seen = set()
            unique_et_pu = []
            for that_et_pu in et_pu:
                if that_et_pu not in seen:
                    seen.add(that_et_pu)
                    unique_et_pu.append(that_et_pu)
            
            dim_unique_et_pu = len(unique_et_pu)
            
            u_et_pu = ''
            for j in range (0, dim_unique_et_pu):
                u_et_pu = u_et_pu + unique_et_pu[j] + ' '
                
            f_data_set.write('set ADD_TERMS_PARENT[' + unique_cons_eqns_types[i] + '] := ' + u_et_pu + '; \n')
        
        for i in range (0, dim_cons_eqns[0]):
            pu_in_eqn = ''
            for j in range (0, dim_cons_eqns_terms[0]):
                if cons_eqns_terms['Parent_eqn'][j] == cons_eqns['Name'][i]:
                    pu_in_eqn = pu_in_eqn + cons_eqns_terms['Parent_unit'][j] + ' '
            
            f_data_set.write('set ADD_TERMS[' + cons_eqns['Name'][i] + '] := ' + pu_in_eqn + '; \n')
        
        f_data_set.write('\n')
        
#######################################################################################################################################
    
    ##Writing the objective function 
    
    all_obj_func = ''
    for i in range (0, dim_obj_func):
        all_obj_func = all_obj_func + obj_func[i] + ' '
    
    f_data_set.write('set OBJ_FUNC_TYPES := ' + all_obj_func + '; \n')
    
    for i in range (0, dim_obj_func):
        f_data_set.write('set OBJ_FUNC[' + obj_func[i] + '] := ' + units + '; \n')
    
    f_data_set.write('\n')
#######################################################################################################################################
#######################################################################################################################################    
    
    ##Writing the parameters 

#######################################################################################################################################

    ##writing objective function parameters
    
    fmin = ''
    fmax = ''
    for i in range (0, dim_utilitylist[0]):
        fmin = fmin + utilitylist['Name'][i] + ' ' + str(utilitylist['Fmin'][i]) + '\n'
        fmax = fmax + utilitylist['Name'][i] + ' ' + str(utilitylist['Fmax'][i]) + '\n'
    for i in range (0, dim_processlist[0]):
        fmin = fmin + processlist['Name'][i] + ' ' + str(processlist['Fmin'][i]) + '\n'
        fmax = fmax + processlist['Name'][i] + ' ' + str(processlist['Fmax'][i]) + '\n'        
    
    obj1 = {}
    obj2 = {}

    for i in range (0, dim_obj_func):
        obj1[obj_func[i]] = ''
        obj2[obj_func[i]] = ''
        
        for j in range (0, dim_utilitylist[0]):
            if obj_func[i] == 'investment_cost':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Cost1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Cost2'][j]) + ' \n'
            elif obj_func[i] == 'operation_cost':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Cinv1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Cinv2'][j]) + ' \n'
            elif obj_func[i] == 'power':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Power1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Power2'][j]) + ' \n'
            elif obj_func[i] == 'impact':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Impact1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + utilitylist['Name'][j] + ' ' + str(utilitylist['Impact2'][j]) + ' \n'
        
        for j in range (0, dim_processlist[0]):
            if obj_func[i] == 'investment_cost':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Cost1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Cost2'][j]) + ' \n'
            elif obj_func[i] == 'operation_cost':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Cinv1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Cinv2'][j]) + ' \n'
            elif obj_func[i] == 'power':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Power1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Power2'][j]) + ' \n'
            elif obj_func[i] == 'impact':
                obj1[obj_func[i]] = obj1[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Impact1'][j]) + ' \n'
                obj2[obj_func[i]] = obj2[obj_func[i]] + obj_func[i] + ' ' + processlist['Name'][j] + ' ' + str(processlist['Impact2'][j]) + ' \n'            
            
    f_data_set.write('param fmin := \n' + fmin + '; \n')
    f_data_set.write('\n')
    f_data_set.write('param fmax := \n' + fmax + '; \n')
    f_data_set.write('\n')
    
    obj1_param = ''
    obj2_param = ''
    for i in range (0, dim_obj_func):
        obj1_param = obj1_param + obj1[obj_func[i]]
        obj2_param = obj2_param + obj2[obj_func[i]]
        
    f_data_set.write('param obj1 := \n' + obj1_param + '; \n')
    f_data_set.write('\n')
    f_data_set.write('param obj2 := \n' + obj2_param + '; \n')
    f_data_set.write('\n')        

#######################################################################################################################################

    ##Writing layers parameters 
    
    layers_const = ''
    layers_grad = ''
    
    for i in range (0, dim_streams[0]):
        if streams['InOut'][i] == 'out':
            layers_const = layers_const + streams['Type'][i] + ' ' + streams['Layer'][i] + ' ' + 'in' + ' ' + streams['Parent'][i] + ' ' + str(streams['Flow_min'][i]) + '\n'
            layers_grad = layers_grad + streams['Type'][i] + ' ' + streams['Layer'][i] + ' ' + 'in' + ' ' + streams['Parent'][i] + ' ' + str(streams['Flow_grad'][i]) + '\n'
    for i in range (0, dim_streams[0]):
        if streams['InOut'][i] == 'in':
            layers_const = layers_const + streams['Type'][i] + ' ' + streams['Layer'][i] + ' ' + 'out' + ' ' + streams['Parent'][i] + ' ' + str(streams['Flow_min'][i]) + '\n'
            layers_grad = layers_grad + streams['Type'][i] + ' ' + streams['Layer'][i] + ' ' + 'out' + ' ' + streams['Parent'][i] + ' ' + str(streams['Flow_grad'][i]) + '\n'

    f_data_set.write('param layers_const := \n' + layers_const + '; \n')
    f_data_set.write('\n')
    f_data_set.write('param layers_grad := \n' + layers_grad + '; \n')
    f_data_set.write('\n')    

#######################################################################################################################################

    ##Writing additional constraints parameters 
    
    if 'unit_binary' in unique_cons_eqns_types:
        for i in range (0, dim_unique_add_cons_sign):
            
            if unique_add_cons_sign[i] == 'less_than_equal_to':
                
                ub_ltet_rhs = ''
                ub_pe_list = []
                
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Sign'][j] == 'less_than_equal_to') and (cons_eqns['Type'][j] == 'unit_binary'):
                        ub_ltet_rhs = ub_ltet_rhs + cons_eqns['Name'][j] + ' ' + str(cons_eqns['RHS_value'][j]) + '\n'
                        ub_pe_list.append(cons_eqns['Name'][j])
                ub_ltet_terms_coeff = ''
                for j in range (0, dim_cons_eqns_terms[0]):
                    if cons_eqns_terms['Parent_eqn'][j] in ub_pe_list:
                        ub_ltet_terms_coeff = ub_ltet_terms_coeff + cons_eqns_terms['Parent_unit'][j] + ' ' + str(cons_eqns_terms['Coefficient'][j]) + '\n'
        
                f_data_set.write('param less_than_equal_to_unit_binary := \n')
                f_data_set.write(ub_ltet_rhs + ';')
                f_data_set.write('\n \n')
                f_data_set.write('param less_than_equal_to_unit_binary_terms_coeff := \n')
                f_data_set.write(ub_ltet_terms_coeff + ';')
                f_data_set.write('\n \n')
            
            elif unique_add_cons_sign[i] == 'greater_than_equal_to':
                
                ub_gtet_rhs = ''
                ub_pe_list = []
                
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Sign'][j] == 'greater_than_equal_to') and (cons_eqns['Type'][j] == 'unit_binary'):
                        ub_gtet_rhs = ub_gtet_rhs + cons_eqns['Name'][j] + ' ' + str(cons_eqns['RHS_value'][j]) + '\n'
                        ub_pe_list.append(cons_eqns['Name'][j])
                ub_gtet_terms_coeff = ''
                for j in range (0, dim_cons_eqns_terms[0]):
                    if cons_eqns_terms['Parent_eqn'][j] in ub_pe_list:
                        ub_gtet_terms_coeff = ub_gtet_terms_coeff + cons_eqns_terms['Parent_unit'][j] + ' ' + str(cons_eqns_terms['Coefficient'][j]) + '\n'
        
                f_data_set.write('param greater_than_equal_to_unit_binary := \n')
                f_data_set.write(ub_gtet_rhs + ';')
                f_data_set.write('\n \n')
                f_data_set.write('param greater_than_equal_to_unit_binary_terms_coeff := \n')
                f_data_set.write(ub_gtet_terms_coeff + ';')
                f_data_set.write('\n \n')
            
            elif unique_add_cons_sign[i] == 'equal_to':
              
                ub_et_rhs = ''
                ub_pe_list = []
                
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Sign'][j] == 'equal_to') and (cons_eqns['Type'][j] == 'unit_binary'):
                        ub_et_rhs = ub_et_rhs + cons_eqns['Name'][j] + ' ' + str(cons_eqns['RHS_value'][j]) + '\n'
                        ub_pe_list.append(cons_eqns['Name'][j])
                ub_et_terms_coeff = ''
                for j in range (0, dim_cons_eqns_terms[0]):
                    if cons_eqns_terms['Parent_eqn'][j] in ub_pe_list:
                        ub_et_terms_coeff = ub_et_terms_coeff + cons_eqns_terms['Parent_unit'][j] + ' ' + str(cons_eqns_terms['Coefficient'][j]) + '\n'
        
                f_data_set.write('param equal_to_unit_binary := \n')
                f_data_set.write(ub_et_rhs + ';')
                f_data_set.write('\n \n')
                f_data_set.write('param equal_to_unit_binary_terms_coeff := \n')
                f_data_set.write(ub_et_terms_coeff + ';')
                f_data_set.write('\n \n')
                
    if 'stream_limit' in unique_cons_eqns_types:
        
        sl_cons_eqns = []
        for i in range (0, dim_cons_eqns[0]):
            if cons_eqns['Type'][i] == 'stream_limit':
                sl_cons_eqns.append(cons_eqns['Name'][i])
        
        sl_corres_ps = []
        for i in range (0, dim_cons_eqns_terms[0]):
            if cons_eqns_terms['Parent_eqn'][i] in sl_cons_eqns:
                sl_corres_ps.append(cons_eqns_terms['Parent_stream'][i])
        
        add_terms_streams_const = ''
        add_terms_streams_grad = ''
        dim_sl_corres_ps = len(sl_corres_ps)
        for i in range (0, dim_sl_corres_ps):
            for j in range (0, dim_streams[0]):
                if streams['Name'][j] == sl_corres_ps[i]:
                    add_terms_streams_const = add_terms_streams_const + sl_cons_eqns[i] + ' ' + str(streams['Flow_min'][j]) + '\n'
                    add_terms_streams_grad = add_terms_streams_grad + sl_cons_eqns[i] + ' ' + str(streams['Flow_grad'][j]) + '\n'
        
        f_data_set.write('param add_terms_streams_const := \n')
        f_data_set.write(add_terms_streams_const + ';')
        f_data_set.write('\n \n')             
        f_data_set.write('param add_terms_streams_grad := \n')
        f_data_set.write(add_terms_streams_grad + ';')        
        f_data_set.write('\n \n')           
        
        for i in range (0, dim_unique_add_cons_sign):
            
            if unique_add_cons_sign[i] == 'less_than_equal_to':
                ltet_sl = ''
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Name'][j] in sl_cons_eqns) and (cons_eqns['Sign'][j] == 'less_than_equal_to'):
                        ltet_sl = ltet_sl + cons_eqns['Name'][j] + ' ' + str(cons_eqns['RHS_value'][j]) + '\n'
            
                f_data_set.write('param less_than_equal_to_stream_limit := \n')
                f_data_set.write(ltet_sl + ';')
                f_data_set.write('\n \n')
                
            elif unique_add_cons_sign[i] == 'greater_than_equal_to':
                gtet_sl = ''
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Name'][j] in sl_cons_eqns) and (cons_eqns['Sign'][j] == 'greater_than_equal_to'):
                        gtet_sl = gtet_sl + cons_eqns['Name'][j] + ' ' + str(cons_eqns['RHS_value'][j]) + '\n'
            
                f_data_set.write('param greater_than_equal_to_stream_limit := \n')
                f_data_set.write(gtet_sl + ';')
                f_data_set.write('\n \n')       
                
            elif unique_add_cons_sign[i] == 'equal_to':
                et_sl = ''
                for j in range (0, dim_cons_eqns[0]):
                    if (cons_eqns['Name'][j] in sl_cons_eqns) and (cons_eqns['Sign'][j] == 'equal_to'):
                        et_sl = et_sl + cons_eqns['Name'][j] + ' ' + str(cons_eqns['RHS_value'][j]) + '\n'
            
                f_data_set.write('param equal_to_stream_limit := \n')
                f_data_set.write(et_sl + ';')
                f_data_set.write('\n \n')   

#######################################################################################################################################

    f_data_set.write('end; \n') 
    f_data_set.close
    
#######################################################################################################################################
    return 

    
    
    
    
