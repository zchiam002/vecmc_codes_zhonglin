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

    
def substation_cp (sscp_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    from substation_cp_compute import substation_cp_compute

    ##Model description: 
    ##This model ensures that a predefined demand is met 
    ##This is an intermediate model, hence the untilization does not have any meaning 
    
    ##Legend of input variables 
    
    ##sscp_inflow       - the flowrate through the system (m3/h)
    ##sscp_tnwkflow     - the total flowrate through the parallel systems (m3/h)
    
    ##Processing list of master decision variables as parameters 
    sscp_inflow = sscp_mdv['Value'][0]
    sscp_tnwkflow = sscp_mdv['Value'][1]
    
    ##Defining dictionary of values
    
    substation_cp = {}
    
    ##Input constants
    
    ##1
    sscp_demand = {}
    sscp_demand['value'] = 0
    sscp_demand['units'] = 'kWh'
    sscp_demand['status'] = 'cst_input'
    substation_cp['sscp_demand'] = sscp_demand

    ##2
    sscp_flowrate = {}
    sscp_flowrate['value'] = sscp_inflow
    sscp_flowrate['units'] = 'm3/h'
    sscp_flowrate['status'] = 'cst_input'
    substation_cp['sscp_flowrate'] = sscp_flowrate

    ##3
    sscp_totalnwkflow = {}
    sscp_totalnwkflow['value'] = sscp_tnwkflow
    sscp_totalnwkflow['units'] = 'm3/h'
    sscp_totalnwkflow['status'] = 'cst_input'
    substation_cp['sscp_totalnwkflow'] = sscp_totalnwkflow

    ##Dependent constants 
    sscp_dc = np.zeros((3,1))
    
    sscp_dc[0,0] = substation_cp['sscp_demand']['value']
    sscp_dc[1,0] = substation_cp['sscp_flowrate']['value']
    sscp_dc[2,0] = substation_cp['sscp_totalnwkflow']['value']

    sscp_dc_calc = substation_cp_compute(sscp_dc)
    
    ##4
    sscp_delt = {}
    sscp_delt['value'] = sscp_dc_calc[0,0]
    sscp_delt['units'] = 'K'
    sscp_delt['status'] = 'calc'
    substation_cp['sscp_delt'] = sscp_delt

    ##5
    sscp_fratio={}
    sscp_fratio['value'] = sscp_dc_calc[1,0]
    sscp_fratio['units'] = '-'
    sscp_fratio['status'] = 'calc'
    substation_cp['sscp_fratio'] = sscp_fratio
    
    ##Unit definition
    
    ##Unit 1
    sscp = {}
    sscp['Name'] = 'sscp'
    sscp['Fmin'] = 0                                                            ##The min and max does not have any meaning here
    sscp['Fmax'] = 1
    sscp['Cost1'] = 0
    sscp['Cost2'] = 0
    sscp['Cinv1'] = 0
    sscp['Cinv2'] = 0
    sscp['Power1'] = 0
    sscp['Power2'] = 0
    sscp['Impact1'] = 0
    sscp['Impact2'] = 0

    unitinput = [sscp['Name'], sscp['Fmin'], sscp['Fmax'], sscp['Cost1'], sscp['Cost2'], sscp['Cinv1'], sscp['Cinv2'], 
                 sscp['Power1'], sscp['Power2'], sscp['Impact1'], sscp['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)

    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'sscp'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'sp12cp_tin'
    stream1['Layer'] = 'sp12cp'
    stream1['Min_Flow'] = 0                                                     ##Similarly the min and max flow does not have any meaning here 
    stream1['Grad_Flow'] = 1000 - stream1['Min_Flow']
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    #Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'sscp'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ss2sp2_tout'
    stream2['Layer'] = 'ss2sp2'
    stream2['Min_Flow'] = (stream1['Min_Flow']+substation_cp['sscp_delt']['value'])*substation_cp['sscp_fratio']['value']
    stream2['Grad_Flow'] = (((1*stream1['Grad_Flow'])+stream1['Min_Flow'])-stream2['Min_Flow'])*substation_cp['sscp_fratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definition 
    
    ##Equation terms 
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms