import time
import random

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract the number of warehouses and customers
    m, n = map(int, lines[0].split())
    data = {'warehouses': [], 'customers': []}

    # Read warehouses
    for i in range(1, m + 1):
        parts = lines[i].split()
        fixed_cost = float(parts[1])  # Fixed cost
        data['warehouses'].append({'fixed_cost': fixed_cost})

    line_index = m + 1
    while line_index < len(lines):
        # Read the customer number (ignored, not necessary)
        customer_number = int(lines[line_index].strip())
        line_index += 1

        # Read the allocation costs from the customer to each warehouse
        costs = []
        while line_index < len(lines) and not lines[line_index].strip().isdigit():
            costs.extend(map(float, lines[line_index].strip().split()))
            line_index += 1

        # Add the customer to the list with the combined costs
        data['customers'].append({'costs': costs})

    return data

def calculate_total_cost(solution, warehouses, customers):
    total_cost = 0
    warehouse_used = [False] * len(warehouses)  # Track if the warehouse has been used
    
    for customer_idx, warehouse_idx in enumerate(solution):
        warehouse = warehouses[warehouse_idx]
        customer = customers[customer_idx]
        
        # Add the fixed cost of the warehouse if it is the first time it is used
        if not warehouse_used[warehouse_idx]:
            total_cost += warehouse['fixed_cost']
            warehouse_used[warehouse_idx] = True
        
        # Add the variable cost of the customer to the current warehouse
        total_cost += customer['costs'][warehouse_idx]
    
    return total_cost

def local_search_first_improvement(initial_solution, warehouses, customers):
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
            
            # Try each warehouse different from the current one
            for new_warehouse_idx in range(len(warehouses)):
                if new_warehouse_idx != current_warehouse_idx:
                    new_solution = current_solution[:]
                    new_solution[customer_idx] = new_warehouse_idx
                    
                    new_cost = calculate_total_cost(new_solution, warehouses, customers)
                    
                    if new_cost < best_cost:
                        best_solution = new_solution[:]
                        best_cost = new_cost
                        found_better = True
                        print(f"Found better solution:")
                        print(f"  Solution: {best_solution}")
                        print(f"  Cost: {best_cost:.5f}")
                        print("")
                        break  # Found an improvement, stop looking for this customer
        
        if not found_better:
            break
        else:
            current_solution = best_solution[:]
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return best_solution, best_cost, execution_time

def generate_random_solution(num_customers, num_warehouses):
    return [random.randint(0, num_warehouses - 1) for _ in range(num_customers)]

def main(filename):
    data = read_data(filename)
    num_customers = len(data['customers'])
    num_warehouses = len(data['warehouses'])
    
    # Generate a random initial solution
    initial_solution = generate_random_solution(num_customers, num_warehouses)
    
    # Execute local search using the First-Improvement method
    best_solution, best_cost, execution_time = local_search_first_improvement(initial_solution, data['warehouses'], data['customers'])
    
    # Display the result of the local search
    print("\nBest solution found by Local Search (First Improvement):")
    print(f"Solution: {best_solution}")
    print(f"Cost: {best_cost:.5f}")
    print(f"Execution time: {execution_time:.5f} seconds")

if __name__ == "__main__":
    filename = "FicheirosTeste\M\Kcapmo1.txt"  # New input file name
    main(filename)
