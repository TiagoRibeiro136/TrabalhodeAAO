import time
import random
from collections import deque

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extrair o número de armazéns e clientes
    m, n = map(int, lines[0].split())
    data = {'warehouses': [], 'customers': []}

    # Leitura dos armazéns
    for i in range(1, m + 1):
        parts = lines[i].split()
        fixed_cost = float(parts[1])  # Custo fixo
        data['warehouses'].append({'fixed_cost': fixed_cost})

    line_index = m + 1
    while line_index < len(lines):
        # Leitura do número do cliente (ignorada, pois não é necessária)
        customer_number = int(lines[line_index].strip())
        line_index += 1

        # Leitura dos custos de alocação do cliente para cada armazém
        costs = []
        while line_index < len(lines) and not lines[line_index].strip().isdigit():
            costs.extend(map(float, lines[line_index].strip().split()))
            line_index += 1

        # Adicionar o cliente à lista com os custos combinados
        data['customers'].append({'costs': costs})

    return data

def calculate_total_cost(solution, warehouses, customers):
    total_cost = 0
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
    
    return total_cost

def tabu_search(initial_solution, warehouses, customers, max_iterations, tabu_tenure, max_no_improvement_iterations):
    start_time = time.time()
    
    # Inicializar a solução corrente (current_solution) e a melhor solução encontrada (best_solution).
    current_solution = initial_solution[:]
    best_solution = current_solution[:]
    best_cost = calculate_total_cost(best_solution, warehouses, customers)
    
    # Lista tabu para armazenar soluções recentes
    tabu_list = deque(maxlen=tabu_tenure)
    tabu_list.append(tuple(current_solution))
    iteration = 0
    no_improvement_iterations = 0

    print(f"Initial Solution: {best_solution}")
    print(f"Initial Cost: {best_cost:.5f}")
    print("")
    
    # Inicializar o contador de iterações (iteration = 0).
    while iteration < max_iterations and no_improvement_iterations < max_no_improvement_iterations:
        neighborhood = []
        
        # Gerar vizinhança N(current_solution)
        for customer_idx in range(len(customers)):
            current_warehouse_idx = current_solution[customer_idx]
            for new_warehouse_idx in range(len(warehouses)):
                if new_warehouse_idx != current_warehouse_idx:
                    new_solution = current_solution[:]
                    new_solution[customer_idx] = new_warehouse_idx
                    neighborhood.append((new_solution, calculate_total_cost(new_solution, warehouses, customers)))
        
        # Se N(current_solution) - S(tabu_list) != ∅ (indica que o algoritmo deve prosseguir apenas se houver pelo menos uma solução na vizinhança que não esteja na lista tabu)
        neighborhood = sorted(neighborhood, key=lambda x: x[1])
        found_better = False
        
        for new_solution, new_cost in neighborhood:
            if tuple(new_solution) not in tabu_list:
                # Incrementar a iteração e selecionar a melhor solução (best_solution) em N(current_solution) - S(tabu_list)
                current_solution = new_solution[:]
                tabu_list.append(tuple(current_solution))
                
                # Se f(new_solution) < f(current_solution), então best_solution = new_solution.
                if new_cost < best_cost:
                    best_solution = current_solution[:]
                    best_cost = new_cost
                    found_better = True
                    no_improvement_iterations = 0
                    print(f"Iteration {iteration + 1}: Found better solution:")
                    print(f"  Solution: {best_solution}")
                    print(f"  Cost: {best_cost:.5f}")
                    print("")
                else:
                    # Senão, N(current_solution) = N(current_solution) - new_solution
                    neighborhood = [neighbor for neighbor in neighborhood if tuple(neighbor[0]) != tuple(new_solution)]
                break
        
        if not found_better:
            no_improvement_iterations += 1
        
        iteration += 1
        # Atualizar a lista tabu (S(tabu_list))
        # A atualização da lista tabu ocorre durante a adição de novos elementos e remove automaticamente quando o limite é excedido
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return best_solution, best_cost, execution_time

def generate_random_solution(num_customers, num_warehouses):
    return [random.randint(0, num_warehouses - 1) for _ in range(num_customers)]

def main(filename):
    data = read_data(filename)
    num_customers = len(data['customers'])
    num_warehouses = len(data['warehouses'])
    
    # Gera uma solução inicial aleatória
    initial_solution = generate_random_solution(num_customers, num_warehouses)
    
    # Executa a Tabu Search
    max_iterations = 100  # Define o número máximo de iterações
    tabu_tenure = 10  # Define a duração da lista tabu
    max_no_improvement_iterations = 200  # Define o número máximo de iterações consecutivas sem melhoria
    best_solution, best_cost, execution_time = tabu_search(initial_solution, data['warehouses'], data['customers'], max_iterations, tabu_tenure, max_no_improvement_iterations)
    
    # Exibe o resultado da Tabu Search
    print("\nMelhor solução encontrada pela Busca Tabu:")
    print(f"Solução: {best_solution}")
    print(f"Custo: {best_cost:.5f}")
    print(f"Tempo de execução: {execution_time:.5f} segundos")

if __name__ == "__main__":
    filename = "FicheirosTeste/ORLIB/cap133.txt"  # Nome do arquivo de entrada
    main(filename)
