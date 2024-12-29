import numpy as np
import random
import matplotlib.pyplot as plt

# Parameters
m = 10  # Number of groups
n = 10  # Individuals per group
w = 0.1  # Selection intensity
alpha = 0.8  # Probability of ingroup interaction
kappa = 0.025  # Frequency of group conflict
lambda_migration = 0.0  # Migration rate
q_split = 0.01  # Probability of group splitting
z_steepness = 0.5  # Steepness of contest function
b = 2.0  # Benefit of cooperation
c = 1.0  # Cost of cooperation

generations = 1000  # Total number of generations

# Strategy codes
EGOIST = 0
ALTRUIST = 1
PAROCHIALIST = 2

# Initialize population
def initialize_population():
    population = []
    for _ in range(m):
        group = [random.choice([EGOIST, ALTRUIST, PAROCHIALIST]) for _ in range(n)]
        population.append(group)
    return population

# Interaction payoff calculation
def calculate_payoff(individual, partner, interaction_type):
    if interaction_type == "ingroup":
        if individual == ALTRUIST or (individual == PAROCHIALIST and partner != EGOIST):
            return b - c
        else:
            return 0
    elif interaction_type == "outgroup":
        if individual == ALTRUIST:
            return -c
        return 0

# Fitness calculation
def calculate_fitness(population):
    fitness = [[(1 - w) for _ in group] for group in population]
    for i, group in enumerate(population):
        for j, individual in enumerate(group):
            payoff = 0
            for _ in range(n):
                interaction_type = "ingroup" if random.random() < alpha else "outgroup"
                if interaction_type == "ingroup":
                    partner = random.choice(group)
                else:
                    partner_group = random.choice([g for g in population if g != group])
                    partner = random.choice(partner_group)
                payoff += calculate_payoff(individual, partner, interaction_type)
            fitness[i][j] += w * payoff
    return fitness

# Reproduction with migration
def reproduction(population, fitness):
    new_population = []
    for i, group in enumerate(population):
        new_group = []
        for _ in range(n):
            selected = random.choices(group, weights=fitness[i])[0]
            if random.random() < lambda_migration:
                target_group = random.choice([g for g in population if g != group])
                target_group.append(selected)
            else:
                new_group.append(selected)
        new_population.append(new_group)
    return new_population

# Group conflict
def group_conflict(population, fitness):
    groups_in_conflict = random.sample(range(len(population)), int(kappa * len(population)))
    for i in range(0, len(groups_in_conflict), 2):
        if i + 1 >= len(groups_in_conflict):
            break
        group1 = groups_in_conflict[i]
        group2 = groups_in_conflict[i + 1]
        fitness_sum1 = sum(fitness[group1])
        fitness_sum2 = sum(fitness[group2])
        prob_group1_wins = fitness_sum1**z_steepness / (fitness_sum1**z_steepness + fitness_sum2**z_steepness)
        if random.random() < prob_group1_wins:
            population[group2] = population[group1]
        else:
            population[group1] = population[group2]
    return population

# Group splitting
def group_splitting(population):
    for i, group in enumerate(population):
        if len(group) > n:
            if random.random() < q_split:
                half = len(group) // 2
                population.append(group[:half])
                population[i] = group[half:] 
            # fumer le gars TODO
    return population[:m]  # Keep the population size constant

# Simulation with result tracking
def simulate():
    population = initialize_population()
    strategy_counts_over_time = []

    for gen in range(generations):
        fitness = calculate_fitness(population)
        population = reproduction(population, fitness)
        population = group_conflict(population, fitness)
        population = group_splitting(population)

        # Track strategy counts
        strategy_counts = {EGOIST: 0, ALTRUIST: 0, PAROCHIALIST: 0}
        for group in population:
            for individual in group:
                strategy_counts[individual] += 1
        strategy_counts_over_time.append(strategy_counts)

    return strategy_counts_over_time

# Plotting results
def plot_results(strategy_counts_over_time):
    egoists = [counts[EGOIST] for counts in strategy_counts_over_time]
    altruists = [counts[ALTRUIST] for counts in strategy_counts_over_time]
    parochialists = [counts[PAROCHIALIST] for counts in strategy_counts_over_time]

    generations = range(len(strategy_counts_over_time))

    plt.figure(figsize=(10, 6))
    plt.plot(generations, egoists, label="Egoists", linestyle='--')
    plt.plot(generations, altruists, label="Altruists", linestyle='-.')
    plt.plot(generations, parochialists, label="Parochialists", linestyle='-')

    plt.xlabel("Generations")
    plt.ylabel("Count of Individuals")
    plt.title("Strategy Dynamics Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

# Run simulation and plot results
strategy_counts_over_time = simulate()
plot_results(strategy_counts_over_time)
