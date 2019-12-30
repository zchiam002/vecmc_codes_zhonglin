##This is the multiprocessing lock excercise 

##Why do we need lock at the same time? to lock variables so that multiple process are unable to access it at the same time 
##If we do not so that? 


import time 
import multiprocessing 

def deposit(balance, lock):
    for i in range (100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()
    return 
    
def withdraw(balance, lock):
    for i in range (100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()
        
if __name__ == '__main__':
    ##This is a shared memory resource 
    balance = multiprocessing.Value('i', 200)
    ##create a lock variable 
    lock = multiprocessing.Lock()
    d = multiprocessing.Process(target=deposit, args = (balance, lock))
    w = multiprocessing.Process(target=withdraw, args = (balance, lock))
    d.start()
    w.start()
    d.join()
    w.join()
    
    print(balance.value)
