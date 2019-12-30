##This model consist of 5 units (as many as the number of parallel streams in the distribution network) to consolidate the pressure drop 
##associated with each branch 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type
    
def dist_nwk_consol (distnwk_consol_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd
    import numpy as np
    
    ##Model description: 
    ##Individual models to capture the components of the pressure drop

    ##Define dictionary of values 

    dist_nwk_consol = {}

    ##Defined constants
    
    ##1
    dn_consol_gv2delpmax = {}
    dn_consol_gv2delpmax['value'] = 100
    dn_consol_gv2delpmax['units'] = 'mh20'
    dn_consol_gv2delpmax['status'] = 'cst'
    dist_nwk_consol['dn_consol_gv2delpmax'] = dn_consol_gv2delpmax

    ##2
    dn_consol_hsbdelpmax = {}
    dn_consol_hsbdelpmax['value'] = 100
    dn_consol_hsbdelpmax['units'] = 'mh20'
    dn_consol_hsbdelpmax['status'] = 'cst'
    dist_nwk_consol['dn_consol_hsbdelpmax'] = dn_consol_hsbdelpmax

    ##3
    dn_consol_pfadelpmax = {}
    dn_consol_pfadelpmax['value'] = 100
    dn_consol_pfadelpmax['units'] = 'mh20'
    dn_consol_pfadelpmax['status'] = 'cst'
    dist_nwk_consol['dn_consol_pfadelpmax'] = dn_consol_pfadelpmax

    ##4
    dn_consol_serdelpmax = {}
    dn_consol_serdelpmax['value'] = 100
    dn_consol_serdelpmax['units'] = 'mh20'
    dn_consol_serdelpmax['status'] = 'cst'
    dist_nwk_consol['dn_consol_serdelpmax'] = dn_consol_serdelpmax

    ##5
    dn_consol_firdelpmax = {}
    dn_consol_firdelpmax['value'] = 100
    dn_consol_firdelpmax['units'] = 'mh20'
    dn_consol_firdelpmax['status'] = 'cst'
    dist_nwk_consol['dn_consol_firdelpmax'] = dn_consol_firdelpmax
    
    ##Unit definition 
    
    ##Unit 1
    delp_gv2 = {}
    delp_gv2['Name'] = 'delp_gv2'
    delp_gv2['Variable1'] = 'delp'
    delp_gv2['Variable2'] = '-'
    delp_gv2['Fmin_v1'] = 0
    delp_gv2['Fmax_v1'] = dist_nwk_consol['dn_consol_gv2delpmax']['value'] 
    delp_gv2['Fmin_v2'] = 0                                                
    delp_gv2['Fmax_v2'] = 0
    delp_gv2['Coeff_v1_2'] = 0                                     
    delp_gv2['Coeff_v1_1'] = 0                                                 
    delp_gv2['Coeff_v2_2'] = 0
    delp_gv2['Coeff_v2_1'] = 0
    delp_gv2['Coeff_v1_v2'] = 0
    delp_gv2['Coeff_cst'] = 0
    delp_gv2['Fmin'] = 0
    delp_gv2['Fmax'] = 0
    delp_gv2['Cost_v1_2'] = 0
    delp_gv2['Cost_v1_1'] = 0
    delp_gv2['Cost_v2_2'] = 0
    delp_gv2['Cost_v2_1'] = 0
    delp_gv2['Cost_v1_v2'] = 0
    delp_gv2['Cost_cst'] = 0
    delp_gv2['Cinv_v1_2'] = 0
    delp_gv2['Cinv_v1_1'] = 0
    delp_gv2['Cinv_v2_2'] = 0
    delp_gv2['Cinv_v2_1'] = 0
    delp_gv2['Cinv_v1_v2'] = 0
    delp_gv2['Cinv_cst'] = 0
    delp_gv2['Power_v1_2'] = 0
    delp_gv2['Power_v1_1'] = 0
    delp_gv2['Power_v2_2'] = 0
    delp_gv2['Power_v2_1'] = 0
    delp_gv2['Power_v1_v2'] = 0
    delp_gv2['Power_cst'] = 0
    delp_gv2['Impact_v1_2'] = 0
    delp_gv2['Impact_v1_1'] = 0
    delp_gv2['Impact_v2_2'] = 0
    delp_gv2['Impact_v2_1'] = 0
    delp_gv2['Impact_v1_v2'] = 0
    delp_gv2['Impact_cst'] = 0

    unitinput = [delp_gv2['Name'], delp_gv2['Variable1'], delp_gv2['Variable2'], delp_gv2['Fmin_v1'], delp_gv2['Fmax_v1'], delp_gv2['Fmin_v2'], delp_gv2['Fmax_v2'], delp_gv2['Coeff_v1_2'], 
                delp_gv2['Coeff_v1_1'], delp_gv2['Coeff_v2_2'], delp_gv2['Coeff_v2_1'], delp_gv2['Coeff_v1_v2'], delp_gv2['Coeff_cst'], delp_gv2['Fmin'], delp_gv2['Fmax'], delp_gv2['Cost_v1_2'], 
                delp_gv2['Cost_v1_1'], delp_gv2['Cost_v2_2'], delp_gv2['Cost_v2_1'], delp_gv2['Cost_v1_v2'], delp_gv2['Cost_cst'], delp_gv2['Cinv_v1_2'], delp_gv2['Cinv_v1_1'], delp_gv2['Cinv_v2_2'], 
                delp_gv2['Cinv_v2_1'], delp_gv2['Cinv_v1_v2'], delp_gv2['Cinv_cst'], delp_gv2['Power_v1_2'], delp_gv2['Power_v1_1'], delp_gv2['Power_v2_2'], delp_gv2['Power_v2_1'], 
                delp_gv2['Power_v1_v2'], delp_gv2['Power_cst'], delp_gv2['Impact_v1_2'], delp_gv2['Impact_v1_1'], delp_gv2['Impact_v2_2'], delp_gv2['Impact_v2_1'], delp_gv2['Impact_v1_v2'], 
                delp_gv2['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)   

    ##Unit 2
    delp_hsb = {}
    delp_hsb['Name'] = 'delp_hsb'
    delp_hsb['Variable1'] = 'delp'
    delp_hsb['Variable2'] = '-'
    delp_hsb['Fmin_v1'] = 0
    delp_hsb['Fmax_v1'] = dist_nwk_consol['dn_consol_hsbdelpmax']['value'] 
    delp_hsb['Fmin_v2'] = 0                                                
    delp_hsb['Fmax_v2'] = 0
    delp_hsb['Coeff_v1_2'] = 0                                     
    delp_hsb['Coeff_v1_1'] = 0                                                 
    delp_hsb['Coeff_v2_2'] = 0
    delp_hsb['Coeff_v2_1'] = 0
    delp_hsb['Coeff_v1_v2'] = 0
    delp_hsb['Coeff_cst'] = 0
    delp_hsb['Fmin'] = 0
    delp_hsb['Fmax'] = 0
    delp_hsb['Cost_v1_2'] = 0
    delp_hsb['Cost_v1_1'] = 0
    delp_hsb['Cost_v2_2'] = 0
    delp_hsb['Cost_v2_1'] = 0
    delp_hsb['Cost_v1_v2'] = 0
    delp_hsb['Cost_cst'] = 0
    delp_hsb['Cinv_v1_2'] = 0
    delp_hsb['Cinv_v1_1'] = 0
    delp_hsb['Cinv_v2_2'] = 0
    delp_hsb['Cinv_v2_1'] = 0
    delp_hsb['Cinv_v1_v2'] = 0
    delp_hsb['Cinv_cst'] = 0
    delp_hsb['Power_v1_2'] = 0
    delp_hsb['Power_v1_1'] = 0
    delp_hsb['Power_v2_2'] = 0
    delp_hsb['Power_v2_1'] = 0
    delp_hsb['Power_v1_v2'] = 0
    delp_hsb['Power_cst'] = 0
    delp_hsb['Impact_v1_2'] = 0
    delp_hsb['Impact_v1_1'] = 0
    delp_hsb['Impact_v2_2'] = 0
    delp_hsb['Impact_v2_1'] = 0
    delp_hsb['Impact_v1_v2'] = 0
    delp_hsb['Impact_cst'] = 0

    unitinput = [delp_hsb['Name'], delp_hsb['Variable1'], delp_hsb['Variable2'], delp_hsb['Fmin_v1'], delp_hsb['Fmax_v1'], delp_hsb['Fmin_v2'], delp_hsb['Fmax_v2'], delp_hsb['Coeff_v1_2'], 
                delp_hsb['Coeff_v1_1'], delp_hsb['Coeff_v2_2'], delp_hsb['Coeff_v2_1'], delp_hsb['Coeff_v1_v2'], delp_hsb['Coeff_cst'], delp_hsb['Fmin'], delp_hsb['Fmax'], delp_hsb['Cost_v1_2'], 
                delp_hsb['Cost_v1_1'], delp_hsb['Cost_v2_2'], delp_hsb['Cost_v2_1'], delp_hsb['Cost_v1_v2'], delp_hsb['Cost_cst'], delp_hsb['Cinv_v1_2'], delp_hsb['Cinv_v1_1'], delp_hsb['Cinv_v2_2'], 
                delp_hsb['Cinv_v2_1'], delp_hsb['Cinv_v1_v2'], delp_hsb['Cinv_cst'], delp_hsb['Power_v1_2'], delp_hsb['Power_v1_1'], delp_hsb['Power_v2_2'], delp_hsb['Power_v2_1'], 
                delp_hsb['Power_v1_v2'], delp_hsb['Power_cst'], delp_hsb['Impact_v1_2'], delp_hsb['Impact_v1_1'], delp_hsb['Impact_v2_2'], delp_hsb['Impact_v2_1'], delp_hsb['Impact_v1_v2'], 
                delp_hsb['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)   
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}                                                                ##The delp into this consolidating unit 
    stream1['Parent'] = 'delp_gv2'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'delp_gv2_in'
    stream1['Layer'] = 'ice_nwkandgv2_nwk_delp'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 1
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = 0
    stream1['Stream_coeff_v1_v2'] = 0
    stream1['Stream_coeff_cst'] = 0
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 2
    stream2 = {}                                                                ##The delp out of ths consolidating unit  
    stream2['Parent'] = 'delp_gv2'
    stream2['Type'] = 'network_parallel'
    stream2['Name'] = 'delp_gv2_out'
    stream2['Layer'] = 'dist_nwk2_selected_pump1'
    stream2['Stream_coeff_v1_2'] = 0
    stream2['Stream_coeff_v1_1'] = 1
    stream2['Stream_coeff_v2_2'] = 0
    stream2['Stream_coeff_v2_1'] = 0
    stream2['Stream_coeff_v1_v2'] = 0
    stream2['Stream_coeff_cst'] = 0
    stream2['InOut'] = 'out'
    
    streaminput = [stream2['Parent'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Stream_coeff_v1_2'], stream2['Stream_coeff_v1_1'], stream2['Stream_coeff_v2_2'],
                   stream2['Stream_coeff_v2_1'], stream2['Stream_coeff_v1_v2'], stream2['Stream_coeff_cst'], stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    ##Stream 3
    stream3 = {}                                                                ##The delp into this consolidating unit 
    stream3['Parent'] = 'delp_hsb'
    stream3['Type'] = 'balancing_only'
    stream3['Name'] = 'delp_hsb_in'
    stream3['Layer'] = 'ice_nwkandhsb_nwk_delp'
    stream3['Stream_coeff_v1_2'] = 0
    stream3['Stream_coeff_v1_1'] = 1
    stream3['Stream_coeff_v2_2'] = 0
    stream3['Stream_coeff_v2_1'] = 0
    stream3['Stream_coeff_v1_v2'] = 0
    stream3['Stream_coeff_cst'] = 0
    stream3['InOut'] = 'in'
    
    streaminput = [stream3['Parent'], stream3['Type'], stream3['Name'], stream3['Layer'], stream3['Stream_coeff_v1_2'], stream3['Stream_coeff_v1_1'], stream3['Stream_coeff_v2_2'],
                   stream3['Stream_coeff_v2_1'], stream3['Stream_coeff_v1_v2'], stream3['Stream_coeff_cst'], stream3['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream 4
    stream4 = {}                                                                ##The delp out of ths consolidating unit  
    stream4['Parent'] = 'delp_hsb'
    stream4['Type'] = 'network_parallel'
    stream4['Name'] = 'delp_hsb_out'
    stream4['Layer'] = 'dist_nwk2_selected_pump1'
    stream4['Stream_coeff_v1_2'] = 0
    stream4['Stream_coeff_v1_1'] = 1
    stream4['Stream_coeff_v2_2'] = 0
    stream4['Stream_coeff_v2_1'] = 0
    stream4['Stream_coeff_v1_v2'] = 0
    stream4['Stream_coeff_cst'] = 0
    stream4['InOut'] = 'out'
    
    streaminput = [stream4['Parent'], stream4['Type'], stream4['Name'], stream4['Layer'], stream4['Stream_coeff_v1_2'], stream4['Stream_coeff_v1_1'], stream4['Stream_coeff_v2_2'],
                   stream4['Stream_coeff_v2_1'], stream4['Stream_coeff_v1_v2'], stream4['Stream_coeff_cst'], stream4['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms