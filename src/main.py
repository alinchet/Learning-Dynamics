from population import Population
from datetime import datetime

nbr_runs = 1
winner_strategy = []

now = datetime.now()

def main():
    for i in range(nbr_runs):
        print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
        population = Population(num_groups=10, num_individuals=10)
        winner_strategy.append(population.run_simulation())


if __name__ == '__main__':
    main()