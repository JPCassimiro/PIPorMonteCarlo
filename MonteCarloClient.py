import socket  
import random  
import time  

# Função que calcula uma estimativa de pi usando o método Monte Carlo
def estimate_pi(total_points):
    hits = 0  # Inicializa a variável para contar os pontos dentro do círculo
    for _ in range(total_points):  # Itera sobre o número total de pontos
        x = random.uniform(-1, 1)  # Gera um valor aleatório para a coordenada x
        y = random.uniform(-1, 1)  # Gera um valor aleatório para a coordenada y
        # Verifica se o ponto está dentro do círculo de raio 1
        if x**2 + y**2 <= 1:
            hits += 1  # Conta o ponto como um "acerto" se estiver dentro do círculo
    return hits  # Retorna o número de acertos (pontos dentro do círculo)

# Bloco principal do código
if __name__ == "__main__":  
    # Obtém o nome do host
    HOST = socket.gethostname()
    PORT = 4500 

    try:
        # Cria o socket e tenta estabelecer a conexão com o servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))  
            print("Conectado ao servidor.")

            s.sendall(b"Hello World")  # Envia uma mensagem inicial para o servidor

            # Recebe a quantidade de pontos que o servidor deseja calcular
            received_slice = int(s.recv(1024).decode())  # Decodifica os dados recebidos e converte para inteiro
            if received_slice > 0:
                print(f"Recebido para cálculo: {received_slice} pontos.")

                # Mede o tempo de execução do cálculo de pi
                start_time = time.perf_counter() 
                result = estimate_pi(received_slice) 
                end_time = time.perf_counter() 

                # Calcula o tempo gasto para o cálculo
                elapsed_time = (end_time - start_time) * 1000 
                s.sendall(str(result).encode('utf-8'))  # Envia o resultado do cálculo de volta ao servidor
                print(f"Processo concluído em {elapsed_time:.2f}ms.")

            else:  # Caso o número de pontos seja zero ou menor
                print("Nenhum ponto para calcular.")

    except Exception as e:  # Captura todos os erros
        print(f"Erro inesperado: {e}")
