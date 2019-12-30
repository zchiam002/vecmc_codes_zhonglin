## This is the water supply model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type


def water_supply (ws_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    #import numpy as np
    
    ##Model description:
    ##This is just a unit to supply water. Its utilization gives us an idea of how much water is used
    
    ##Legend of input variables 
    ##There are no required input variables 
    
    ##Processing list of master decision variables as parameters
    ##There are no required input variables from the master optimizer
    
    ##Define dictionary of values 
    
    water_sup = {}
    ##Input constants 
    
    ##1
    ws_max_cap = {}
    ws_max_cap['value'] = 100000
    ws_max_cap['units'] = 'm3/h'
    ws_max_cap['status'] = 'cst'
    water_sup['ws_max_cap'] = ws_max_cap
    
    ##Unit definition 
    ##Unit 1
    water_s = {}
    water_s['Name'] = 'water_supply'
    water_s['Fmin'] = 0
    water_s['Fmax'] = 1
    water_s['Cost1'] = 0
    water_s['Cost2'] = 0
    water_s['Cinv1'] = 0
    water_s['Cinv2'] = 0
    water_s['Power1'] = 0
    water_s['Power2'] = 0
    water_s['Impact1'] = 0
    water_s['Impact2'] = 0

    unitinput = [water_s['Name'], water_s['Fmin'], water_s['Fmax'], water_s['Cost1'], water_s['Cost2'], water_s['Cinv1'], water_s['Cinv2'], 
                 water_s['Power1'], water_s['Power2'], water_s['Impact1'], water_s['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)    
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'water_supply'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'water_supply_out'
    stream1['Layer'] = 'water_exchange'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = water_sup['ws_max_cap']['value']
    stream1['InOut'] = 'out'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms   
    