from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from src.models.population import Population
from src.settings.constants import Strategy

def single_simulation(num_groups: int = 10, num_individuals: int = 10, mutant_strategy: Strategy = Strategy.ALTRUIST) -> bool:
    """
    Runs a single simulation and returns the result.

    Args:
        mutant_strategy (Strategy): Strategy for the mutant.

    Returns:
        bool: True if mutant strategy fixed, False otherwise.
    """
    try:
        population = Population(num_groups, num_individuals, mutant_strategy)
        result = population.run_simulation()
        return result == mutant_strategy
    except Exception as e:
        logging.error(f"Simulation error: {e}")
        return False

def simulate_fixation_probabilities(runs=10, mutant_strategy=Strategy.ALTRUIST, max_workers=4) -> float:
    """
    Simulates fixation probabilities using multithreading.

    Args:
        runs (int): Number of simulations to run.
        mutant_strategy (Strategy): Strategy to test.
        max_workers (int): Maximum number of threads.

    Returns:
        float: Fixation probability (proportion of mutant's strategy outcomes).
    """
    success_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(single_simulation, 10, 10, mutant_strategy) for _ in range(runs)]

        for i, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result()
                if result:
                    success_count += 1
                logging.info(f"Completed simulation {i}/{runs}, Result: {'MUTANT' if result else 'EGOIST'}")
            except Exception as e:
                logging.error(f"Error in simulation {i}: {e}")

    fixation_prob = success_count / runs
    logging.info(f"Fixation probability for {mutant_strategy.name}: {fixation_prob:.4f}")
    return fixation_prob
