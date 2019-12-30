## This is a chiller model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type


def chiller3 (ch3_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from chiller3_compute import chiller3_compute
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##Built based on Gordon-Ng's Universal Chiller model
    ##The COP is kept constant at 4 predefined steps in equally spaced intervals 
    ##The inputs to this function are variables to the eyes of the Master optimizer 
    
    ##Legend of input variables 
    
    ##ch3_em          - evaporator volume flowrate (m3/h)
    ##ch3_etret       - evaporator return temperature (K)
    ##ch3_cm          - condenser volume flowrate (m3/h)
    ##ch3_ctin        - condenser inlet temperature (K)
    ##ch3_tenwkflow   - total flowrate through parallel systems (m3/h)
    ##ch3_tcnwkflow   - total flowrate through parallel systems (m3/h)
    
    ##Processing list of master decision variables as parameters
    ch3_em = ch3_mdv['Value'][0]
    ch3_etret = ch3_mdv['Value'][1]
    ch3_cm = ch3_mdv['Value'][2]
    ch3_ctin = ch3_mdv['Value'][3]
    ch3_tenwkflow = ch3_mdv['Value'][4]                    ##Total flowrate through all evaporators of all chillers 
    ch3_tcnwkflow = ch3_mdv['Value'][5]                    ##Total flowrate through all condensers of all chillers 

    ##Define dictionary of values 

    chiller3 = {}
    ##Input constants 
    
    ##1
    ch3_evapflow = {}
    ch3_evapflow['value'] = ch3_em
    ch3_evapflow['units'] = 'm3/h'
    ch3_evapflow['status'] = 'cst_input'
    chiller3['ch3_evapflow'] = ch3_evapflow

    ##2
    ch3_evaptret = {}
    ch3_evaptret['value'] = ch3_etret
    ch3_evaptret['units'] = 'K'
    ch3_evaptret['status'] = 'cst_input'
    chiller3['ch3_evaptret'] = ch3_evaptret

    ##3
    ch3_condflow = {}
    ch3_condflow['value'] = ch3_cm
    ch3_condflow['units'] = 'm3/h'
    ch3_condflow['status'] = 'cst_input'
    chiller3['ch3_condflow'] = ch3_condflow

    ##4
    ch3_condtin = {}
    ch3_condtin['value'] = ch3_ctin
    ch3_condtin['units'] = 'K'
    ch3_condtin['status'] = 'cst_input'
    chiller3['ch3_condtin'] = ch3_condtin

    ##5
    ch3_totalenwkflow = {}
    ch3_totalenwkflow['value'] = ch3_tenwkflow
    ch3_totalenwkflow['units'] = 'm3/h'
    ch3_totalenwkflow['status'] = 'cst_input'
    chiller3['ch3_totalenwkflow'] = ch3_totalenwkflow

    ##6
    ch3_totalcnwkflow = {}
    ch3_totalcnwkflow['value'] = ch3_tcnwkflow
    ch3_totalcnwkflow['units'] = 'm3/h'
    ch3_totalcnwkflow['status'] = 'cst_input'
    chiller3['ch3_totalcnwkflow'] = ch3_totalcnwkflow

    ##Defined constants
    
    ##7
    ch3_rated_cap = {}                              #The rated capacity of the chiller
    ch3_rated_cap['value'] = 7330
    ch3_rated_cap['units'] = 'kWh'
    ch3_rated_cap['status'] = 'cst'
    chiller3['ch3_rated_cap'] = ch3_rated_cap
    
    ##8
    ch3_b0 = {}
    ch3_b0['value'] =  1.35049420632748            #Regression-derived constants
    ch3_b0['units'] = '-'
    ch3_b0['status'] = 'cst'
    chiller3['ch3_b0'] = ch3_b0

    ##9    
    ch3_b1 = {}
    ch3_b1['value'] =  -134.853705222833            
    ch3_b1['units'] = '-'
    ch3_b1['status'] = 'cst'
    chiller3['ch3_b1'] = ch3_b1
    
    ##10
    ch3_b2 = {}
    ch3_b2['value'] =  0.00430128306723068            
    ch3_b2['units'] = '-'
    ch3_b2['status'] = 'cst'
    chiller3['ch3_b2'] = ch3_b2

    ##11
    ch3_qc_coeff = {}
    ch3_qc_coeff['value'] = 1.10348067074030        #The relationship between Qe and Qc
    ch3_qc_coeff['units'] = '-'
    ch3_qc_coeff['status'] = 'cst'
    chiller3['ch3_qc_coeff'] = ch3_qc_coeff

    ##Dependent constants
    ch3_dc = np.zeros((11,1))                       #Initialize the list, note the number of constants
    
    ch3_dc[0,0] = chiller3['ch3_evapflow']['value']
    ch3_dc[1,0] = chiller3['ch3_evaptret']['value']
    ch3_dc[2,0] = chiller3['ch3_condflow']['value']
    ch3_dc[3,0] = chiller3['ch3_condtin']['value']
    ch3_dc[4,0] = chiller3['ch3_rated_cap']['value']
    ch3_dc[5,0] = chiller3['ch3_b0']['value']    
    ch3_dc[6,0] = chiller3['ch3_b1']['value']
    ch3_dc[7,0] = chiller3['ch3_b2']['value']
    ch3_dc[8,0] = chiller3['ch3_qc_coeff']['value']
    ch3_dc[9,0] = chiller3['ch3_totalenwkflow']['value']
    ch3_dc[10,0] = chiller3['ch3_totalcnwkflow']['value']

    ch3_dc_calc = chiller3_compute(ch3_dc)
    
    ##12
    ch3_int1 = {}
    ch3_int1['value'] = ch3_dc_calc[0,0]            #Intercpets of step-wise linearity
    ch3_int1['units'] = '-'
    ch3_int1['status'] = 'calc'
    chiller3['ch3_int1'] = ch3_int1

    ##13
    ch3_int2 = {}
    ch3_int2['value'] = ch3_dc_calc[1,0]
    ch3_int2['units'] = '-'
    ch3_int2['status'] = 'calc'
    chiller3['ch3_int2'] = ch3_int2

    ##14
    ch3_int3 = {}
    ch3_int3['value'] = ch3_dc_calc[2,0]
    ch3_int3['units'] = '-'
    ch3_int3['status'] = 'calc'
    chiller3['ch3_int3'] = ch3_int3

    ##15
    ch3_int4 = {}
    ch3_int4['value'] = ch3_dc_calc[3,0]
    ch3_int4['units'] = '-'
    ch3_int4['status'] = 'calc'
    chiller3['ch3_int4'] = ch3_int4

    ##16
    ch3_egrad1 = {}
    ch3_egrad1['value'] = ch3_dc_calc[4,0]
    ch3_egrad1['units'] = '-'
    ch3_egrad1['status'] = 'calc'
    chiller3['ch3_egrad1'] = ch3_egrad1

    ##17
    ch3_egrad2 = {}
    ch3_egrad2['value'] = ch3_dc_calc[5,0]
    ch3_egrad2['units'] = '-'
    ch3_egrad2['status'] = 'calc'
    chiller3['ch3_egrad2'] = ch3_egrad2  

    ##18
    ch3_egrad3 = {}
    ch3_egrad3['value'] = ch3_dc_calc[6,0]
    ch3_egrad3['units'] = '-'
    ch3_egrad3['status'] = 'calc'
    chiller3['ch3_egrad3'] = ch3_egrad3

    ##19
    ch3_egrad4 = {}
    ch3_egrad4['value'] = ch3_dc_calc[7,0]
    ch3_egrad4['units'] = '-'
    ch3_egrad4['status'] = 'calc'
    chiller3['ch3_egrad4'] = ch3_egrad4 
 
    ##20
    ch3_maxdelt = {}
    ch3_maxdelt['value'] = ch3_dc_calc[8,0]
    ch3_maxdelt['units'] = '-'
    ch3_maxdelt['status'] = 'calc'
    chiller3['ch3_maxdelt'] = ch3_maxdelt

    ##21
    ch3_eratio = {}
    ch3_eratio['value'] = ch3_dc_calc[9,0]
    ch3_eratio['units'] = '-'
    ch3_eratio['status'] = 'calc'
    chiller3['ch3_eratio'] = ch3_eratio

    ##22
    ch3_cratio = {}
    ch3_cratio['value'] = ch3_dc_calc[10,0]
    ch3_cratio['units'] = '-'
    ch3_cratio['status'] = 'calc'
    chiller3['ch3_cratio'] = ch3_cratio

    ##23
    ch3_cond_maxdelt = {}
    ch3_cond_maxdelt['value'] = ch3_dc_calc[11,0]
    ch3_cond_maxdelt['units'] = '-'
    ch3_cond_maxdelt['status'] = 'calc'
    chiller3['ch3_cond_maxdelt'] = ch3_cond_maxdelt  
    
    ##24
    ch3_f1 = {}
    ch3_f1['value'] = ch3_dc_calc[12,0]
    ch3_f1['units'] = '-'
    ch3_f1['status'] = 'calc'
    chiller3['ch3_f1'] = ch3_f1  
    
    ##25
    ch3_f2 = {}
    ch3_f2['value'] = ch3_dc_calc[13,0]
    ch3_f2['units'] = '-'
    ch3_f2['status'] = 'calc'
    chiller3['ch3_f2'] = ch3_f2  
    
    ##26
    ch3_f3 = {}
    ch3_f3['value'] = ch3_dc_calc[14,0]
    ch3_f3['units'] = '-'
    ch3_f3['status'] = 'calc'
    chiller3['ch3_f3'] = ch3_f3
    
    ##27
    ch3_f4 = {}
    ch3_f4['value'] = ch3_dc_calc[15,0]
    ch3_f4['units'] = '-'
    ch3_f4['status'] = 'calc'
    chiller3['ch3_f4'] = ch3_f4
    
    ##28
    ch3_f5 = {}
    ch3_f5['value'] = ch3_dc_calc[16,0]
    ch3_f5['units'] = '-'
    ch3_f5['status'] = 'calc'
    chiller3['ch3_f5'] = ch3_f5

    ##Unit definition 
    
    ##Unit 1
    ch3_1 = {}
    ch3_1['Name'] = 'ch3_1'
    ch3_1['Fmin'] = chiller3['ch3_f1']['value']
    ch3_1['Fmax'] = chiller3['ch3_f2']['value']
    ch3_1['Cost1'] = 0
    ch3_1['Cost2'] = 0
    ch3_1['Cinv1'] = 0
    ch3_1['Cinv2'] = 0
    ch3_1['Power1'] = chiller3['ch3_int1']['value']
    ch3_1['Power2'] = chiller3['ch3_egrad1']['value']
    ch3_1['Impact1'] = 0
    ch3_1['Impact2'] = 0

    unitinput = [ch3_1['Name'], ch3_1['Fmin'], ch3_1['Fmax'], ch3_1['Cost1'], ch3_1['Cost2'], ch3_1['Cinv1'], ch3_1['Cinv2'], 
                 ch3_1['Power1'], ch3_1['Power2'], ch3_1['Impact1'], ch3_1['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 2
    ch3_2 = {}
    ch3_2['Name'] = 'ch3_2'
    ch3_2['Fmin'] = chiller3['ch3_f2']['value']
    ch3_2['Fmax'] = chiller3['ch3_f3']['value']
    ch3_2['Cost1'] = 0
    ch3_2['Cost2'] = 0
    ch3_2['Cinv1'] = 0
    ch3_2['Cinv2'] = 0
    ch3_2['Power1'] = chiller3['ch3_int2']['value']
    ch3_2['Power2'] = chiller3['ch3_egrad2']['value']
    ch3_2['Impact1'] = 0
    ch3_2['Impact2'] = 0
    
    unitinput = [ch3_2['Name'], ch3_2['Fmin'], ch3_2['Fmax'], ch3_2['Cost1'], ch3_2['Cost2'], ch3_2['Cinv1'], ch3_2['Cinv2'], 
                 ch3_2['Power1'], ch3_2['Power2'], ch3_2['Impact1'], ch3_2['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)  
    
    ##Unit 3
    ch3_3 = {}
    ch3_3['Name'] = 'ch3_3'
    ch3_3['Fmin'] = chiller3['ch3_f3']['value']
    ch3_3['Fmax'] = chiller3['ch3_f4']['value']
    ch3_3['Cost1'] = 0
    ch3_3['Cost2'] = 0
    ch3_3['Cinv1'] = 0
    ch3_3['Cinv2'] = 0
    ch3_3['Power1'] = chiller3['ch3_int3']['value']
    ch3_3['Power2'] = chiller3['ch3_egrad3']['value']
    ch3_3['Impact1'] = 0
    ch3_3['Impact2'] = 0

    unitinput = [ch3_3['Name'], ch3_3['Fmin'], ch3_3['Fmax'], ch3_3['Cost1'], ch3_3['Cost2'], ch3_3['Cinv1'], ch3_3['Cinv2'], 
                 ch3_3['Power1'], ch3_3['Power2'], ch3_3['Impact1'], ch3_3['Impact2']]    
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)  
    
    ##Unit 4
    ch3_4 = {}
    ch3_4['Name'] = 'ch3_4'
    ch3_4['Fmin'] = chiller3['ch3_f4']['value']
    ch3_4['Fmax'] = chiller3['ch3_f5']['value']
    ch3_4['Cost1'] = 0
    ch3_4['Cost2'] = 0
    ch3_4['Cinv1'] = 0
    ch3_4['Cinv2'] = 0
    ch3_4['Power1'] = chiller3['ch3_int4']['value']
    ch3_4['Power2'] = chiller3['ch3_egrad4']['value']
    ch3_4['Impact1'] = 0
    ch3_4['Impact2'] = 0
    
    unitinput = [ch3_4['Name'], ch3_4['Fmin'], ch3_4['Fmax'], ch3_4['Cost1'], ch3_4['Cost2'], ch3_4['Cinv1'], ch3_4['Cinv2'], 
                 ch3_4['Power1'], ch3_4['Power2'], ch3_4['Impact1'], ch3_4['Impact2']]      
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)  

    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ch3_1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch3_1_tout'
    stream1['Layer'] = 'chil2sp1'
    stream1['Min_Flow'] = chiller3['ch3_evaptret']['value']*chiller3['ch3_eratio']['value']
    stream1['Grad_Flow'] = -chiller3['ch3_maxdelt']['value']*chiller3['ch3_eratio']['value']
    stream1['InOut'] = 'out'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'ch3_1'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ch3_1_cond_tout'
    stream2['Layer'] = 'chilcond2sp3'
    stream2['Min_Flow'] = chiller3['ch3_condtin']['value']*chiller3['ch3_cratio']['value']
    stream2['Grad_Flow'] = chiller3['ch3_cond_maxdelt']['value']*chiller3['ch3_cratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 3
    stream3 = {}
    stream3['Unit_Name'] = 'ch3_2'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'ch3_2_tout'
    stream3['Layer'] = 'chil2sp1'
    stream3['Min_Flow'] = chiller3['ch3_evaptret']['value']*chiller3['ch3_eratio']['value']
    stream3['Grad_Flow'] = -chiller3['ch3_maxdelt']['value']*chiller3['ch3_eratio']['value']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Unit_Name'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Min_Flow'], stream3['Grad_Flow'], 
                   stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 4
    stream4 = {}
    stream4['Unit_Name'] = 'ch3_2'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'ch3_2_cond_tout'
    stream4['Layer'] = 'chilcond2sp3'
    stream4['Min_Flow'] = chiller3['ch3_condtin']['value']*chiller3['ch3_cratio']['value']
    stream4['Grad_Flow'] = chiller3['ch3_cond_maxdelt']['value']*chiller3['ch3_cratio']['value']
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Unit_Name'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Min_Flow'], stream4['Grad_Flow'], 
                   stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 5
    stream5 = {}
    stream5['Unit_Name'] = 'ch3_3'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'ch3_3_tout'
    stream5['Layer'] = 'chil2sp1'
    stream5['Min_Flow'] = chiller3['ch3_evaptret']['value']*chiller3['ch3_eratio']['value']
    stream5['Grad_Flow'] = -chiller3['ch3_maxdelt']['value']*chiller3['ch3_eratio']['value']
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Unit_Name'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Min_Flow'], stream5['Grad_Flow'], 
                   stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 6
    stream6 = {}
    stream6['Unit_Name'] = 'ch3_3'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'ch3_3_cond_tout'
    stream6['Layer'] = 'chilcond2sp3'
    stream6['Min_Flow'] = chiller3['ch3_condtin']['value']*chiller3['ch3_cratio']['value']
    stream6['Grad_Flow'] = chiller3['ch3_cond_maxdelt']['value']*chiller3['ch3_cratio']['value']
    stream6['InOut'] = 'out'
    
    streaminput = [stream6['Unit_Name'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Min_Flow'], stream6['Grad_Flow'], 
                   stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 7
    stream7 = {}
    stream7['Unit_Name'] = 'ch3_4'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'ch3_4_tout'
    stream7['Layer'] = 'chil2sp1'
    stream7['Min_Flow'] = chiller3['ch3_evaptret']['value']*chiller3['ch3_eratio']['value']
    stream7['Grad_Flow'] = -chiller3['ch3_maxdelt']['value']*chiller3['ch3_eratio']['value']
    stream7['InOut'] = 'out'
    
    streaminput = [stream7['Unit_Name'], stream7['Type'], stream7['Name'], stream7['Layer'], stream7['Min_Flow'], stream7['Grad_Flow'], 
                   stream7['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 8
    stream8 = {}
    stream8['Unit_Name'] = 'ch3_4'
    stream8['Type'] = 'balancing_only'
    stream8['Name'] = 'ch3_4_cond_tout'
    stream8['Layer'] = 'chilcond2sp3'
    stream8['Min_Flow'] = chiller3['ch3_condtin']['value']*chiller3['ch3_cratio']['value']
    stream8['Grad_Flow'] = chiller3['ch3_cond_maxdelt']['value']*chiller3['ch3_cratio']['value']
    stream8['InOut'] = 'out'
    
    streaminput = [stream8['Unit_Name'], stream8['Type'], stream8['Name'], stream8['Layer'], stream8['Min_Flow'], stream8['Grad_Flow'], 
                   stream8['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)   
    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'totaluse_ch3'
    eqn1['Type'] = 'unit_binary'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = 1
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)

    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Name'] = 'ch3_1_use'
    term1['Parent_unit'] = 'ch3_1'
    term1['Parent_eqn'] = 'totaluse_ch3'
    term1['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1

    terminput = [term1['Name'], term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2
    term2 = {}
    term2['Name'] = 'ch3_2_use'
    term2['Parent_unit'] = 'ch3_2'
    term2['Parent_eqn'] = 'totaluse_ch3'
    term2['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1

    terminput = [term2['Name'], term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 3
    term3 = {}
    term3['Name'] = 'ch3_3_use'
    term3['Parent_unit'] = 'ch3_3'
    term3['Parent_eqn'] = 'totaluse_ch3'
    term3['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term3['Coefficient'] = 1

    terminput = [term3['Name'], term3['Parent_unit'], term3['Parent_eqn'], term3['Parent_stream'], term3['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 4
    term4 = {}
    term4['Name'] = 'ch3_4_use'
    term4['Parent_unit'] = 'ch3_4'
    term4['Parent_eqn'] = 'totaluse_ch3'
    term4['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term4['Coefficient'] = 1
    
    terminput = [term4['Name'], term4['Parent_unit'], term4['Parent_eqn'], term4['Parent_stream'], term4['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms

    

