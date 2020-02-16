## This is a chiller condenser return model for temperature and flowrate, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt

def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'process'
    return unit_type
    
def chiller_cond_ret_mflow (cg_c_r_mf_mdv, processlist, streams, cons_eqns, cons_eqns_terms):
    import pandas as pd 

    ##Model description:
    ##This model represents the required return temperature demand from the chiller model 
    
    ##Legend of input variables 
    
    ##ch_c_r_ctret       --- condenser return temperature (K)
    ##ch_c_r_mret        --- condenser netwrok total mass flowrate (m3/h)
    
    ##Processing list of master decision variables as parameters 
    ch_c_r_tret = cg_c_r_mf_mdv['Value'][0]
    ch_c_r_mret = cg_c_r_mf_mdv['Value'][1]

    ##Define dictionary of values 
    
    chiller_cond_ret_mflow = {}
    ##Input constants 
    
    ##1
    ch_r_crettemp = {}
    ch_r_crettemp['value'] = ch_c_r_tret
    ch_r_crettemp['units'] = 'K'
    ch_r_crettemp['status'] = 'cst_input'
    chiller_cond_ret_mflow['ch_r_crettemp'] = ch_r_crettemp    

    ##2
    ch_r_cretflow = {}
    ch_r_cretflow['value'] = ch_c_r_mret
    ch_r_cretflow['units'] = 'K'
    ch_r_cretflow['status'] = 'cst_input'
    chiller_cond_ret_mflow['ch_r_cretflow'] = ch_r_cretflow   

    ##Unit definition 
    
    ##Unit 1
    ch_ret_mf = {}
    ch_ret_mf['Name'] = 'ch_ret_mf_cond'
    ch_ret_mf['Variable1'] = 'tcond_ret'                                                                                                     
    ch_ret_mf['Variable2'] = 'm_perc' 
    ch_ret_mf['Fmin_v1'] = 0 
    ch_ret_mf['Fmax_v1'] = chiller_cond_ret_mflow['ch_r_erettemp']['value']                                                                                                                   
    ch_ret_mf['Fmin_v2'] = 0                                                                                                          
    ch_ret_mf['Fmax_v2'] = 1                                                                              
    ch_ret_mf['Coeff_v1_2'] = 0                                                                                                                
    ch_ret_mf['Coeff_v1_1'] = 0          
    ch_ret_mf['Coeff_v2_2'] = 0
    ch_ret_mf['Coeff_v2_1'] = 0
    ch_ret_mf['Coeff_v1_v2'] = 0 
    ch_ret_mf['Coeff_cst'] = 0
    ch_ret_mf['Fmin'] = 0
    ch_ret_mf['Fmax'] = 0
    ch_ret_mf['Cost_v1_2'] = 0
    ch_ret_mf['Cost_v1_1'] = 0
    ch_ret_mf['Cost_v2_2'] = 0
    ch_ret_mf['Cost_v2_1'] = 0
    ch_ret_mf['Cost_v1_v2'] = 0
    ch_ret_mf['Cost_cst'] = 0
    ch_ret_mf['Cinv_v1_2'] = 0
    ch_ret_mf['Cinv_v1_1'] = 0
    ch_ret_mf['Cinv_v2_2'] = 0
    ch_ret_mf['Cinv_v2_1'] = 0
    ch_ret_mf['Cinv_v1_v2'] = 0
    ch_ret_mf['Cinv_cst'] = 0
    ch_ret_mf['Power_v1_2'] = 0
    ch_ret_mf['Power_v1_1'] = 0
    ch_ret_mf['Power_v2_2'] = 0
    ch_ret_mf['Power_v2_1'] = 0
    ch_ret_mf['Power_v1_v2'] = 0
    ch_ret_mf['Power_cst'] = 0
    ch_ret_mf['Impact_v1_2'] = 0
    ch_ret_mf['Impact_v1_1'] = 0
    ch_ret_mf['Impact_v2_2'] = 0
    ch_ret_mf['Impact_v2_1'] = 0
    ch_ret_mf['Impact_v1_v2'] = 0
    ch_ret_mf['Impact_cst'] = 0

    unitinput = [ch_ret_mf['Name'], ch_ret_mf['Variable1'], ch_ret_mf['Variable2'], ch_ret_mf['Fmin_v1'], ch_ret_mf['Fmax_v1'], ch_ret_mf['Fmin_v2'], ch_ret_mf['Fmax_v2'], ch_ret_mf['Coeff_v1_2'], 
                ch_ret_mf['Coeff_v1_1'], ch_ret_mf['Coeff_v2_2'], ch_ret_mf['Coeff_v2_1'], ch_ret_mf['Coeff_v1_v2'], ch_ret_mf['Coeff_cst'], ch_ret_mf['Fmin'], ch_ret_mf['Fmax'], ch_ret_mf['Cost_v1_2'], 
                ch_ret_mf['Cost_v1_1'], ch_ret_mf['Cost_v2_2'], ch_ret_mf['Cost_v2_1'], ch_ret_mf['Cost_v1_v2'], ch_ret_mf['Cost_cst'], ch_ret_mf['Cinv_v1_2'], ch_ret_mf['Cinv_v1_1'], ch_ret_mf['Cinv_v2_2'], 
                ch_ret_mf['Cinv_v2_1'], ch_ret_mf['Cinv_v1_v2'], ch_ret_mf['Cinv_cst'], ch_ret_mf['Power_v1_2'], ch_ret_mf['Power_v1_1'], ch_ret_mf['Power_v2_2'], ch_ret_mf['Power_v2_1'], 
                ch_ret_mf['Power_v1_v2'], ch_ret_mf['Power_cst'], ch_ret_mf['Impact_v1_2'], ch_ret_mf['Impact_v1_1'], ch_ret_mf['Impact_v2_2'], ch_ret_mf['Impact_v2_1'], ch_ret_mf['Impact_v1_v2'], 
                ch_ret_mf['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    processlist = processlist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    stream1 = {}                                                                
    stream1['Parent'] = 'ch_ret_mf_cond'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ch_ret_mf_cond_mfin'
    stream1['Layer'] = 'chil2condret_flow'
    stream1['Stream_coeff_v1_2'] = 0
    stream1['Stream_coeff_v1_1'] = 0
    stream1['Stream_coeff_v2_2'] = 0
    stream1['Stream_coeff_v2_1'] = chiller_cond_ret_mflow['ch_r_cretflow']['value'] 
    stream1['Stream_coeff_v1_v2'] = 0
    stream1['Stream_coeff_cst'] = 0
    stream1['InOut'] = 'in'
    
    streaminput = [stream1['Parent'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Stream_coeff_v1_2'], stream1['Stream_coeff_v1_1'], stream1['Stream_coeff_v2_2'],
                   stream1['Stream_coeff_v2_1'], stream1['Stream_coeff_v1_v2'], stream1['Stream_coeff_cst'], stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
    return processlist, streams, cons_eqns, cons_eqns_terms