##This is the choosing function for combinations 

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def ncr(n, r):
    
    num = factorial(n)
    
    den = factorial(r) * factorial(n-r)    
    return num/den