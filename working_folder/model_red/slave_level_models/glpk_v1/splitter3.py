##This is the temperature aggregator for and stream splitter model for chiller condensers and cooling towers

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'process'
    return unit_type
    
def splitter3 (sp3_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    ##Model description 
    ##This model aggregates the inlet stream and duplicates it to the required number of outlet streams 
    
    ##Legend of input variables 
    
    ##req_ct_tin        - the required inlet temperature for the cooling tower
    
    ##Processing list of master decision variables as parameters 
    req_ct_tin = sp3_mdv['Value'][0]
    
    ##Define dictionary of values 
    
    splitter3 = {}
    ##Input constants 
    
    ##1
    sp3_req_tin = {}
    sp3_req_tin['value'] = req_ct_tin
    sp3_req_tin['units'] = 'K'
    sp3_req_tin['status'] = 'cst_input'
    splitter3['sp3_req_tin'] = sp3_req_tin    
    
    ##Unit definition 
    
    #Unit 1
    sp3 = {}
    sp3['Name'] = 'sp3'
    sp3['Fmin'] = 1                                                             ##It is a process, hence the utilization needs to be always at 100%
    sp3['Fmax'] = 1
    sp3['Cost1'] = 0
    sp3['Cost2'] = 0
    sp3['Cinv1'] = 0
    sp3['Cinv2'] = 0
    sp3['Power1'] = 0
    sp3['Power2'] = 0
    sp3['Impact1'] = 0
    sp3['Impact2'] = 0

    unitinput = [sp3['Name'], sp3['Fmin'], sp3['Fmax'], sp3['Cost1'], sp3['Cost2'], sp3['Cinv1'], sp3['Cinv2'], 
                 sp3['Power1'], sp3['Power2'], sp3['Impact1'], sp3['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    processlist = processlist.append(unitdf, ignore_index=True)    
    
    ##Layer and stream definition
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'sp3'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'chilcond2sp3_tin'
    stream1['Layer'] = 'chilcond2sp3'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = splitter3['sp3_req_tin']['value'] - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)  
    
    return processlist, streams, cons_eqns, cons_eqns_terms  