import random
import time

def estimate_pi(num_samples):
    num_inside = 0
    for i in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            num_inside += 1
    pi_estimate = 4 * num_inside / num_samples
    timeEnd = int(round(time.time() * 1000))
    return pi_estimate

for i in range(10):
  timeStart = int(round(time.time() * 1000))
  pi_estimate = estimate_pi(4550000)
  timeEnd = int(round(time.time() * 1000))
  print("Estimated value of pi:", pi_estimate)
  print("\nIn: ", (timeEnd-timeStart),"ms")
