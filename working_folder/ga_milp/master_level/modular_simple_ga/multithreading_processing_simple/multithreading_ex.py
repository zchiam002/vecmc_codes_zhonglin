##This is a multithreading excercise 

import time 

def calc_square(numbers):
    print('calculate square numbers')
    for n in numbers:
        time.sleep(0.2)
        print('square:', n*n)
    return

def calc_cube(numbers):
    print('calculate cube of numbers')
    for n in numbers:
        time.sleep(0.2)
        print('cube:', n*n*n)
    return
    
arr = [2,3,8,9]

t = time.time()
calc_square(arr)
calc_cube(arr)

print('done in : ', time.time() - t)
print('hah... I am done with my work now! \n')

##To demonstrate how multi-threading will be useful
##The time delay was introduced to make the cpu do work during time delay

import threading 


def calc_square(numbers):
    print('calculate square numbers')
    for n in numbers:
        time.sleep(0.2)
        print('square:', n*n)
    return

def calc_cube(numbers):
    print('calculate cube of numbers')
    for n in numbers:
        time.sleep(0.2)
        print('cube:', n*n*n)
    return
    
arr = [2,3,8,9]

t = time.time()

##Create threads
t1 = threading.Thread(target = calc_square, args = (arr,))
t2 = threading.Thread(target = calc_cube, args = (arr,))

##Starting the threads 
t1.start()
t2.start()

##Wait until the thread is done, this is the waiting function 
t1.join()
t2.join()


print('done in : ', time.time() - t)
print('hah... I am done with my work now!')

##Multithreading is used when the cpu is idle... or else it will not be of any benefit 