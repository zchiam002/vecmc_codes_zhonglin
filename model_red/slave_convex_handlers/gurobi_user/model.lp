\ Model milp_model_id_10013
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  82.0718991851011 ch1_1_evap_u0 + 82.0718991851011 ch1_1_evap_v0
   - 82.0718991851011 ch1_1_evap_u1 + 246.2156975553033 ch1_1_evap_v1
   + 66.260176378973 ch2_1_evap_u0 + 66.260176378973 ch2_1_evap_v0
   - 66.260176378973 ch2_1_evap_u1 + 198.780529136919 ch2_1_evap_v1
   + 66.260176378973 ch3_1_evap_u0 + 66.260176378973 ch3_1_evap_v0
   - 66.260176378973 ch3_1_evap_u1 + 198.780529136919 ch3_1_evap_v1
   + 104.2101600195621 ch1_1_evap_u0_y + 268.3539583897643 ch1_1_evap_u1_y
   + 393.9334001239313 ch2_1_evap_u0_y + 526.4537528818773 ch2_1_evap_u1_y
   + 393.9334001239313 ch3_1_evap_u0_y + 526.4537528818773 ch3_1_evap_u1_y
Subject To
 c0: - sp1_temp_t_inout <= 0
 c1: sp1_temp_t_inout - sp1_temp_y <= 0
 c2: - sp2_temp_t_inout <= 0
 c3: sp2_temp_t_inout - sp2_temp_y <= 0
 c4: - ch1_1_evap_u0 <= 0
 c5: ch1_1_evap_u0 - ch1_1_evap_u0_y <= 0
 c6: - ch1_1_evap_v0 - ch1_1_evap_v0_y <= 0
 c7: ch1_1_evap_v0 <= 0
 c8: - ch1_1_evap_u1 + ch1_1_evap_u1_y <= 0
 c9: ch1_1_evap_u1 - 2 ch1_1_evap_u1_y <= 0
 c10: - ch1_1_evap_v1 <= 0
 c11: ch1_1_evap_v1 - ch1_1_evap_v1_y <= 0
 c12: - ch2_1_evap_u0 <= 0
 c13: ch2_1_evap_u0 - ch2_1_evap_u0_y <= 0
 c14: - ch2_1_evap_v0 - ch2_1_evap_v0_y <= 0
 c15: ch2_1_evap_v0 <= 0
 c16: - ch2_1_evap_u1 + ch2_1_evap_u1_y <= 0
 c17: ch2_1_evap_u1 - 2 ch2_1_evap_u1_y <= 0
 c18: - ch2_1_evap_v1 <= 0
 c19: ch2_1_evap_v1 - ch2_1_evap_v1_y <= 0
 c20: - ch3_1_evap_u0 <= 0
 c21: ch3_1_evap_u0 - ch3_1_evap_u0_y <= 0
 c22: - ch3_1_evap_v0 - ch3_1_evap_v0_y <= 0
 c23: ch3_1_evap_v0 <= 0
 c24: - ch3_1_evap_u1 + ch3_1_evap_u1_y <= 0
 c25: ch3_1_evap_u1 - 2 ch3_1_evap_u1_y <= 0
 c26: - ch3_1_evap_v1 <= 0
 c27: ch3_1_evap_v1 - ch3_1_evap_v1_y <= 0
 c28: - cb_ss_u0 <= 0
 c29: cb_ss_u0 - cb_ss_u0_y <= 0
 c30: - cb_ss_v0 - cb_ss_v0_y <= 0
 c31: cb_ss_v0 <= 0
 c32: - cb_ss_u1 + cb_ss_u1_y <= 0
 c33: cb_ss_u1 - 2 cb_ss_u1_y <= 0
 c34: - cb_ss_v1 <= 0
 c35: cb_ss_v1 - cb_ss_v1_y <= 0
 c36: - cp_nwk_u0 <= 0
 c37: cp_nwk_u0 - cp_nwk_u0_y <= 0
 c38: - cp_nwk_v0 - cp_nwk_v0_y <= 0
 c39: cp_nwk_v0 <= 0
 c40: - cp_nwk_u1 + cp_nwk_u1_y <= 0
 c41: cp_nwk_u1 - 2 cp_nwk_u1_y <= 0
 c42: - cp_nwk_v1 <= 0
 c43: cp_nwk_v1 - cp_nwk_v1_y <= 0
 c44: - ch1_1_evap_u0 - ch1_1_evap_v0 - ch1_1_evap_u1 - ch1_1_evap_v1 <= 0
 c45: ch1_1_evap_u0 + ch1_1_evap_v0 + ch1_1_evap_u1 + ch1_1_evap_v1
   - 2 ch1_1_evap_y <= 0
 c46: - ch1_1_evap_u0 + ch1_1_evap_v0 - ch1_1_evap_u1 + ch1_1_evap_v1 <= 0
 c47: ch1_1_evap_u0 - ch1_1_evap_v0 + ch1_1_evap_u1 - ch1_1_evap_v1
   - 2 ch1_1_evap_y <= 0
 c48: - ch2_1_evap_u0 - ch2_1_evap_v0 - ch2_1_evap_u1 - ch2_1_evap_v1 <= 0
 c49: ch2_1_evap_u0 + ch2_1_evap_v0 + ch2_1_evap_u1 + ch2_1_evap_v1
   - 2 ch2_1_evap_y <= 0
 c50: - ch2_1_evap_u0 + ch2_1_evap_v0 - ch2_1_evap_u1 + ch2_1_evap_v1 <= 0
 c51: ch2_1_evap_u0 - ch2_1_evap_v0 + ch2_1_evap_u1 - ch2_1_evap_v1
   - 2 ch2_1_evap_y <= 0
 c52: - ch3_1_evap_u0 - ch3_1_evap_v0 - ch3_1_evap_u1 - ch3_1_evap_v1 <= 0
 c53: ch3_1_evap_u0 + ch3_1_evap_v0 + ch3_1_evap_u1 + ch3_1_evap_v1
   - 2 ch3_1_evap_y <= 0
 c54: - ch3_1_evap_u0 + ch3_1_evap_v0 - ch3_1_evap_u1 + ch3_1_evap_v1 <= 0
 c55: ch3_1_evap_u0 - ch3_1_evap_v0 + ch3_1_evap_u1 - ch3_1_evap_v1
   - 2 ch3_1_evap_y <= 0
 c56: - cb_ss_u0 - cb_ss_v0 - cb_ss_u1 - cb_ss_v1 <= 0
 c57: cb_ss_u0 + cb_ss_v0 + cb_ss_u1 + cb_ss_v1 - 2 cb_ss_y <= 0
 c58: - cb_ss_u0 + cb_ss_v0 - cb_ss_u1 + cb_ss_v1 <= 0
 c59: cb_ss_u0 - cb_ss_v0 + cb_ss_u1 - cb_ss_v1 - 2 cb_ss_y <= 0
 c60: - cp_nwk_u0 - cp_nwk_v0 - cp_nwk_u1 - cp_nwk_v1 <= 0
 c61: cp_nwk_u0 + cp_nwk_v0 + cp_nwk_u1 + cp_nwk_v1 - 2 cp_nwk_y <= 0
 c62: - cp_nwk_u0 + cp_nwk_v0 - cp_nwk_u1 + cp_nwk_v1 <= 0
 c63: cp_nwk_u0 - cp_nwk_v0 + cp_nwk_u1 - cp_nwk_v1 - 2 cp_nwk_y <= 0
 c64: ch_evap_ret_t_in = 1
 c65: ch_evap_ret_y = 1
 c66: ch_e_f_c_mass_flow = 1
 c67: ch_e_f_c_y = 1
 c68: 30 sp1_temp_t_inout - 138.5496774193547 ch1_1_evap_u0
   - 138.5496774193547 ch1_1_evap_v0 - 141.4990322580643 ch1_1_evap_u1
   - 135.6003225806452 ch1_1_evap_v1 - 138.5496774193547 ch2_1_evap_u0
   - 138.5496774193547 ch2_1_evap_v0 - 141.4990322580643 ch2_1_evap_u1
   - 135.6003225806452 ch2_1_evap_v1 - 138.5496774193547 ch3_1_evap_u0
   - 138.5496774193547 ch3_1_evap_v0 - 141.4990322580643 ch3_1_evap_u1
   - 135.6003225806452 ch3_1_evap_v1 + 273.15 sp1_temp_y
   + 2.949354838709525 ch1_1_evap_u1_y + 2.949354838709525 ch2_1_evap_u1_y
   + 2.949354838709525 ch3_1_evap_u1_y >= 0
 c69: - 30 sp1_temp_t_inout + 15 cp_nwk_u0 - 15 cp_nwk_v0 + 15 cp_nwk_u1
   - 15 cp_nwk_v1 - 273.15 sp1_temp_y + 273.15 cp_nwk_u0_y
   + 273.15 cp_nwk_u1_y >= 0
 c70: - 30 sp1_temp_t_inout + 2 cb_ss_u0 - 2 cb_ss_v0 + 2 cb_ss_u1
   - 2 cb_ss_v1 - 273.15 sp1_temp_y + 274.15 cb_ss_u0_y + 274.15 cb_ss_u1_y
   >= 0
 c71: - 93.411773256479 cb_ss_u0 - 93.411773256479 cb_ss_v0
   - 93.411773256479 cb_ss_u1 - 93.411773256479 cb_ss_v1
   - 93.411773256479 cp_nwk_u0 - 93.411773256479 cp_nwk_v0
   - 93.411773256479 cp_nwk_u1 - 93.411773256479 cp_nwk_v1
   + 186.823546512958 ch_e_f_c_mass_flow = 0
 c72: - 93.411773256479 ch1_1_evap_u0 - 93.411773256479 ch1_1_evap_v0
   - 93.411773256479 ch1_1_evap_u1 - 93.411773256479 ch1_1_evap_v1
   - 93.411773256479 ch2_1_evap_u0 - 93.411773256479 ch2_1_evap_v0
   - 93.411773256479 ch2_1_evap_u1 - 93.411773256479 ch2_1_evap_v1
   - 93.411773256479 ch3_1_evap_u0 - 93.411773256479 ch3_1_evap_v0
   - 93.411773256479 ch3_1_evap_u1 - 93.411773256479 ch3_1_evap_v1
   + 93.411773256479 cb_ss_u0 + 93.411773256479 cb_ss_v0
   + 93.411773256479 cb_ss_u1 + 93.411773256479 cb_ss_v1
   + 93.411773256479 cp_nwk_u0 + 93.411773256479 cp_nwk_v0
   + 93.411773256479 cp_nwk_u1 + 93.411773256479 cp_nwk_v1 <= 0
 c73: 30 sp2_temp_t_inout - 138.075 cb_ss_u0 - 138.075 cb_ss_v0
   - 140.075 cb_ss_u1 - 136.075 cb_ss_v1 - 144.075 cp_nwk_u0
   - 144.075 cp_nwk_v0 - 159.075 cp_nwk_u1 - 129.075 cp_nwk_v1
   + 273.15 sp2_temp_y - 3.902679378124388 cb_ss_u0_y
   - 1.902679378124388 cb_ss_u1_y + 15 cp_nwk_u1_y >= 0
 c74: - 30 sp2_temp_t_inout + 280.048709677419 ch_evap_ret_t_in
   - 273.15 sp2_temp_y = 0
 c75: ch1_1_evap_u0_y + ch1_1_evap_u1_y <= 1
 c76: ch1_1_evap_v0_y + ch1_1_evap_v1_y <= 1
 c77: ch2_1_evap_u0_y + ch2_1_evap_u1_y <= 1
 c78: ch2_1_evap_v0_y + ch2_1_evap_v1_y <= 1
 c79: ch3_1_evap_u0_y + ch3_1_evap_u1_y <= 1
 c80: ch3_1_evap_v0_y + ch3_1_evap_v1_y <= 1
 c81: cb_ss_u0_y + cb_ss_u1_y <= 1
 c82: cb_ss_v0_y + cb_ss_v1_y <= 1
 c83: cp_nwk_u0_y + cp_nwk_u1_y <= 1
 c84: cp_nwk_v0_y + cp_nwk_v1_y <= 1
 c85: ch1_1_evap_y <= 1
 c86: ch2_1_evap_y <= 1
 c87: ch3_1_evap_y <= 1
 c88: - 2 ch1_1_evap_y + ch1_1_evap_u0_y + ch1_1_evap_v0_y
   + ch1_1_evap_u1_y + ch1_1_evap_v1_y = 0
 c89: - 2 ch2_1_evap_y + ch2_1_evap_u0_y + ch2_1_evap_v0_y
   + ch2_1_evap_u1_y + ch2_1_evap_v1_y = 0
 c90: - 2 ch3_1_evap_y + ch3_1_evap_u0_y + ch3_1_evap_v0_y
   + ch3_1_evap_u1_y + ch3_1_evap_v1_y = 0
 c91: - 2 cb_ss_y + cb_ss_u0_y + cb_ss_v0_y + cb_ss_u1_y + cb_ss_v1_y = 0
 c92: - 2 cp_nwk_y + cp_nwk_u0_y + cp_nwk_v0_y + cp_nwk_u1_y + cp_nwk_v1_y
   = 0
 c93: 93.411773256479 ch1_1_evap_u0 + 93.411773256479 ch1_1_evap_v0
   + 93.411773256479 ch1_1_evap_u1 + 93.411773256479 ch1_1_evap_v1
   <= 218.3903135
 c94: 93.411773256479 ch2_1_evap_u0 + 93.411773256479 ch2_1_evap_v0
   + 93.411773256479 ch2_1_evap_u1 + 93.411773256479 ch2_1_evap_v1
   <= 820.4531779
 c95: 93.411773256479 ch3_1_evap_u0 + 93.411773256479 ch3_1_evap_v0
   + 93.411773256479 ch3_1_evap_u1 + 93.411773256479 ch3_1_evap_v1
   <= 820.4531779
 c96: 0.4620532889850569 cb_ss_u0 + 0.4620532889850569 cb_ss_v0
   + 0.4620532889850569 cb_ss_u1 + 0.4620532889850569 cb_ss_v1 >= 0.1
 c97: 320.8433169767347 ch1_1_evap_u0 + 320.8433169767347 ch1_1_evap_v0
   - 320.8433169767347 ch1_1_evap_u1 + 962.5299509302042 ch1_1_evap_v1
   + 641.6866339534695 ch1_1_evap_u1_y >= 0
 c98: 320.8433169767347 ch2_1_evap_u0 + 320.8433169767347 ch2_1_evap_v0
   - 320.8433169767347 ch2_1_evap_u1 + 962.5299509302042 ch2_1_evap_v1
   + 641.6866339534695 ch2_1_evap_u1_y >= 0
 c99: 320.8433169767347 ch3_1_evap_u0 + 320.8433169767347 ch3_1_evap_v0
   - 320.8433169767347 ch3_1_evap_u1 + 962.5299509302042 ch3_1_evap_v1
   + 641.6866339534695 ch3_1_evap_u1_y >= 0
 c100: 320.8433169767347 ch1_1_evap_u0 + 320.8433169767347 ch1_1_evap_v0
   - 320.8433169767347 ch1_1_evap_u1 + 962.5299509302042 ch1_1_evap_v1
   - 2000 ch1_1_evap_y + 641.6866339534695 ch1_1_evap_u1_y <= 0
 c101: 320.8433169767347 ch2_1_evap_u0 + 320.8433169767347 ch2_1_evap_v0
   - 320.8433169767347 ch2_1_evap_u1 + 962.5299509302042 ch2_1_evap_v1
   - 7330 ch2_1_evap_y + 641.6866339534695 ch2_1_evap_u1_y <= 0
 c102: 320.8433169767347 ch3_1_evap_u0 + 320.8433169767347 ch3_1_evap_v0
   - 320.8433169767347 ch3_1_evap_u1 + 962.5299509302042 ch3_1_evap_v1
   - 7330 ch3_1_evap_y + 641.6866339534695 ch3_1_evap_u1_y <= 0
Bounds
Binaries
 ch1_1_evap_y ch2_1_evap_y ch3_1_evap_y cb_ss_y cp_nwk_y sp1_temp_y
 sp2_temp_y ch1_1_evap_u0_y ch1_1_evap_v0_y ch1_1_evap_u1_y ch1_1_evap_v1_y
 ch2_1_evap_u0_y ch2_1_evap_v0_y ch2_1_evap_u1_y ch2_1_evap_v1_y
 ch3_1_evap_u0_y ch3_1_evap_v0_y ch3_1_evap_u1_y ch3_1_evap_v1_y cb_ss_u0_y
 cb_ss_v0_y cb_ss_u1_y cb_ss_v1_y cp_nwk_u0_y cp_nwk_v0_y cp_nwk_u1_y
 cp_nwk_v1_y ch_evap_ret_y ch_e_f_c_y
End
