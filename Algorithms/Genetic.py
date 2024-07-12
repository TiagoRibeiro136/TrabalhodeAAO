import random  # Importa a biblioteca random para gerar números aleatórios
import time  # Importa a biblioteca time para medir o tempo de execução

def read_data(filename):
    # Abre o ficheiro e lê todas as linhas
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Lê a primeira linha para obter o número de armazéns (m) e clientes (n)
    m, n = map(int, lines[0].split())
    data = {'warehouses': [], 'customers': []}

    # Lê os dados dos armazéns (ignorando a capacidade)
    for i in range(1, m + 1):
        parts = lines[i].split()  # Divide a linha em partes
        fixed_cost = float(parts[1])  # Obtém o custo fixo do armazém
        data['warehouses'].append({'fixed_cost': fixed_cost, 'opened': False})  # Adiciona o armazém à lista

    line_index = m + 1  # Define o índice da linha atual
    while line_index < len(lines):
        # Avança uma linha, ignorando a demanda do cliente
        line_index += 1

        # Lê os custos de transporte dos clientes para os armazéns
        costs = []  # Inicializa a lista de custos
        while line_index < len(lines) and not lines[line_index].strip().isdigit():
            costs.extend(lines[line_index].strip().split())  # Adiciona os custos à lista
            line_index += 1  # Avança para a próxima linha

        # Adiciona os custos de transporte do cliente à lista de clientes
        data['customers'].append({'costs': [float(cost) for cost in costs]})

    return data  # Retorna os dados lidos

def fitness(solution, data):
    total_cost = 0  # Inicializa o custo total
    warehouse_usage = [False] * len(data['warehouses'])  # Inicializa a utilização dos armazéns

    for i, customer in enumerate(data['customers']):
        warehouse_idx = solution[i]  # Obtém o índice do armazém para o cliente
        if warehouse_idx >= len(data['warehouses']):
            return float('inf')  # Solução inválida
        warehouse = data['warehouses'][warehouse_idx]
        
        # Adiciona o custo fixo do armazém se ele ainda não foi aberto
        if not warehouse_usage[warehouse_idx]:
            total_cost += warehouse['fixed_cost']
            warehouse_usage[warehouse_idx] = True
        
        # Adiciona o custo de transporte do cliente para o armazém
        total_cost += customer['costs'][warehouse_idx]

    return total_cost  # Retorna o custo total

def initialize_population(data, pop_size):
    population = []  # Inicializa a população
    num_warehouses = len(data['warehouses'])  # Obtém o número de armazéns
    # Gera uma solução aleatória para cada cliente
    for _ in range(pop_size):
        solution = [random.randint(0, num_warehouses - 1) for _ in range(len(data['customers']))]  # Solução aleatória
        population.append(solution)  # Adiciona a solução à população
    
    return population  # Retorna a população

def select_parents(population, fitnesses, num_parents):
    total_fitness = sum(fitnesses)  # Calcula o custo total
    normalized_fitnesses = [f / total_fitness for f in fitnesses]  # Normaliza as fitnesses
    selected_indices = random.choices(range(len(population)), weights=normalized_fitnesses, k=num_parents)  # Seleciona os índices dos pais
    return [population[i] for i in selected_indices]  # Retorna os pais selecionados

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)  # Escolhe um ponto de corte aleatório
    child1 = parent1[:point] + parent2[point:]  # Gera o primeiro filho
    child2 = parent2[:point] + parent1[point:]  # Gera o segundo filho
    return child1, child2  # Retorna os filhos

def mutate(solution, mutation_rate, num_warehouses):
    for i in range(len(solution)):
        if random.random() < mutation_rate:  # Verifica se ocorre a mutação
            solution[i] = random.randint(0, num_warehouses - 1)  # Realiza a mutação

def replace_population(population, new_individuals, data):
    combined_population = population + new_individuals  # Combina a população antiga com os novos indivíduos
    combined_population.sort(key=lambda sol: fitness(sol, data))  # Ordena pela fitness
    return combined_population[:len(population)]  # Retorna a nova população

def genetic_algorithm(data, pop_size=100, generations=1000, mutation_rate=0.01):
    start_time = time.time()  # Marca o tempo de início
    
    # 1. Escolher uma população inicial aleatória de indivíduos
    population = initialize_population(data, pop_size)
    best_solution = None  # Inicializa a melhor solução
    best_fitness = float('inf')  # Inicializa a melhor fitness
    
    for generation in range(generations):
        # 2. Avaliar a fitness dos indivíduos
        fitnesses = [1 / (fitness(solution, data) + 1e-9) for solution in population]  # Calcula a fitness
        
        # 3. Repetir:
        # Selecionar os melhores indivíduos para serem usados pelos operadores genéticos
        parents = select_parents(population, fitnesses, pop_size // 2)
        
        next_population = []  # Inicializa a próxima população
        while len(next_population) < pop_size:
            parent1, parent2 = random.sample(parents, 2)  # Seleciona dois pais
            # Gerar novos indivíduos usando crossover e mutação
            child1, child2 = crossover(parent1, parent2)  # Realiza o crossover
            mutate(child1, mutation_rate, len(data['warehouses']))  # Realiza a mutação no primeiro filho
            mutate(child2, mutation_rate, len(data['warehouses']))  # Realiza a mutação no segundo filho
            next_population.append(child1)  # Adiciona o primeiro filho à próxima população
            if len(next_population) < pop_size:
                next_population.append(child2)  # Adiciona o segundo filho à próxima população

        # 4. Avaliar a fitness dos novos indivíduos
        new_fitnesses = [fitness(solution, data) for solution in next_population]  # Calcula a fitness dos novos indivíduos
        
        # Substituir os piores indivíduos da população pelos melhores novos indivíduos
        population = replace_population(population, next_population, data)

        # Atualizar a melhor solução encontrada
        for solution in population:
            current_fitness = fitness(solution, data)
            if current_fitness < best_fitness:
                best_fitness = current_fitness  # Atualiza a melhor fitness
                best_solution = solution  # Atualiza a melhor solução

        if generation % 100 == 0:
            print(f"Geração {generation}: Melhor Custo = {best_fitness:.5f}")  # Imprime a melhor fitness a cada 100 gerações

    end_time = time.time()  # Marca o tempo de fim
    execution_time = end_time - start_time  # Calcula o tempo de execução
    
    return best_solution, best_fitness, execution_time  # Retorna a melhor solução, fitness e tempo de execução

def format_output(best_solution, total_value):
    output = " ".join(map(str, best_solution)) + " "  # Formata a solução
    output += f"{total_value:.5f}"  # Adiciona a fitness formatada
    return output  # Retorna a string formatada

def main(filename):
    data = read_data(filename)  # Lê os dados do ficheiro
    
    best_solution, best_fitness, execution_time = genetic_algorithm(data)  # Executa o algoritmo genético
    
    print("\nMelhor solução encontrada pelo Algoritmo Genético:")
    print(f"Solução: {best_solution}")  # Imprime a melhor solução
    print(f"Custo: {best_fitness:.5f}")  # Imprime a melhor fitness
    print(f"Tempo de execução: {execution_time:.5f} segundos")  # Imprime o tempo de execução
    
    output = format_output(best_solution, best_fitness)  # Formata a saída
    print("\nFormato de saída:")
    print(output)  # Imprime a saída formatada

if __name__ == "__main__":
    filename = "FicheirosTeste/ORLIB/cap133.txt"  # Nome do ficheiro de entrada
    main(filename)  # Executa a função principal
