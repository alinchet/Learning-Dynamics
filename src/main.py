from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import logging
import os

from src.classes.population import Population
from src.settings.constants import Strategy
import src.settings.config as config

# --- Logging Setup ---
logging.basicConfig(
    filename='logs/simulation.log',  # Log file name
    level=logging.INFO,             # Log level (you can adjust to DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp
)

def single_simulation(mutant_strategy):
    """
    Runs a single simulation and returns the result.
    Args:
        mutant_strategy (Strategy): Strategy for the mutant.

    Returns:
        bool: True if mutant strategy fixed, False otherwise.
    """
    try:
        population = Population(mutant_strategy)
        result = population.run_simulation()
        return result == mutant_strategy
    except Exception as e:
        logging.error(f"Simulation error: {e}")
        return False

def simulate_fixation_probabilities(runs=10, mutant_strategy=Strategy.ALTRUIST, max_workers=4):
    """
    Simulates fixation probabilities using multithreading.

    Args:
        runs (int): Number of simulations to run.
        mutant_strategy (Strategy): Strategy to test.
        max_workers (int): Maximum number of threads.

    Returns:
        float: Fixation probability (proportion of mutant's strategy outcomes).
    """
    counter = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all simulation tasks
        futures = [executor.submit(single_simulation, mutant_strategy) for _ in range(runs)]

        # Process results as they complete
        for i, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result()
                if result:
                    counter += 1
                print(f"Completed simulation {i}/{runs}, Result: {'MUTANT' if result else 'EGOIST'}")
            except Exception as e:
                logging.error(f"Error in simulation {i}: {e}")
                continue

    # Calculate fixation probability
    fixation_prob = counter / runs
    logging.info(f"Fixation probability for {mutant_strategy.name}: {fixation_prob}")
    return fixation_prob

# Figure 2: Fixation probability vs b/c
def fig2_fixation_vs_bc(runs=15, max_workers=4):
    os.makedirs('plots', exist_ok=True)

    bc_values = np.arange(1.5, 5.1, 0.5)
    altruist_results = []
    parochialist_results = []

    for bc in bc_values:
        # Update b/c ratio
        config.b, config.c = 1.0, 1 / bc

        # Simulate for altruist mutants
        mutant_strategy = Strategy.ALTRUIST
        print(f"\nSimulating for altruist mutants with b/c={bc:.2f}")
        altruist_fixation_prob = simulate_fixation_probabilities(runs, mutant_strategy=mutant_strategy, max_workers=max_workers)
        altruist_results.append(altruist_fixation_prob)

        # Simulate for parochialist mutants
        mutant_strategy = Strategy.PAROCHIALIST
        print(f"\nSimulating for parochialist mutants with b/c={bc:.2f}")
        parochialist_fixation_prob = simulate_fixation_probabilities(runs, mutant_strategy=mutant_strategy, max_workers=max_workers)
        parochialist_results.append(parochialist_fixation_prob)

    # Plot altruist fixation probabilities (green line)
    plt.plot(bc_values, altruist_results, 'g-', label='Altruists')

    # Plot parochialist fixation probabilities (red line)
    plt.plot(bc_values, parochialist_results, 'r-', label='Parochialists')

    # Add neutral mutant threshold (black dashed line)
    plt.axhline(y=0.01, color='black', label='Selection')

    # Add labels, title, legend, and grid
    plt.xlabel('b/c (Benefit-to-Cost Ratio)')
    plt.ylabel('Fixation Probability')
    plt.title('Fixation Probability vs b/c')
    plt.legend(loc='upper right')
    plt.grid(True)

    # Add timestamp to the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'plots/fig2_fixation_vs_bc_{timestamp}.png'
    plt.savefig(output_file)
    print(f"\nPlot saved to {output_file}")

# Run all simulations and save figures
def main():
    runs = 10  # Number of simulations per data point
    max_workers = 8  # Number of threads
    fig2_fixation_vs_bc(runs, max_workers)

if __name__ == "__main__":
    main()