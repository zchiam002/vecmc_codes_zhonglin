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

def splitter1 (sp1_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    
    #Model description 
    ##This model copies the inlet stream and duplicates it to the required number of outlet streams 
    
    ##Unit definition
    
    ##Unit 1
    sp1 = {}
    sp1['Name'] = 'sp1'
    sp1['Fmin'] = 0
    sp1['Fmax'] = 1
    sp1['Cost1'] = 0
    sp1['Cost2'] = 0
    sp1['Cinv1'] = 0
    sp1['Cinv2'] = 0
    sp1['Power1'] = 0
    sp1['Power2'] = 0
    sp1['Impact1'] = 0
    sp1['Impact2'] = 0

    unitinput = [sp1['Name'], sp1['Fmin'], sp1['Fmax'], sp1['Cost1'], sp1['Cost2'], sp1['Cinv1'], sp1['Cinv2'], 
                 sp1['Power1'], sp1['Power2'], sp1['Impact1'], sp1['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'sp1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'chil2sp1_tin'
    stream1['Layer'] = 'chil2sp1'
    stream1['Min_Flow'] = 0
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'sp1'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'sp12cp_tout'
    stream2['Layer'] = 'sp12cp'
    stream2['Min_Flow'] = 0
    stream2['Grad_Flow'] = 1000 - stream2['Min_Flow']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 3
    stream3 = {}
    stream3['Unit_Name'] = 'sp1'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'sp12gv2_tout'
    stream3['Layer'] = 'sp12gv2'
    stream3['Min_Flow'] = 0
    stream3['Grad_Flow'] = 1000 - stream3['Min_Flow']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Unit_Name'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Min_Flow'], stream3['Grad_Flow'], 
                   stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 4
    stream4 = {}
    stream4['Unit_Name'] = 'sp1'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'sp12hsb_tout'
    stream4['Layer'] = 'sp12hsb'
    stream4['Min_Flow'] = 0
    stream4['Grad_Flow'] = 1000 - stream4['Min_Flow']
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Unit_Name'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Min_Flow'], stream4['Grad_Flow'], 
                   stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 5
    stream5 = {}
    stream5['Unit_Name'] = 'sp1'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'sp12pfa_tout'
    stream5['Layer'] = 'sp12pfa'
    stream5['Min_Flow'] = 0
    stream5['Grad_Flow'] = 1000 - stream5['Min_Flow']
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Unit_Name'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Min_Flow'], stream5['Grad_Flow'], 
                   stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 6
    stream6 = {}
    stream6['Unit_Name'] = 'sp1'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'sp12ser_tout'
    stream6['Layer'] = 'sp12ser'
    stream6['Min_Flow'] = 0
    stream6['Grad_Flow'] = 1000 - stream6['Min_Flow']
    stream6['InOut'] = 'out'
    
    streaminput = [stream6['Unit_Name'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Min_Flow'], stream6['Grad_Flow'], 
                   stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 7
    stream7 = {}
    stream7['Unit_Name'] = 'sp1'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'sp12fir_tout'
    stream7['Layer'] = 'sp12fir'
    stream7['Min_Flow'] = 0
    stream7['Grad_Flow'] = 1000 - stream7['Min_Flow']
    stream7['InOut'] = 'out'
    
    streaminput = [stream7['Unit_Name'], stream7['Type'], stream7['Name'], stream7['Layer'], stream7['Min_Flow'], stream7['Grad_Flow'], 
                   stream7['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
