##This is the multiprocessing pool example 
import multiprocessing 
#print (multiprocessing.cpu_count())
import time 


def f(n):
    sum = 0
    print(n)
    for x in range(n):
#        if x == 3:
#            time.sleep(5)
        sum += x*x
        
    return sum 

if __name__ == '__main__':
    array = [1,2,3,4,5]
    t1 = time.time()
    p = multiprocessing.Pool()
    ##Dividing the load amongst all available cores on the cpu
    result = p.map(f, array)
    print(result)
    ##Close up the pools 
    p.close()
    p.join()        
    print('Pool took:', time.time() - t1)
    
    t2 = time.time()
    result = []
    for x in range (1,6):
        result.append((f(x)))
    print(result)
        
    print('Serial processing took: ', time.time() - t2)