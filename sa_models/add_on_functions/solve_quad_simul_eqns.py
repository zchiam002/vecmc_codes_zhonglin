##This is the script for calculating the intersection points of the selected pump.
##It returns the pressure-drop value and associated flowrate of the point of intersection 

def solve_quad_simul_eqns(A, B):
    ##A[0]      --- x^2 coeff of A
    ##A[1]      --- x coeff of A
    ##A[2]      --- constant of A
    ##B[0]      --- x^2 coeff of B
    ##B[1]      --- x coeff of B
    ##B[2]      --- constant of B
    
    C = []
    C.append(A[0]-B[0])     ##x^2 new coefficient 
    C.append(A[1]-B[1])     ##x new coefficient 
    C.append(A[2]-B[2])     ##new constant 
    
    ##Since only the value which is 'more' positive is needed, 
    
    discriminant = pow(C[1],2) - (4*C[0]*C[2])
    x_eval1 = (-C[1]-(pow(discriminant ,0.5)))/(2*C[0])
    y_eval1 = A[0]*pow(x_eval1,2) + A[1]*x_eval1 + A[2]

    x_eval2 = (-C[1]+(pow(discriminant ,0.5)))/(2*C[0])
    y_eval2 = A[0]*pow(x_eval2,2) + A[1]*x_eval2 + A[2]    

    if x_eval1 > x_eval2:
        x_eval = x_eval1
        y_eval = y_eval1
    else:
        x_eval = x_eval2
        y_eval = y_eval2
        
    D = []
    D.append(x_eval)
    D.append(y_eval)
    
    return D