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

def substation_pfa (sspfa_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    from substation_pfa_compute import substation_pfa_compute
    
    ##Model description:
    ##This model ensures that a predefined demand is met 
    ##This is an intermediate model, hence utilization does not have any meaning 
    
    ##Legend of input variables 
    
    ##sspfa_inflow          - the flowrate through the system (m3/h)
    ##sspfa_tnwkflow        - the total flowrate through the parallel systems (m3/h)
    ##sspfa_tinlim          - the inlet temperature limit (K)
    ##sspfa_toutlim         - the outlet temperature limit (K)
    ##sspfa_demand_input    - the associated demand (kWh)
    
    ##Processing list of master decision varibles as parameters 
    sspfa_inflow = sspfa_mdv['Value'][0]
    sspfa_tnwkflow = sspfa_mdv['Value'][1]
    sspfa_tinlim = sspfa_mdv['Value'][2]
    sspfa_toutlim = sspfa_mdv['Value'][3]
    sspfa_demand_input = sspfa_mdv['Value'][4]

    #Defining dictionary of values
    
    substation_pfa = {}
    
    ##Input constants
    
    ##1
    sspfa_demand = {}
    sspfa_demand['value'] = sspfa_demand_input
    sspfa_demand['units'] = 'kWh'
    sspfa_demand['status'] = 'cst_input'
    substation_pfa['sspfa_demand'] = sspfa_demand

    ##2
    sspfa_flowrate = {}
    sspfa_flowrate['value'] = sspfa_inflow
    sspfa_flowrate['units'] = 'm3/h'
    sspfa_flowrate['status'] = 'cst_input'
    substation_pfa['sspfa_flowrate'] = sspfa_flowrate

    ##3
    sspfa_totalnwkflow = {}
    sspfa_totalnwkflow['value'] = sspfa_tnwkflow
    sspfa_totalnwkflow['units'] = 'm3/h'
    sspfa_totalnwkflow['status'] = 'cst_input'
    substation_pfa['sspfa_totalnwkflow'] = sspfa_totalnwkflow

    ##4
    sspfa_tinmax = {}
    sspfa_tinmax['value'] = sspfa_tinlim
    sspfa_tinmax['units'] = 'K'
    sspfa_tinmax['status'] = 'cst_input'
    substation_pfa['sspfa_tinmax'] = sspfa_tinmax

    ##5
    sspfa_toutmax = {}
    sspfa_toutmax['value'] = sspfa_toutlim
    sspfa_toutmax['units'] = 'K'
    sspfa_toutmax['status'] = 'cst_input'
    substation_pfa['sspfa_toutmax'] = sspfa_toutmax

    ##Dependent constants
    sspfa_dc = np.zeros((3,1))
    
    sspfa_dc[0,0] = substation_pfa['sspfa_demand']['value']
    sspfa_dc[1,0] = substation_pfa['sspfa_flowrate']['value']
    sspfa_dc[2,0] = substation_pfa['sspfa_totalnwkflow']['value']

    sspfa_dc_calc = substation_pfa_compute(sspfa_dc)
    
    ##6
    sspfa_delt = {}
    sspfa_delt['value'] = sspfa_dc_calc[0,0]
    sspfa_delt['units'] = 'K'
    sspfa_delt['status'] = 'calc'
    substation_pfa['sspfa_delt'] = sspfa_delt

    ##7
    sspfa_fratio={}
    sspfa_fratio['value'] = sspfa_dc_calc[1,0]
    sspfa_fratio['units'] = '-'
    sspfa_fratio['status'] = 'calc'
    substation_pfa['sspfa_fratio'] = sspfa_fratio

    ##Unit definition
    
    ##Unit 1
    sspfa = {}
    sspfa['Name'] = 'sspfa'
    sspfa['Fmin'] = 0                                                            ##The min and max does not have any meaning here
    sspfa['Fmax'] = 1
    sspfa['Cost1'] = 0
    sspfa['Cost2'] = 0
    sspfa['Cinv1'] = 0
    sspfa['Cinv2'] = 0
    sspfa['Power1'] = 0
    sspfa['Power2'] = 0
    sspfa['Impact1'] = 0
    sspfa['Impact2'] = 0
    
    unitinput = [sspfa['Name'], sspfa['Fmin'], sspfa['Fmax'], sspfa['Cost1'], sspfa['Cost2'], sspfa['Cinv1'], sspfa['Cinv2'], 
                 sspfa['Power1'], sspfa['Power2'], sspfa['Impact1'], sspfa['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'sspfa'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'sp12pfa_tin'
    stream1['Layer'] = 'sp12pfa'
    stream1['Min_Flow'] = 0                                                     ##Similarly the min and max flow does not have any meaning here 
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    #Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'sspfa'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'sspfa2sp2_tout'
    stream2['Layer'] = 'ss2sp2'
    stream2['Min_Flow'] = (stream1['Min_Flow']+substation_pfa['sspfa_delt']['value'])*substation_pfa['sspfa_fratio']['value']
    stream2['Grad_Flow'] = (((1*stream1['Grad_Flow'])+stream1['Min_Flow'])-stream2['Min_Flow'])*substation_pfa['sspfa_fratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definition 
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'sspfa_in'
    eqn1['Type'] = 'stream_limit'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = substation_pfa['sspfa_tinmax']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 2
    eqn2 = {}
    eqn2['Name'] = 'sspfa_out'
    eqn2['Type'] = 'stream_limit'
    eqn2['Sign'] = 'less_than_equal_to'
    eqn2['RHS_value'] = substation_pfa['sspfa_toutmax']['value']
    
    eqninput = [eqn2['Name'], eqn2['Type'], eqn2['Sign'], eqn2['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Name'] = 'sspfa_in_temp'
    term1['Parent_unit'] = 'sspfa'
    term1['Parent_eqn'] = 'sspfa_in'
    term1['Parent_stream'] = 'sp12pfa_tin'                                      ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1

    terminput = [term1['Name'], term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2 
    term2 = {}
    term2['Name'] = 'sspfa_out_temp'
    term2['Parent_unit'] = 'sspfa'
    term2['Parent_eqn'] = 'sspfa_out'
    term2['Parent_stream'] = 'sspfa2sp2_tout'                                   ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1

    terminput = [term2['Name'], term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms