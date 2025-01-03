from src.population import Population
from datetime import datetime
import os

nbr_runs = 1
winner_strategy = []


newpath = r"./run_logs/"
if not os.path.exists(newpath):
    os.makedirs(newpath)
    print(f"Directory '{newpath}' created successfully.")
else:
    print(f"Directory '{newpath}' already exists.")

now = datetime.now()

def main():
    for i in range(nbr_runs):
        print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
        population = Population(num_groups=10, num_individuals=10)
        winner_strategy.append(population.run_simulation())
        print(f"Current Time: {now.strftime('%H:%M:%S')}\n")


if __name__ == '__main__':
    main()