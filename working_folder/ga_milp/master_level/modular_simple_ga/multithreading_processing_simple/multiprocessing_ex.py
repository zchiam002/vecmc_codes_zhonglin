import time 
import multiprocessing 

square_result = []

def calc_square(numbers):
    for n in numbers:
        print('square ' + str(n*n))
    return
    
def calc_cube(numbers):
    for n in numbers:
        print('cube ' + str(n*n*n))
    return
    
def calc_square_global_var(numbers):
    global square_result
    #time.sleep(5)
    for n in numbers:
        print('square ' + str(n*n))

        square_result.append(n*n)
    print('within a process: result ' + str(square_result))

    return

#if __name__ == '__main__':
#    arr= [2,3,8,9]
#    p1 = multiprocessing.Process(target = calc_square, args = (arr,))
#    p2 = multiprocessing.Process(target = calc_cube, args = (arr,))
#    
#    ##Start the processes
#    p1.start()
#    p2.start()
#    
#    ##Wait until the processes are over
#    p1.join()
#    p2.join()
#    
#    
#    print('Done! \n')

##intoducing a global variable
if __name__ == '__main__':

    arr= [2,3,8,9]
    p1 = multiprocessing.Process(target = calc_square_global_var, args = (arr,))
    
    ##Start the processes
    p1.start()
    
    ##Wait until the processes are over
    p1.join()
    
    ##Result will be empty because each process will be it copies and modifies within 
    ##The process only. it does not return the values
    print('result ' + str(square_result))

    print('Done! \n')


    
    