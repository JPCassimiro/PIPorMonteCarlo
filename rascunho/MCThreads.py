import random
import time
import threading

# lock para resultsThread
lock = threading.Lock()

#globais
num_inside = 0

resultsThreads = [] # array que vai armazenar o resultado

def estimate_piThread(totalPoints, resultsThreads, localRandom):
    timeStart = int(round(time.time() * 1000))
    hitLocal = 0  #varaivel local para cada thread
    for i in range(totalPoints):
        x = localRandom.uniform(-1,1)
        y = localRandom.uniform(-1,1)
        if x**2 + y**2 <= 1:
            hitLocal += 1
    timeEnd = int(round(time.time() * 1000))
    with lock:
        resultsThreads.append(hitLocal)
    print("\n",threading.current_thread().name, "terminou sua parte em: ", (timeEnd - timeStart), "ms")
    
if __name__ == "__main__":
    iterate = 4550000 #valor padrão
    # iterate = 3000
    # iterate = 9000
    # iterate = 500000
    # iterate = 1000000000000 #trava    
    numThreads = 30
    timeStart = int(round(time.time() * 1000))

    threads = []
    for i in range(numThreads):  # criando threads
        localRandom = random # passa instace de random para cada thread, assim cada thread tem seu random individual
        t = threading.Thread(target=estimate_piThread, args=(iterate // numThreads, resultsThreads, localRandom))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

    num_inside = sum(resultsThreads)

    piResult = 4 * num_inside / iterate

    timeEnd = int(round(time.time() * 1000))

    print("\nEstimativa de pi: ", piResult)
    print("\nO processo todo demorou: ", (timeEnd - timeStart), "ms")