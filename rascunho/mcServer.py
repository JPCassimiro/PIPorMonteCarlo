import socket
import threading
import time

#!!TODO LIST
#criar conexão client server ✓
#garantir que o server não explode se o client desconectar ✓
#iniciar uma operação de teste, um "hello world" no client ✓
#permitir a conexão de multiplos clients ✓
#criar uma forma de identificar quantos clientes estão conectados ao servidor ✓

#fazer uma fila de conexões, espera os 4 clients entrarem antes de começar as threads ✓
    #problemas com a fila:
        #fazer operações sobre ela parece mais simples, coisas como len, pop e append deixa mais simples de lidar com clients
        #mas nas threads(fator inevitavel do código) causa não só condição de corrida(facilmente resolvivel) mas causa problemas com o index da fila
            #condição de corrida resolve facil com lock, muitas vezes nem é necessario no python pq threads não podem rodar ao mesmo tempo(GIL)
            #dar pop na fila causa os index mudarem, fazendo com que não de pra dar pop por index
            #se for pra dar pop sem index pode ocorrer de tirar outro client que não tem nada a ver da lista sem necessidade
            # possivel solução
                #simplesmente iniciar logo que 4 clients se conectem, sem fazer esquema de pop na thread
                #com essa aproximação, a maior parte do codigo se mantem 
                #possivel problema é que não exite uma verificação pra ver se o client desconectou durante o processo da thread
                #também não fica possivel manipular o array na thread
                    #a forma de saber quantos clients estão conectados a cada momento passa a ser usar um contador externo
                    #só depois remover os clients do array
    #outras formas de resolver:
        #trocar a fila pra um counter
            #perde a funcionalidade de esperar por todos
            #ainda pode funcionar, mas fica meio sem sentido pra medição de tempo
            #manter essa aproximação em mente para caso de merda
                
#traduzir o codigo da operação no for de java pra python ✓
#colocar o codigo como uma função no client ✓
#dividir a porcentagem do problema para cada client ✓
#executar ✓
#receber ✓
#juntar as partes ✓

#!!lidar com desconexão do client antes de cada um receber sua thread(se não der não deu)

#!!opcional
#usar select para deteção de desconexão antes do calculo
#encontrar uma forma de lidar com uma possivel desconexão durante o calculo

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
            conn.sendto(bytes(str(slice),'UTF-8'),addr)#envia slices para o client
            client_result = int(conn.recv(1024).decode())#recebe resultado do client
            print(f"\nResultado da operação feita pelo client {addr}: {client_result}")
            if(client_result > 0):#verificação só ta aqui pro break ficar dentro de um if e não "solto"
                with lock:#lock para evitar condição de corrida
                    partial_results.append(client_result)#coloca os resultados no array de resultados parciais
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
        s.bind((HOST,PORT))#vai atuar nesse host e nessa porta
        s.listen()#espera conexões
        loop = True
        while loop:
            print(f"\nEsperando conexão: ({HOST},{PORT})")
            conn, addr = s.accept()#aceita conexão
            connected_clients.append({'conn':conn,'addr':addr})#entra na lista na forma de dicionario
            if(len(connected_clients) == MAX_CLIENTS):#caso de maximo de clients
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