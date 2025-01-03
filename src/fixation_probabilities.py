#!/usr/bin/env python3
"""
Script to compute and plot fixation probabilities by varying parameters,
using the provided 'Population' class and the simulation code.

We do:
1) A parameter sweep (e.g. over b/c ratio or alpha, etc.).
2) For each parameter value, run multiple simulations.
3) Check which strategy wins (ALTRUIST, PAROCHIALIST, or EGOIST).
4) Compute the fraction of simulations that end in the mutant strategy's fixation.
5) Plot fixation probability against the parameter, along with the selection threshold 1/n.
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import copy

# Import from your existing files
from src.population import Population
from src.constants import Strategy
from src.config import n, m, b, c, alpha, kappa, q, lambda_mig, w, z

# -------------------------------------------------------------------------
# Example function to run a batch of simulations for a single parameter
# -------------------------------------------------------------------------
def fixation_probability_for_param(
    num_runs: int,
    num_groups: int,
    group_size: int,
    mutant_strategy: Strategy,
    # We can pass the parameter we want to vary as an argument (e.g. b_over_c)
    b_over_c: float
) -> float:
    """
    Run multiple simulations with a given b/c ratio (or other parameter),
    and compute the fraction of runs that end with the mutant_strategy's fixation.

    :param num_runs:        How many replicate simulations to run.
    :param num_groups:      Number of groups in the population.
    :param group_size:      Number of individuals per group.
    :param mutant_strategy: The mutant strategy we want to track (ALTRUIST or PAROCHIALIST).
    :param b_over_c:        The ratio b/c we want to apply.
    :return:                Fixation probability of that mutant.
    """
    # We'll override the config values b,c globally, or you can set them in your code in other ways
    # For a simple approach, we directly hack the global config. 
    # Alternatively, you could pass them in a more robust manner to your Population or config.

    import src.config as config
    config.b = b_over_c * config.c  # e.g. c=1, then b = b_over_c
    # or if you want to keep c=1, effectively b = b_over_c

    # Count how many times we end with the same strategy that we started as mutant
    wins = 0

    for _ in range(num_runs):
        pop = Population(
            num_groups=num_groups,
            num_individuals=group_size,
            mutant_strategy=mutant_strategy
        )
        winning_strat = pop.run_simulation()
        if winning_strat == mutant_strategy:
            wins += 1

    return wins / num_runs


# -------------------------------------------------------------------------
# Main function to demonstrate parameter sweeps and plotting
# -------------------------------------------------------------------------
def main():
    # For demonstration, let's vary the ratio b/c from 1.0 up to 5.0 
    # in increments (you can adjust as you like).
    bc_values = np.linspace(1.0, 5.0, 6)  # e.g. [1.0, 1.8, 2.6, 3.4, 4.2, 5.0]
    num_runs = 50  # number of replicates per parameter

    # We'll track fixation probabilities for ALTRUIST and PAROCHIALIST
    fix_prob_altruist = []
    fix_prob_parochialist = []

    for bc in bc_values:
        print(f"Running simulations for b/c = {bc:.2f}")

        # ALTRUIST
        fpA = fixation_probability_for_param(
            num_runs=num_runs,
            num_groups=m,
            group_size=n,
            mutant_strategy=Strategy.ALTRUIST,
            b_over_c=bc
        )
        fix_prob_altruist.append(fpA)

        # PAROCHIALIST
        fpP = fixation_probability_for_param(
            num_runs=num_runs,
            num_groups=m,
            group_size=n,
            mutant_strategy=Strategy.PAROCHIALIST,
            b_over_c=bc
        )
        fix_prob_parochialist.append(fpP)

    # Plot the results
    # We'll also add the "selection threshold" 1/n = 1/10
    selection_threshold = 1.0 / n

    plt.figure(figsize=(7,5))
    plt.plot(bc_values, fix_prob_altruist, 'ro-', label='Altruist Fixation Prob')
    plt.plot(bc_values, fix_prob_parochialist, 'bo-', label='Parochialist Fixation Prob')
    plt.axhline(selection_threshold, color='k', linestyle='--', label='Selection Threshold (1/n)')
    plt.xlabel("b/c ratio")
    plt.ylabel("Fixation Probability")
    plt.title("Fixation Probability vs b/c ratio")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Example: if you want to show final numeric results:
    print("b/c  |  FixProb(Altruist)  |  FixProb(Parochialist)")
    for bc, fA, fP in zip(bc_values, fix_prob_altruist, fix_prob_parochialist):
        print(f"{bc:4.2f} |      {fA:6.3f}       |      {fP:6.3f}")


if __name__ == "__main__":
    main()
