## This is a chiller condenser model, formulated as an input to a quadratic program

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype_chiller1_cond_4nc (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type

def chiller1_cond_4nc (ch1_c_4nc_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):

    import pandas as pd
    import numpy as np
    
    ##This is the condenser side of chiller1_evap_4nc
    
    ##Model description: 
    ##Built based on Gordon-Ng's Universal Chiller model
    ##The COP is kept constant at 4 predefined steps in equally spaced intervals 
    ##The inputs to this function are variables to the eyes of the Master optimizer 
    
    ##ch1_c_4nc_mdv --- the master decision variables which are used as parameters at this stage 
    ##utilitylist --- a dataframe to hold essential values for writing the MILP script 
    ##streams --- a dataframe to write connections to other units 
    ##cons_eqns --- additional constraints are explicitly stated here 
    ##cons_eqns_terms --- the terms to the constraints 
    
    ##Defining inputs 
    
    ##Processing list of master decision variables
    ch1_4nc_tcnwkflow = ch1_c_4nc_mdv['Value'][0]
    ch1_4nc_ctin = ch1_c_4nc_mdv['Value'][1]
    
    ##Defined constants 
    ch1_4nc_cp = 4.2
    ch1_4nc_tout_max = 7 + ch1_4nc_ctin
    ch1_4nc_req_flow = 407
    ch1_4nc_perc = ch1_4nc_req_flow / ch1_4nc_tcnwkflow
     
#################################################################################################################################################################################################        
    ##Unit definition 
    
    ##Evaporator stepwise
    ud = {}
    ud['Name'] = 'ch1_4nc_cond'
    ud['Variable1'] = 'm_perc'                                                                                      ##Percentage of flowrate from the entire condenser network 
    ud['Variable2'] = 't_out'                                                                                        ##Water outlet temperature of the condenser 
    ud['Fmin_v1'] = 0.99 * ch1_4nc_perc
    ud['Fmax_v1'] = 1.01 * ch1_4nc_perc                                                                             ##Maximum percentage is 100% 
    ud['Fmin_v2'] = 0                                                                                               
    ud['Fmax_v2'] = 1                                                                                               
    ud['Coeff_v1_2'] = 0                                                                                            
    ud['Coeff_v1_1'] = 0             
    ud['Coeff_v2_2'] = 0
    ud['Coeff_v2_1'] = 0
    ud['Coeff_v1_v2'] = 0 
    ud['Coeff_cst'] = 0
    ud['Fmin'] = 0
    ud['Fmax'] = 0
    ud['Cost_v1_2'] = 0
    ud['Cost_v1_1'] = 0
    ud['Cost_v2_2'] = 0
    ud['Cost_v2_1'] = 0
    ud['Cost_v1_v2'] = 0
    ud['Cost_cst'] = 0
    ud['Cinv_v1_2'] = 0
    ud['Cinv_v1_1'] = 0
    ud['Cinv_v2_2'] = 0
    ud['Cinv_v2_1'] = 0
    ud['Cinv_v1_v2'] = 0
    ud['Cinv_cst'] = 0
    ud['Power_v1_2'] = 0
    ud['Power_v1_1'] = 0
    ud['Power_v2_2'] = 0
    ud['Power_v2_1'] = 0
    ud['Power_v1_v2'] = 0
    ud['Power_cst'] = 0                                                         
    ud['Impact_v1_2'] = 0
    ud['Impact_v1_1'] = 0
    ud['Impact_v2_2'] = 0
    ud['Impact_v2_1'] = 0
    ud['Impact_v1_v2'] = 0
    ud['Impact_cst'] = 0

    unitinput = [ud['Name'], ud['Variable1'], ud['Variable2'], ud['Fmin_v1'], ud['Fmax_v1'], ud['Fmin_v2'], ud['Fmax_v2'], ud['Coeff_v1_2'], 
                ud['Coeff_v1_1'], ud['Coeff_v2_2'], ud['Coeff_v2_1'], ud['Coeff_v1_v2'], ud['Coeff_cst'], ud['Fmin'], ud['Fmax'], ud['Cost_v1_2'], 
                ud['Cost_v1_1'], ud['Cost_v2_2'], ud['Cost_v2_1'], ud['Cost_v1_v2'], ud['Cost_cst'], ud['Cinv_v1_2'], ud['Cinv_v1_1'], ud['Cinv_v2_2'], 
                ud['Cinv_v2_1'], ud['Cinv_v1_v2'], ud['Cinv_cst'], ud['Power_v1_2'], ud['Power_v1_1'], ud['Power_v2_2'], ud['Power_v2_1'], 
                ud['Power_v1_v2'], ud['Power_cst'], ud['Impact_v1_2'], ud['Impact_v1_1'], ud['Impact_v2_2'], ud['Impact_v2_1'], ud['Impact_v1_v2'], 
                ud['Impact_cst']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)   
        
####################################################################################################################################################################################################        
    ##Stream definition 
    
    ##Stream --- energy rejection
    stream = {}                         
    stream['Parent'] = 'ch1_4nc_cond'
    stream['Type'] = 'energy_reverse'
    stream['Name'] = 'ch1_4nc_cond_energyin'
    stream['Layer'] = 'ch1_evap2cond'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = 0
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = (ch1_4nc_tcnwkflow * 998.2 / 3600) * ch1_4nc_cp * (ch1_4nc_tout_max - ch1_4nc_ctin)
    stream['Stream_coeff_cst'] = 0
    stream['InOut'] = 'in'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)

    ##Stream --- flowrate 
    stream = {}                                                                
    stream['Parent'] = 'ch1_4nc_cond'
    stream['Type'] = 'flow_reverse'
    stream['Name'] = 'ch1_4nc_cond_mfout'
    stream['Layer'] = 'ch1_2_ch1condnwk_flow'
    stream['Stream_coeff_v1_2'] = 0
    stream['Stream_coeff_v1_1'] = ch1_4nc_tcnwkflow 
    stream['Stream_coeff_v2_2'] = 0
    stream['Stream_coeff_v2_1'] = 0
    stream['Stream_coeff_v1_v2'] = 0
    stream['Stream_coeff_cst'] = 0
    stream['InOut'] = 'out'
    
    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)
    
#    ##Stream --- temperature out of condenser
#    stream = {}                                                                
#    stream['Parent'] = 'ch1_4nc_cond'
#    stream['Type'] = 'temp_chil'
#    stream['Name'] = 'ch1_4nc_cond_tout'
#    stream['Layer'] = 'chilcond2sp3_temp'
#    stream['Stream_coeff_v1_2'] = 0
#    stream['Stream_coeff_v1_1'] = ch1_4nc_ctin 
#    stream['Stream_coeff_v2_2'] = 0
#    stream['Stream_coeff_v2_1'] = 0
#    stream['Stream_coeff_v1_v2'] = ch1_4nc_tout_max - ch1_4nc_ctin
#    stream['Stream_coeff_cst'] = 0
#    stream['InOut'] = 'out'
#    
#    streaminput = [stream['Parent'], stream['Type'], stream['Name'], stream['Layer'], stream['Stream_coeff_v1_2'], stream['Stream_coeff_v1_1'], stream['Stream_coeff_v2_2'],
#                   stream['Stream_coeff_v2_1'], stream['Stream_coeff_v1_v2'], stream['Stream_coeff_cst'], stream['InOut']]
#    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
#                                                          'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
#    streams = streams.append(streamdf, ignore_index=True)

############################################################################################################################################################################################################

    ##Constraint definition
    
    ##Equation definitions

    return utilitylist, streams, cons_eqns, cons_eqns_terms    