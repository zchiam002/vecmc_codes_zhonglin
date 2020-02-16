\\ Objective function for all utilities and processes 
 
Minimize 

obj: 0.0 sp1_temp_t_inout + 0.0 sp1_temp_y + 0.0 sp2_temp_t_inout + 0.0 sp2_temp_y + 82.0718991851011 ch1_1_evap_u0 + 104.21016001956207 ch1_1_evap_u0_y + 82.0718991851011 ch1_1_evap_v0 + 0.0 ch1_1_evap_v0_y - 82.0718991851011 ch1_1_evap_u1 + 268.3539583897643 ch1_1_evap_u1_y + 246.2156975553033 ch1_1_evap_v1 + 0.0 ch1_1_evap_v1_y + 66.260176378973 ch2_1_evap_u0 + 393.9334001239313 ch2_1_evap_u0_y + 66.260176378973 ch2_1_evap_v0 + 0.0 ch2_1_evap_v0_y - 66.260176378973 ch2_1_evap_u1 + 526.4537528818773 ch2_1_evap_u1_y + 198.780529136919 ch2_1_evap_v1 + 0.0 ch2_1_evap_v1_y + 66.260176378973 ch3_1_evap_u0 + 393.9334001239313 ch3_1_evap_u0_y + 66.260176378973 ch3_1_evap_v0 + 0.0 ch3_1_evap_v0_y - 66.260176378973 ch3_1_evap_u1 + 526.4537528818773 ch3_1_evap_u1_y + 198.780529136919 ch3_1_evap_v1 + 0.0 ch3_1_evap_v1_y + 0.0 cb_ss_u0 + 0.0 cb_ss_u0_y + 0.0 cb_ss_v0 + 0.0 cb_ss_v0_y + 0.0 cb_ss_u1 + 0.0 cb_ss_u1_y + 0.0 cb_ss_v1 + 0.0 cb_ss_v1_y + 0.0 cp_nwk_u0 + 0.0 cp_nwk_u0_y + 0.0 cp_nwk_v0 + 0.0 cp_nwk_v0_y + 0.0 cp_nwk_u1 + 0.0 cp_nwk_u1_y + 0.0 cp_nwk_v1 + 0.0 cp_nwk_v1_y + 0.0 ch_evap_ret_t_in + 0.0 ch_evap_ret_y + 0.0 ch_e_f_c_mass_flow + 0.0 ch_e_f_c_y
 
Subject To 
 
\\Writing Fmin, Fmax constraints for utilities linear 
 
c1: 0 sp1_temp_y - sp1_temp_t_inout <= 0
c2: sp1_temp_t_inout - 1 sp1_temp_y <= 0
c3: 0 sp2_temp_y - sp2_temp_t_inout <= 0
c4: sp2_temp_t_inout - 1 sp2_temp_y <= 0

\\Writing Fmin, Fmax constraints for utilities bilinear 
 
c5: 0.0 ch1_1_evap_u0_y - ch1_1_evap_u0 <= 0
c6: ch1_1_evap_u0 - 1.0 ch1_1_evap_u0_y <= 0
c7: -1.0 ch1_1_evap_v0_y - ch1_1_evap_v0 <= 0
c8: ch1_1_evap_v0 - 0.0 ch1_1_evap_v0_y <= 0
c9: 1.0 ch1_1_evap_u1_y - ch1_1_evap_u1 <= 0
c10: ch1_1_evap_u1 - 2.0 ch1_1_evap_u1_y <= 0
c11: 0.0 ch1_1_evap_v1_y - ch1_1_evap_v1 <= 0
c12: ch1_1_evap_v1 - 1.0 ch1_1_evap_v1_y <= 0
c13: 0.0 ch2_1_evap_u0_y - ch2_1_evap_u0 <= 0
c14: ch2_1_evap_u0 - 1.0 ch2_1_evap_u0_y <= 0
c15: -1.0 ch2_1_evap_v0_y - ch2_1_evap_v0 <= 0
c16: ch2_1_evap_v0 - 0.0 ch2_1_evap_v0_y <= 0
c17: 1.0 ch2_1_evap_u1_y - ch2_1_evap_u1 <= 0
c18: ch2_1_evap_u1 - 2.0 ch2_1_evap_u1_y <= 0
c19: 0.0 ch2_1_evap_v1_y - ch2_1_evap_v1 <= 0
c20: ch2_1_evap_v1 - 1.0 ch2_1_evap_v1_y <= 0
c21: 0.0 ch3_1_evap_u0_y - ch3_1_evap_u0 <= 0
c22: ch3_1_evap_u0 - 1.0 ch3_1_evap_u0_y <= 0
c23: -1.0 ch3_1_evap_v0_y - ch3_1_evap_v0 <= 0
c24: ch3_1_evap_v0 - 0.0 ch3_1_evap_v0_y <= 0
c25: 1.0 ch3_1_evap_u1_y - ch3_1_evap_u1 <= 0
c26: ch3_1_evap_u1 - 2.0 ch3_1_evap_u1_y <= 0
c27: 0.0 ch3_1_evap_v1_y - ch3_1_evap_v1 <= 0
c28: ch3_1_evap_v1 - 1.0 ch3_1_evap_v1_y <= 0
c29: 0.0 cb_ss_u0_y - cb_ss_u0 <= 0
c30: cb_ss_u0 - 1.0 cb_ss_u0_y <= 0
c31: -1.0 cb_ss_v0_y - cb_ss_v0 <= 0
c32: cb_ss_v0 - 0.0 cb_ss_v0_y <= 0
c33: 1.0 cb_ss_u1_y - cb_ss_u1 <= 0
c34: cb_ss_u1 - 2.0 cb_ss_u1_y <= 0
c35: 0.0 cb_ss_v1_y - cb_ss_v1 <= 0
c36: cb_ss_v1 - 1.0 cb_ss_v1_y <= 0
c37: 0.0 cp_nwk_u0_y - cp_nwk_u0 <= 0
c38: cp_nwk_u0 - 1.0 cp_nwk_u0_y <= 0
c39: -1.0 cp_nwk_v0_y - cp_nwk_v0 <= 0
c40: cp_nwk_v0 - 0.0 cp_nwk_v0_y <= 0
c41: 1.0 cp_nwk_u1_y - cp_nwk_u1 <= 0
c42: cp_nwk_u1 - 2.0 cp_nwk_u1_y <= 0
c43: 0.0 cp_nwk_v1_y - cp_nwk_v1 <= 0
c44: cp_nwk_v1 - 1.0 cp_nwk_v1_y <= 0

\\Writing the fmin and fmax constraint in relation to x and y for utilities 
 
c45: 0 ch1_1_evap_y - ch1_1_evap_u0 - ch1_1_evap_u1 - ch1_1_evap_v0 - ch1_1_evap_v1 <= 0
c46: ch1_1_evap_u0 + ch1_1_evap_u1 + ch1_1_evap_v0 + ch1_1_evap_v1 - 2 ch1_1_evap_y <= 0
c47: 0 ch1_1_evap_y - ch1_1_evap_u0 - ch1_1_evap_u1 + ch1_1_evap_v0 + ch1_1_evap_v1 <= 0
c48: ch1_1_evap_u0 + ch1_1_evap_u1 - ch1_1_evap_v0 - ch1_1_evap_v1 - 2 ch1_1_evap_y <= 0
c49: 0 ch2_1_evap_y - ch2_1_evap_u0 - ch2_1_evap_u1 - ch2_1_evap_v0 - ch2_1_evap_v1 <= 0
c50: ch2_1_evap_u0 + ch2_1_evap_u1 + ch2_1_evap_v0 + ch2_1_evap_v1 - 2 ch2_1_evap_y <= 0
c51: 0 ch2_1_evap_y - ch2_1_evap_u0 - ch2_1_evap_u1 + ch2_1_evap_v0 + ch2_1_evap_v1 <= 0
c52: ch2_1_evap_u0 + ch2_1_evap_u1 - ch2_1_evap_v0 - ch2_1_evap_v1 - 2 ch2_1_evap_y <= 0
c53: 0 ch3_1_evap_y - ch3_1_evap_u0 - ch3_1_evap_u1 - ch3_1_evap_v0 - ch3_1_evap_v1 <= 0
c54: ch3_1_evap_u0 + ch3_1_evap_u1 + ch3_1_evap_v0 + ch3_1_evap_v1 - 2 ch3_1_evap_y <= 0
c55: 0 ch3_1_evap_y - ch3_1_evap_u0 - ch3_1_evap_u1 + ch3_1_evap_v0 + ch3_1_evap_v1 <= 0
c56: ch3_1_evap_u0 + ch3_1_evap_u1 - ch3_1_evap_v0 - ch3_1_evap_v1 - 2 ch3_1_evap_y <= 0
c57: 0 cb_ss_y - cb_ss_u0 - cb_ss_u1 - cb_ss_v0 - cb_ss_v1 <= 0
c58: cb_ss_u0 + cb_ss_u1 + cb_ss_v0 + cb_ss_v1 - 2 cb_ss_y <= 0
c59: 0 cb_ss_y - cb_ss_u0 - cb_ss_u1 + cb_ss_v0 + cb_ss_v1 <= 0
c60: cb_ss_u0 + cb_ss_u1 - cb_ss_v0 - cb_ss_v1 - 2 cb_ss_y <= 0
c61: 0 cp_nwk_y - cp_nwk_u0 - cp_nwk_u1 - cp_nwk_v0 - cp_nwk_v1 <= 0
c62: cp_nwk_u0 + cp_nwk_u1 + cp_nwk_v0 + cp_nwk_v1 - 2 cp_nwk_y <= 0
c63: 0 cp_nwk_y - cp_nwk_u0 - cp_nwk_u1 + cp_nwk_v0 + cp_nwk_v1 <= 0
c64: cp_nwk_u0 + cp_nwk_u1 - cp_nwk_v0 - cp_nwk_v1 - 2 cp_nwk_y <= 0

\\Writing Fmin, Fmax constraints for process linear 
 
c65: ch_evap_ret_t_in = 1
c66: ch_evap_ret_y = 1.0
c67: ch_e_f_c_mass_flow = 1
c68: ch_e_f_c_y = 1.0

\\Writing Fmin, Fmax constraints for process bilinear 
 

\\Writing the fmin and fmax constraint in relation to x and y for processes 
 

\\Writing stream constraints 
 
c69: 30.0 sp1_temp_t_inout + 273.15 sp1_temp_y - 138.54967741935474 ch1_1_evap_u0 - 0.0 ch1_1_evap_u0_y - 138.54967741935474 ch1_1_evap_v0 - 0.0 ch1_1_evap_v0_y - 141.4990322580643 ch1_1_evap_u1 + 2.9493548387095245 ch1_1_evap_u1_y - 135.60032258064524 ch1_1_evap_v1 - 0.0 ch1_1_evap_v1_y - 138.54967741935474 ch2_1_evap_u0 - 0.0 ch2_1_evap_u0_y - 138.54967741935474 ch2_1_evap_v0 - 0.0 ch2_1_evap_v0_y - 141.4990322580643 ch2_1_evap_u1 + 2.9493548387095245 ch2_1_evap_u1_y - 135.60032258064524 ch2_1_evap_v1 - 0.0 ch2_1_evap_v1_y - 138.54967741935474 ch3_1_evap_u0 - 0.0 ch3_1_evap_u0_y - 138.54967741935474 ch3_1_evap_v0 - 0.0 ch3_1_evap_v0_y - 141.4990322580643 ch3_1_evap_u1 + 2.9493548387095245 ch3_1_evap_u1_y - 135.60032258064524 ch3_1_evap_v1 - 0.0 ch3_1_evap_v1_y >= 0
c70: 15.0 cp_nwk_u0 + 273.15 cp_nwk_u0_y - 15.0 cp_nwk_v0 + 0.0 cp_nwk_v0_y + 15.0 cp_nwk_u1 + 273.15 cp_nwk_u1_y - 15.0 cp_nwk_v1 + 0.0 cp_nwk_v1_y - 30.0 sp1_temp_t_inout - 273.15 sp1_temp_y >= 0
c71: 2.0 cb_ss_u0 + 274.15 cb_ss_u0_y - 2.0 cb_ss_v0 + 0.0 cb_ss_v0_y + 2.0 cb_ss_u1 + 274.15 cb_ss_u1_y - 2.0 cb_ss_v1 + 0.0 cb_ss_v1_y - 30.0 sp1_temp_t_inout - 273.15 sp1_temp_y >= 0
c72: 186.823546512958 ch_e_f_c_mass_flow + 0.0 ch_e_f_c_y - 93.411773256479 cb_ss_u0 - 0.0 cb_ss_u0_y - 93.411773256479 cb_ss_v0 - 0.0 cb_ss_v0_y - 93.411773256479 cb_ss_u1 - 0.0 cb_ss_u1_y - 93.411773256479 cb_ss_v1 - 0.0 cb_ss_v1_y - 93.411773256479 cp_nwk_u0 - 0.0 cp_nwk_u0_y - 93.411773256479 cp_nwk_v0 - 0.0 cp_nwk_v0_y - 93.411773256479 cp_nwk_u1 - 0.0 cp_nwk_u1_y - 93.411773256479 cp_nwk_v1 - 0.0 cp_nwk_v1_y = 0
c73: 93.411773256479 cb_ss_u0 + 0.0 cb_ss_u0_y + 93.411773256479 cb_ss_v0 + 0.0 cb_ss_v0_y + 93.411773256479 cb_ss_u1 + 0.0 cb_ss_u1_y + 93.411773256479 cb_ss_v1 + 0.0 cb_ss_v1_y + 93.411773256479 cp_nwk_u0 + 0.0 cp_nwk_u0_y + 93.411773256479 cp_nwk_v0 + 0.0 cp_nwk_v0_y + 93.411773256479 cp_nwk_u1 + 0.0 cp_nwk_u1_y + 93.411773256479 cp_nwk_v1 + 0.0 cp_nwk_v1_y - 93.411773256479 ch1_1_evap_u0 - 0.0 ch1_1_evap_u0_y - 93.411773256479 ch1_1_evap_v0 - 0.0 ch1_1_evap_v0_y - 93.411773256479 ch1_1_evap_u1 - 0.0 ch1_1_evap_u1_y - 93.411773256479 ch1_1_evap_v1 - 0.0 ch1_1_evap_v1_y - 93.411773256479 ch2_1_evap_u0 - 0.0 ch2_1_evap_u0_y - 93.411773256479 ch2_1_evap_v0 - 0.0 ch2_1_evap_v0_y - 93.411773256479 ch2_1_evap_u1 - 0.0 ch2_1_evap_u1_y - 93.411773256479 ch2_1_evap_v1 - 0.0 ch2_1_evap_v1_y - 93.411773256479 ch3_1_evap_u0 - 0.0 ch3_1_evap_u0_y - 93.411773256479 ch3_1_evap_v0 - 0.0 ch3_1_evap_v0_y - 93.411773256479 ch3_1_evap_u1 - 0.0 ch3_1_evap_u1_y - 93.411773256479 ch3_1_evap_v1 - 0.0 ch3_1_evap_v1_y <= 0
c74: 30.0 sp2_temp_t_inout + 273.15 sp2_temp_y - 138.075 cb_ss_u0 - 3.902679378124388 cb_ss_u0_y - 138.075 cb_ss_v0 - 0.0 cb_ss_v0_y - 140.075 cb_ss_u1 - 1.9026793781243878 cb_ss_u1_y - 136.075 cb_ss_v1 - 0.0 cb_ss_v1_y - 144.075 cp_nwk_u0 - 0.0 cp_nwk_u0_y - 144.075 cp_nwk_v0 - 0.0 cp_nwk_v0_y - 159.075 cp_nwk_u1 + 15.0 cp_nwk_u1_y - 129.075 cp_nwk_v1 - 0.0 cp_nwk_v1_y >= 0
c75: 280.048709677419 ch_evap_ret_t_in + 0.0 ch_evap_ret_y - 30.0 sp2_temp_t_inout - 273.15 sp2_temp_y = 0

\\Writing additional constraints 
 
\\Writing additional constraints: unit_binary 
 
c76: 1 ch1_1_evap_u0_y + 1 ch1_1_evap_u1_y <= 1
c77: 1 ch1_1_evap_v0_y + 1 ch1_1_evap_v1_y <= 1
c78: 1 ch2_1_evap_u0_y + 1 ch2_1_evap_u1_y <= 1
c79: 1 ch2_1_evap_v0_y + 1 ch2_1_evap_v1_y <= 1
c80: 1 ch3_1_evap_u0_y + 1 ch3_1_evap_u1_y <= 1
c81: 1 ch3_1_evap_v0_y + 1 ch3_1_evap_v1_y <= 1
c82: 1 cb_ss_u0_y + 1 cb_ss_u1_y <= 1
c83: 1 cb_ss_v0_y + 1 cb_ss_v1_y <= 1
c84: 1 cp_nwk_u0_y + 1 cp_nwk_u1_y <= 1
c85: 1 cp_nwk_v0_y + 1 cp_nwk_v1_y <= 1
c86: 1 ch1_1_evap_y <= 1
c87: 1 ch2_1_evap_y <= 1
c88: 1 ch3_1_evap_y <= 1

\\Writing additional constraints: unit_binary_equality 
 
c89: 1 ch1_1_evap_u0_y + 1 ch1_1_evap_v0_y + 1 ch1_1_evap_u1_y + 1 ch1_1_evap_v1_y - 2 ch1_1_evap_y = 0
c90: 1 ch2_1_evap_u0_y + 1 ch2_1_evap_v0_y + 1 ch2_1_evap_u1_y + 1 ch2_1_evap_v1_y - 2 ch2_1_evap_y = 0
c91: 1 ch3_1_evap_u0_y + 1 ch3_1_evap_v0_y + 1 ch3_1_evap_u1_y + 1 ch3_1_evap_v1_y - 2 ch3_1_evap_y = 0
c92: 1 cb_ss_u0_y + 1 cb_ss_v0_y + 1 cb_ss_u1_y + 1 cb_ss_v1_y - 2 cb_ss_y = 0
c93: 1 cp_nwk_u0_y + 1 cp_nwk_v0_y + 1 cp_nwk_u1_y + 1 cp_nwk_v1_y - 2 cp_nwk_y = 0

\\Writing additional constraints: stream_limit_modified 
 
c94: 93.411773256479 ch1_1_evap_u0 + 0.0 ch1_1_evap_u0_y + 93.411773256479 ch1_1_evap_v0 + 0.0 ch1_1_evap_v0_y + 93.411773256479 ch1_1_evap_u1 + 0.0 ch1_1_evap_u1_y + 93.411773256479 ch1_1_evap_v1 + 0.0 ch1_1_evap_v1_y <= 218.3903135
c95: 93.411773256479 ch2_1_evap_u0 + 0.0 ch2_1_evap_u0_y + 93.411773256479 ch2_1_evap_v0 + 0.0 ch2_1_evap_v0_y + 93.411773256479 ch2_1_evap_u1 + 0.0 ch2_1_evap_u1_y + 93.411773256479 ch2_1_evap_v1 + 0.0 ch2_1_evap_v1_y <= 820.4531779
c96: 93.411773256479 ch3_1_evap_u0 + 0.0 ch3_1_evap_u0_y + 93.411773256479 ch3_1_evap_v0 + 0.0 ch3_1_evap_v0_y + 93.411773256479 ch3_1_evap_u1 + 0.0 ch3_1_evap_u1_y + 93.411773256479 ch3_1_evap_v1 + 0.0 ch3_1_evap_v1_y <= 820.4531779
c97: 0.4620532889850569 cb_ss_u0 + 0.0 cb_ss_u0_y + 0.4620532889850569 cb_ss_v0 + 0.0 cb_ss_v0_y + 0.4620532889850569 cb_ss_u1 + 0.0 cb_ss_u1_y + 0.4620532889850569 cb_ss_v1 + 0.0 cb_ss_v1_y >= 0.1

\\Writing additional constraints: bilinear_limits_fmin_util 
 
c98: 320.84331697673474 ch1_1_evap_u0 + 0.0 ch1_1_evap_u0_y + 320.84331697673474 ch1_1_evap_v0 + 0.0 ch1_1_evap_v0_y - 320.84331697673474 ch1_1_evap_u1 + 641.6866339534695 ch1_1_evap_u1_y + 962.5299509302042 ch1_1_evap_v1 + 0.0 ch1_1_evap_v1_y  - 0.0 ch1_1_evap_y >= 0
c99: 320.84331697673474 ch2_1_evap_u0 + 0.0 ch2_1_evap_u0_y + 320.84331697673474 ch2_1_evap_v0 + 0.0 ch2_1_evap_v0_y - 320.84331697673474 ch2_1_evap_u1 + 641.6866339534695 ch2_1_evap_u1_y + 962.5299509302042 ch2_1_evap_v1 + 0.0 ch2_1_evap_v1_y  - 0.0 ch2_1_evap_y >= 0
c100: 320.84331697673474 ch3_1_evap_u0 + 0.0 ch3_1_evap_u0_y + 320.84331697673474 ch3_1_evap_v0 + 0.0 ch3_1_evap_v0_y - 320.84331697673474 ch3_1_evap_u1 + 641.6866339534695 ch3_1_evap_u1_y + 962.5299509302042 ch3_1_evap_v1 + 0.0 ch3_1_evap_v1_y  - 0.0 ch3_1_evap_y >= 0

\\Writing additional constraints: bilinear_limits_fmax_util 
 
c101: 320.84331697673474 ch1_1_evap_u0 + 0.0 ch1_1_evap_u0_y + 320.84331697673474 ch1_1_evap_v0 + 0.0 ch1_1_evap_v0_y - 320.84331697673474 ch1_1_evap_u1 + 641.6866339534695 ch1_1_evap_u1_y + 962.5299509302042 ch1_1_evap_v1 + 0.0 ch1_1_evap_v1_y - 2000.0 ch1_1_evap_y <= 0
c102: 320.84331697673474 ch2_1_evap_u0 + 0.0 ch2_1_evap_u0_y + 320.84331697673474 ch2_1_evap_v0 + 0.0 ch2_1_evap_v0_y - 320.84331697673474 ch2_1_evap_u1 + 641.6866339534695 ch2_1_evap_u1_y + 962.5299509302042 ch2_1_evap_v1 + 0.0 ch2_1_evap_v1_y - 7330.0 ch2_1_evap_y <= 0
c103: 320.84331697673474 ch3_1_evap_u0 + 0.0 ch3_1_evap_u0_y + 320.84331697673474 ch3_1_evap_v0 + 0.0 ch3_1_evap_v0_y - 320.84331697673474 ch3_1_evap_u1 + 641.6866339534695 ch3_1_evap_u1_y + 962.5299509302042 ch3_1_evap_v1 + 0.0 ch3_1_evap_v1_y - 7330.0 ch3_1_evap_y <= 0

\\Writing additional constraints: bilinear_limits_fmax_proc, equality 
 

Binary 
 
ch1_1_evap_y
ch2_1_evap_y
ch3_1_evap_y
cb_ss_y
cp_nwk_y
sp1_temp_y
sp2_temp_y
ch1_1_evap_u0_y
ch1_1_evap_v0_y
ch1_1_evap_u1_y
ch1_1_evap_v1_y
ch2_1_evap_u0_y
ch2_1_evap_v0_y
ch2_1_evap_u1_y
ch2_1_evap_v1_y
ch3_1_evap_u0_y
ch3_1_evap_v0_y
ch3_1_evap_u1_y
ch3_1_evap_v1_y
cb_ss_u0_y
cb_ss_v0_y
cb_ss_u1_y
cb_ss_v1_y
cp_nwk_u0_y
cp_nwk_v0_y
cp_nwk_u1_y
cp_nwk_v1_y

End 
