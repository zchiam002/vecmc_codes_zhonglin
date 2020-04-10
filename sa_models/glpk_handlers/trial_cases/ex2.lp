Minimize

obj: 0.00 y_ch1_1 + 23.93 y_ch1_2 - 68.94 y_ch1_3 - 225.79 y_ch1_4 + 0.00 y_ch2_1 + 279.49 y_ch2_2 + 34.47 y_ch2_3 - 367.07 y_ch2_4 + 0.00 y_ch3_1 + 279.49 y_ch3_2 + 34.47 y_ch3_3 - 367.074 y_ch3_4 + 0.00 y_sp1 + 0.00 y_sscp 
     + 0.00 y_ssgv2 + 0.00 y_sshsb + 0.00 y_sspfa + 0.00 y_ssser + 0.00 y_ssfir + 0.00 y_sp2 + 403.94 u_ch1_1 + 308.20 u_ch1_2 + 493.97 u_ch1_3 + 703.10 u_ch1_4 + 2027.47 u_ch2_1 + 909.50 u_ch2_2 + 1399.54 u_ch2_3 
     + 1934.93 u_ch2_4 + 2027.47 u_ch3_1 + 909.50 u_ch3_2 + 1399.54 u_ch3_3 + 1934.93 u_ch3_4 + 0.00 u_sp1 + 0.00 u_sscp + 0.00 u_ssgv2 + 0.00 u_sshsb + 0.00 u_sspfa + 0.00 u_ssser + 0.00 u_ssfir + 0.00 u_sp2 

Subject To

c1: 0 y_ch1_1 - u_ch1_1 <= 0
c2: 0.25 y_ch1_2 - u_ch1_2 <= 0
c3: 0.5 y_ch1_3 - u_ch1_3 <= 0
c4: 0.75 y_ch1_4 - u_ch1_4 <= 0
c5: 0 y_ch2_1 - u_ch2_1 <= 0
c6: 0.25 y_ch2_2 - u_ch2_2 <= 0
c7: 0.5 y_ch2_3 - u_ch2_3 <= 0
c8: 0.75 y_ch2_4 - u_ch2_4 <= 0
c9: 0 y_ch3_1 - u_ch3_1 <= 0
c10: 0.25 y_ch3_2 - u_ch3_2 <= 0
c11: 0.5 y_ch3_3 - u_ch3_3 <= 0
c12: 0.75 y_ch3_4 - u_ch3_4 <= 0

c13: 0 y_sp1 - u_sp1 <= 0
c14: 0 y_sscp - u_sscp <= 0
c15: 0 y_ssgv2 - u_ssgv2 <= 0
c16: 0 y_sshsb - u_sshsb <= 0
c17: 0 y_sspfa - u_sspfa <= 0
c18: 0 y_ssser - u_ssser <= 0
c19: 0 y_ssfir - u_ssfir <= 0
c20: 0 y_sp2 - u_sp2 <= 0

c21: u_ch1_1 - 0.25 y_ch1_1 <= 0
c22: u_ch1_2 - 0.5 y_ch1_2 <= 0
c23: u_ch1_3 - 0.75 y_ch1_3 <= 0
c24: u_ch1_4 - 1 y_ch1_4 <= 0
c25: u_ch2_1 - 0.25 y_ch2_1 <= 0
c26: u_ch2_2 - 0.5 y_ch2_2 <= 0
c27: u_ch2_3 - 0.75 y_ch2_3 <= 0
c28: u_ch2_4 - 1 y_ch2_4 <= 0
c29: u_ch3_1 - 0.25 y_ch3_1 <= 0
c30: u_ch3_2 - 0.5 y_ch3_2 <= 0
c31: u_ch3_3 - 0.75 y_ch3_3 <= 0
c32: u_ch3_4 - 1 y_ch3_4 <= 0
c33: u_sp1 - 1 y_sp1 <= 0
c34: u_sscp - 1 y_sscp <= 0
c35: u_ssgv2 - 1 y_ssgv2 <= 0
c36: u_sshsb - 1 y_sshsb <= 0
c37: u_sspfa - 1 y_sspfa <= 0
c38: u_ssser - 1 y_ssser <= 0
c39: u_ssfir - 1 y_ssfir <= 0
c40: u_sp2 - 1 y_sp2 <= 0

c41: 27.87 y_ch1_1 + 27.87 y_ch1_2 + 27.87 y_ch1_3 + 27.87 y_ch1_4 + 128.56 y_ch2_1 + 128.56 y_ch2_2 + 128.56 y_ch2_3 + 128.56 y_ch2_4 + 128.56 y_ch3_1 + 128.56 y_ch3_2 + 128.56 y_ch3_3 + 128.56 y_ch3_4 
     - 0.81 u_ch1_1 - 0.81 u_ch1_2 - 0.81 u_ch1_3 - 0.81 u_ch1_4 - 4.89 u_ch2_1 - 4.89 u_ch2_2 - 4.89 u_ch2_3 - 4.89 u_ch2_4 - 4.89 u_ch3_1 - 4.89 u_ch3_2 - 4.89 u_ch3_3 - 4.89 u_ch3_4 - 0 y_sp1 - 1000 u_sp1 = 0

c42: 0 y_sp1 + 1000 u_sp1 - 0 y_sscp - 1000 u_sscp = 0
c43: 0 y_sp1 + 1000 u_sp1 - 0 y_ssgv2 - 1000 u_ssgv2 = 0
c44: 0 y_sp1 + 1000 u_sp1 - 0 y_sshsb - 1000 u_sshsb = 0
c45: 0 y_sp1 + 1000 u_sp1 - 0 y_sspfa - 1000 u_sspfa = 0
c46: 0 y_sp1 + 1000 u_sp1 - 0 y_ssser - 1000 u_ssser = 0
c47: 0 y_sp1 + 1000 u_sp1 - 0 y_ssfir - 1000 u_ssfir = 0

c48: 0 y_sscp + 0.63 y_ssgv2 + 0.63 y_sshsb + 0.63 y_sspfa + 0.63 y_ssser + 0 y_ssfir + 100 u_sscp + 299.81 u_ssgv2 + 199.87 u_sshsb + 199.87 u_sspfa + 199.87 u_ssser + 0 u_ssfir - 0 y_sp2 - 1000 u_sp2 = 0

c49: 0 y_sp2 + 1000 u_sp2 - 0 y_ch1_ret - 285 u_ch1_ret = 0
c50: 0 y_sp2 + 1000 u_sp2 - 0 y_ch2_ret - 285 u_ch2_ret = 0
c51: 0 y_sp2 + 1000 u_sp2 - 0 y_ch3_ret - 285 u_ch3_ret = 0
c52: y_ch1_ret = 1
c53: y_ch2_ret = 1
c54: y_ch3_ret = 1
c55: u_ch1_ret = 1
c56: u_ch2_ret = 1
c57: u_ch3_ret = 1

c58: y_ch1_1 + y_ch1_2 + y_ch1_3 + y_ch1_4 <= 1
c59: y_ch2_1 + y_ch2_2 + y_ch2_3 + y_ch2_4 <= 1
c60: y_ch3_1 + y_ch3_2 + y_ch3_3 + y_ch3_4 <= 1

Bounds

0 <= y_ch1_1 <= 1
0 <= y_ch1_2 <= 1
0 <= y_ch1_3 <= 1
0 <= y_ch1_4 <= 1
0 <= y_ch2_1 <= 1
0 <= y_ch2_2 <= 1
0 <= y_ch2_3 <= 1
0 <= y_ch2_4 <= 1
0 <= y_ch3_1 <= 1
0 <= y_ch3_2 <= 1
0 <= y_ch3_3 <= 1
0 <= y_ch3_4 <= 1
0 <= y_sp1 <= 1
0 <= y_sscp <= 1
0 <= y_ssgv2 <= 1
0 <= y_sshsb <= 1
0 <= y_sspfa <= 1
0 <= y_ssser <= 1
0 <= y_ssfir <= 1
0 <= y_sp2 <= 1
0 <= u_ch1_1 <= 1000
0 <= u_ch1_2 <= 1000
0 <= u_ch1_3 <= 1000
0 <= u_ch1_4 <= 1000
0 <= u_ch2_1 <= 1000
0 <= u_ch2_2 <= 1000
0 <= u_ch2_3 <= 1000
0 <= u_ch2_4 <= 1000
0 <= u_ch3_1 <= 1000
0 <= u_ch3_2 <= 1000
0 <= u_ch3_3 <= 1000
0 <= u_ch3_4 <= 1000
0 <= u_sp1 <= 1000
0 <= u_sscp <= 1000
0 <= u_ssgv2 <= 1000
0 <= u_sshsb <= 1000
0 <= u_sspfa <= 1000
0 <= u_ssser <= 1000
0 <= u_ssfir <= 1000
0 <= u_sp2 <= 1000

Integer

y_ch1_1
y_ch1_2
y_ch1_3
y_ch1_4
y_ch2_1
y_ch2_2
y_ch2_3
y_ch2_4
y_ch3_1
y_ch3_2
y_ch3_3
y_ch3_4
y_sp1
y_sscp
y_ssgv2
y_sshsb
y_sspfa
y_ssser
y_ssfir
y_sp2


End

