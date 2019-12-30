import threading 
from queue import Queue 
import time 

##print function is locked 
print_lock = threading.Lock()

def exampleJob(worker):
    time.sleep(0.5)
    
    with print_lock:
        print(threading.current_thread().name, worker)

def threader():
    while True: 
        worker = q.get()
        exampleJob(worker)
        q.task_done()
        
        
q = Queue()

for x in range (0,10):
    t = threading.Thread(target = threader)
    t.daemon = True ##dies when the main thread dies, default is false  
    t.start()
    
start = time.time()

for worker in range (0,200):
    q.put(worker)
    
##Wait until the thread terminates
q.join()

print('Entire job took: ' + str(time.time() - start))
