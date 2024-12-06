import socket

HOST = socket.gethostname()
PORT = 4500


if __name__=="__main__":

    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conectado: {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(bytes("Who",'UTF-8'))