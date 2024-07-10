import time
start_time = time.time()
def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extrair o número de armazéns e clientes
    m, n = map(int, lines[0].split())
    data = {'warehouses': [], 'customers': []}

    # Leitura dos armazéns
    for i in range(1, m + 1):
        parts = lines[i].split()
        capacity = float(parts[0])  # Capacidade (não necessária)
        fixed_cost = float(parts[1])  # Custo fixo
        data['warehouses'].append({'capacity': capacity, 'fixed_cost': fixed_cost, 'allocated': 0, 'opened': False})

    line_index = m + 1
    while line_index < len(lines):
        # Leitura da demanda do cliente (ignorada, pois não é necessária)
        customer_number = int(lines[line_index].strip())
        line_index += 1

        # Leitura dos custos de alocação do cliente para cada armazém
        costs = []
        while line_index < len(lines) and not lines[line_index].strip().isdigit():
            costs.extend(map(float, lines[line_index].strip().split()))
            line_index += 1

        # Adicionar o cliente à lista com os custos combinados
        data['customers'].append({'demand': 0, 'costs': costs})

    return data

def greedy_algorithm(data):
    warehouses = data['warehouses']
    customers = data['customers']
    total_value = 0
    selected_items = []
    # Itera sobre cada cliente
    for customer in customers:
        min_cost = float('inf')
        min_warehouse_idx = -1

        for i, warehouse in enumerate(warehouses):
            if i < len(customer['costs']):  # Verifica se o índice do armazém está dentro dos limites da lista de custos do cliente
                if warehouse['capacity'] >= customer['demand']: # Verifica a capacidade do armazem 
                    if not warehouse['opened']:# Se o armazém não estiver aberto, inclui o custo fixo
                        cost = warehouse['fixed_cost'] + customer['costs'][i]
                    else:# Se o armazém já estiver aberto, apenas inclui o custo variável
                        cost = customer['costs'][i]
                    
                    if cost < min_cost:# Atualiza o custo mínimo
                        min_cost = cost
                        min_warehouse_idx = i

        if min_warehouse_idx != -1:# Se foi encontrado um armazém válido
            total_value += min_cost
            
            selected_warehouse = min_warehouse_idx
            selected_items.append((selected_warehouse, warehouses[selected_warehouse]))
            
            # Atualiza o armazém selecionado
            warehouses[selected_warehouse]['allocated'] += customer['demand']
            
            # Marca o armazém como aberto após o primeiro cliente
            warehouses[selected_warehouse]['opened'] = True

    end_time = time.time()
    execution_time = end_time - start_time
    
    return total_value, selected_items, execution_time

def format_output(total_value, selected_items):
    output = ""
    output += " ".join(str(item[0]) for item in selected_items) + " "
    output += f"{total_value:.5f}"
    return output

def save_solution_to_file(solution, filename='cap70_130/initial_solution.txt'):
    with open(filename, 'w') as file:
        file.write(' '.join(map(str, solution)))

def main(filename):
    data = read_data(filename)
    
    # Executa o algoritmo guloso
    total_value, selected_items, execution_time = greedy_algorithm(data)
    
    # Formata a saída
    output = format_output(total_value, selected_items)
    print(output)
    print(f"Tempo de execução: {execution_time:.5f} segundos")
    
    # Salva a solução encontrada pelo algoritmo guloso no arquivo initial_solution.txt
    solution_indices = [item[0] for item in selected_items]
    save_solution_to_file(solution_indices)

if __name__ == "__main__":
    filename = "FicheirosTeste/ORLIB/cap71.txt"
    main(filename)
