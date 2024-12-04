import random
import time

def estimate_pi(totalPoints):
    hit = 0
    for i in range(totalPoints):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            hit += 1
    piResult = 4 * hit / totalPoints
    return piResult

if __name__=="__main__":
    totalRuns = 1
    
    iterate = 4550000
    # iterate = 3000
    # iterate = 9000
    # iterate = 500000
    # iterate = 1000000000000 #trava

    for i in range(totalRuns):
        timeStart = int(round(time.time() * 1000))
        piResult = estimate_pi(iterate)
        timeEnd = int(round(time.time() * 1000))
        print("\nEstimativa de pi: : ", piResult)
        print("\nEm: ", (timeEnd-timeStart),"ms")
