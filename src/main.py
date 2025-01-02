from src.population import Population

def main():
    population = Population(num_groups=10, num_individuals=10)
    population.run_simulation()

if __name__ == '__main__':
    main()