import multiprocessing 

##Queue is used to share data between processes

def calc_square(numbers, q):
    for n in numbers:
        ##Placing data at the end of the queue
        q.put(n*n)
        
if __name__ == '__main__':
    numbers = [2,3,5]
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target= calc_square, args = (numbers, q))
    
    p.start()
    p.join()
    
    while q.empty() is False :
        ##Getting the data from the front of the queue 
        print(q.get())