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

def substation_ser (ssser_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    from substation_ser_compute import substation_ser_compute
    
    ##Model description:
    ##This model ensures that a predefined demand is met 
    ##This is an intermediate model, hence utilization does not have any meaning 
    
    ##Legend of input variables 
    
    ##ssser_inflow          - the flowrate through the system (m3/h)
    ##ssser_tnwkflow        - the total flowrate through the parallel systems (m3/h)
    ##ssser_tinlim          - the inlet temperature limit (K)
    ##ssser_toutlim         - the outlet temperature limit (K)
    ##ssser_demand_input    - the associated demand (kWh)
    
    ##Processing list of master decision varibles as parameters 
    ssser_inflow = ssser_mdv['Value'][0]
    ssser_tnwkflow = ssser_mdv['Value'][1]
    ssser_tinlim = ssser_mdv['Value'][2]
    ssser_toutlim = ssser_mdv['Value'][3]
    ssser_demand_input = ssser_mdv['Value'][4]

    #Defining dictionary of values
    
    substation_ser = {}
    
    ##Input constants
    
    ##1
    ssser_demand = {}
    ssser_demand['value'] = ssser_demand_input
    ssser_demand['units'] = 'kWh'
    ssser_demand['status'] = 'cst_input'
    substation_ser['ssser_demand'] = ssser_demand

    ##2
    ssser_flowrate = {}
    ssser_flowrate['value'] = ssser_inflow
    ssser_flowrate['units'] = 'm3/h'
    ssser_flowrate['status'] = 'cst_input'
    substation_ser['ssser_flowrate'] = ssser_flowrate

    ##3
    ssser_totalnwkflow = {}
    ssser_totalnwkflow['value'] = ssser_tnwkflow
    ssser_totalnwkflow['units'] = 'm3/h'
    ssser_totalnwkflow['status'] = 'cst_input'
    substation_ser['ssser_totalnwkflow'] = ssser_totalnwkflow

    ##4
    ssser_tinmax = {}
    ssser_tinmax['value'] = ssser_tinlim
    ssser_tinmax['units'] = 'K'
    ssser_tinmax['status'] = 'cst_input'
    substation_ser['ssser_tinmax'] = ssser_tinmax

    ##5
    ssser_toutmax = {}
    ssser_toutmax['value'] = ssser_toutlim
    ssser_toutmax['units'] = 'K'
    ssser_toutmax['status'] = 'cst_input'
    substation_ser['ssser_toutmax'] = ssser_toutmax

    ##Dependent constants
    ssser_dc = np.zeros((3,1))
    
    ssser_dc[0,0] = substation_ser['ssser_demand']['value']
    ssser_dc[1,0] = substation_ser['ssser_flowrate']['value']
    ssser_dc[2,0] = substation_ser['ssser_totalnwkflow']['value']

    ssser_dc_calc = substation_ser_compute(ssser_dc)
    
    ##6
    ssser_delt = {}
    ssser_delt['value'] = ssser_dc_calc[0,0]
    ssser_delt['units'] = 'K'
    ssser_delt['status'] = 'calc'
    substation_ser['ssser_delt'] = ssser_delt

    ##7
    ssser_fratio={}
    ssser_fratio['value'] = ssser_dc_calc[1,0]
    ssser_fratio['units'] = '-'
    ssser_fratio['status'] = 'calc'
    substation_ser['ssser_fratio'] = ssser_fratio

    ##Unit definition
    
    ##Unit 1
    ssser = {}
    ssser['Name'] = 'ssser'
    ssser['Fmin'] = 0                                                            ##The min and max does not have any meaning here
    ssser['Fmax'] = 1
    ssser['Cost1'] = 0
    ssser['Cost2'] = 0
    ssser['Cinv1'] = 0
    ssser['Cinv2'] = 0
    ssser['Power1'] = 0
    ssser['Power2'] = 0
    ssser['Impact1'] = 0
    ssser['Impact2'] = 0
    
    unitinput = [ssser['Name'], ssser['Fmin'], ssser['Fmax'], ssser['Cost1'], ssser['Cost2'], ssser['Cinv1'], ssser['Cinv2'], 
                 ssser['Power1'], ssser['Power2'], ssser['Impact1'], ssser['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ssser'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'sp12ser_tin'
    stream1['Layer'] = 'sp12ser'
    stream1['Min_Flow'] = 0                                                     ##Similarly the min and max flow does not have any meaning here 
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    #Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'ssser'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ssser2sp2_tout'
    stream2['Layer'] = 'ss2sp2'
    stream2['Min_Flow'] = (stream1['Min_Flow']+substation_ser['ssser_delt']['value'])*substation_ser['ssser_fratio']['value']
    stream2['Grad_Flow'] = (((1*stream1['Grad_Flow'])+stream1['Min_Flow'])-stream2['Min_Flow'])*substation_ser['ssser_fratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definition 
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'ssser_in'
    eqn1['Type'] = 'stream_limit'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = substation_ser['ssser_tinmax']['value']
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation 2
    eqn2 = {}
    eqn2['Name'] = 'ssser_out'
    eqn2['Type'] = 'stream_limit'
    eqn2['Sign'] = 'less_than_equal_to'
    eqn2['RHS_value'] = substation_ser['ssser_toutmax']['value']
    
    eqninput = [eqn2['Name'], eqn2['Type'], eqn2['Sign'], eqn2['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)
    
    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Name'] = 'ssser_in_temp'
    term1['Parent_unit'] = 'ssser'
    term1['Parent_eqn'] = 'ssser_in'
    term1['Parent_stream'] = 'sp12ser_tin'                                      ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1

    terminput = [term1['Name'], term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2 
    term2 = {}
    term2['Name'] = 'ssser_out_temp'
    term2['Parent_unit'] = 'ssser'
    term2['Parent_eqn'] = 'ssser_out'
    term2['Parent_stream'] = 'ssser2sp2_tout'                                   ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1

    terminput = [term2['Name'], term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms