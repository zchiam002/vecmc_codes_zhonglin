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

def substation_gv2 (ssgv2_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    from substation_gv2_compute import substation_gv2_compute
    
    ##Model description:
    ##This model ensures that a predefined demand is met 
    ##This is an intermediate model, hence utilization does not have any meaning 
    
    ##Legend of input variables 
    
    ##ssgv2_inflow          - the flowrate through the system (m3/h)
    ##ssgv2_tnwkflow        - the total flowrate through the parallel systems (m3/h)
    ##ssgv2_tinlim          - the inlet temperature limit (K)
    ##ssgv2_toutlim         - the outlet temperature limit (K)
    ##ssgv2_demand_input    - the associated demand (kWh)
    
    ##Processing list of master decision varibles as parameters 
    ssgv2_inflow = ssgv2_mdv['Value'][0]
    ssgv2_tnwkflow = ssgv2_mdv['Value'][1]
    ssgv2_tinlim = ssgv2_mdv['Value'][2]
    ssgv2_toutlim = ssgv2_mdv['Value'][3]
    ssgv2_demand_input = ssgv2_mdv['Value'][4]

    #Defining dictionary of values
    
    substation_gv2 = {}
    
    ##Input constants
    
    ##1
    ssgv2_demand = {}
    ssgv2_demand['value'] = ssgv2_demand_input
    ssgv2_demand['units'] = 'kWh'
    ssgv2_demand['status'] = 'cst_input'
    substation_gv2['ssgv2_demand'] = ssgv2_demand

    ##2
    ssgv2_flowrate = {}
    ssgv2_flowrate['value'] = ssgv2_inflow
    ssgv2_flowrate['units'] = 'm3/h'
    ssgv2_flowrate['status'] = 'cst_input'
    substation_gv2['ssgv2_flowrate'] = ssgv2_flowrate

    ##3
    ssgv2_totalnwkflow = {}
    ssgv2_totalnwkflow['value'] = ssgv2_tnwkflow
    ssgv2_totalnwkflow['units'] = 'm3/h'
    ssgv2_totalnwkflow['status'] = 'cst_input'
    substation_gv2['ssgv2_totalnwkflow'] = ssgv2_totalnwkflow

    ##4
    ssgv2_tinmax = {}
    ssgv2_tinmax['value'] = ssgv2_tinlim
    ssgv2_tinmax['units'] = 'K'
    ssgv2_tinmax['status'] = 'cst_input'
    substation_gv2['ssgv2_tinmax'] = ssgv2_tinmax

    ##5
    ssgv2_toutmax = {}
    ssgv2_toutmax['value'] = ssgv2_toutlim
    ssgv2_toutmax['units'] = 'K'
    ssgv2_toutmax['status'] = 'cst_input'
    substation_gv2['ssgv2_toutmax'] = ssgv2_toutmax

    ##Dependent constants
    ssgv2_dc = np.zeros((3,1))
    
    ssgv2_dc[0,0] = substation_gv2['ssgv2_demand']['value']
    ssgv2_dc[1,0] = substation_gv2['ssgv2_flowrate']['value']
    ssgv2_dc[2,0] = substation_gv2['ssgv2_totalnwkflow']['value']

    ssgv2_dc_calc = substation_gv2_compute(ssgv2_dc)
    
    ##6
    ssgv2_delt = {}
    ssgv2_delt['value'] = ssgv2_dc_calc[0,0]
    ssgv2_delt['units'] = 'K'
    ssgv2_delt['status'] = 'calc'
    substation_gv2['ssgv2_delt'] = ssgv2_delt

    ##7
    ssgv2_fratio={}
    ssgv2_fratio['value'] = ssgv2_dc_calc[1,0]
    ssgv2_fratio['units'] = '-'
    ssgv2_fratio['status'] = 'calc'
    substation_gv2['ssgv2_fratio'] = ssgv2_fratio
    
    ##Unit definition
    
    ##Unit 1
    ssgv2 = {}
    ssgv2['Name'] = 'ssgv2'
    ssgv2['Fmin'] = 0                                                            ##The min and max does not have any meaning here
    ssgv2['Fmax'] = 1
    ssgv2['Cost1'] = 0
    ssgv2['Cost2'] = 0
    ssgv2['Cinv1'] = 0
    ssgv2['Cinv2'] = 0
    ssgv2['Power1'] = 0
    ssgv2['Power2'] = 0
    ssgv2['Impact1'] = 0
    ssgv2['Impact2'] = 0
    
    unitinput = [ssgv2['Name'], ssgv2['Fmin'], ssgv2['Fmax'], ssgv2['Cost1'], ssgv2['Cost2'], ssgv2['Cinv1'], ssgv2['Cinv2'], 
                 ssgv2['Power1'], ssgv2['Power2'], ssgv2['Impact1'], ssgv2['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ssgv2'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'sp12gv2_tin'
    stream1['Layer'] = 'sp12gv2'
    stream1['Min_Flow'] = 0                                                     ##Similarly the min and max flow does not have any meaning here 
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    #Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'ssgv2'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ssgv22sp2_tout'
    stream2['Layer'] = 'ss2sp2'
    stream2['Min_Flow'] = (stream1['Min_Flow']+substation_gv2['ssgv2_delt']['value'])*substation_gv2['ssgv2_fratio']['value']
    stream2['Grad_Flow'] = (((1*stream1['Grad_Flow'])+stream1['Min_Flow'])-stream2['Min_Flow'])*substation_gv2['ssgv2_fratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definition 
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'ssgv2_in'
    eqn1['Type'] = 'stream_limit'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = substation_gv2['ssgv2_tinmax']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 2
    eqn2 = {}
    eqn2['Name'] = 'ssgv2_out'
    eqn2['Type'] = 'stream_limit'
    eqn2['Sign'] = 'less_than_equal_to'
    eqn2['RHS_value'] = substation_gv2['ssgv2_toutmax']['value']
    
    eqninput = [eqn2['Name'], eqn2['Type'], eqn2['Sign'], eqn2['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Name'] = 'ssgv2_in_temp'
    term1['Parent_unit'] = 'ssgv2'
    term1['Parent_eqn'] = 'ssgv2_in'
    term1['Parent_stream'] = 'sp12gv2_tin'                                      ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1

    terminput = [term1['Name'], term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2 
    term2 = {}
    term2['Name'] = 'ssgv2_out_temp'
    term2['Parent_unit'] = 'ssgv2'
    term2['Parent_eqn'] = 'ssgv2_out'
    term2['Parent_stream'] = 'ssgv22sp2_tout'                                   ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1

    terminput = [term2['Name'], term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms