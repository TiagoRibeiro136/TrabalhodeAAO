import random
import copy

def generate_random_initial_solution(num_customers, num_warehouses):
    initial_solution = [random.randint(0, num_warehouses - 1) for _ in range(num_customers)]
    return initial_solution

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    num_warehouses, num_customers = map(int, lines[0].strip().split())
    
    warehouse_costs = []
    warehouse_capacities = []
    for i in range(1, num_warehouses + 1):
        parts = list(map(float, lines[i].strip().split()))
        warehouse_costs.append(parts[0])
        warehouse_capacities.append(parts[1])
    
    customer_demands = []
    customer_costs = []
    current_line = num_warehouses + 1
    while current_line < len(lines):
        if lines[current_line].strip():
            try:
                customer_demands.append(float(lines[current_line].strip()))
                current_line += 1
                costs = []
                while current_line < len(lines) and not lines[current_line].strip().isdigit():
                    costs.extend(list(map(float, lines[current_line].strip().split())))
                    current_line += 1
                customer_costs.append(costs)
            except ValueError:
                current_line += 1
    
    warehouses = []
    for i in range(num_warehouses):
        warehouses.append({
            'cost': warehouse_costs[i],
            'capacity': warehouse_capacities[i],
            'allocated': 0
        })
    
    customers = []
    for i in range(num_customers):
        customers.append({
            'demand': customer_demands[i],
            'costs': customer_costs[i],
            'assigned_to': -1
        })
    
    return {'warehouses': warehouses, 'customers': customers}

def first_improvement_search(initial_solution, warehouses, customers, max_iterations=200):
    current_solution = initial_solution
    current_cost = calculate_total_cost(current_solution, warehouses, customers)
    best_solution = current_solution[:]
    best_cost = current_cost
    improvement_found = True
    
    iteration = 1
    no_improvement_count = 0
    max_no_improvement = 1000  # Define um limite para o número de iterações sem melhoria significativa
    
    while improvement_found and iteration <= max_iterations:
        improvement_found = False                                                             
        
        for customer_index in range(len(customers)):
            current_warehouse = current_solution[customer_index]
            
            for warehouse_index in range(len(warehouses)):
                if warehouse_index != current_warehouse:
                    new_solution = current_solution[:]
                    new_solution[customer_index] = warehouse_index
                    
                    if is_feasible(new_solution, warehouses, customers):
                        new_cost = calculate_total_cost(new_solution, warehouses, customers)
                        
                        if new_cost < best_cost:
                            current_solution = new_solution[:]
                            current_cost = new_cost
                            best_solution = new_solution[:]
                            best_cost = new_cost
                            improvement_found = True
                            no_improvement_count = 0  # Reinicia o contador de iterações sem melhoria
                            break  # Sai do loop interno para iniciar do primeiro cliente novamente
            
            if improvement_found:
                break  # Sai do loop externo para iniciar do primeiro cliente novamente
        
        print(f"Iteration {iteration}: Best cost = {best_cost}")
        iteration += 1
        no_improvement_count += 1
        
        if no_improvement_count >= max_no_improvement:
            break  # Sai do loop se não houver melhoria significativa por várias iterações
    
    return best_solution, best_cost

def calculate_total_cost(solution, warehouses, customers):
    total_cost = 0
    
    for warehouse in warehouses:
        warehouse['allocated'] = 0
    
    for customer_index, warehouse_index in enumerate(solution):
        customer = customers[customer_index]
        warehouse = warehouses[warehouse_index]
        total_cost += customer['costs'][warehouse_index]
        warehouse['allocated'] += customer['demand']
    
    for warehouse in warehouses:
        if warehouse['allocated'] > 0:
            total_cost += warehouse['cost']
    
    return total_cost

def is_feasible(solution, warehouses, customers):
    for warehouse in warehouses:
        warehouse['allocated'] = 0
    
    for customer_index, warehouse_index in enumerate(solution):
        customer = customers[customer_index]
        warehouse = warehouses[warehouse_index]
        
        if warehouse['allocated'] + customer['demand'] > warehouse['capacity']:
            return False
        warehouse['allocated'] += customer['demand']
    
    return True

def main(filename):
    data = read_data(filename)
    initial_solution = generate_random_initial_solution(len(data['customers']), len(data['warehouses']))
    
    print("Initial Solution:", initial_solution)
    
    best_solution, best_cost = first_improvement_search(initial_solution, data['warehouses'], data['customers'])
    
    print("\nFinal Results:")
    print("Best solution:", best_solution)
    print("Best cost:", best_cost)

if __name__ == "__main__":
    filename = "FicheirosTeste/ORLIB/cap133.txt"
    main(filename)