from src.population import Population
from datetime import datetime
import os
import json
import src.config as config


def check_config(file_path):
    """
    Reads a JSON configuration file and validates all its values.
    
    Parameters:
        file_path (str): The path to the JSON configuration file.
    
    Returns:
        None
    """
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        # Validate each value
        for key, value in config.items():
            print(f"{key}: {value}")
        print("\nBasic configuration loaded.")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def create_logs_folder():
    newpath = r"./run_logs/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print(f"Directory '{newpath}' created successfully.")
    else:
        print(f"Directory '{newpath}' already exists.")

def reset_config():
    basic_config = check_config('./src/config.json')
    config.kappa = basic_config["kappa"]
    config.q = basic_config["q"]
    config.n = basic_config["n"]
    config.m = basic_config["m"]
    config.b = basic_config["b"]
    config.c = basic_config["c"]
    config.z = basic_config["z"]
    config.alpha = basic_config["alpha"]
    config.lambda_mig = basic_config["lambda_mig"]
    config.w = basic_config["w"]
    config.N = basic_config["N"]

def main(nbr_runs,winner_strategy):
    
    now = datetime.now()
    for i in range(nbr_runs):
        print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
        population = Population(num_groups=10, num_individuals=10)
        winner_strategy.append(population.run_simulation())
        print(f"Current Time: {now.strftime('%H:%M:%S')}\n")


# All runs
def run_bc_simulation(nbr_runs):
    reset_config()
    now = datetime.now()
    winner_strategy = []
    
    #Config values
    bc_ratios = [1.5+i/2 for i in range(0,8,1)]
    for bc_ratio in bc_ratios:
        for i in range(nbr_runs):
            #Config modifaction
            config.c = config.b*bc_ratio
            
            #Run simulation
            print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
            population = Population(num_groups=10, num_individuals=10)
            winner_strategy.append(population.run_simulation())
            print(f"Current Time: {now.strftime('%H:%M:%S')}\n")

def run_lambda_mig_simulation(nbr_runs):
    reset_config()
    now = datetime.now()
    winner_strategy = []
    
    #Config values
    migration_values = [0+i/10 for i in range(0,110,10)]
    for migration in migration_values:
        for i in range(nbr_runs):
            #Config modifaction
            config.lambda_mig = migration
            
            #Run simulation
            print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
            population = Population(num_groups=10, num_individuals=10)
            winner_strategy.append(population.run_simulation())
            print(f"Current Time: {now.strftime('%H:%M:%S')}\n")

def run_n_simulation(nbr_runs):
    reset_config()
    now = datetime.now()
    winner_strategy = []
    
    #Config values
    group_size_values = [5+i for i in range(0,16)]
    for group_size in group_size_values:
        for i in range(nbr_runs):
            #Config modifaction
            config.n = group_size
            
            #Run simulation
            print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
            population = Population(num_groups=10, num_individuals=10)
            winner_strategy.append(population.run_simulation())
            print(f"Current Time: {now.strftime('%H:%M:%S')}\n")

def run_m_simulation(nbr_runs):
    reset_config()
    now = datetime.now()
    winner_strategy = []
    
    #Config values
    group_number_values = [5+i for i in range(0,16)]
    for group_number in group_number_values:
        for i in range(nbr_runs):
            #Config modifaction
            config.m = group_number
            
            #Run simulation
            print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
            population = Population(num_groups=10, num_individuals=10)
            winner_strategy.append(population.run_simulation())
            print(f"Current Time: {now.strftime('%H:%M:%S')}\n")

def run_alpha_simulation(nbr_runs):
    reset_config()
    now = datetime.now()
    winner_strategy = []
    
    #Config values
    alpha_values = [0+i/10 for i in range(0,110,10)]
    for alpha in alpha_values:
        for i in range(nbr_runs):
            #Config modifaction
            config.alpha = alpha
            
            #Run simulation
            print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
            population = Population(num_groups=10, num_individuals=10)
            winner_strategy.append(population.run_simulation())
            print(f"Current Time: {now.strftime('%H:%M:%S')}\n")

