import time
import random

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
        data['warehouses'].append({'fixed_cost': fixed_cost, 'opened': False})

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

def greedy_randomized_construction(data, seed):
    random.seed(seed)
    warehouses = data['warehouses']
    customers = data['customers']
    solution = [-1] * len(customers)
    
    for customer_idx, customer in enumerate(customers):
        candidates = []
        
        for warehouse_idx, warehouse in enumerate(warehouses):
            cost = warehouse['fixed_cost'] if not warehouse['opened'] else 0
            cost += customer['costs'][warehouse_idx]
            candidates.append((cost, warehouse_idx))
        
        candidates.sort()
        
        alpha = 0.1  # Parâmetro de aleatoriedade
        rcl_size = max(1, int(alpha * len(candidates)))
        selected = random.choice(candidates[:rcl_size])
        
        selected_warehouse = selected[1]
        solution[customer_idx] = selected_warehouse
        
        if not warehouses[selected_warehouse]['opened']:
            warehouses[selected_warehouse]['opened'] = True
    
    return solution

def local_search(initial_solution, warehouses, customers):
    current_solution = initial_solution[:]
    best_solution = current_solution[:]
    best_cost = calculate_total_cost(best_solution, warehouses, customers)
    
    while True:
        found_better = False
        for customer_idx in range(len(customers)):
            current_warehouse_idx = current_solution[customer_idx]
            
            for new_warehouse_idx in range(len(warehouses)):
                if new_warehouse_idx != current_warehouse_idx:
                    new_solution = current_solution[:]
                    new_solution[customer_idx] = new_warehouse_idx
                    
                    new_cost = calculate_total_cost(new_solution, warehouses, customers)
                    
                    if new_cost < best_cost:
                        best_solution = new_solution[:]
                        best_cost = new_cost
                        found_better = True
        
        if not found_better:
            break
        else:
            current_solution = best_solution[:]
    
    return best_solution, best_cost

def grasp(filename, max_iterations, seed):
    data = read_data(filename)
    best_solution = None
    best_cost = float('inf')
    
    for _ in range(max_iterations):
        warehouses_copy = [wh.copy() for wh in data['warehouses']]  # Cria uma cópia dos armazéns
        initial_solution = greedy_randomized_construction({'warehouses': warehouses_copy, 'customers': data['customers']}, seed)
        
        solution, cost = local_search(initial_solution, data['warehouses'], data['customers'])
        
        if cost < best_cost:
            best_solution = solution
            best_cost = cost
    
    return best_solution, best_cost

def main(filename):
    max_iterations = 100
    seed = 42
    
    best_solution, best_cost = grasp(filename, max_iterations, seed)
    
    # Exibe o resultado do GRASP
    print(f"Solução: {' '.join(map(str, best_solution))}")
    print(f"Custo: {best_cost:.5f}")

    # Salva a solução encontrada pelo GRASP no arquivo initial_solution.txt
    # with open('capABC/initial_solution.txt', 'w') as file:
    #     file.write(' '.join(map(str, best_solution)))

if __name__ == "__main__":
    filename = "FicheirosTeste/ORLIB/cap72.txt"
    main(filename)
