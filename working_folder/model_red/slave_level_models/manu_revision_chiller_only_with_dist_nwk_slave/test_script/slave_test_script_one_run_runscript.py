##This script runs the main script for the slave_test_script_one_run

def run_slave_test_script_one_run ():

    import pandas as pd
    import numpy as np
    from datetime import datetime
    startTime = datetime.now()
    from slave_test_script_one_run import slave_test_script_one_run 
    
    dt = 'high'
    ah = 0
    t_evap_ret = 3 + 273.15
    t_e_flow = 400
    ps = 1
    bp = 2
    
    slave_test_script_one_run(dt, ah, t_evap_ret, t_e_flow, ps, bp)
    
    return

#########################################################################################################################################################################
##Running the test script for base_case one run
if __name__ == '__main__':
    run_slave_test_script_one_run ()
    