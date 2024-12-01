import random
import time
import threading

#globais
num_inside = 0
iterate = 4550000
results = []

def estimate_piThread(num_samples, result):
    timeStart = int(round(time.time() * 1000))
    num_inside_local = 0  #varaivel local para cada thread
    for i in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            num_inside_local += 1
    result.append(num_inside_local)  
    timeEnd = int(round(time.time() * 1000))
    print("\nUma thread terminou sua parte em: ", (timeEnd - timeStart), "ms")
    
timeStart = int(round(time.time() * 1000))

threads = []
for i in range(8):  # Criando 8 threads
    t = threading.Thread(target=estimate_piThread, args=(iterate // 8, results))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

num_inside = sum(results)

pi_estimate = 4 * num_inside / iterate

timeEnd = int(round(time.time() * 1000))

print("\nEstimativa de pi: ", pi_estimate)
print("\nO processo todo demorou: ", (timeEnd - timeStart), "ms")