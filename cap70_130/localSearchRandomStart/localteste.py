import time
import random

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    m, n = map(int, lines[0].split())
    data = {'warehouses': [], 'customers': []}

    # Leitura dos armazéns
    for i in range(1, m + 1):
        capacity, fixed_cost = lines[i].split()
        data['warehouses'].append({'capacity': float(capacity), 'fixed_cost': float(fixed_cost), 'allocated': 0, 'opened': False})

    line_index = m + 1
    while line_index < len(lines):
        # Leitura da demanda do cliente
        demand = lines[line_index].strip()
        line_index += 1

        # Leitura dos custos
        costs = []
        while line_index < len(lines) and not lines[line_index].strip().isdigit():
            costs.extend(lines[line_index].strip().split())
            line_index += 1

        # Adicionar o cliente à lista com a demanda e os custos combinados
        data['customers'].append({'demand': float(demand), 'costs': [float(cost) for cost in costs]})

    return data

def calculate_total_cost(solution, warehouses, customers):
    total_cost = 0
    warehouse_usage = [0] * len(warehouses)  # Lista para rastrear a capacidade usada por cada armazém
    
    for customer_idx, warehouse_idx in enumerate(solution):
        warehouse = warehouses[warehouse_idx]
        customer = customers[customer_idx]
        
        # Adiciona o custo fixo do armazém se for a primeira vez que o armazém é usado
        if warehouse_usage[warehouse_idx] == 0:
            total_cost += warehouse['fixed_cost']
        
        # Adiciona o custo variável do cliente para o armazém atual
        total_cost += customer['costs'][warehouse_idx]
        
        # Atualiza a capacidade usada pelo armazém com a demanda do cliente
        warehouse_usage[warehouse_idx] += customer['demand']
    
    return total_cost

def local_search(initial_solution, warehouses, customers):
    start_time = time.time()
    
    current_solution = initial_solution[:]
    best_solution = current_solution[:]
    best_cost = calculate_total_cost(best_solution, warehouses, customers)
    
    print(f"Initial Solution: {best_solution}")
    print(f"Initial Cost: {best_cost:.5f}")
    print("")

    while True:
        found_better = False
        for customer_idx in range(len(customers)):
            current_warehouse_idx = current_solution[customer_idx]
            
            for new_warehouse_idx in range(len(warehouses)):
                if new_warehouse_idx != current_warehouse_idx:
                    # Verificar se a mudança é viável
                    new_solution = current_solution[:]
                    new_solution[customer_idx] = new_warehouse_idx
                    
                    # Verificar se o novo armazém tem capacidade suficiente
                    warehouse = warehouses[new_warehouse_idx]
                    customer = customers[customer_idx]
                    
                    if warehouse['capacity'] >= customer['demand']:
                        new_cost = calculate_total_cost(new_solution, warehouses, customers)
                        
                        if new_cost < best_cost:
                            best_solution = new_solution[:]
                            best_cost = new_cost
                            found_better = True
                            print(f"Found better solution:")
                            print(f"  Solution: {best_solution}")
                            print(f"  Cost: {best_cost:.5f}")
                            print("")
        
        if not found_better:
            break
        else:
            current_solution = best_solution[:]
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return best_solution, best_cost, execution_time

def format_output(total_value, selected_items):
    output = ""
    output += " ".join(str(item[0]) for item in selected_items) + " "
    output += f"{total_value:.5f}"
    return output

def generate_random_solution(num_customers, num_warehouses):
    return [random.randint(0, num_warehouses - 1) for _ in range(num_customers)]

def main(filename):
    data = read_data(filename)
    num_customers = len(data['customers'])
    num_warehouses = len(data['warehouses'])
    
    # Gera uma solução inicial aleatória
    initial_solution = generate_random_solution(num_customers, num_warehouses)
    
    # Executa a pesquisa local usando a solução inicial aleatória
    best_solution, best_cost, execution_time = local_search(initial_solution, data['warehouses'], data['customers'])
    
    # Exibe o resultado da pesquisa local
    print("\nMelhor solução encontrada pela Pesquisa Local:")
    print(f"Solução: {best_solution}")
    print(f"Custo: {best_cost:.5f}")
    print(f"Tempo de execução: {execution_time:.5f} segundos")

if __name__ == "__main__":
    filename = "FicheirosTeste\ORLIB\cap134.txt"  # Nome do arquivo de entrada
    main(filename)
