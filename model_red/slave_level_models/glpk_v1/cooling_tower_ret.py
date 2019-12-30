## This is the chiller return model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt

def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'process'
    return unit_type
    
def cooling_tower_ret (ct_r_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd 
    import numpy as np 

    ##Model description:
    ##This model represents the required return temperature demand from the cooling tower models
    
    ##Legend of input variables 
    
    ##ct_r_etret       - cooling tower return (K)
    
    ##Processing list of master decision variables as parameters 
    ct_ret_t = ct_r_mdv['Value'][0]

    ##Define dictionary of values 
    
    cooling_tower_ret = {} 
    ##Input constants 
    
    ##1
    ct_ret_temp = {}
    ct_ret_temp['value'] = ct_ret_t
    ct_ret_temp['units'] = 'K'
    ct_ret_temp['status'] = 'cst_input'
    cooling_tower_ret['ct_ret_temp'] = ct_ret_temp 

    ##Unit definition 
    
    ##Unit 1 
    ct_ret = {}
    ct_ret['Name'] = 'ct_ret'
    ct_ret['Fmin'] = 1
    ct_ret['Fmax'] = 1
    ct_ret['Cost1'] = 0
    ct_ret['Cost2'] = 0
    ct_ret['Cinv1'] = 0
    ct_ret['Cinv2'] = 0
    ct_ret['Power1'] = 0
    ct_ret['Power2'] = 0
    ct_ret['Impact1'] = 0
    ct_ret['Impact2'] = 0

    unitinput = [ct_ret['Name'], ct_ret['Fmin'], ct_ret['Fmax'], ct_ret['Cost1'], ct_ret['Cost2'], ct_ret['Cinv1'], ct_ret['Cinv2'], 
                 ct_ret['Power1'], ct_ret['Power2'], ct_ret['Impact1'], ct_ret['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    processlist = processlist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ct_ret'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ct_tout'
    stream1['Layer'] = 'ct2chilcond_ret'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = cooling_tower_ret['ct_ret_temp']['value']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return processlist, streams, cons_eqns, cons_eqns_terms