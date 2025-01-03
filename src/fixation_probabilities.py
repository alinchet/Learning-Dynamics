import logging
from src.population import Population, Strategy
import matplotlib.pyplot as plt



def run_simulation_with_bc(self, bc_values, num_simulations=100):
    """
    Run multiple simulations for each b/c value to calculate fixation probabilities.

    Args:
        bc_values (list[float]): List of b/c ratios to test.
        num_simulations (int): Number of simulations to run for each b/c value.

    Returns:
        dict: A dictionary mapping b/c values to fixation probabilities.
    """
    fixation_probabilities = {bc: 0 for bc in bc_values}

    for bc in bc_values:
        # Set the benefit and cost based on the current b/c ratio
        b = 1.0  # Keep the cost fixed at 1.0
        c = b / bc

        # Run simulations and count how often the mutant strategy fixates
        fixation_count = 0
        for _ in range(num_simulations):
            # Reset the population with a mutant
            population = Population(mutant_strategy=Strategy.ALTRUIST)
            winner = population.run_simulation()

            if winner == Strategy.ALTRUIST:
                fixation_count += 1

        # Calculate fixation probability for the current b/c ratio
        fixation_probabilities[bc] = fixation_count / num_simulations
        logging.info(f"Fixation probability for b/c={bc}: {fixation_probabilities[bc]}")

    return fixation_probabilities




def plot_fixation_probabilities(fixation_probabilities):
    """
    Plot the fixation probabilities as a function of the b/c ratio.

    Args:
        fixation_probabilities (dict): Dictionary mapping b/c values to fixation probabilities.
    """
    bc_values = list(fixation_probabilities.keys())
    fixation_probs = list(fixation_probabilities.values())

    plt.figure(figsize=(10, 6))
    plt.plot(bc_values, fixation_probs, marker='o', linestyle='-', color='b')
    plt.axhline(y=1/(10 * 10), color='r', linestyle='--', label='Neutral Threshold (1/N)')
    plt.xlabel("b/c Ratio")
    plt.ylabel("Fixation Probability")
    plt.title("Fixation Probability of Altruist Mutant vs. b/c Ratio")
    plt.legend()
    plt.grid(True)
    plt.show()







bc_values = [1.5, 2.0, 2.5, 3.0, 4.0, 5.0] # List of b/c ratios to test, make bigger

# Create a Population instance
population = Population()

# Run the simulations and get fixation probabilities
fixation_probabilities = population.run_simulation_with_bc(bc_values, num_simulations=100)

# Plot the results
plot_fixation_probabilities(fixation_probabilities)