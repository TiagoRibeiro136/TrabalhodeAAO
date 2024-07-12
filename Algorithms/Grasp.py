import time  # Importa a biblioteca time para medir o tempo de execução
import random  # Importa a biblioteca random para gerar números aleatórios

def read_data(filename):
    print(f"Lendo dados do arquivo: {filename}")  # Exibe uma mensagem indicando a leitura do arquivo
    with open(filename, 'r') as file:
        lines = file.readlines()  # Lê todas as linhas do arquivo

    # Extrair o número de armazéns (m) e clientes (n)
    m, n = map(int, lines[0].split())
    data = {'warehouses': [], 'customers': []}  # Inicializa o dicionário para armazenar os dados

    # Leitura dos armazéns
    for i in range(1, m + 1):
        parts = lines[i].split()  # Divide a linha em partes
        fixed_cost = float(parts[1])  # Extrai o custo fixo do armazém
        data['warehouses'].append({'fixed_cost': fixed_cost, 'opened': False})  # Adiciona o armazém à lista

    line_index = m + 1  # Define o índice da linha atual
    while line_index < len(lines):
        # Leitura do número do cliente (ignorada, pois não é necessária)
        customer_number = int(lines[line_index].strip())  # Extrai o número do cliente
        line_index += 1  # Avança para a próxima linha

        # Leitura dos custos de alocação do cliente para cada armazém
        costs = []  # Inicializa a lista de custos
        while line_index < len(lines) and not lines[line_index].strip().isdigit():
            costs.extend(map(float, lines[line_index].strip().split()))  # Adiciona os custos à lista
            line_index += 1  # Avança para a próxima linha

        # Adicionar o cliente à lista com os custos combinados
        data['customers'].append({'costs': costs})  # Adiciona o cliente com seus custos

    print("Leitura dos dados concluída.")  # Exibe uma mensagem indicando que a leitura dos dados foi concluída
    return data  # Retorna os dados lidos

def calculate_total_cost(solution, warehouses, customers):
    total_cost = 0  # Inicializa o custo total
    warehouse_used = [False] * len(warehouses)  # Lista para rastrear se o armazém foi usado
    
    for customer_idx, warehouse_idx in enumerate(solution):
        warehouse = warehouses[warehouse_idx]
        customer = customers[customer_idx]
        
        # Adiciona o custo fixo do armazém se for a primeira vez que o armazém é usado
        if not warehouse_used[warehouse_idx]:
            total_cost += warehouse['fixed_cost']
            warehouse_used[warehouse_idx] = True
        
        # Adiciona o custo variável do cliente para o armazém atual
        total_cost += customer['costs'][warehouse_idx]
    
    return total_cost  # Retorna o custo total

def greedy_randomized_construction(data, seed):
    random.seed(seed)  # Define a seed para gerar números aleatórios
    warehouses = data['warehouses']
    customers = data['customers']
    solution = [-1] * len(customers)  # Inicializa a solução com -1 para cada cliente
    
    for customer_idx, customer in enumerate(customers):
        candidates = []  # Inicializa a lista de candidatos
        
        for warehouse_idx, warehouse in enumerate(warehouses):
            cost = warehouse['fixed_cost'] if not warehouse['opened'] else 0
            cost += customer['costs'][warehouse_idx]
            candidates.append((cost, warehouse_idx))  # Adiciona o custo e o índice do armazém à lista de candidatos
        
        candidates.sort()  # Ordena os candidatos pelo custo
        
        alpha = 0.1  # Parâmetro de aleatoriedade
        rcl_size = max(1, int(alpha * len(candidates)))  # Define o tamanho da lista restrita de candidatos (RCL)
        selected = random.choice(candidates[:rcl_size])  # Seleciona aleatoriamente um candidato da RCL
        
        selected_warehouse = selected[1]
        solution[customer_idx] = selected_warehouse  # Atualiza a solução com o armazém selecionado
        
        if not warehouses[selected_warehouse]['opened']:
            warehouses[selected_warehouse]['opened'] = True  # Marca o armazém como aberto
    
    return solution  # Retorna a solução

def local_search(initial_solution, warehouses, customers):
    current_solution = initial_solution[:]  # Copia a solução inicial
    best_solution = current_solution[:]  # Define a melhor solução como a solução inicial
    best_cost = calculate_total_cost(best_solution, warehouses, customers)  # Calcula o custo da melhor solução
    print(f"Inicializando busca local. Custo inicial: {best_cost:.5f}")  # Exibe o custo inicial
    
    iteration = 0  # Inicializa o contador de iterações
    while True:
        found_better = False  # Inicializa a variável para procurar se uma melhor solução foi encontrada
        for customer_idx in range(len(customers)):
            current_warehouse_idx = current_solution[customer_idx]
            
            for new_warehouse_idx in range(len(warehouses)):
                if new_warehouse_idx != current_warehouse_idx:
                    new_solution = current_solution[:]  # Copia a solução atual
                    new_solution[customer_idx] = new_warehouse_idx  # Altera a alocação do cliente para o novo armazém
                    
                    new_cost = calculate_total_cost(new_solution, warehouses, customers)  # Calcula o custo da nova solução
                    
                    if new_cost < best_cost:
                        best_solution = new_solution[:]  # Atualiza a melhor solução
                        best_cost = new_cost  # Atualiza o melhor custo
                        found_better = True  # Marca que uma melhor solução foi encontrada
                        print(f"Iteração {iteration}: Encontrada melhor solução com custo {best_cost:.5f}")  # Exibe a nova melhor solução
        
        if not found_better:
            break  # Interrompe a busca se nenhuma melhor solução for encontrada
        else:
            current_solution = best_solution[:]  # Atualiza a solução atual com a melhor solução encontrada
        
        iteration += 1  # Incrementa o contador de iterações
    
    print("Busca local concluída.")  # Exibe uma mensagem indicando que a busca local foi concluída
    return best_solution, best_cost  # Retorna a melhor solução e seu custo

def grasp(filename, max_iterations, seed):
    data = read_data(filename)  # Lê os dados do arquivo
    best_solution = None  # Inicializa a melhor solução como None
    best_cost = float('inf')  # Inicializa o melhor custo como infinito
    
    for iteration in range(max_iterations):
        print(f"Iniciando iteração {iteration + 1} do GRASP")  # Exibe uma mensagem indicando o início da iteração
        warehouses_copy = [wh.copy() for wh in data['warehouses']]  # Cria uma cópia dos armazéns
        initial_solution = greedy_randomized_construction({'warehouses': warehouses_copy, 'customers': data['customers']}, seed)  # Gera uma solução inicial
        
        solution, cost = local_search(initial_solution, data['warehouses'], data['customers'])  # Realiza a busca local
        
        if cost < best_cost:
            best_solution = solution  # Atualiza a melhor solução
            best_cost = cost  # Atualiza o melhor custo
            print(f"Nova melhor solução encontrada na iteração {iteration + 1} com custo {best_cost:.5f}")  # Exibe a nova melhor solução
    
    return best_solution, best_cost  # Retorna a melhor solução e seu custo

def main(filename):
    max_iterations = 1  # Define o número máximo de iterações do GRASP
    seed = 42  # Define a semente para geração de números aleatórios
    
    best_solution, best_cost = grasp(filename, max_iterations, seed)  # Executa o GRASP
    
    # Exibe o resultado do GRASP
    print(f"Solução: {' '.join(map(str, best_solution))}")  # Exibe a melhor solução
    print(f"Custo: {best_cost:.5f}")  # Exibe o melhor custo

    # Salva a solução encontrada pelo GRASP no arquivo initial_solution.txt
    # with open('capABC/initial_solution.txt', 'w') as file:
    #     file.write(' '.join(map(str, best_solution)))

if __name__ == "__main__":
    filename = "FicheirosTeste/M/Kcapmo1.txt"  # Nome do arquivo de entrada
    main(filename)  # Executa a função principal
