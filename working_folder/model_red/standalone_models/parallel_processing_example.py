##Parallel processing example 

#Multi-threading example  
def multithreading_example():
    import time 
    import threading 
    
    def calc_square(numbers):
        print('calculate square numbers')
        
        for n in numbers:
            time.sleep(0.2)
            print('square: ' ,n*n)
            
    def calc_cube(numbers):
        print('calculate cube of numbers')
        for n in numbers:
            time.sleep(0.2)
            print('cube:', n*n*n)
            
    arr = [2,3,8,9]
    t = time.time()
    
    ##Create a thread 
    t1 = threading.Thread(target = calc_square, args=(arr, ))
    t2 = threading.Thread(target = calc_cube, args=(arr, ))
    
    ##Start the threads
    t1.start()
    t2.start()
    ##Wait until the threads are done, before executing the rest of the code  
    t1.join()
    t2.join()
    
    #calc_square(arr)
    #calc_cube(arr)
    
    print('done in: ', time.time() - t)
    print('Hah... I am done with all my work now!')
    
    return

##Multi-processing example
def multiprocessing_example():
    import time  
    import multiprocessing 
    
    def calc_square1(numbers):
        print('calculate square numbers')
        
        for n in numbers:
            time.sleep(0.2)
            print('square: ' + str(n*n))
    
    def calc_cube1(numbers):
        print('calculate cube of numbers')
        for n in numbers:
            time.sleep(0.2)
            print('cube:' + str(n*n*n))
    
    if __name__ == '__main__':
        arr = [2,3,8,9]
        p1 = multiprocessing.Process(target=calc_square1, args=(arr,))
        p2 = multiprocessing.Process(target=calc_cube1, args=(arr,))
    
        ##Start the processes
        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
        
        
        print('Done!')
    return

multiprocessing_example()