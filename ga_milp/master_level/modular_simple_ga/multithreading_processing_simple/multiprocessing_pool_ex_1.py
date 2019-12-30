##This is the multiprocessing pool example 2

def calc_math (x1, x2, x3):
    
   sum1 = 0    
   if x3 == 'ok':
        for i in range (0, x1):
            sum1 = sum1 + x2
       
   return sum1

if __name__ == '__main__':
    import multiprocessing as mp
    
    array_x1 = [1, 4, 5]
    array_x2 = [10, 20, 30]
    array_x3 = ['ok', 'not_ok', 'ok']
    
    array_compiled = [array_x1, array_x2, array_x3]
    
    p = mp.Pool()
    result = p.map(calc_math, array_compiled)
    p.close()
    p.join()
    
    print(result)


