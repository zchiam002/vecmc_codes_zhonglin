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
    
def chiller3_ret (ch3_r_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd 
    import numpy as np 
    
    ##Model description:
    ##This model represents the required return temperature demand from the chiller model 
    
    ##Legend of input variables 
    
    ##ch3_r_etret       - evaporator return temperature (K)
    
    ##Processing list of master decision variables as parameters 
    ch3_r_etret = ch3_r_mdv['Value'][0]

    ##Define dictionary of values 
    
    chiller3_ret = {}
    ##Input constants 
    
    ##1
    ch3_r_erettemp = {}
    ch3_r_erettemp['value'] = ch3_r_etret
    ch3_r_erettemp['units'] = 'K'
    ch3_r_erettemp['status'] = 'cst_input'
    chiller3_ret['ch3_r_erettemp'] = ch3_r_erettemp    

    ##Unit definition 
    
    ##Unit 1 
    ch3_ret = {}
    ch3_ret['Name'] = 'ch3_ret'
    ch3_ret['Fmin'] = 1
    ch3_ret['Fmax'] = 1
    ch3_ret['Cost1'] = 0
    ch3_ret['Cost2'] = 0
    ch3_ret['Cinv1'] = 0
    ch3_ret['Cinv2'] = 0
    ch3_ret['Power1'] = 0
    ch3_ret['Power2'] = 0
    ch3_ret['Impact1'] = 0
    ch3_ret['Impact2'] = 0

    unitinput = [ch3_ret['Name'], ch3_ret['Fmin'], ch3_ret['Fmax'], ch3_ret['Cost1'], ch3_ret['Cost2'], ch3_ret['Cinv1'], ch3_ret['Cinv2'], 
                 ch3_ret['Power1'], ch3_ret['Power2'], ch3_ret['Impact1'], ch3_ret['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    processlist = processlist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ch3_ret'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch3_tin'
    stream1['Layer'] = 'sp22ch3'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = chiller3_ret['ch3_r_erettemp']['value']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return processlist, streams, cons_eqns, cons_eqns_terms