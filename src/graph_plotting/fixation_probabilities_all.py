#!/usr/bin/env python3
"""
multifigure_plots.py

Generates multiple figures similar to those in the paper:
'García & van den Bergh (2011), Evolution of parochial altruism by multilevel selection.'

Assumptions:
-----------
1) You have a 'Population' class with a method `run_simulation()` that:
   - Creates or configures a population (m groups, each size n),
   - Introduces a single mutant (Altruist or Parochialist) in an Egoist population,
   - Runs the evolution until homogeneous,
   - Returns which strategy ended up fixing.

2) You can define or pass parameters for:
   - b/c ratio, alpha, migration rate lambda, conflict freq kappa, group size n, # groups m, etc.
   - A "model version" to indicate no conflict (assortment only), conflict only, or conflict+assortment.

3) The script below performs multiple parameter sweeps, storing the fixation probability of each strategy,
   and then plots them in subplots or separate figures.

4) We include a horizontal line for the selection threshold = 1/(m*n).

5) We keep an example set of parameter ranges. Adjust to replicate the paper's figures.
"""

import matplotlib.pyplot as plt
import random

# Example: import your existing modules
# from population import Population
from src.constants.constants import Strategy
from src.config.config import n as DEFAULT_n, m as DEFAULT_m
from src.config.config import alpha as DEFAULT_alpha
from src.config.config import b, c, kappa, q, lambda_mig, z, w

############################
# Example stubs
############################

def run_simulation(
    model_version: str,
    num_groups: int,
    group_size: int,
    mutant_strategy: Strategy,
    alpha: float,
    bc_value: float,
    lambda_val: float,
    kappa_val: float,
    z_val: float,
    # Possibly other arguments...
    n_reps=1
) -> Strategy:
    """
    Stub for a single run:
    You might instead create a Population object with these parameters,
    then call population.run_simulation(), returning the winning strategy.

    For demonstration, we'll just randomly pick a winner.
    Replace with real logic or integrate your Population class.
    """
    # e.g.:
    # config.alpha = alpha
    # config.b = bc_value * config.c
    # config.lambda_mig = lambda_val
    # ...
    # pop = Population( ... , model_version=model_version, ... )
    # winner = pop.run_simulation()
    # return winner

    # For demonstration, pick randomly a winner among {ALTRUIST, PAROCHIALIST, EGOIST}.
    # Weighted to show how it might vary with bc_value or alpha
    # (Just a silly example!)
    # You *must* replace this with your actual calls.
    winners = [Strategy.ALTRUIST, Strategy.PAROCHIALIST, Strategy.EGOIST]
    # Let's artificially bias it to show some effect:
    pA = min(1.0, 0.1 * bc_value)  # bigger bc => bigger chance for altruist
    pP = 0.05 + 0.05*alpha         # parochialist depends on alpha
    pE = 1.0 - (pA + pP)
    if pE < 0: pE=0

    winner = random.choices(winners, weights=[pA, pP, pE], k=1)[0]
    return winner

def replicate_fixation_probability(
    model_version: str,
    param_name: str,
    param_values: list,
    # plus other "default" arguments
    num_reps=30,
    mutant_strategy=Strategy.ALTRUIST
) -> list[float]:
    """
    For each value in param_values, run many replicate simulations,
    count fraction that fixate the same strategy as 'mutant_strategy'.
    Return a list of fixation probabilities.

    param_name => e.g. "b/c", "alpha", "lambda", etc.
    """
    fix_probs = []
    for val in param_values:
        # We'll interpret param_name to set relevant config or pass to run_simulation
        # Then run multiple replicates
        successes = 0
        for _ in range(num_reps):
            # Example approach: set placeholders
            bc_val = 2.0
            alpha_val = DEFAULT_alpha
            lambda_val = lambda_mig
            kappa_val = kappa
            z_val = z
            group_size = DEFAULT_n
            n_groups   = DEFAULT_m

            if param_name == "b/c":
                bc_val = val
            elif param_name == "alpha":
                alpha_val = val
            elif param_name == "lambda":
                lambda_val = val
            elif param_name == "kappa":
                kappa_val = val
            elif param_name == "z":
                z_val = val
            elif param_name == "n":
                group_size = int(val)
            elif param_name == "m":
                n_groups   = int(val)

            # run 1 simulation
            winner_strat = run_simulation(
                model_version=model_version,
                num_groups=n_groups,
                group_size=group_size,
                mutant_strategy=mutant_strategy,
                alpha=alpha_val,
                bc_value=bc_val,
                lambda_val=lambda_val,
                kappa_val=kappa_val,
                z_val=z_val,
                n_reps=1
            )
            if winner_strat == mutant_strategy:
                successes += 1
        fix_probs.append(successes / num_reps)
    return fix_probs

############################
# Plotting
############################

def plot_fixation(
    param_values: list[float],
    fix_prob_altruist: list[float],
    fix_prob_parochialist: list[float],
    param_name: str,
    model_version: str,
    n_groups: int,
    group_size: int
):
    """
    Plots fixation probabilities for Altruist & Parochialist vs param_values,
    plus a horizontal line for selection threshold = 1/(m*n).
    """
    # selection threshold
    threshold = 1.0 / (n_groups * group_size)

    plt.figure(figsize=(7,5))
    plt.plot(param_values, fix_prob_altruist, 'ro--', label="Altruist")
    plt.plot(param_values, fix_prob_parochialist, 'bo--', label="Parochialist")
    plt.axhline(y=threshold, color='k', linestyle='--', label=f"Selection threshold 1/({n_groups}*{group_size})")
    plt.xlabel(param_name)
    plt.ylabel("Fixation Probability")
    plt.title(f"Fixation Prob vs {param_name} ({model_version})")
    plt.ylim([0,1])
    plt.legend()
    plt.tight_layout()

    # Show or save:
    plt.show()
    # plt.savefig(f"fixprob_{model_version}_{param_name}.png")
    plt.close()

############################
# Main "multi-figure" driver
############################

def main():
    random.seed(1234)

    # For demonstration, define a few param sweeps:
    # 1. b/c
    bc_values = [1.5, 2.0, 3.0, 4.0]
    # 2. alpha
    alpha_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    # 3. group size n
    n_values = [5, 10, 15, 20]
    # (You can define more param sets as needed)

    # We'll define one function that runs for each model version: 
    # "assortment_only", "conflict_only", "conflict_plus_assortment".
    # In a real setup, you'd pass toggles to your run_simulation or Population.

    # Example loop over "assortment_only":
    for model_version in ["assortment_only", "conflict_only", "conflict_plus_assortment"]:
        print(f"\n=== Model Version: {model_version} ===")

        # 1) b/c sweep
        fix_prob_A_bc = replicate_fixation_probability(
            model_version=model_version,
            param_name="b/c",
            param_values=bc_values,
            num_reps=30,  # repeated sims
            mutant_strategy=Strategy.ALTRUIST
        )
        fix_prob_P_bc = replicate_fixation_probability(
            model_version=model_version,
            param_name="b/c",
            param_values=bc_values,
            num_reps=30,
            mutant_strategy=Strategy.PAROCHIALIST
        )
        plot_fixation(
            bc_values,
            fix_prob_A_bc,
            fix_prob_P_bc,
            param_name="b/c",
            model_version=model_version,
            n_groups=DEFAULT_m,
            group_size=DEFAULT_n
        )

        # 2) alpha sweep
        fix_prob_A_alpha = replicate_fixation_probability(
            model_version=model_version,
            param_name="alpha",
            param_values=alpha_values,
            num_reps=30,
            mutant_strategy=Strategy.ALTRUIST
        )
        fix_prob_P_alpha = replicate_fixation_probability(
            model_version=model_version,
            param_name="alpha",
            param_values=alpha_values,
            num_reps=30,
            mutant_strategy=Strategy.PAROCHIALIST
        )
        plot_fixation(
            alpha_values,
            fix_prob_A_alpha,
            fix_prob_P_alpha,
            param_name="alpha",
            model_version=model_version,
            n_groups=DEFAULT_m,
            group_size=DEFAULT_n
        )

        # 3) group size n sweep
        fix_prob_A_n = replicate_fixation_probability(
            model_version=model_version,
            param_name="n",
            param_values=n_values,
            num_reps=30,
            mutant_strategy=Strategy.ALTRUIST
        )
        fix_prob_P_n = replicate_fixation_probability(
            model_version=model_version,
            param_name="n",
            param_values=n_values,
            num_reps=30,
            mutant_strategy=Strategy.PAROCHIALIST
        )
        plot_fixation(
            n_values,
            fix_prob_A_n,
            fix_prob_P_n,
            param_name="n",
            model_version=model_version,
            n_groups=DEFAULT_m,  # caution: we're changing 'n', but this is a baseline in config
            group_size=DEFAULT_n
        )

if __name__ == "__main__":
    main()
