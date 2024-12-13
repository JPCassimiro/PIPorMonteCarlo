import socket
import random
import time


def estimate_pi(totalPoints):
    hit = 0
    for i in range(totalPoints):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            hit += 1
    return hit

if __name__=="__main__":
    HOST = socket.gethostname()
    PORT = 4500
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))#não iniciar recebendo mensagem do server 
        loop = True
        s.sendall(bytes("\nHello World",'UTF-8'))
        while loop:
            try:
                # data = s.recv(1024).decode()
                # print(f"{str(data)}")
                
                recieved_slice = int(s.recv(1024).decode())
                print(f"{recieved_slice}")

                if(recieved_slice > 0):
                    time_start = int(round(time.time() * 1000))
                    return_value = estimate_pi(recieved_slice)
                    time_end = int(round(time.time() * 1000))
                    s.sendall(bytes(str(return_value),'UTF-8'))
                    print(f"\nProcesso terminado em {time_end-time_start}ms")
                    loop = False
                    break
                    
            except:
                print("\nErro na conexão")
                loop = False
                break
                
            
