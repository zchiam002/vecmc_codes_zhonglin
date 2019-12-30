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

def substation_hsb (sshsb_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    from substation_hsb_compute import substation_hsb_compute
    
    ##Model description:
    ##This model ensures that a predefined demand is met 
    ##This is an intermediate model, hence utilization does not have any meaning 
    
    ##Legend of input variables 
    
    ##sshsb_inflow          - the flowrate through the system (m3/h)
    ##sshsb_tnwkflow        - the total flowrate through the parallel systems (m3/h)
    ##sshsb_tinlim          - the inlet temperature limit (K)
    ##sshsb_toutlim         - the outlet temperature limit (K)
    ##sshsb_demand_input    - the associated demand (kWh)
    
    ##Processing list of master decision varibles as parameters 
    sshsb_inflow = sshsb_mdv['Value'][0]
    sshsb_tnwkflow = sshsb_mdv['Value'][1]
    sshsb_tinlim = sshsb_mdv['Value'][2]
    sshsb_toutlim = sshsb_mdv['Value'][3]
    sshsb_demand_input = sshsb_mdv['Value'][4]

    #Defining dictionary of values
    
    substation_hsb = {}
    
    ##Input constants
    
    ##1
    sshsb_demand = {}
    sshsb_demand['value'] = sshsb_demand_input
    sshsb_demand['units'] = 'kWh'
    sshsb_demand['status'] = 'cst_input'
    substation_hsb['sshsb_demand'] = sshsb_demand

    ##2
    sshsb_flowrate = {}
    sshsb_flowrate['value'] = sshsb_inflow
    sshsb_flowrate['units'] = 'm3/h'
    sshsb_flowrate['status'] = 'cst_input'
    substation_hsb['sshsb_flowrate'] = sshsb_flowrate

    ##3
    sshsb_totalnwkflow = {}
    sshsb_totalnwkflow['value'] = sshsb_tnwkflow
    sshsb_totalnwkflow['units'] = 'm3/h'
    sshsb_totalnwkflow['status'] = 'cst_input'
    substation_hsb['sshsb_totalnwkflow'] = sshsb_totalnwkflow

    ##4
    sshsb_tinmax = {}
    sshsb_tinmax['value'] = sshsb_tinlim
    sshsb_tinmax['units'] = 'K'
    sshsb_tinmax['status'] = 'cst_input'
    substation_hsb['sshsb_tinmax'] = sshsb_tinmax

    ##5
    sshsb_toutmax = {}
    sshsb_toutmax['value'] = sshsb_toutlim
    sshsb_toutmax['units'] = 'K'
    sshsb_toutmax['status'] = 'cst_input'
    substation_hsb['sshsb_toutmax'] = sshsb_toutmax

    ##Dependent constants
    sshsb_dc = np.zeros((3,1))
    
    sshsb_dc[0,0] = substation_hsb['sshsb_demand']['value']
    sshsb_dc[1,0] = substation_hsb['sshsb_flowrate']['value']
    sshsb_dc[2,0] = substation_hsb['sshsb_totalnwkflow']['value']

    sshsb_dc_calc = substation_hsb_compute(sshsb_dc)
    
    ##6
    sshsb_delt = {}
    sshsb_delt['value'] = sshsb_dc_calc[0,0]
    sshsb_delt['units'] = 'K'
    sshsb_delt['status'] = 'calc'
    substation_hsb['sshsb_delt'] = sshsb_delt

    ##7
    sshsb_fratio={}
    sshsb_fratio['value'] = sshsb_dc_calc[1,0]
    sshsb_fratio['units'] = '-'
    sshsb_fratio['status'] = 'calc'
    substation_hsb['sshsb_fratio'] = sshsb_fratio
    
    ##Unit definition
    
    ##Unit 1
    sshsb = {}
    sshsb['Name'] = 'sshsb'
    sshsb['Fmin'] = 0                                                            ##The min and max does not have any meaning here
    sshsb['Fmax'] = 1
    sshsb['Cost1'] = 0
    sshsb['Cost2'] = 0
    sshsb['Cinv1'] = 0
    sshsb['Cinv2'] = 0
    sshsb['Power1'] = 0
    sshsb['Power2'] = 0
    sshsb['Impact1'] = 0
    sshsb['Impact2'] = 0
    
    unitinput = [sshsb['Name'], sshsb['Fmin'], sshsb['Fmax'], sshsb['Cost1'], sshsb['Cost2'], sshsb['Cinv1'], sshsb['Cinv2'], 
                 sshsb['Power1'], sshsb['Power2'], sshsb['Impact1'], sshsb['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'sshsb'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'sp12hsb_tin'
    stream1['Layer'] = 'sp12hsb'
    stream1['Min_Flow'] = 0                                                     ##Similarly the min and max flow does not have any meaning here 
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    #Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'sshsb'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'sshsb2sp2_tout'
    stream2['Layer'] = 'ss2sp2'
    stream2['Min_Flow'] = (stream1['Min_Flow']+substation_hsb['sshsb_delt']['value'])*substation_hsb['sshsb_fratio']['value']
    stream2['Grad_Flow'] = (((1*stream1['Grad_Flow'])+stream1['Min_Flow'])-stream2['Min_Flow'])*substation_hsb['sshsb_fratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definition 
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'sshsb_in'
    eqn1['Type'] = 'stream_limit'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = substation_hsb['sshsb_tinmax']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 2
    eqn2 = {}
    eqn2['Name'] = 'sshsb_out'
    eqn2['Type'] = 'stream_limit'
    eqn2['Sign'] = 'less_than_equal_to'
    eqn2['RHS_value'] = substation_hsb['sshsb_toutmax']['value']
    
    eqninput = [eqn2['Name'], eqn2['Type'], eqn2['Sign'], eqn2['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Name'] = 'sshsb_in_temp'
    term1['Parent_unit'] = 'sshsb'
    term1['Parent_eqn'] = 'sshsb_in'
    term1['Parent_stream'] = 'sp12hsb_tin'                                      ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1

    terminput = [term1['Name'], term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2 
    term2 = {}
    term2['Name'] = 'sshsb_out_temp'
    term2['Parent_unit'] = 'sshsb'
    term2['Parent_eqn'] = 'sshsb_out'
    term2['Parent_stream'] = 'sshsb2sp2_tout'                                   ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1

    terminput = [term2['Name'], term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms