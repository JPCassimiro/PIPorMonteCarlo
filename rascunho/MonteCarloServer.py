import socket
from _thread import *

#!!COMO QUE FAZ?
#criar conexção client server ✓
#garantir que o server não explode se o client desconectar ✓
#iniciar uma operação de teste, um "hello world" no client ✓
#permitir a conexão de multiplos clients ✓
#criar uma forma de identificar quantos clientes estão conectados ao servidor
#traduzir o codigo da operação no for de java pra python
#aplicar o codigo traduzido no clientRpc
#dividir a porcentagem do problema para cada client
#executar
#receber
#juntar as partes

#usar select para deteção de desconexão antes do calculo

#encontrar uma forma de lidar com uma possivel desconexão durante o calculo


HOST = socket.gethostname()
PORT = 4500
MAX_CLIENTS = 4

current_clients = 0

def threadClient(conn, addr):
    print(f"Cliente conectado: {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendto(bytes("Who",'UTF-8'),addr)
    
def main():
    global current_clients
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            if(current_clients < MAX_CLIENTS):
                current_clients+=1
                start_new_thread(threadClient, (conn, addr))

if __name__=="__main__":
    main()