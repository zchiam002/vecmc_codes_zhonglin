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
    ch2_ret['Name'] = 'ch2_ret'
    ch2_ret['Fmin'] = 1
    ch2_ret['Fmax'] = 1
    ch2_ret['Cost1'] = 0
    ch2_ret['Cost2'] = 0
    ch2_ret['Cinv1'] = 0
    ch2_ret['Cinv2'] = 0
    ch2_ret['Power1'] = 0
    ch2_ret['Power2'] = 0
    ch2_ret['Impact1'] = 0
    ch2_ret['Impact2'] = 0

    unitinput = [ch2_ret['Name'], ch2_ret['Fmin'], ch2_ret['Fmax'], ch2_ret['Cost1'], ch2_ret['Cost2'], ch2_ret['Cinv1'], ch2_ret['Cinv2'], 
                 ch2_ret['Power1'], ch2_ret['Power2'], ch2_ret['Impact1'], ch2_ret['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    processlist = processlist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ch2_ret'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch2_tin'
    stream1['Layer'] = 'sp22ch2'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = chiller2_ret['ch2_r_erettemp']['value']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return processlist, streams, cons_eqns, cons_eqns_terms