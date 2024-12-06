import socket

if __name__=="__main__":
    HOST = socket.gethostname()
    PORT = 4500
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))#não iniciar recebendo mensagem do server 
        while True:
            s.sendall(bytes("\nHelloWorld",'UTF-8'))
            recieved = str(s.recv(1024).decode())
            print(recieved)
