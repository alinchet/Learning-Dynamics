
from src.constants.constants import Strategy
import src.config.config as config

from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
import json


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
        return config
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def reset_config():
    basic_config = check_config('src/config/config.json')

    print("Loaded Configuration:")
    for key, value in basic_config.items():
        print(f"  {key}: {value}")

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

def main(nbr_runs,winner_strategy):
    from src.classes.population import Population
    
    for i in range(nbr_runs):
        now = datetime.now()
        print(f"Current Time: {now.strftime('%H:%M:%S')} and Run : {i}")
        population = Population(num_groups=10, num_individuals=10)
        winner_strategy.append(population.run_simulation())
        print(f"Current Time: {now.strftime('%H:%M:%S')}\n")

def save_run_output(tested_feature,tested_feature_name,probabilities):
    with open("save.txt","a") as f:
        sentence = f"""Result:
            -{tested_feature_name} : {tested_feature}
            -probabilities : {probabilities}
        """
        f.write(sentence)

def save_graph(selected_feature,probabilities,x_label,y_label,color):
    sentence = f"""Here are the given input to the function save_graph:
        -selected_feature : {selected_feature}
        -probabilities : {probabilities}
        -x_label : {x_label}
        -y_label : {y_label}
    """
    print(sentence)

    plt.plot(selected_feature,probabilities,color)
    plt.title(f"{y_label} Vs {x_label}")
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Save the plot to a file
    plt.savefig(f"{y_label}_Vs_{x_label}.png")
    plt.close()

def save_graphs(selected_feature, probabilities, x_label, y_label,nbr_runs):
    """
    Plot the fixation probabilities for different strategies as separate lines.

    Parameters:
        selected_feature: List of x-axis values.
        probabilities: Dictionary mapping each x-axis value to a dictionary of strategies and their probabilities.
        x_label: Label for the x-axis.
        y_label: Label for the y-axis.
    """
    # Extract strategies
    strategies = list(next(iter(probabilities.values())).keys())
    
    # Create a plot for each strategy
    for strategy in strategies:
        # Extract the probabilities for this strategy
        strategy_probabilities = [probabilities[feature].get(strategy, 0) for feature in selected_feature]
        
        # Plot the line for this strategy
        plt.plot(selected_feature, strategy_probabilities, label=strategy)
    
    # Add plot title and axis labels
    plt.title(f"{y_label} Vs {x_label} on {nbr_runs} runs")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    # Add a legend
    plt.legend()
    
    # Save the plot to a file
    plt.savefig(f"{y_label}_Vs_{x_label}.png")
    plt.close()
# All runs

def run_simulation(nbr_runs, parameter_name, parameter_values, config_modifier):
    from src.classes.population import Population
    reset_config()
    # Store probabilities for each parameter value
    probabilities = {}

    for value in parameter_values:
        print(f"Running simulations for {parameter_name}: {value}")
        winner_strategy = []

        for i in range(nbr_runs):
            # Modify configuration using the provided modifier function
            config_modifier(value)
            

            # Run simulation
            now = datetime.now()
            print(f"Current Time: {now.strftime('%H:%M:%S')} and Run: {i}")
            population = Population(num_groups=10, num_individuals=10)
            winner_strategy.append(population.run_simulation())

        # Calculate probabilities of each strategy
        total_runs = len(winner_strategy)
        strategy_counts = Counter(winner_strategy)
        probabilities[value] = {
            strategy.name: strategy_counts.get(strategy, 0) / total_runs
            for strategy in Strategy
        }

        print(f"Probabilities for {parameter_name} {value}: {probabilities[value]}\n")

    return parameter_values, probabilities

def run_bc_simulation(nbr_runs):
    bc_ratios = [1.5 + i / 2 for i in range(0, 8, 1)]
    
    
    return run_simulation(
        nbr_runs,
        "bc_ratio",
        bc_ratios,
        lambda bc_ratio: setattr(config, "c", config.b * bc_ratio)
    ),"bc_ratio","Fixation Probability"

def run_lambda_simulation(nbr_runs):
    migration_values = [0 + i / 10 for i in range(0, 110, 10)]
    return run_simulation(
        nbr_runs,
        "lambda_mig",
        migration_values,
        lambda migration: setattr(config, "lambda_mig", migration)
    ),"lambda_mig","Fixation Probability"

def run_n_simulation(nbr_runs):
    group_size_values = [5 + i for i in range(0, 16)]
    return run_simulation(
        nbr_runs,
        "group_size",
        group_size_values,
        lambda group_size: setattr(config, "n", group_size)
    ),"group_size","Fixation Probability"

def run_m_simulation(nbr_runs):
    group_number_values = [5 + i for i in range(0, 16)]
    return run_simulation(
        nbr_runs,
        "group_number",
        group_number_values,
        lambda group_number: setattr(config, "m", group_number)
    ),"group_number","Fixation Probability"

def run_alpha_simulation(nbr_runs):
    alpha_values = [0 + i / 100 for i in range(0, 110, 10)]
    return run_simulation(
        nbr_runs,
        "alpha",
        alpha_values,
        lambda alpha: setattr(config, "alpha", alpha)
    ),"alpha","Fixation Probability"
