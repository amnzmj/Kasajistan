import random

# distancia de ciudad a ciudad
ciudades = {
    'A': {'A':0,'B':1,'C':3,'D':7,'E':1,'F':0,'G':1,'H':1,'I':5,'J':2,'K':8,'L':3,'M':4,'N':7,'O':7},

    'B': {'A':1,'B':0,'C':1,'D':7,'E':1,'F':1,'G':1,'H':1,'I':1,'J':1,'K':1,'L':1,'M':1,'N':1,'O':1},

    'C': {'A':3,'B':1,'C':0,'D':3,'E':3,'F':3,'G':3,'H':3,'I':3,'J':3,'K':3,'L':3,'M':3,'N':3,'O':3},

    'D': {'A':7,'B':7,'C':3,'D':0,'E':7,'F':7,'G':7,'H':7,'I':7,'J':7,'K':7,'L':7,'M':7,'N':7,'O':7},

    'E': {'A':1,'B':1,'C':3,'D':7,'E':0,'F':1,'G':1,'H':1,'I':1,'J':1,'K':1,'L':1,'M':1,'N':1,'O':1},

    'F': {'A':0,'B':1,'C':3,'D':7,'E':1,'F':0,'G':5,'H':1,'I':5,'J':5,'K':8,'L':6,'M':9,'N':7,'O':6},

    'G': {'A':1,'B':1,'C':3,'D':7,'E':1,'F':5,'G':0,'H':1,'I':1,'J':1,'K':1,'L':1,'M':3,'N':1,'O':1},

    'H': {'A':1,'B':1,'C':3,'D':7,'E':1,'F':1,'G':1,'H':0,'I':3,'J':3,'K':3,'L':1,'M':3,'N':7,'O':3},

    'I': {'A':5,'B':1,'C':3,'D':7,'E':1,'F':5,'G':1,'H':3,'I':0,'J':7,'K':9,'L':7,'M':3,'N':7,'O':1},

    'J': {'A':2,'B':1,'C':3,'D':7,'E':1,'F':5,'G':1,'H':3,'I':7,'J':0,'K':1,'L':1,'M':1,'N':7,'O':7},

    'K': {'A':8,'B':1,'C':3,'D':7,'E':1,'F':8,'G':1,'H':3,'I':9,'J':1,'K':0,'L':9,'M':3,'N':9,'O':8},

    'L': {'A':3,'B':1,'C':3,'D':7,'E':1,'F':6,'G':1,'H':1,'I':7,'J':1,'K':9,'L':0,'M':4,'N':7,'O':1},

    'M': {'A':4,'B':1,'C':3,'D':7,'E':1,'F':9,'G':3,'H':3,'I':7,'J':1,'K':3,'L':4,'M':0,'N':3,'O':4},

    'N': {'A':7,'B':1,'C':3,'D':7,'E':1,'F':7,'G':1,'H':3,'I':7,'J':7,'K':9,'L':7,'M':3,'N':0,'O':9},

    'O': {'A':7,'B':1,'C':3,'D':7,'E':1,'F':6,'G':1,'H':3,'I':1,'J':7,'K':8,'L':1,'M':4,'N':9,'O':0},
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
generation_number, fitness_values, population, index= evolutionary_algorithm(population_size=10, mutation_rate=0.3, max_generations=100)
print("poblacion", population)
print("fitness values",fitness_values)
print(index)
print("ruta mas corta:", population[index])
print("distancia:", fitness_values[index])
print("generaciones", generation_number)