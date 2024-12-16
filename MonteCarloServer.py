import socket
import threading
import time

#setup com porta, host e numero maximo de clients
HOST = socket.gethostname()
PORT = 4500
MAX_CLIENTS = 4

#array de clients esperando para receber uma thread
connected_clients = []

#array de resultados
partial_results = []

#lock para evitar condição de corrida
lock = threading.Lock()

#thread do client
def thread_client(conn, addr, slice):
    time_start = int(round(time.time() * 1000))
    loop = True
    data = conn.recv(1024).decode()
    print(f"\n{str(data)} de client: {addr}")
    while loop:
        try: 
            conn.sendto(bytes(str(slice),'UTF-8'),addr) #envia slices para o client
            client_result = int(conn.recv(1024).decode())   #recebe resultado do client
            print(f"\nResultado da operação feita pelo client {addr}: {client_result}")
            if(client_result > 0):  
                with lock:  #lock para evitar condição de corrida
                    partial_results.append(client_result)   #coloca os resultados no array de resultados parciais
                loop = False
                time_end = int(round(time.time() * 1000))
                print(f"\nThread do client {addr} terminou em: {time_end-time_start}ms")
                break
        except:
                #caso encontre qualquer exception, quebra loop
                loop = False
                break
            
def main():
    global connected_clients
    total_points = 4550000
    threads = []
    time_start = int(round(time.time() * 1000))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT)) #vai atuar nesse host e nessa porta
        s.listen()  #espera conexões
        loop = True
        while loop:
            print(f"\nEsperando conexão: ({HOST},{PORT})")
            conn, addr = s.accept() #aceita conexão
            connected_clients.append({'conn':conn,'addr':addr}) #entra na lista na forma de dicionario
            if(len(connected_clients) == MAX_CLIENTS):  #caso de maximo de clients
                for i in range(len(connected_clients)):
                    client_dict = connected_clients[i]
                    #dedica uma thread ao client
                    t = threading.Thread(target=thread_client, args=(client_dict.get('conn'),client_dict.get('addr'),total_points//MAX_CLIENTS))
                    threads.append(t)
                    t.start()
                loop = False
                break
            elif(len(connected_clients) > MAX_CLIENTS):
                print("\nMaximo de clients")
                connected_clients.pop()
                conn.shutdown(2)
                conn.close()
                
    #a partir desse ponto, não aceitamos mais conexões
    
    #junta as threads          
    for t in threads:
        t.join()
        
    #resultado final
    num_inside = sum(partial_results)
    pi_result = 4 * num_inside / total_points

    time_end = int(round(time.time() * 1000))

    print(f"\nResultado final: {pi_result} obtido em {time_end-time_start}ms")
                
if __name__=="__main__":
    main()

#!funcionamento
#escolhe host e porta
#começa a escutar esperando por clients
#entra no loop
#aceita conexões quando um client tenta conectar
#coloca info de conexão na lista de clients
#ao chegar no maximo de clients
    #dedica uma thread pra cada client, colocando cada thread no array
    #caso mais um client tente conectar a conexão é recusada
#na thread
    #recebe uma mensagem do client
    #envia slice do problema para o client
    #recebe a resposta
    #da append no array de soluções parciais
    #finaliza a thread
#junta as thread
#gera o resultado final