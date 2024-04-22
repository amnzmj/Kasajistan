import random

# distancia de ciudad a ciudad
ciudades = {
    'A': {'A': 0, 'B': 1, 'C': 3, 'D': 7, 'E': 1},
    'B': {'A': 1, 'B': 0, 'C': 1, 'D': 6, 'E': 4},
    'C': {'A': 3, 'B': 1, 'C': 0, 'D': 1, 'E': 2},
    'D': {'A': 7, 'B': 6, 'C': 1, 'D': 0, 'E': 1},
    'E': {'A': 1, 'B': 4, 'C': 2, 'D': 1, 'E': 0}
}
def fitness(route):
    total_distance = sum(ciudades[route[i]][route[i+1]] for i in range(len(route)-1))
    # Add distance from last city back to the starting city
    total_distance += ciudades[route[-1]][route[0]]
   
    return total_distance
# Generate random route 
def generate_random_route(ciudades):
    route = list(ciudades.keys())
    random.shuffle(route)
    return route
def crossover(parent1, parent2):
    # print("parent 1 t",parent1)
    crossover_point = random.randint(1, len(parent1) - 1) #Se resta 1 a la longitud de parent1 para asegurarse de que el punto de cruce no sea el último índice de la lista. 
    child1 = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [city for city in parent1 if city not in parent2[:crossover_point]]
    # print("parent 1",parent1)
    # print("parent 2",parent2)
    # print("child 1",child1)
    # print("child 2",child2)
    
    return child1, child2
# Mutation for TSP
def mutate(route, mutation_rate):
    if random.random() < mutation_rate:#probabilidad que mute
        idx1, idx2 = random.sample(range(len(route)), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]
    return route
# Roulette wheel selection for TSP
def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    #print(total_fitness)
    selection_probabilities = [fitness / total_fitness for fitness in fitness_values]
    #print(selection_probabilities)
    cumulative_probabilities = [sum(selection_probabilities[:i+1]) for i in range(len(selection_probabilities))]
    selected_parents = []
    for _ in range(2):
        random_value = random.random()
        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if random_value <= cumulative_probability:
                selected_parents.append(population[i])
                break
            print()
    return selected_parents
# Evolutionary algorithm for TSP
def evolutionary_algorithm(population_size, mutation_rate, max_generations):
    population = [generate_random_route(ciudades) for _ in range(population_size)]
    generation_number = 1
    #print(population)

    for generation in range(max_generations):
        fitness_values = [fitness(route) for route in population]
        #print(fitness_values)
        if min(fitness_values) == 0:  
            index = fitness_values.index(0)
            return population[index], generation_number

        selected_parents = roulette_wheel_selection(population, fitness_values)
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = selected_parents
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population
        generation_number += 1

    # If no perfect solution is found, return the best solution found so far
    index = fitness_values.index(min(fitness_values))
    #print(fitness_values)
    #print (fitness_values.index)
    #print(index)
    #print(population)
    
    return  generation_number, fitness_values, population, index
# Run the evolutionary algorithm
generation_number, fitness_values, population, index= evolutionary_algorithm(population_size=10, mutation_rate=0.1, max_generations=10)
print("poblacion", population)
print("fitness values",fitness_values)
print(index)
print("ruta mas corta:", population[index])
print("distancia:", fitness_values[index])
print("generaciones", generation_number)