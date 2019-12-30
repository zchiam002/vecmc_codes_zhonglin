##This is the temperature aggregator and stream splitter model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def splitter2 (sp2_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    #Model description 
    ##This model copies the inlet stream and duplicates it to the required number of outlet streams 
    
    ##Unit definition
    
    ##Unit 1
    sp2 = {}
    sp2['Name'] = 'sp2'
    sp2['Fmin'] = 0
    sp2['Fmax'] = 1
    sp2['Cost1'] = 0
    sp2['Cost2'] = 0
    sp2['Cinv1'] = 0
    sp2['Cinv2'] = 0
    sp2['Power1'] = 0
    sp2['Power2'] = 0
    sp2['Impact1'] = 0
    sp2['Impact2'] = 0

    unitinput = [sp2['Name'], sp2['Fmin'], sp2['Fmax'], sp2['Cost1'], sp2['Cost2'], sp2['Cinv1'], sp2['Cinv2'], 
                 sp2['Power1'], sp2['Power2'], sp2['Impact1'], sp2['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'sp2'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ss2sp2_tin'
    stream1['Layer'] = 'ss2sp2'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'sp2'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'sp22ch1_tout'
    stream2['Layer'] = 'sp22ch1'
    stream2['Min_Flow'] = 0
    stream2['Grad_Flow'] = 1000 - stream2['Min_Flow']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 3
    stream3 = {}
    stream3['Unit_Name'] = 'sp2'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'sp22ch2_tout'
    stream3['Layer'] = 'sp22ch2'
    stream3['Min_Flow'] = 0
    stream3['Grad_Flow'] = 1000 - stream3['Min_Flow']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Unit_Name'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Min_Flow'], stream3['Grad_Flow'], 
                   stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 4
    stream4 = {}
    stream4['Unit_Name'] = 'sp2'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'sp22ch3_tout'
    stream4['Layer'] = 'sp22ch3'
    stream4['Min_Flow'] = 0
    stream4['Grad_Flow'] = 1000 - stream4['Min_Flow']
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Unit_Name'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Min_Flow'], stream4['Grad_Flow'], 
                   stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms

