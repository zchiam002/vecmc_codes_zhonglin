\\ Objective function for all utilities and processes 
 
Minimize 

obj: 0.0 ch1_enwk_1_m_perc + 0.0 ch1_enwk_1_y + 0.0 ch2_enwk_1_m_perc + 0.0 ch2_enwk_1_y + 0.017967538 ch1_ep_1_m_flow + 0.208225612 ch1_ep_1_y + 0.259072758 ch1_ep_1_delp + 0.032272906000000004 ch2_ep_1_m_flow + 1.518957414 ch2_ep_1_y + 0.79445631 ch2_ep_1_delp + 0.0 sp1_temp_t_inout + 0.0 sp1_temp_y + 0.0 ice_nwk_1_m_perc + 0.0 ice_nwk_1_y + 0.0 gv2_nwk_1_m_perc + 0.0 gv2_nwk_1_y + 0.0 hsb_nwk_1_m_perc + 0.0 hsb_nwk_1_y + 0.0 para_nwk_con_delp + 0.0 para_nwk_con_y + 0.05916007784270439 dist_np_combi_0_0_m_flow + 3.495743360094252 dist_np_combi_0_0_y + 0.8909347520947662 dist_np_combi_0_0_delp + 0.095006738985388 dist_np_combi_1_0_m_flow + 0.7291675439780576 dist_np_combi_1_0_y + 0.4659878716144978 dist_np_combi_1_0_delp + 0.08836866838225241 dist_np_combi_2_0_m_flow + 6.184809806912327 dist_np_combi_2_0_y + 0.6950652215603353 dist_np_combi_2_0_delp + 0.09451397631785663 dist_np_combi_3_0_m_flow + 12.031048423773882 dist_np_combi_3_0_y + 1.4109045001638756 dist_np_combi_3_0_delp + 0.08746920085292287 dist_np_combi_4_0_m_flow + 30.918686396394662 dist_np_combi_4_0_y + 2.7800001674126125 dist_np_combi_4_0_delp + 0.06870694371026757 dist_np_combi_5_0_m_flow + 0.4113596061435239 dist_np_combi_5_0_y + 0.3693427012085625 dist_np_combi_5_0_delp + 0.05916007784270439 dist_np_combi_6_0_m_flow + 3.495743360094252 dist_np_combi_6_0_y + 0.8909347520947662 dist_np_combi_6_0_delp + 55.322001073771354 ch1_1_u0 + 134.3364448846704 ch1_1_u0_y + 55.322001073771354 ch1_1_v0 + 0.0 ch1_1_v0_y - 55.32200107377135 ch1_1_u1 + 244.98044703221314 ch1_1_u1_y + 165.96600322131405 ch1_1_v1 + 0.0 ch1_1_v1_y + 45.15766074535411 ch2_1_u0 + 393.4258332671286 ch2_1_u0_y + 45.15766074535411 ch2_1_v0 + 0.0 ch2_1_v0_y - 45.15766074535409 ch2_1_u1 + 483.74115475783685 ch2_1_u1_y + 135.4729822360623 ch2_1_v1 + 0.0 ch2_1_v1_y + 0.0 cp_nwk_u0 + 0.0 cp_nwk_u0_y + 0.0 cp_nwk_v0 + 0.0 cp_nwk_v0_y + 0.0 cp_nwk_u1 + 0.0 cp_nwk_u1_y + 0.0 cp_nwk_v1 + 0.0 cp_nwk_v1_y + 0.0 gv2_ss_u0 + 0.0 gv2_ss_u0_y + 0.0 gv2_ss_v0 + 0.0 gv2_ss_v0_y + 0.0 gv2_ss_u1 + 0.0 gv2_ss_u1_y + 0.0 gv2_ss_v1 + 0.0 gv2_ss_v1_y + 0.0 hsb_ss_u0 + 0.0 hsb_ss_u0_y + 0.0 hsb_ss_v0 + 0.0 hsb_ss_v0_y + 0.0 hsb_ss_u1 + 0.0 hsb_ss_u1_y + 0.0 hsb_ss_v1 + 0.0 hsb_ss_v1_y + 0.0 ch_e_f_c_m_perc + 0.0 ch_e_f_c_y + 0.0 ch_evap_ret_t_in + 0.0 ch_evap_ret_y
 
Subject To 
 
\\Writing Fmin, Fmax constraints for utilities linear 
 
c1: 0.0 ch1_enwk_1_y - ch1_enwk_1_m_perc <= 0
c2: ch1_enwk_1_m_perc - 1.0 ch1_enwk_1_y <= 0
c3: 0.0 ch2_enwk_1_y - ch2_enwk_1_m_perc <= 0
c4: ch2_enwk_1_m_perc - 1.0 ch2_enwk_1_y <= 0
c5: 0.0 ch1_ep_1_y - ch1_ep_1_m_flow <= 0
c6: ch1_ep_1_m_flow - 218.3903135 ch1_ep_1_y <= 0
c7: 0.0 ch1_ep_1_y - ch1_ep_1_delp <= 0
c8: ch1_ep_1_delp - 15.0 ch1_ep_1_y <= 0
c9: 0.0 ch2_ep_1_y - ch2_ep_1_m_flow <= 0
c10: ch2_ep_1_m_flow - 820.4531779 ch2_ep_1_y <= 0
c11: 0.0 ch2_ep_1_y - ch2_ep_1_delp <= 0
c12: ch2_ep_1_delp - 23.0 ch2_ep_1_y <= 0
c13: 0 sp1_temp_y - sp1_temp_t_inout <= 0
c14: sp1_temp_t_inout - 1 sp1_temp_y <= 0
c15: 0.0 ice_nwk_1_y - ice_nwk_1_m_perc <= 0
c16: ice_nwk_1_m_perc - 1.0 ice_nwk_1_y <= 0
c17: 0.0 gv2_nwk_1_y - gv2_nwk_1_m_perc <= 0
c18: gv2_nwk_1_m_perc - 1.0 gv2_nwk_1_y <= 0
c19: 0.0 hsb_nwk_1_y - hsb_nwk_1_m_perc <= 0
c20: hsb_nwk_1_m_perc - 1.0 hsb_nwk_1_y <= 0
c21: 0 para_nwk_con_y - para_nwk_con_delp <= 0
c22: para_nwk_con_delp - 80 para_nwk_con_y <= 0
c23: 0.0 dist_np_combi_0_0_y - dist_np_combi_0_0_m_flow <= 0
c24: dist_np_combi_0_0_m_flow - 1128.8211815773864 dist_np_combi_0_0_y <= 0
c25: 0.0 dist_np_combi_0_0_y - dist_np_combi_0_0_delp <= 0
c26: dist_np_combi_0_0_delp - 40.0 dist_np_combi_0_0_y <= 0
c27: 0.0 dist_np_combi_1_0_y - dist_np_combi_1_0_m_flow <= 0
c28: dist_np_combi_1_0_m_flow - 778.9949418600381 dist_np_combi_1_0_y <= 0
c29: 0.0 dist_np_combi_1_0_y - dist_np_combi_1_0_delp <= 0
c30: dist_np_combi_1_0_delp - 50.0 dist_np_combi_1_0_y <= 0
c31: 0.0 dist_np_combi_2_0_y - dist_np_combi_2_0_m_flow <= 0
c32: dist_np_combi_2_0_m_flow - 1365.0266783562731 dist_np_combi_2_0_y <= 0
c33: 0.0 dist_np_combi_2_0_y - dist_np_combi_2_0_delp <= 0
c34: dist_np_combi_2_0_delp - 55.0 dist_np_combi_2_0_y <= 0
c35: 0.0 dist_np_combi_3_0_y - dist_np_combi_3_0_m_flow <= 0
c36: dist_np_combi_3_0_m_flow - 1699.6877800309853 dist_np_combi_3_0_y <= 0
c37: 0.0 dist_np_combi_3_0_y - dist_np_combi_3_0_delp <= 0
c38: dist_np_combi_3_0_delp - 65.0 dist_np_combi_3_0_y <= 0
c39: 0.0 dist_np_combi_4_0_y - dist_np_combi_4_0_m_flow <= 0
c40: dist_np_combi_4_0_m_flow - 2195.715661169962 dist_np_combi_4_0_y <= 0
c41: 0.0 dist_np_combi_4_0_y - dist_np_combi_4_0_delp <= 0
c42: dist_np_combi_4_0_delp - 75.0 dist_np_combi_4_0_y <= 0
c43: 0.0 dist_np_combi_5_0_y - dist_np_combi_5_0_m_flow <= 0
c44: dist_np_combi_5_0_m_flow - 632.3090700071897 dist_np_combi_5_0_y <= 0
c45: 0.0 dist_np_combi_5_0_y - dist_np_combi_5_0_delp <= 0
c46: dist_np_combi_5_0_delp - 40.0 dist_np_combi_5_0_y <= 0
c47: 0.0 dist_np_combi_6_0_y - dist_np_combi_6_0_m_flow <= 0
c48: dist_np_combi_6_0_m_flow - 1128.8211815773864 dist_np_combi_6_0_y <= 0
c49: 0.0 dist_np_combi_6_0_y - dist_np_combi_6_0_delp <= 0
c50: dist_np_combi_6_0_delp - 40.0 dist_np_combi_6_0_y <= 0

\\Writing Fmin, Fmax constraints for utilities bilinear 
 
c51: 0.0 ch1_1_u0_y - ch1_1_u0 <= 0
c52: ch1_1_u0 - 1.0 ch1_1_u0_y <= 0
c53: -1.0 ch1_1_v0_y - ch1_1_v0 <= 0
c54: ch1_1_v0 - 0.0 ch1_1_v0_y <= 0
c55: 1.0 ch1_1_u1_y - ch1_1_u1 <= 0
c56: ch1_1_u1 - 2.0 ch1_1_u1_y <= 0
c57: 0.0 ch1_1_v1_y - ch1_1_v1 <= 0
c58: ch1_1_v1 - 1.0 ch1_1_v1_y <= 0
c59: 0.0 ch2_1_u0_y - ch2_1_u0 <= 0
c60: ch2_1_u0 - 1.0 ch2_1_u0_y <= 0
c61: -1.0 ch2_1_v0_y - ch2_1_v0 <= 0
c62: ch2_1_v0 - 0.0 ch2_1_v0_y <= 0
c63: 1.0 ch2_1_u1_y - ch2_1_u1 <= 0
c64: ch2_1_u1 - 2.0 ch2_1_u1_y <= 0
c65: 0.0 ch2_1_v1_y - ch2_1_v1 <= 0
c66: ch2_1_v1 - 1.0 ch2_1_v1_y <= 0
c67: 0.0 cp_nwk_u0_y - cp_nwk_u0 <= 0
c68: cp_nwk_u0 - 1.0 cp_nwk_u0_y <= 0
c69: -1.0 cp_nwk_v0_y - cp_nwk_v0 <= 0
c70: cp_nwk_v0 - 0.0 cp_nwk_v0_y <= 0
c71: 1.0 cp_nwk_u1_y - cp_nwk_u1 <= 0
c72: cp_nwk_u1 - 2.0 cp_nwk_u1_y <= 0
c73: 0.0 cp_nwk_v1_y - cp_nwk_v1 <= 0
c74: cp_nwk_v1 - 1.0 cp_nwk_v1_y <= 0
c75: 0.0 gv2_ss_u0_y - gv2_ss_u0 <= 0
c76: gv2_ss_u0 - 1.0 gv2_ss_u0_y <= 0
c77: -1.0 gv2_ss_v0_y - gv2_ss_v0 <= 0
c78: gv2_ss_v0 - 0.0 gv2_ss_v0_y <= 0
c79: 1.0 gv2_ss_u1_y - gv2_ss_u1 <= 0
c80: gv2_ss_u1 - 2.0 gv2_ss_u1_y <= 0
c81: 0.0 gv2_ss_v1_y - gv2_ss_v1 <= 0
c82: gv2_ss_v1 - 1.0 gv2_ss_v1_y <= 0
c83: 0.0 hsb_ss_u0_y - hsb_ss_u0 <= 0
c84: hsb_ss_u0 - 1.0 hsb_ss_u0_y <= 0
c85: -1.0 hsb_ss_v0_y - hsb_ss_v0 <= 0
c86: hsb_ss_v0 - 0.0 hsb_ss_v0_y <= 0
c87: 1.0 hsb_ss_u1_y - hsb_ss_u1 <= 0
c88: hsb_ss_u1 - 2.0 hsb_ss_u1_y <= 0
c89: 0.0 hsb_ss_v1_y - hsb_ss_v1 <= 0
c90: hsb_ss_v1 - 1.0 hsb_ss_v1_y <= 0

\\Writing the fmin and fmax constraint in relation to x and y for utilities 
 
c91: 0 ch1_1_y - ch1_1_u0 - ch1_1_u1 - ch1_1_v0 - ch1_1_v1 <= 0
c92: ch1_1_u0 + ch1_1_u1 + ch1_1_v0 + ch1_1_v1 - 2 ch1_1_y <= 0
c93: 0 ch1_1_y - ch1_1_u0 - ch1_1_u1 + ch1_1_v0 + ch1_1_v1 <= 0
c94: ch1_1_u0 + ch1_1_u1 - ch1_1_v0 - ch1_1_v1 - 2 ch1_1_y <= 0
c95: 0 ch2_1_y - ch2_1_u0 - ch2_1_u1 - ch2_1_v0 - ch2_1_v1 <= 0
c96: ch2_1_u0 + ch2_1_u1 + ch2_1_v0 + ch2_1_v1 - 2 ch2_1_y <= 0
c97: 0 ch2_1_y - ch2_1_u0 - ch2_1_u1 + ch2_1_v0 + ch2_1_v1 <= 0
c98: ch2_1_u0 + ch2_1_u1 - ch2_1_v0 - ch2_1_v1 - 2 ch2_1_y <= 0
c99: 0 cp_nwk_y - cp_nwk_u0 - cp_nwk_u1 - cp_nwk_v0 - cp_nwk_v1 <= 0
c100: cp_nwk_u0 + cp_nwk_u1 + cp_nwk_v0 + cp_nwk_v1 - 2 cp_nwk_y <= 0
c101: 0 cp_nwk_y - cp_nwk_u0 - cp_nwk_u1 + cp_nwk_v0 + cp_nwk_v1 <= 0
c102: cp_nwk_u0 + cp_nwk_u1 - cp_nwk_v0 - cp_nwk_v1 - 2 cp_nwk_y <= 0
c103: 0 gv2_ss_y - gv2_ss_u0 - gv2_ss_u1 - gv2_ss_v0 - gv2_ss_v1 <= 0
c104: gv2_ss_u0 + gv2_ss_u1 + gv2_ss_v0 + gv2_ss_v1 - 2 gv2_ss_y <= 0
c105: 0 gv2_ss_y - gv2_ss_u0 - gv2_ss_u1 + gv2_ss_v0 + gv2_ss_v1 <= 0
c106: gv2_ss_u0 + gv2_ss_u1 - gv2_ss_v0 - gv2_ss_v1 - 2 gv2_ss_y <= 0
c107: 0 hsb_ss_y - hsb_ss_u0 - hsb_ss_u1 - hsb_ss_v0 - hsb_ss_v1 <= 0
c108: hsb_ss_u0 + hsb_ss_u1 + hsb_ss_v0 + hsb_ss_v1 - 2 hsb_ss_y <= 0
c109: 0 hsb_ss_y - hsb_ss_u0 - hsb_ss_u1 + hsb_ss_v0 + hsb_ss_v1 <= 0
c110: hsb_ss_u0 + hsb_ss_u1 - hsb_ss_v0 - hsb_ss_v1 - 2 hsb_ss_y <= 0

\\Writing Fmin, Fmax constraints for process linear 
 
c111: ch_e_f_c_m_perc = 1
c112: ch_e_f_c_y = 1.0
c113: ch_evap_ret_t_in = 1
c114: ch_evap_ret_y = 1.0

\\Writing Fmin, Fmax constraints for process bilinear 
 

\\Writing the fmin and fmax constraint in relation to x and y for processes 
 

\\Writing stream constraints 
 
c115: 755.0 ch1_enwk_1_m_perc + 0.0 ch1_enwk_1_y - 377.5 ch1_1_u0 - 0.0 ch1_1_u0_y - 377.5 ch1_1_v0 - 0.0 ch1_1_v0_y - 377.5 ch1_1_u1 - 0.0 ch1_1_u1_y - 377.5 ch1_1_v1 - 0.0 ch1_1_v1_y <= 0
c116: 755.0 ch2_enwk_1_m_perc + 0.0 ch2_enwk_1_y - 377.5 ch2_1_u0 - 0.0 ch2_1_u0_y - 377.5 ch2_1_v0 - 0.0 ch2_1_v0_y - 377.5 ch2_1_u1 - 0.0 ch2_1_u1_y - 377.5 ch2_1_v1 - 0.0 ch2_1_v1_y <= 0
c117: 30.0 sp1_temp_t_inout + 273.15 sp1_temp_y - 137.2875 ch1_1_u0 - 0.0 ch1_1_u0_y - 137.2875 ch1_1_v0 - 0.0 ch1_1_v0_y - 137.7125 ch1_1_u1 + 0.42500000000001137 ch1_1_u1_y - 136.86249999999998 ch1_1_v1 - 0.0 ch1_1_v1_y - 137.2875 ch2_1_u0 - 0.0 ch2_1_u0_y - 137.2875 ch2_1_v0 - 0.0 ch2_1_v0_y - 137.7125 ch2_1_u1 + 0.42500000000001137 ch2_1_u1_y - 136.86249999999998 ch2_1_v1 - 0.0 ch2_1_v1_y >= 0
c118: 1.0 ch1_ep_1_m_flow + 0.0 ch1_ep_1_y + 0.0 ch1_ep_1_delp - 755.0 ch1_enwk_1_m_perc - 0.0 ch1_enwk_1_y <= 0
c119: 1.0 ch2_ep_1_m_flow + 0.0 ch2_ep_1_y + 0.0 ch2_ep_1_delp - 755.0 ch2_enwk_1_m_perc - 0.0 ch2_enwk_1_y <= 0
c120: 0.0 ch1_ep_1_m_flow + 0.0 ch1_ep_1_y + 1.0 ch1_ep_1_delp - 24.000586233825587 ch1_enwk_1_m_perc - 3.5629306781598657 ch1_enwk_1_y >= 0
c121: 0.0 ch2_ep_1_m_flow + 0.0 ch2_ep_1_y + 1.0 ch2_ep_1_delp - 8.351813213711074 ch2_enwk_1_m_perc - 3.5629306781598675 ch2_enwk_1_y >= 0
c122: 755.0 ice_nwk_1_m_perc + 0.0 ice_nwk_1_y + 377.5 cp_nwk_u0 + 0.0 cp_nwk_u0_y + 377.5 cp_nwk_v0 + 0.0 cp_nwk_v0_y + 377.5 cp_nwk_u1 + 0.0 cp_nwk_u1_y + 377.5 cp_nwk_v1 + 0.0 cp_nwk_v1_y - 1.0 ch1_ep_1_m_flow - 0.0 ch1_ep_1_y - 0.0 ch1_ep_1_delp - 1.0 ch2_ep_1_m_flow - 0.0 ch2_ep_1_y - 0.0 ch2_ep_1_delp <= 0
c123: 15.0 cp_nwk_u0 + 273.15 cp_nwk_u0_y - 15.0 cp_nwk_v0 + 0.0 cp_nwk_v0_y + 15.0 cp_nwk_u1 + 273.15 cp_nwk_u1_y - 15.0 cp_nwk_v1 + 0.0 cp_nwk_v1_y - 30.0 sp1_temp_t_inout - 273.15 sp1_temp_y >= 0
c124: 2.0 gv2_ss_u0 + 274.15 gv2_ss_u0_y - 2.0 gv2_ss_v0 + 0.0 gv2_ss_v0_y + 2.0 gv2_ss_u1 + 274.15 gv2_ss_u1_y - 2.0 gv2_ss_v1 + 0.0 gv2_ss_v1_y - 30.0 sp1_temp_t_inout - 273.15 sp1_temp_y >= 0
c125: 2.0 hsb_ss_u0 + 274.15 hsb_ss_u0_y - 2.0 hsb_ss_v0 + 0.0 hsb_ss_v0_y + 2.0 hsb_ss_u1 + 274.15 hsb_ss_u1_y - 2.0 hsb_ss_v1 + 0.0 hsb_ss_v1_y - 30.0 sp1_temp_t_inout - 273.15 sp1_temp_y >= 0
c126: 755.0 gv2_nwk_1_m_perc + 0.0 gv2_nwk_1_y + 755.0 hsb_nwk_1_m_perc + 0.0 hsb_nwk_1_y - 755.0 ice_nwk_1_m_perc - 0.0 ice_nwk_1_y <= 0
c127: 377.5 gv2_ss_u0 + 0.0 gv2_ss_u0_y + 377.5 gv2_ss_v0 + 0.0 gv2_ss_v0_y + 377.5 gv2_ss_u1 + 0.0 gv2_ss_u1_y + 377.5 gv2_ss_v1 + 0.0 gv2_ss_v1_y - 755.0 gv2_nwk_1_m_perc - 0.0 gv2_nwk_1_y <= 0
c128: 1.0 para_nwk_con_delp + 0.0 para_nwk_con_y - 2.2281195562364466 ice_nwk_1_m_perc - 0.0 ice_nwk_1_y - 14.376128730059445 gv2_nwk_1_m_perc - 0.0 gv2_nwk_1_y >= 0
c129: 377.5 hsb_ss_u0 + 0.0 hsb_ss_u0_y + 377.5 hsb_ss_v0 + 0.0 hsb_ss_v0_y + 377.5 hsb_ss_u1 + 0.0 hsb_ss_u1_y + 377.5 hsb_ss_v1 + 0.0 hsb_ss_v1_y - 755.0 hsb_nwk_1_m_perc - 0.0 hsb_nwk_1_y <= 0
c130: 1.0 para_nwk_con_delp + 0.0 para_nwk_con_y - 2.2281195562364466 ice_nwk_1_m_perc - 0.0 ice_nwk_1_y - 740.8246107170422 hsb_nwk_1_m_perc - 0.0 hsb_nwk_1_y >= 0
c131: 1.0 dist_np_combi_0_0_m_flow + 0.0 dist_np_combi_0_0_y + 0.0 dist_np_combi_0_0_delp + 1.0 dist_np_combi_1_0_m_flow + 0.0 dist_np_combi_1_0_y + 0.0 dist_np_combi_1_0_delp + 1.0 dist_np_combi_2_0_m_flow + 0.0 dist_np_combi_2_0_y + 0.0 dist_np_combi_2_0_delp + 1.0 dist_np_combi_3_0_m_flow + 0.0 dist_np_combi_3_0_y + 0.0 dist_np_combi_3_0_delp + 1.0 dist_np_combi_4_0_m_flow + 0.0 dist_np_combi_4_0_y + 0.0 dist_np_combi_4_0_delp + 1.0 dist_np_combi_5_0_m_flow + 0.0 dist_np_combi_5_0_y + 0.0 dist_np_combi_5_0_delp + 1.0 dist_np_combi_6_0_m_flow + 0.0 dist_np_combi_6_0_y + 0.0 dist_np_combi_6_0_delp - 377.5 gv2_ss_u0 - 0.0 gv2_ss_u0_y - 377.5 gv2_ss_v0 - 0.0 gv2_ss_v0_y - 377.5 gv2_ss_u1 - 0.0 gv2_ss_u1_y - 377.5 gv2_ss_v1 - 0.0 gv2_ss_v1_y - 377.5 hsb_ss_u0 - 0.0 hsb_ss_u0_y - 377.5 hsb_ss_v0 - 0.0 hsb_ss_v0_y - 377.5 hsb_ss_u1 - 0.0 hsb_ss_u1_y - 377.5 hsb_ss_v1 - 0.0 hsb_ss_v1_y <= 0
c132: 0.0 dist_np_combi_0_0_m_flow + 0.0 dist_np_combi_0_0_y + 1.0 dist_np_combi_0_0_delp + 0.0 dist_np_combi_1_0_m_flow + 0.0 dist_np_combi_1_0_y + 1.0 dist_np_combi_1_0_delp + 0.0 dist_np_combi_2_0_m_flow + 0.0 dist_np_combi_2_0_y + 1.0 dist_np_combi_2_0_delp + 0.0 dist_np_combi_3_0_m_flow + 0.0 dist_np_combi_3_0_y + 1.0 dist_np_combi_3_0_delp + 0.0 dist_np_combi_4_0_m_flow + 0.0 dist_np_combi_4_0_y + 1.0 dist_np_combi_4_0_delp + 0.0 dist_np_combi_5_0_m_flow + 0.0 dist_np_combi_5_0_y + 1.0 dist_np_combi_5_0_delp + 0.0 dist_np_combi_6_0_m_flow + 0.0 dist_np_combi_6_0_y + 1.0 dist_np_combi_6_0_delp - 1.0 para_nwk_con_delp - 0.0 para_nwk_con_y >= 0
c133: 755.0 ch_e_f_c_m_perc + 0.0 ch_e_f_c_y - 1.0 dist_np_combi_0_0_m_flow - 0.0 dist_np_combi_0_0_y - 0.0 dist_np_combi_0_0_delp - 1.0 dist_np_combi_1_0_m_flow - 0.0 dist_np_combi_1_0_y - 0.0 dist_np_combi_1_0_delp - 1.0 dist_np_combi_2_0_m_flow - 0.0 dist_np_combi_2_0_y - 0.0 dist_np_combi_2_0_delp - 1.0 dist_np_combi_3_0_m_flow - 0.0 dist_np_combi_3_0_y - 0.0 dist_np_combi_3_0_delp - 1.0 dist_np_combi_4_0_m_flow - 0.0 dist_np_combi_4_0_y - 0.0 dist_np_combi_4_0_delp - 1.0 dist_np_combi_5_0_m_flow - 0.0 dist_np_combi_5_0_y - 0.0 dist_np_combi_5_0_delp - 1.0 dist_np_combi_6_0_m_flow - 0.0 dist_np_combi_6_0_y - 0.0 dist_np_combi_6_0_delp - 377.5 cp_nwk_u0 - 0.0 cp_nwk_u0_y - 377.5 cp_nwk_v0 - 0.0 cp_nwk_v0_y - 377.5 cp_nwk_u1 - 0.0 cp_nwk_u1_y - 377.5 cp_nwk_v1 - 0.0 cp_nwk_v1_y = 0
c134: 275.0 ch_evap_ret_t_in + 0.0 ch_evap_ret_y - 144.075 cp_nwk_u0 - 0.0 cp_nwk_u0_y - 144.075 cp_nwk_v0 - 0.0 cp_nwk_v0_y - 159.075 cp_nwk_u1 + 15.0 cp_nwk_u1_y - 129.075 cp_nwk_v1 - 0.0 cp_nwk_v1_y - 138.075 gv2_ss_u0 - 0.5676442762535477 gv2_ss_u0_y - 138.075 gv2_ss_v0 - 0.0 gv2_ss_v0_y - 140.075 gv2_ss_u1 + 1.4323557237464524 gv2_ss_u1_y - 136.075 gv2_ss_v1 - 0.0 gv2_ss_v1_y - 138.075 hsb_ss_u0 - 0.34120072706083815 hsb_ss_u0_y - 138.075 hsb_ss_v0 - 0.0 hsb_ss_v0_y - 140.075 hsb_ss_u1 + 1.6587992729391619 hsb_ss_u1_y - 136.075 hsb_ss_v1 - 0.0 hsb_ss_v1_y >= 0

\\Writing additional constraints 
 
\\Writing additional constraints: unit_binary 
 
c135: 1 ch1_1_u0_y + 1 ch1_1_u1_y <= 1
c136: 1 ch1_1_v0_y + 1 ch1_1_v1_y <= 1
c137: 1 ch2_1_u0_y + 1 ch2_1_u1_y <= 1
c138: 1 ch2_1_v0_y + 1 ch2_1_v1_y <= 1
c139: 1 cp_nwk_u0_y + 1 cp_nwk_u1_y <= 1
c140: 1 cp_nwk_v0_y + 1 cp_nwk_v1_y <= 1
c141: 1 gv2_ss_u0_y + 1 gv2_ss_u1_y <= 1
c142: 1 gv2_ss_v0_y + 1 gv2_ss_v1_y <= 1
c143: 1 hsb_ss_u0_y + 1 hsb_ss_u1_y <= 1
c144: 1 hsb_ss_v0_y + 1 hsb_ss_v1_y <= 1
c145: 1 ch1_1_y <= 1
c146: 1 ch2_1_y <= 1
c147: 1 ch1_enwk_1_y <= 1
c148: 1 ch2_enwk_1_y <= 1
c149: 1 ch1_ep_1_y <= 1
c150: 1 ch2_ep_1_y <= 1
c151: 1 ice_nwk_1_y <= 1
c152: 1 gv2_nwk_1_y <= 1
c153: 1 hsb_nwk_1_y <= 1
c154: 1 dist_np_combi_0_0_y + 1 dist_np_combi_1_0_y + 1 dist_np_combi_2_0_y + 1 dist_np_combi_3_0_y + 1 dist_np_combi_4_0_y + 1 dist_np_combi_5_0_y + 1 dist_np_combi_6_0_y <= 1

\\Writing additional constraints: unit_binary_equality 
 
c155: 1 ch1_1_u0_y + 1 ch1_1_v0_y + 1 ch1_1_u1_y + 1 ch1_1_v1_y - 2 ch1_1_y = 0
c156: 1 ch2_1_u0_y + 1 ch2_1_v0_y + 1 ch2_1_u1_y + 1 ch2_1_v1_y - 2 ch2_1_y = 0
c157: 1 cp_nwk_u0_y + 1 cp_nwk_v0_y + 1 cp_nwk_u1_y + 1 cp_nwk_v1_y - 2 cp_nwk_y = 0
c158: 1 gv2_ss_u0_y + 1 gv2_ss_v0_y + 1 gv2_ss_u1_y + 1 gv2_ss_v1_y - 2 gv2_ss_y = 0
c159: 1 hsb_ss_u0_y + 1 hsb_ss_v0_y + 1 hsb_ss_u1_y + 1 hsb_ss_v1_y - 2 hsb_ss_y = 0

\\Writing additional constraints: stream_limit_modified 
 
c160: 377.5 ch1_1_u0 - 109.19515675 ch1_1_u0_y + 377.5 ch1_1_v0 + 0.0 ch1_1_v0_y + 377.5 ch1_1_u1 - 109.19515675 ch1_1_u1_y + 377.5 ch1_1_v1 + 0.0 ch1_1_v1_y >= 0
c161: 377.5 ch2_1_u0 - 410.22658895 ch2_1_u0_y + 377.5 ch2_1_v0 + 0.0 ch2_1_v0_y + 377.5 ch2_1_u1 - 410.22658895 ch2_1_u1_y + 377.5 ch2_1_v1 + 0.0 ch2_1_v1_y >= 0
c162: 0.01642977629679675 ch1_ep_1_m_flow + 0.0 ch1_ep_1_y + 1 ch1_ep_1_delp <= 12.3463827922
c163: 0.011014262430158663 ch2_ep_1_m_flow + 0.0 ch2_ep_1_y + 1 ch2_ep_1_delp <= 21.4327511013
c164: 0.015650263985336702 dist_np_combi_0_0_m_flow + 0.0 dist_np_combi_0_0_y + 1 dist_np_combi_0_0_delp <= 34.0585340963
c165: 0.0483851457282987 dist_np_combi_1_0_m_flow + 0.0 dist_np_combi_1_0_y + 1 dist_np_combi_1_0_delp <= 46.1796318122
c166: 0.019894118806164172 dist_np_combi_2_0_m_flow + 0.0 dist_np_combi_2_0_y + 1 dist_np_combi_2_0_delp <= 50.3198893609
c167: 0.01381832039734728 dist_np_combi_3_0_m_flow + 0.0 dist_np_combi_3_0_y + 1 dist_np_combi_3_0_delp <= 58.2250275059
c168: 0.007755557609803185 dist_np_combi_4_0_m_flow + 0.0 dist_np_combi_4_0_y + 1 dist_np_combi_4_0_delp <= 73.1928514998
c169: 0.04639114698064178 dist_np_combi_5_0_m_flow + 0.0 dist_np_combi_5_0_y + 1 dist_np_combi_5_0_delp <= 35.2618445622
c170: 0.015650263985336702 dist_np_combi_6_0_m_flow + 0.0 dist_np_combi_6_0_y + 1 dist_np_combi_6_0_delp <= 34.0585340963
c171: 0.8808333333333335 gv2_ss_u0 - 0.2 gv2_ss_u0_y + 0.8808333333333335 gv2_ss_v0 + 0.0 gv2_ss_v0_y + 0.8808333333333335 gv2_ss_u1 - 0.2 gv2_ss_u1_y + 0.8808333333333335 gv2_ss_v1 + 0.0 gv2_ss_v1_y >= 0
c172: 1.4654130555555558 hsb_ss_u0 - 0.1 hsb_ss_u0_y + 1.4654130555555558 hsb_ss_v0 + 0.0 hsb_ss_v0_y + 1.4654130555555558 hsb_ss_u1 - 0.1 hsb_ss_u1_y + 1.4654130555555558 hsb_ss_v1 + 0.0 hsb_ss_v1_y >= 0

\\Writing additional constraints: bilinear_limits_fmin_util 
 
c173: 186.84016458333835 ch1_1_u0 + 0.0 ch1_1_u0_y + 186.84016458333835 ch1_1_v0 + 0.0 ch1_1_v0_y - 186.84016458333832 ch1_1_u1 + 373.6803291666767 ch1_1_u1_y + 560.520493750015 ch1_1_v1 + 0.0 ch1_1_v1_y  - 0.0 ch1_1_y >= 0
c174: 186.84016458333835 ch2_1_u0 + 0.0 ch2_1_u0_y + 186.84016458333835 ch2_1_v0 + 0.0 ch2_1_v0_y - 186.84016458333832 ch2_1_u1 + 373.6803291666767 ch2_1_u1_y + 560.520493750015 ch2_1_v1 + 0.0 ch2_1_v1_y  - 0.0 ch2_1_y >= 0

\\Writing additional constraints: bilinear_limits_fmax_util 
 
c175: 186.84016458333835 ch1_1_u0 + 0.0 ch1_1_u0_y + 186.84016458333835 ch1_1_v0 + 0.0 ch1_1_v0_y - 186.84016458333832 ch1_1_u1 + 373.6803291666767 ch1_1_u1_y + 560.520493750015 ch1_1_v1 + 0.0 ch1_1_v1_y - 2000.0 ch1_1_y <= 0
c176: 186.84016458333835 ch2_1_u0 + 0.0 ch2_1_u0_y + 186.84016458333835 ch2_1_v0 + 0.0 ch2_1_v0_y - 186.84016458333832 ch2_1_u1 + 373.6803291666767 ch2_1_u1_y + 560.520493750015 ch2_1_v1 + 0.0 ch2_1_v1_y - 7330.0 ch2_1_y <= 0

\\Writing additional constraints: bilinear_limits_fmax_proc, equality 
 

Binary 
 
ch1_1_y
ch2_1_y
ch1_enwk_1_y
ch2_enwk_1_y
ch1_ep_1_y
ch2_ep_1_y
sp1_temp_y
cp_nwk_y
ice_nwk_1_y
gv2_nwk_1_y
hsb_nwk_1_y
para_nwk_con_y
dist_np_combi_0_0_y
dist_np_combi_1_0_y
dist_np_combi_2_0_y
dist_np_combi_3_0_y
dist_np_combi_4_0_y
dist_np_combi_5_0_y
dist_np_combi_6_0_y
gv2_ss_y
hsb_ss_y
ch1_1_u0_y
ch1_1_v0_y
ch1_1_u1_y
ch1_1_v1_y
ch2_1_u0_y
ch2_1_v0_y
ch2_1_u1_y
ch2_1_v1_y
cp_nwk_u0_y
cp_nwk_v0_y
cp_nwk_u1_y
cp_nwk_v1_y
gv2_ss_u0_y
gv2_ss_v0_y
gv2_ss_u1_y
gv2_ss_v1_y
hsb_ss_u0_y
hsb_ss_v0_y
hsb_ss_u1_y
hsb_ss_v1_y

End 
