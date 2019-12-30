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
    x_eval = (-C[1]-(pow(discriminant ,0.5)))/(2*C[0])
    y_eval = A[0]*pow(x_eval,2) + A[1]*x_eval + A[2]

    D = []
    D.append(x_eval)
    D.append(y_eval)
    
    return D