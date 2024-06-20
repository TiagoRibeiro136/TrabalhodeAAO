import random
import time

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

def fitness(solution, data):
    total_cost = 0
    warehouse_usage = [0] * len(data['warehouses'])

    for i, customer in enumerate(data['customers']):
        warehouse_idx = solution[i]
        if warehouse_idx >= len(data['warehouses']):
            return float('inf')  # Invalid solution
        warehouse = data['warehouses'][warehouse_idx]
        
        # Verifica se o armazém já está aberto para este cliente
        if not warehouse['opened']:
            total_cost += warehouse['fixed_cost']
            warehouse['opened'] = True
        
        # Verifica se o armazém tem capacidade suficiente para atender o cliente
        if warehouse_usage[warehouse_idx] + customer['demand'] > warehouse['capacity']:
            return float('inf')  # Invalid solution
        
        total_cost += customer['costs'][warehouse_idx]
        warehouse_usage[warehouse_idx] += customer['demand']

    return total_cost

def initialize_population(data, pop_size):
    population = []
    num_warehouses = len(data['warehouses'])
    # Gera uma solução aleatória para cada cliente
    for _ in range(pop_size):
        solution = [random.randint(0, num_warehouses - 1) for _ in range(len(data['customers']))]
        population.append(solution)
    
    return population

def select_parents(population, fitnesses, num_parents):
    selected_indices = random.choices(range(len(population)), weights=fitnesses, k=num_parents)
    return [population[i] for i in selected_indices]
# Função de crossover
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2
# Função de mutação para introduzir variação
def mutate(solution, mutation_rate, num_warehouses):
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            solution[i] = random.randint(0, num_warehouses - 1)

def genetic_algorithm(data, pop_size=100, generations=2000, mutation_rate=0.01):
    start_time = time.time()
    
    population = initialize_population(data, pop_size)
    best_solution = None
    best_fitness = float('inf')
    # Calcula a fitness de cada solução na população
    for generation in range(generations):
        fitnesses = [1 / (fitness(solution, data) + 1e-9) for solution in population]
        # Seleciona os pais
        parents = select_parents(population, fitnesses, pop_size // 2)

        next_population = []
        while len(next_population) < pop_size:
            parent1, parent2 = random.sample(parents, 2)
            # Aplica crossover
            child1, child2 = crossover(parent1, parent2)
            # Aplica mutação aos filhos
            mutate(child1, mutation_rate, len(data['warehouses']))
            mutate(child2, mutation_rate, len(data['warehouses']))
            next_population.append(child1)
            if len(next_population) < pop_size:
                next_population.append(child2)

        population = next_population
        # Atualiza a melhor solução encontrada
        for solution in population:
            current_fitness = fitness(solution, data)
            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_solution = solution

    end_time = time.time()
    execution_time = end_time - start_time
    return best_solution, best_fitness, execution_time

def format_output(best_solution, total_value):
    output = " ".join(map(str, best_solution)) + " "
    output += f"{total_value:.5f}"
    return output

def main(filename):
    data = read_data(filename)
    
    best_solution, best_fitness, execution_time = genetic_algorithm(data)
    
    print("\nMelhor solução encontrada pelo Algoritmo Genético:")
    print(f"Solução: {best_solution}")
    print(f"Custo: {best_fitness:.5f}")
    print(f"Tempo de execução: {execution_time:.5f} segundos")
    
    output = format_output(best_solution, best_fitness)
    print("\nFormato de saída:")
    print(output)

if __name__ == "__main__":
    filename = "FicheirosTeste/ORLIB/cap71.txt"
    main(filename)
