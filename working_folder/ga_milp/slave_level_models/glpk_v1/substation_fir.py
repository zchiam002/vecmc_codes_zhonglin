##This is a substation model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def substation_fir (ssfir_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    from substation_fir_compute import substation_fir_compute
    
    ##Model description:
    ##This model ensures that a predefined demand is met 
    ##This is an intermediate model, hence utilization does not have any meaning 
    
    ##Legend of input variables 
    
    ##ssfir_inflow          - the flowrate through the system (m3/h)
    ##ssfir_tnwkflow        - the total flowrate through the parallel systems (m3/h)
    ##ssfir_tinlim          - the inlet temperature limit (K)
    ##ssfir_toutlim         - the outlet temperature limit (K)
    ##ssfir_demand_input    - the associated demand (kWh)
    
    ##Processing list of master decision varibles as parameters 
    ssfir_inflow = ssfir_mdv['Value'][0]
    ssfir_tnwkflow = ssfir_mdv['Value'][1]
    ssfir_tinlim = ssfir_mdv['Value'][2]
    ssfir_toutlim = ssfir_mdv['Value'][3]
    ssfir_demand_input = ssfir_mdv['Value'][4]

    #Defining dictionary of values
    
    substation_fir = {}
    
    ##Input constants
    
    ##1
    ssfir_demand = {}
    ssfir_demand['value'] = ssfir_demand_input
    ssfir_demand['units'] = 'kWh'
    ssfir_demand['status'] = 'cst_input'
    substation_fir['ssfir_demand'] = ssfir_demand

    ##2
    ssfir_flowrate = {}
    ssfir_flowrate['value'] = ssfir_inflow
    ssfir_flowrate['units'] = 'm3/h'
    ssfir_flowrate['status'] = 'cst_input'
    substation_fir['ssfir_flowrate'] = ssfir_flowrate

    ##3
    ssfir_totalnwkflow = {}
    ssfir_totalnwkflow['value'] = ssfir_tnwkflow
    ssfir_totalnwkflow['units'] = 'm3/h'
    ssfir_totalnwkflow['status'] = 'cst_input'
    substation_fir['ssfir_totalnwkflow'] = ssfir_totalnwkflow

    ##4
    ssfir_tinmax = {}
    ssfir_tinmax['value'] = ssfir_tinlim
    ssfir_tinmax['units'] = 'K'
    ssfir_tinmax['status'] = 'cst_input'
    substation_fir['ssfir_tinmax'] = ssfir_tinmax

    ##5
    ssfir_toutmax = {}
    ssfir_toutmax['value'] = ssfir_toutlim
    ssfir_toutmax['units'] = 'K'
    ssfir_toutmax['status'] = 'cst_input'
    substation_fir['ssfir_toutmax'] = ssfir_toutmax

    ##Dependent constants
    ssfir_dc = np.zeros((3,1))
    
    ssfir_dc[0,0] = substation_fir['ssfir_demand']['value']
    ssfir_dc[1,0] = substation_fir['ssfir_flowrate']['value']
    ssfir_dc[2,0] = substation_fir['ssfir_totalnwkflow']['value']

    ssfir_dc_calc = substation_fir_compute(ssfir_dc)
    
    ##6
    ssfir_delt = {}
    ssfir_delt['value'] = ssfir_dc_calc[0,0]
    ssfir_delt['units'] = 'K'
    ssfir_delt['status'] = 'calc'
    substation_fir['ssfir_delt'] = ssfir_delt

    ##7
    ssfir_fratio={}
    ssfir_fratio['value'] = ssfir_dc_calc[1,0]
    ssfir_fratio['units'] = '-'
    ssfir_fratio['status'] = 'calc'
    substation_fir['ssfir_fratio'] = ssfir_fratio
    
    ##Unit definition
    
    ##Unit 1
    ssfir = {}
    ssfir['Name'] = 'ssfir'
    ssfir['Fmin'] = 0                                                            ##The min and max does not have any meaning here
    ssfir['Fmax'] = 1
    ssfir['Cost1'] = 0
    ssfir['Cost2'] = 0
    ssfir['Cinv1'] = 0
    ssfir['Cinv2'] = 0
    ssfir['Power1'] = 0
    ssfir['Power2'] = 0
    ssfir['Impact1'] = 0
    ssfir['Impact2'] = 0
    
    unitinput = [ssfir['Name'], ssfir['Fmin'], ssfir['Fmax'], ssfir['Cost1'], ssfir['Cost2'], ssfir['Cinv1'], ssfir['Cinv2'], 
                 ssfir['Power1'], ssfir['Power2'], ssfir['Impact1'], ssfir['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ssfir'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'sp12fir_tin'
    stream1['Layer'] = 'sp12fir'
    stream1['Min_Flow'] = 0                                                     ##Similarly the min and max flow does not have any meaning here 
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    #Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'ssfir'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ssfir2sp2_tout'
    stream2['Layer'] = 'ss2sp2'
    stream2['Min_Flow'] = (stream1['Min_Flow']+substation_fir['ssfir_delt']['value'])*substation_fir['ssfir_fratio']['value']
    stream2['Grad_Flow'] = (((1*stream1['Grad_Flow'])+stream1['Min_Flow'])-stream2['Min_Flow'])*substation_fir['ssfir_fratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definition 
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'ssfir_in'
    eqn1['Type'] = 'stream_limit'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = substation_fir['ssfir_tinmax']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 2
    eqn2 = {}
    eqn2['Name'] = 'ssfir_out'
    eqn2['Type'] = 'stream_limit'
    eqn2['Sign'] = 'less_than_equal_to'
    eqn2['RHS_value'] = substation_fir['ssfir_toutmax']['value']
    
    eqninput = [eqn2['Name'], eqn2['Type'], eqn2['Sign'], eqn2['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Name'] = 'ssfir_in_temp'
    term1['Parent_unit'] = 'ssfir'
    term1['Parent_eqn'] = 'ssfir_in'
    term1['Parent_stream'] = 'sp12fir_tin'                                      ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1

    terminput = [term1['Name'], term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2 
    term2 = {}
    term2['Name'] = 'ssfir_out_temp'
    term2['Parent_unit'] = 'ssfir'
    term2['Parent_eqn'] = 'ssfir_out'
    term2['Parent_stream'] = 'ssfir2sp2_tout'                                   ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1

    terminput = [term2['Name'], term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms