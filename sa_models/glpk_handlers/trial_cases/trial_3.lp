Minimize 
obj: 447.30 u_ch1 + 0 y_ch1 + 1567.86 u_ch2 + 0 y_ch2 + 1567.86 u_ch3 + 0 y_ch3

Subject To
c1: 0 y_ch1 - u_ch1 <= 0
c2: -1 y_ch1 + u_ch1 <= 0
c3: 0 y_ch2 - u_ch2 <= 0
c4: -1 y_ch2 + u_ch2 <= 0 
c5: 0 y_ch3 - u_ch3 <= 0
c6: -1 y_ch3 + u_ch3 <= 0

c7: 1.11337509 u_ch1 + 41.41543847 y_ch1 + 4.18098747 u_ch2 + 116.36728077 y_ch2 + 4.18098747 u_ch3 + 116.36728077 y_ch3 - L1_in = 0

c8: L1_in - L1_out = 0
c9: L1_out - T_s1_in = 0

c10: T_s1_in - L2_in = 0
c11: T_s1_in - L3_in = 0
c12: T_s1_in - L4_in = 0
c13: T_s1_in - L5_in = 0
c14: T_s1_in - L6_in = 0
c15: T_s1_in - L7_in = 0

c16: L2_in-L2_out = 0
c17: L3_in-L3_out = 0
c18: L4_in-L4_out = 0
c19: L5_in-L5_out = 0
c20: L6_in-L6_out = 0
c21: L7_in-L7_out = 0

c22: L2_out-SS1_in = 0
c23: L3_out-SS2_in = 0
c24: L4_out-SS3_in = 0
c25: L5_out-SS4_in = 0
c26: L6_out-SS5_in = 0
c27: L7_out-SS6_in = 0

c28: 0.1 SS1_in - 0.1 SS1_out = 0
c29: 0.3 SS2_in - 0.3 SS2_out = -2.4
c30: 0.2 SS3_in - 0.2 SS3_out = -2
c31: 0.2 SS4_in - 0.2 SS4_out = -2
c32: 0.2 SS5_in - 0.2 SS5_out = -2
c33: 0 SS6_in - 0 SS6_out = 0

c34: 0.1 SS1_out - L8_in = 0
c35: 0.3 SS2_out - L9_in = 0
c36: 0.2 SS3_out - L10_in = 0
c37: 0.2 SS4_out - L11_in = 0
c38: 0.2 SS5_out - L12_in = 0
c39: 0 SS6_out - L13_in = 0

c40: L8_in - L8_out = 0
c41: L9_in - L9_out = 0
c42: L10_in - L10_out = 0
c43: L11_in - L11_out = 0
c44: L12_in - L12_out = 0
c45: L13_in - L13_out = 0

c46: L8_out + L9_out + L10_out + L11_out + L12_out + L13_out - T_s2_in = 0
c47: T_s2_in - T_s2_out = 0

c48: T_s2_out - L14_in = 0
c49: T_s2_out - L15_in = 0
c50: T_s2_out - L16_in = 0

c51: L14_out - L14_in = 0
c52: L15_out - L15_in = 0
c53: L16_out - L16_in = 0

c54: L14_in = 285
c55: L15_in = 285
c56: L16_in = 285

Bounds 
0 <= u_ch1 <= 1
0 <= y_ch1 <= 1
0 <= u_ch2 <= 1
0 <= y_ch2 <= 1
0 <= u_ch3 <= 1
0 <= y_ch3 <= 1

General 
y_ch1
y_ch2
y_ch3

End