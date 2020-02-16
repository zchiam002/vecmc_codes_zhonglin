## This is a chiller return model for temperature, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt

def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'process'
    return unit_type
    
def chiller2_ret (ch2_r_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd 
    import numpy as np 

    ##Model description:
    ##This model represents the required return temperature demand from the chiller model 
    
    ##Legend of input variables 
    
    ##ch2_r_etret       - evaporator return temperature (K)
    
    ##Processing list of master decision variables as parameters 
    ch2_r_etret = ch2_r_mdv['Value'][0]

    ##Define dictionary of values 
    
    chiller2_ret = {}
    ##Input constants 
    
    ##1
    ch2_r_erettemp = {}
    ch2_r_erettemp['value'] = ch2_r_etret
    ch2_r_erettemp['units'] = 'K'
    ch2_r_erettemp['status'] = 'cst_input'
    chiller2_ret['ch2_r_erettemp'] = ch2_r_erettemp    

    ##Unit definition 
    
    ##Unit 1
    ch2_ret = {}
    ch2_ret['Name'] = 'ch2_ret_evap'
    ch2_ret['Variable1'] = 'tevap_ret'                                                                                                     
    ch2_ret['Variable2'] = '-' 
    ch2_ret['Fmin_v1'] = 0 
    ch2_ret['Fmax_v1'] = chiller2_ret['ch2_r_erettemp']['value']                                                                                                                   
    ch2_ret['Fmin_v2'] = 0                                                                                                          
    ch2_ret['Fmax_v2'] = 0                                                                                   
    ch2_ret['Coeff_v1_2'] = 0                                                                                                                
    ch2_ret['Coeff_v1_1'] = 0          
    ch2_ret['Coeff_v2_2'] = 0
    ch2_ret['Coeff_v2_1'] = 0
    ch2_ret['Coeff_v1_v2'] = 0 
    ch2_ret['Coeff_cst'] = 0
    ch2_ret['Fmin'] = 0
    ch2_ret['Fmax'] = 0
    ch2_ret['Cost_v1_2'] = 0
    ch2_ret['Cost_v1_1'] = 0
    ch2_ret['Cost_v2_2'] = 0
    ch2_ret['Cost_v2_1'] = 0
    ch2_ret['Cost_v1_v2'] = 0
    ch2_ret['Cost_cst'] = 0
    ch2_ret['Cinv_v1_2'] = 0
    ch2_ret['Cinv_v1_1'] = 0
    ch2_ret['Cinv_v2_2'] = 0
    ch2_ret['Cinv_v2_1'] = 0
    ch2_ret['Cinv_v1_v2'] = 0
    ch2_ret['Cinv_cst'] = 0
    ch2_ret['Power_v1_2'] = 0
    ch2_ret['Power_v1_1'] = 0
    ch2_ret['Power_v2_2'] = 0
    ch2_ret['Power_v2_1'] = 0
    ch2_ret['Power_v1_v2'] = 0
    ch2_ret['Power_cst'] = 0
    ch2_ret['Impact_v1_2'] = 0
    ch2_ret['Impact_v1_1'] = 0
    ch2_ret['Impact_v2_2'] = 0
    ch2_ret['Impact_v2_1'] = 0
    ch2_ret['Impact_v1_v2'] = 0
    ch2_ret['Impact_cst'] = 0

    unitinput = [ch2_ret['Name'], ch2_ret['Variable1'], ch2_ret['Variable2'], ch2_ret['Fmin_v1'], ch2_ret['Fmax_v1'], ch2_ret['Fmin_v2'], ch2_ret['Fmax_v2'], ch2_ret['Coeff_v1_2'], 
                ch2_ret['Coeff_v1_1'], ch2_ret['Coeff_v2_2'], ch2_ret['Coeff_v2_1'], ch2_ret['Coeff_v1_v2'], ch2_ret['Coeff_cst'], ch2_ret['Fmin'], ch2_ret['Fmax'], ch2_ret['Cost_v1_2'], 
                ch2_ret['Cost_v1_1'], ch2_ret['Cost_v2_2'], ch2_ret['Cost_v2_1'], ch2_ret['Cost_v1_v2'], ch2_ret['Cost_cst'], ch2_ret['Cinv_v1_2'], ch2_ret['Cinv_v1_1'], ch2_ret['Cinv_v2_2'], 
                ch2_ret['Cinv_v2_1'], ch2_ret['Cinv_v1_v2'], ch2_ret['Cinv_cst'], ch2_ret['Power_v1_2'], ch2_ret['Power_v1_1'], ch2_ret['Power_v2_2'], ch2_ret['Power_v2_1'], 
                ch2_ret['Power_v1_v2'], ch2_ret['Power_cst'], ch2_ret['Impact_v1_2'], ch2_ret['Impact_v1_1'], ch2_ret['Impact_v2_2'], ch2_ret['Impact_v2_1'], ch2_ret['Impact_v1_v2'], 
                ch2_ret['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    processlist = processlist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    stream1 = {}                                                                
    stream1['Parent'] = 'ch2_ret_evap'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch2_ret_evap_tin'
    stream1['Layer'] = 'sp2_2_ch2ret_temp'
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