##Shared data between processes using array and value excercise 

import multiprocessing 

##Shared memory has a different set of operators, such as append cannot work 


def calc_square(numbers, result):
    for idx, n in enumerate(numbers):
        result[idx] = n*n
    
if __name__ == '__main__':
    numbers = [2,3,5]
    ##This is the shared memory variable 
    result = multiprocessing.Array('i', 3)
    p = multiprocessing.Process(target = calc_square, args = (numbers, result))
    
    p.start()
    p.join()
    
    print(result[:])
    
