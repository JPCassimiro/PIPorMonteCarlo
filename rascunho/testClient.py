import socket

if __name__=="__main__":
    HOST = socket.gethostname()
    PORT = 4500
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))#não começar iniciando mensagem para o servidor, melhor começar recebendo
        s.sendall(bytes("\nHelloWorld",'UTF-8'))
        recieved = str(s.recv(1024).decode())
        s.close()
        
        
print(recieved)
