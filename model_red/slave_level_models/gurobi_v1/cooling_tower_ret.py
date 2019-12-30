## This is a cooling tower return model for temperature, formulated as an input to a quadratic program

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
    ##This model represents the required return temperature demand from the cooling tower model 
    
    ##Legend of input variables 
    
    ##ct_r_tret       - the required return temperature from the cooling tower model (K)
    
    ##Processing list of master decision variables as parameters 
    ct_r_tret = ct_r_mdv['Value'][0]

    ##Define dictionary of values 
    
    cooling_tower_ret = {}
    ##Input constants 
    
    ##1
    ct_r_rettemp = {}
    ct_r_rettemp['value'] = ct_r_tret
    ct_r_rettemp['units'] = 'K'
    ct_r_rettemp['status'] = 'cst_input'
    cooling_tower_ret['ct_r_rettemp'] = ct_r_rettemp   

    ##Unit definition 
    
    ##Unit 1
    ct_ret = {}
    ct_ret['Name'] = 'ct_ret'
    ct_ret['Variable1'] = 'tret'                                                                                                     
    ct_ret['Variable2'] = '-' 
    ct_ret['Fmin_v1'] = 0 
    ct_ret['Fmax_v1'] = cooling_tower_ret['ct_r_rettemp']['value']                                                                                                                   
    ct_ret['Fmin_v2'] = 0                                                                                                          
    ct_ret['Fmax_v2'] = 0                                                                                   
    ct_ret['Coeff_v1_2'] = 0                                                                                                                
    ct_ret['Coeff_v1_1'] = 0          
    ct_ret['Coeff_v2_2'] = 0
    ct_ret['Coeff_v2_1'] = 0
    ct_ret['Coeff_v1_v2'] = 0 
    ct_ret['Coeff_cst'] = 0
    ct_ret['Fmin'] = 0
    ct_ret['Fmax'] = 0
    ct_ret['Cost_v1_2'] = 0
    ct_ret['Cost_v1_1'] = 0
    ct_ret['Cost_v2_2'] = 0
    ct_ret['Cost_v2_1'] = 0
    ct_ret['Cost_v1_v2'] = 0
    ct_ret['Cost_cst'] = 0
    ct_ret['Cinv_v1_2'] = 0
    ct_ret['Cinv_v1_1'] = 0
    ct_ret['Cinv_v2_2'] = 0
    ct_ret['Cinv_v2_1'] = 0
    ct_ret['Cinv_v1_v2'] = 0
    ct_ret['Cinv_cst'] = 0
    ct_ret['Power_v1_2'] = 0
    ct_ret['Power_v1_1'] = 0
    ct_ret['Power_v2_2'] = 0
    ct_ret['Power_v2_1'] = 0
    ct_ret['Power_v1_v2'] = 0
    ct_ret['Power_cst'] = 0
    ct_ret['Impact_v1_2'] = 0
    ct_ret['Impact_v1_1'] = 0
    ct_ret['Impact_v2_2'] = 0
    ct_ret['Impact_v2_1'] = 0
    ct_ret['Impact_v1_v2'] = 0
    ct_ret['Impact_cst'] = 0

    unitinput = [ct_ret['Name'], ct_ret['Variable1'], ct_ret['Variable2'], ct_ret['Fmin_v1'], ct_ret['Fmax_v1'], ct_ret['Fmin_v2'], ct_ret['Fmax_v2'], ct_ret['Coeff_v1_2'], 
                ct_ret['Coeff_v1_1'], ct_ret['Coeff_v2_2'], ct_ret['Coeff_v2_1'], ct_ret['Coeff_v1_v2'], ct_ret['Coeff_cst'], ct_ret['Fmin'], ct_ret['Fmax'], ct_ret['Cost_v1_2'], 
                ct_ret['Cost_v1_1'], ct_ret['Cost_v2_2'], ct_ret['Cost_v2_1'], ct_ret['Cost_v1_v2'], ct_ret['Cost_cst'], ct_ret['Cinv_v1_2'], ct_ret['Cinv_v1_1'], ct_ret['Cinv_v2_2'], 
                ct_ret['Cinv_v2_1'], ct_ret['Cinv_v1_v2'], ct_ret['Cinv_cst'], ct_ret['Power_v1_2'], ct_ret['Power_v1_1'], ct_ret['Power_v2_2'], ct_ret['Power_v2_1'], 
                ct_ret['Power_v1_v2'], ct_ret['Power_cst'], ct_ret['Impact_v1_2'], ct_ret['Impact_v1_1'], ct_ret['Impact_v2_2'], ct_ret['Impact_v2_1'], ct_ret['Impact_v1_v2'], 
                ct_ret['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    processlist = processlist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    stream1 = {}                                                                
    stream1['Parent'] = 'ct_ret'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ct_ret_tin'
    stream1['Layer'] = 'ct_cond_ret_temp'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 1
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = 0
    stream1['Stream_coeff_v1_v2'] = 0
    stream1['Stream_coeff_cst'] = 0
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return processlist, streams, cons_eqns, cons_eqns_terms