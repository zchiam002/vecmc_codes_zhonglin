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


def chiller1 (ch1_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from chiller1_compute import chiller1_compute
    import pandas as pd
    import numpy as np
    
    
    ##Model description: 
    ##Built based on Gordon-Ng's Universal Chiller model
    ##The COP is kept constant at 4 predefined steps in equally spaced intervals 
    ##The inputs to this function are variables to the eyes of the Master optimizer 
    
    ##Legend of input variables 
    
    ##ch1_em          - evaporator volume flowrate (m3/h)
    ##ch1_etret       - evaporator return temperature (K)
    ##ch1_cm          - condenser volume flowrate (m3/h)
    ##ch1_ctin        - condenser inlet temperature (K)
    ##ch1_tenwkflow   - total flowrate through parallel systems (m3/h)
    ##ch1_tcnwkflow   - total flowrate through parallel systems (m3/h)
    
    ##Processing list of master decision variables as parameters
    ch1_em = ch1_mdv['Value'][0]
    ch1_etret = ch1_mdv['Value'][1]
    ch1_cm = ch1_mdv['Value'][2]
    ch1_ctin = ch1_mdv['Value'][3]
    ch1_tenwkflow = ch1_mdv['Value'][4]                    ##Total flowrate through all evaporators of all chillers 
    ch1_tcnwkflow = ch1_mdv['Value'][5]                    ##Total flowrate through all condensers of all chillers 

    ##Define dictionary of values 

    chiller1 = {}
    ##Input constants 
    
    ##1
    ch1_evapflow = {}
    ch1_evapflow['value'] = ch1_em
    ch1_evapflow['units'] = 'm3/h'
    ch1_evapflow['status'] = 'cst_input'
    chiller1['ch1_evapflow'] = ch1_evapflow

    ##2
    ch1_evaptret = {}
    ch1_evaptret['value'] = ch1_etret
    ch1_evaptret['units'] = 'K'
    ch1_evaptret['status'] = 'cst_input'
    chiller1['ch1_evaptret'] = ch1_evaptret

    ##3
    ch1_condflow = {}
    ch1_condflow['value'] = ch1_cm
    ch1_condflow['units'] = 'm3/h'
    ch1_condflow['status'] = 'cst_input'
    chiller1['ch1_condflow'] = ch1_condflow

    ##4
    ch1_condtin = {}
    ch1_condtin['value'] = ch1_ctin
    ch1_condtin['units'] = 'K'
    ch1_condtin['status'] = 'cst_input'
    chiller1['ch1_condtin'] = ch1_condtin

    ##5
    ch1_totalenwkflow = {}
    ch1_totalenwkflow['value'] = ch1_tenwkflow
    ch1_totalenwkflow['units'] = 'm3/h'
    ch1_totalenwkflow['status'] = 'cst_input'
    chiller1['ch1_totalenwkflow'] = ch1_totalenwkflow

    ##6
    ch1_totalcnwkflow = {}
    ch1_totalcnwkflow['value'] = ch1_tcnwkflow
    ch1_totalcnwkflow['units'] = 'm3/h'
    ch1_totalcnwkflow['status'] = 'cst_input'
    chiller1['ch1_totalcnwkflow'] = ch1_totalcnwkflow

    ##Defined constants
    
    ##7
    ch1_rated_cap = {}                              #The rated capacity of the chiller
    ch1_rated_cap['value'] = 2000
    ch1_rated_cap['units'] = 'kWh'
    ch1_rated_cap['status'] = 'cst'
    chiller1['ch1_rated_cap'] = ch1_rated_cap
    
    ##8
    ch1_b0 = {}
    ch1_b0['value'] =  0.123020043325872            #Regression-derived constants
    ch1_b0['units'] = '-'
    ch1_b0['status'] = 'cst'
    chiller1['ch1_b0'] = ch1_b0

    ##9    
    ch1_b1 = {}
    ch1_b1['value'] =  1044.79734873891            
    ch1_b1['units'] = '-'
    ch1_b1['status'] = 'cst'
    chiller1['ch1_b1'] = ch1_b1
    
    ##10
    ch1_b2 = {}
    ch1_b2['value'] =  0.0204660495029597            
    ch1_b2['units'] = '-'
    ch1_b2['status'] = 'cst'
    chiller1['ch1_b2'] = ch1_b2

    ##11
    ch1_qc_coeff = {}
    ch1_qc_coeff['value'] = 1.09866273284186        #The relationship between Qe and Qc
    ch1_qc_coeff['units'] = '-'
    ch1_qc_coeff['status'] = 'cst'
    chiller1['ch1_qc_coeff'] = ch1_qc_coeff

    ##Dependent constants
    ch1_dc = np.zeros((11,1))                       #Initialize the list, note the number of constants
    
    ch1_dc[0,0] = chiller1['ch1_evapflow']['value']
    ch1_dc[1,0] = chiller1['ch1_evaptret']['value']
    ch1_dc[2,0] = chiller1['ch1_condflow']['value']
    ch1_dc[3,0] = chiller1['ch1_condtin']['value']
    ch1_dc[4,0] = chiller1['ch1_rated_cap']['value']
    ch1_dc[5,0] = chiller1['ch1_b0']['value']    
    ch1_dc[6,0] = chiller1['ch1_b1']['value']
    ch1_dc[7,0] = chiller1['ch1_b2']['value']
    ch1_dc[8,0] = chiller1['ch1_qc_coeff']['value']
    ch1_dc[9,0] = chiller1['ch1_totalenwkflow']['value']
    ch1_dc[10,0] = chiller1['ch1_totalcnwkflow']['value']

    ch1_dc_calc = chiller1_compute(ch1_dc)
    
    ##12
    ch1_int1 = {}
    ch1_int1['value'] = ch1_dc_calc[0,0]            #Intercpets of step-wise linearity
    ch1_int1['units'] = '-'
    ch1_int1['status'] = 'calc'
    chiller1['ch1_int1'] = ch1_int1

    ##13
    ch1_int2 = {}
    ch1_int2['value'] = ch1_dc_calc[1,0]
    ch1_int2['units'] = '-'
    ch1_int2['status'] = 'calc'
    chiller1['ch1_int2'] = ch1_int2

    ##14
    ch1_int3 = {}
    ch1_int3['value'] = ch1_dc_calc[2,0]
    ch1_int3['units'] = '-'
    ch1_int3['status'] = 'calc'
    chiller1['ch1_int3'] = ch1_int3

    ##15
    ch1_int4 = {}
    ch1_int4['value'] = ch1_dc_calc[3,0]
    ch1_int4['units'] = '-'
    ch1_int4['status'] = 'calc'
    chiller1['ch1_int4'] = ch1_int4

    ##16
    ch1_egrad1 = {}
    ch1_egrad1['value'] = ch1_dc_calc[4,0]
    ch1_egrad1['units'] = '-'
    ch1_egrad1['status'] = 'calc'
    chiller1['ch1_egrad1'] = ch1_egrad1

    ##17
    ch1_egrad2 = {}
    ch1_egrad2['value'] = ch1_dc_calc[5,0]
    ch1_egrad2['units'] = '-'
    ch1_egrad2['status'] = 'calc'
    chiller1['ch1_egrad2'] = ch1_egrad2  

    ##18
    ch1_egrad3 = {}
    ch1_egrad3['value'] = ch1_dc_calc[6,0]
    ch1_egrad3['units'] = '-'
    ch1_egrad3['status'] = 'calc'
    chiller1['ch1_egrad3'] = ch1_egrad3

    ##19
    ch1_egrad4 = {}
    ch1_egrad4['value'] = ch1_dc_calc[7,0]
    ch1_egrad4['units'] = '-'
    ch1_egrad4['status'] = 'calc'
    chiller1['ch1_egrad4'] = ch1_egrad4 
 
    ##20
    ch1_maxdelt = {}
    ch1_maxdelt['value'] = ch1_dc_calc[8,0]
    ch1_maxdelt['units'] = '-'
    ch1_maxdelt['status'] = 'calc'
    chiller1['ch1_maxdelt'] = ch1_maxdelt

    ##21
    ch1_eratio = {}
    ch1_eratio['value'] = ch1_dc_calc[9,0]
    ch1_eratio['units'] = '-'
    ch1_eratio['status'] = 'calc'
    chiller1['ch1_eratio'] = ch1_eratio

    ##22
    ch1_cratio = {}
    ch1_cratio['value'] = ch1_dc_calc[10,0]
    ch1_cratio['units'] = '-'
    ch1_cratio['status'] = 'calc'
    chiller1['ch1_cratio'] = ch1_cratio

    ##23
    ch1_cond_maxdelt = {}
    ch1_cond_maxdelt['value'] = ch1_dc_calc[11,0]
    ch1_cond_maxdelt['units'] = '-'
    ch1_cond_maxdelt['status'] = 'calc'
    chiller1['ch1_cond_maxdelt'] = ch1_cond_maxdelt    
    
    ##24
    ch1_f1 = {}
    ch1_f1['value'] = ch1_dc_calc[12,0]
    ch1_f1['units'] = '-'
    ch1_f1['status'] = 'calc'
    chiller1['ch1_f1'] = ch1_f1  
    
    ##25
    ch1_f2 = {}
    ch1_f2['value'] = ch1_dc_calc[13,0]
    ch1_f2['units'] = '-'
    ch1_f2['status'] = 'calc'
    chiller1['ch1_f2'] = ch1_f2  
    
    ##26
    ch1_f3 = {}
    ch1_f3['value'] = ch1_dc_calc[14,0]
    ch1_f3['units'] = '-'
    ch1_f3['status'] = 'calc'
    chiller1['ch1_f3'] = ch1_f3
    
    ##27
    ch1_f4 = {}
    ch1_f4['value'] = ch1_dc_calc[15,0]
    ch1_f4['units'] = '-'
    ch1_f4['status'] = 'calc'
    chiller1['ch1_f4'] = ch1_f4
    
    ##28
    ch1_f5 = {}
    ch1_f5['value'] = ch1_dc_calc[16,0]
    ch1_f5['units'] = '-'
    ch1_f5['status'] = 'calc'
    chiller1['ch1_f5'] = ch1_f5

    ##Unit definition 
    
    ##Unit 1
    ch1_1 = {}
    ch1_1['Name'] = 'ch1_1'
    ch1_1['Fmin'] = chiller1['ch1_f1']['value']
    ch1_1['Fmax'] = chiller1['ch1_f2']['value']
    ch1_1['Cost1'] = 0
    ch1_1['Cost2'] = 0
    ch1_1['Cinv1'] = 0
    ch1_1['Cinv2'] = 0
    ch1_1['Power1'] = chiller1['ch1_int1']['value']
    ch1_1['Power2'] = chiller1['ch1_egrad1']['value']
    ch1_1['Impact1'] = 0
    ch1_1['Impact2'] = 0

    unitinput = [ch1_1['Name'], ch1_1['Fmin'], ch1_1['Fmax'], ch1_1['Cost1'], ch1_1['Cost2'], ch1_1['Cinv1'], ch1_1['Cinv2'], 
                 ch1_1['Power1'], ch1_1['Power2'], ch1_1['Impact1'], ch1_1['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Unit 2
    ch1_2 = {}
    ch1_2['Name'] = 'ch1_2'
    ch1_2['Fmin'] = chiller1['ch1_f2']['value']
    ch1_2['Fmax'] = chiller1['ch1_f3']['value']
    ch1_2['Cost1'] = 0
    ch1_2['Cost2'] = 0
    ch1_2['Cinv1'] = 0
    ch1_2['Cinv2'] = 0
    ch1_2['Power1'] = chiller1['ch1_int2']['value']
    ch1_2['Power2'] = chiller1['ch1_egrad2']['value']
    ch1_2['Impact1'] = 0
    ch1_2['Impact2'] = 0
    
    unitinput = [ch1_2['Name'], ch1_2['Fmin'], ch1_2['Fmax'], ch1_2['Cost1'], ch1_2['Cost2'], ch1_2['Cinv1'], ch1_2['Cinv2'], 
                 ch1_2['Power1'], ch1_2['Power2'], ch1_2['Impact1'], ch1_2['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)  
    
    ##Unit 3
    ch1_3 = {}
    ch1_3['Name'] = 'ch1_3'
    ch1_3['Fmin'] = chiller1['ch1_f3']['value']
    ch1_3['Fmax'] = chiller1['ch1_f4']['value']
    ch1_3['Cost1'] = 0
    ch1_3['Cost2'] = 0
    ch1_3['Cinv1'] = 0
    ch1_3['Cinv2'] = 0
    ch1_3['Power1'] = chiller1['ch1_int3']['value']
    ch1_3['Power2'] = chiller1['ch1_egrad3']['value']
    ch1_3['Impact1'] = 0
    ch1_3['Impact2'] = 0

    unitinput = [ch1_3['Name'], ch1_3['Fmin'], ch1_3['Fmax'], ch1_3['Cost1'], ch1_3['Cost2'], ch1_3['Cinv1'], ch1_3['Cinv2'], 
                 ch1_3['Power1'], ch1_3['Power2'], ch1_3['Impact1'], ch1_3['Impact2']]    
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)  
    
    ##Unit 4
    ch1_4 = {}
    ch1_4['Name'] = 'ch1_4'
    ch1_4['Fmin'] = chiller1['ch1_f4']['value']
    ch1_4['Fmax'] = chiller1['ch1_f5']['value']
    ch1_4['Cost1'] = 0
    ch1_4['Cost2'] = 0
    ch1_4['Cinv1'] = 0
    ch1_4['Cinv2'] = 0
    ch1_4['Power1'] = chiller1['ch1_int4']['value']
    ch1_4['Power2'] = chiller1['ch1_egrad4']['value']
    ch1_4['Impact1'] = 0
    ch1_4['Impact2'] = 0
    
    unitinput = [ch1_4['Name'], ch1_4['Fmin'], ch1_4['Fmax'], ch1_4['Cost1'], ch1_4['Cost2'], ch1_4['Cinv1'], ch1_4['Cinv2'], 
                 ch1_4['Power1'], ch1_4['Power2'], ch1_4['Impact1'], ch1_4['Impact2']]      
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ch1_1'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch1_1_tout'
    stream1['Layer'] = 'chil2sp1'
    stream1['Min_Flow'] = chiller1['ch1_evaptret']['value']*chiller1['ch1_eratio']['value']
    stream1['Grad_Flow'] = -chiller1['ch1_maxdelt']['value']*chiller1['ch1_eratio']['value']
    stream1['InOut'] = 'out'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'ch1_1'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ch1_1_cond_tout'
    stream2['Layer'] = 'chilcond2sp3'
    stream2['Min_Flow'] = chiller1['ch1_condtin']['value']*chiller1['ch1_cratio']['value']
    stream2['Grad_Flow'] = chiller1['ch1_cond_maxdelt']['value']*chiller1['ch1_cratio']['value']
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 3
    stream3 = {}
    stream3['Unit_Name'] = 'ch1_2'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'ch1_2_tout'
    stream3['Layer'] = 'chil2sp1'
    stream3['Min_Flow'] = chiller1['ch1_evaptret']['value']*chiller1['ch1_eratio']['value']
    stream3['Grad_Flow'] = -chiller1['ch1_maxdelt']['value']*chiller1['ch1_eratio']['value']
    stream3['InOut'] = 'out'
    
    streaminput = [stream3['Unit_Name'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Min_Flow'], stream3['Grad_Flow'], 
                   stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 4
    stream4 = {}
    stream4['Unit_Name'] = 'ch1_2'
    stream4['Type'] = 'balancing_only'
    stream4['Name'] = 'ch1_2_cond_tout'
    stream4['Layer'] = 'chilcond2sp3'
    stream4['Min_Flow'] = chiller1['ch1_condtin']['value']*chiller1['ch1_cratio']['value']
    stream4['Grad_Flow'] = chiller1['ch1_cond_maxdelt']['value']*chiller1['ch1_cratio']['value']
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Unit_Name'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Min_Flow'], stream4['Grad_Flow'], 
                   stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 5
    stream5 = {}
    stream5['Unit_Name'] = 'ch1_3'
    stream5['Type'] = 'balancing_only'
    stream5['Name'] = 'ch1_3_tout'
    stream5['Layer'] = 'chil2sp1'
    stream5['Min_Flow'] = chiller1['ch1_evaptret']['value']*chiller1['ch1_eratio']['value']
    stream5['Grad_Flow'] = -chiller1['ch1_maxdelt']['value']*chiller1['ch1_eratio']['value']
    stream5['InOut'] = 'out'
    
    streaminput = [stream5['Unit_Name'], stream5['Type'], stream5['Name'], stream5['Layer'], stream5['Min_Flow'], stream5['Grad_Flow'], 
                   stream5['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 6
    stream6 = {}
    stream6['Unit_Name'] = 'ch1_3'
    stream6['Type'] = 'balancing_only'
    stream6['Name'] = 'ch1_3_cond_tout'
    stream6['Layer'] = 'chilcond2sp3'
    stream6['Min_Flow'] = chiller1['ch1_condtin']['value']*chiller1['ch1_cratio']['value']
    stream6['Grad_Flow'] = chiller1['ch1_cond_maxdelt']['value']*chiller1['ch1_cratio']['value']
    stream6['InOut'] = 'out'
    
    streaminput = [stream6['Unit_Name'], stream6['Type'], stream6['Name'], stream6['Layer'], stream6['Min_Flow'], stream6['Grad_Flow'], 
                   stream6['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 7
    stream7 = {}
    stream7['Unit_Name'] = 'ch1_4'
    stream7['Type'] = 'balancing_only'
    stream7['Name'] = 'ch1_4_tout'
    stream7['Layer'] = 'chil2sp1'
    stream7['Min_Flow'] = chiller1['ch1_evaptret']['value']*chiller1['ch1_eratio']['value']
    stream7['Grad_Flow'] = -chiller1['ch1_maxdelt']['value']*chiller1['ch1_eratio']['value']
    stream7['InOut'] = 'out'
    
    streaminput = [stream7['Unit_Name'], stream7['Type'], stream7['Name'], stream7['Layer'], stream7['Min_Flow'], stream7['Grad_Flow'], 
                   stream7['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 8
    stream8 = {}
    stream8['Unit_Name'] = 'ch1_4'
    stream8['Type'] = 'balancing_only'
    stream8['Name'] = 'ch1_4_cond_tout'
    stream8['Layer'] = 'chilcond2sp3'
    stream8['Min_Flow'] = chiller1['ch1_condtin']['value']*chiller1['ch1_cratio']['value']
    stream8['Grad_Flow'] = chiller1['ch1_cond_maxdelt']['value']*chiller1['ch1_cratio']['value']
    stream8['InOut'] = 'out'
    
    streaminput = [stream8['Unit_Name'], stream8['Type'], stream8['Name'], stream8['Layer'], stream8['Min_Flow'], stream8['Grad_Flow'], 
                   stream8['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Constraint definition
    
    ##Equation definitions
    
    ##Equation 1
    eqn1 = {}
    eqn1['Name'] = 'totaluse_ch1'
    eqn1['Type'] = 'unit_binary'
    eqn1['Sign'] = 'less_than_equal_to'
    eqn1['RHS_value'] = 1
    
    eqninput = [eqn1['Name'], eqn1['Type'], eqn1['Sign'], eqn1['RHS_value']]
    eqninputdf = pd.DataFrame(data = [eqninput], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns = cons_eqns.append(eqninputdf, ignore_index=True)

    ##Equation terms
    
    ##Term 1
    term1 = {}
    term1['Name'] = 'ch1_1_use'
    term1['Parent_unit'] = 'ch1_1'
    term1['Parent_eqn'] = 'totaluse_ch1'
    term1['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term1['Coefficient'] = 1

    terminput = [term1['Name'], term1['Parent_unit'], term1['Parent_eqn'], term1['Parent_stream'], term1['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 2
    term2 = {}
    term2['Name'] = 'ch1_2_use'
    term2['Parent_unit'] = 'ch1_2'
    term2['Parent_eqn'] = 'totaluse_ch1'
    term2['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term2['Coefficient'] = 1

    terminput = [term2['Name'], term2['Parent_unit'], term2['Parent_eqn'], term2['Parent_stream'], term2['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 3
    term3 = {}
    term3['Name'] = 'ch1_3_use'
    term3['Parent_unit'] = 'ch1_3'
    term3['Parent_eqn'] = 'totaluse_ch1'
    term3['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term3['Coefficient'] = 1

    terminput = [term3['Name'], term3['Parent_unit'], term3['Parent_eqn'], term3['Parent_stream'], term3['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)
    
    ##Term 4
    term4 = {}
    term4['Name'] = 'ch1_4_use'
    term4['Parent_unit'] = 'ch1_4'
    term4['Parent_eqn'] = 'totaluse_ch1'
    term4['Parent_stream'] = '-'                            ##Only applicable for stream_limit types 
    term4['Coefficient'] = 1
    
    terminput = [term4['Name'], term4['Parent_unit'], term4['Parent_eqn'], term4['Parent_stream'], term4['Coefficient']]
    terminputdf = pd.DataFrame(data = [terminput], columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    cons_eqns_terms = cons_eqns_terms.append(terminputdf, ignore_index=True)

    return utilitylist, streams, cons_eqns, cons_eqns_terms
        
    
    