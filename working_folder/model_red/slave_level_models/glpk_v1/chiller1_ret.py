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
    
def chiller1_ret (ch1_r_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd 
    import numpy as np 

    ##Model description:
    ##This model represents the required return temperature demand from the chiller model 
    
    ##Legend of input variables 
    
    ##ch1_r_etret       - evaporator return temperature (K)
    
    ##Processing list of master decision variables as parameters 
    ch1_r_etret = ch1_r_mdv['Value'][0]

    ##Define dictionary of values 
    
    chiller1_ret = {}
    ##Input constants 
    
    ##1
    ch1_r_erettemp = {}
    ch1_r_erettemp['value'] = ch1_r_etret
    ch1_r_erettemp['units'] = 'K'
    ch1_r_erettemp['status'] = 'cst_input'
    chiller1_ret['ch1_r_erettemp'] = ch1_r_erettemp    

    ##Unit definition 
    
    ##Unit 1 
    ch1_ret = {}
    ch1_ret['Name'] = 'ch1_ret'
    ch1_ret['Fmin'] = 1
    ch1_ret['Fmax'] = 1
    ch1_ret['Cost1'] = 0
    ch1_ret['Cost2'] = 0
    ch1_ret['Cinv1'] = 0
    ch1_ret['Cinv2'] = 0
    ch1_ret['Power1'] = 0
    ch1_ret['Power2'] = 0
    ch1_ret['Impact1'] = 0
    ch1_ret['Impact2'] = 0

    unitinput = [ch1_ret['Name'], ch1_ret['Fmin'], ch1_ret['Fmax'], ch1_ret['Cost1'], ch1_ret['Cost2'], ch1_ret['Cinv1'], ch1_ret['Cinv2'], 
                 ch1_ret['Power1'], ch1_ret['Power2'], ch1_ret['Impact1'], ch1_ret['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    processlist = processlist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ch1_ret'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch1_tin'
    stream1['Layer'] = 'sp22ch1'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = chiller1_ret['ch1_r_erettemp']['value']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return processlist, streams, cons_eqns, cons_eqns_terms