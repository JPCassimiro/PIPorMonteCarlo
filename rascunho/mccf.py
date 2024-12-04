import random
import time
import concurrent.futures

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
    resultsThreads.append(hitLocal)
    print("\nterminou sua parte em: ", (timeEnd - timeStart), "ms")
    
if __name__ == "__main__":
    iterate = 4550000 #valor padrão
    # iterate = 3000
    # iterate = 9000
    # iterate = 500000
    # iterate = 1000000000000 #trava    
    numThreads = 8
    timeStart = int(round(time.time() * 1000))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        futures = []
        for i in range(numThreads):
            threadRandom = random
            futures.append(executor.submit(estimate_piThread, totalPoints = (iterate//numThreads), resultsThreads=resultsThreads, localRandom=threadRandom))
            
    num_inside = sum(resultsThreads)

    piResult = 4 * num_inside / iterate

    timeEnd = int(round(time.time() * 1000))

    print("\nEstimativa de pi: ", piResult)
    print("\nO processo todo demorou: ", (timeEnd - timeStart), "ms")