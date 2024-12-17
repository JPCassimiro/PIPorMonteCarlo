import socket
import threading
import time

# Configurações do servidor
HOST = socket.gethostname()  # Obtém o nome do host local
PORT = 4500  # Porta para o servidor
MAX_CLIENTS = 4  # Número máximo de clientes que podem se conectar simultaneamente
TOTAL_POINTS = 4550000  # Total de pontos para calcular Pi

# Listas compartilhadas para armazenar os clientes conectados e os resultados parciais
connected_clients = []
partial_results = []

# Lock para evitar condição de corrida ao acessar dados compartilhados
lock = threading.Lock()

def thread_client(conn, addr, slice):
    """
    Função que roda em uma thread para cada cliente.
    Cada cliente calculará uma parte dos pontos e retornará seu resultado.
    """
    try:
        start_time = time.perf_counter()  # Marca o tempo de início da execução da thread
        data = conn.recv(1024).decode()  
        print(f"\n{data} de client: {addr}")  # Exibe a mensagem recebida do cliente
        conn.sendall(str(slice).encode('utf-8'))  # Envia a quantidade de pontos para o cliente

        # Recebe o resultado do cliente (número de pontos dentro do círculo)
        client_result = int(conn.recv(1024).decode())
        print(f"\nResultado da operação feita pelo client {addr}: {client_result}")

        # Protege o acesso à lista de resultados com o lock para evitar condições de corrida
        with lock:
            partial_results.append(client_result)  # Adiciona o resultado parcial à lista

        # Marca o tempo de término da thread e exibe o tempo de execução
        elapsed_time = time.perf_counter() - start_time
        print(f"\nThread do client {addr} terminou em: {elapsed_time:.2f}s")
    except Exception as e:
        print(f"\nErro na thread do client {addr}: {e}")  # Exibe erro, se ocorrer
    finally:
        conn.close()  # Fecha a conexão com o cliente

def main():
    """
    Função principal que configura o servidor, aceita conexões e distribui o trabalho.
    """
    threads = []  # Lista para armazenar as threads
    start_time = time.perf_counter()  # Marca o tempo de início do servidor

    # Criação do socket do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))  # Associa o servidor ao endereço e porta
        s.listen()  # Espera conexões
        print(f"\nEsperando conexões em ({HOST}, {PORT})")

        while len(connected_clients) < MAX_CLIENTS:
            # Aceita conexões dos clientes
            conn, addr = s.accept()
            connected_clients.append({'conn': conn, 'addr': addr})  # Armazena a conexão e o endereço
            print(f"\nCliente conectado: {addr}")

        # Para cada cliente conectado, cria uma thread para processar a tarefa
        for i, client_dict in enumerate(connected_clients):
            conn, addr = client_dict['conn'], client_dict['addr']
            # Divide o total de pontos igualmente entre os clientes
            thread = threading.Thread(target=thread_client, args=(conn, addr, TOTAL_POINTS // MAX_CLIENTS))
            thread.start()  # Inicia a thread
            threads.append(thread)  # Armazena a referência da thread

    # Aguarda o término de todas as threads
    for thread in threads:
        thread.join()  # Espera a execução de cada thread terminar

    # Calcula o valor final de Pi somando os resultados parciais
    num_inside = sum(partial_results)  # Soma os resultados parciais
    pi_result = 4 * num_inside / TOTAL_POINTS  # Cálculo de Pi com o método Monte Carlo

    # Marca o tempo total de execução e exibe o resultado
    elapsed_time = time.perf_counter() - start_time
    print(f"\nResultado final: {pi_result:.6f} obtido em {elapsed_time:.2f}s")

if __name__ == "__main__":
    main() 
