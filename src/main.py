import os
import matplotlib.pyplot as plt
import numpy as np

from src.classes.population import Population
from src.settings.constants import Strategy
import src.settings.config as config

def simulate_fixation_probabilities(runs=10, mutant_strategy=Strategy.ALTRUIST):
    """
    Simulates fixation probabilities based on multiple runs.

    Args:
        runs (int): Number of simulations to run.

    Returns:
        float: Fixation probability (proportion of mutant's strategy outcomes).
    """
    counter = 0
    for i in range(runs):
        try:
            print(f"Run {i+1}/{runs}: Simulating for {mutant_strategy.name}")
            population = Population(mutant_strategy)
            result = population.run_simulation()
            if result == mutant_strategy:
                counter += 1
            print(f"Result for run {i+1}: {result}")
        except Exception as e:
            print(f"Error during simulation run {i+1}: {e}")
            continue

    # Calculate fixation probability
    fixation_prob = counter / runs
    print(f"Fixation probability for {mutant_strategy.name}: {fixation_prob}")
    return fixation_prob

# Figure 2: Fixation probability vs b/c
def fig2_fixation_vs_bc():
    os.makedirs('plots', exist_ok=True)

    bc_values = np.arange(1.5, 5.1, 0.1)
    altruist_results = []
    parochialist_results = []

    for bc in bc_values:
        # Simulate for altruist mutants
        config.b, config.c = bc, 1.0
        mutant_strategy = Strategy.ALTRUIST
        print(f"\nSimulating for altruist mutants with b/c={bc:.2f}")
        altruist_fixation_prob = simulate_fixation_probabilities(runs=10, mutant_strategy=mutant_strategy)
        altruist_results.append(altruist_fixation_prob)

        # Simulate for parochialist mutants
        mutant_strategy = Strategy.PAROCHIALIST
        print(f"\nSimulating for parochialist mutants with b/c={bc:.2f}")
        parochialist_fixation_prob = simulate_fixation_probabilities(runs=10, mutant_strategy=mutant_strategy)
        parochialist_results.append(parochialist_fixation_prob)

    # Plot altruist fixation probabilities (green line)
    plt.plot(bc_values, altruist_results, 'g-', label='Altruists')

    # Plot parochialist fixation probabilities (red line)
    plt.plot(bc_values, parochialist_results, 'r-', label='Parochialists')

    # Add neutral mutant threshold (black dashed line)
    plt.axhline(y=0.01, color='black', linestyle='--', label='Selection')

    # Add labels, title, legend, and grid
    plt.xlabel('b/c (Benefit-to-Cost Ratio)')
    plt.ylabel('Fixation Probability')
    plt.title('Fixation Probability vs b/c')
    plt.legend(loc='upper right')
    plt.grid(True)

    # Save and show the plot
    output_file = 'plots/fig2_fixation_vs_bc.png'
    plt.savefig(output_file)
    print(f"\nPlot saved to {output_file}")

# Run all simulations and save figures
def main():
    fig2_fixation_vs_bc()

if __name__ == "__main__":
    main()