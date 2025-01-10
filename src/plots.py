from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import logging
import os

from src.simulation import simulate_fixation_probabilities
from src.settings.constants import Strategy
import src.settings.config as config

def generate_plot(x_values, altruist_results, parochialist_results, xlabel, title, filename_prefix):
    """
    Generates and saves a plot with given results.

    Args:
        x_values (list): X-axis values.
        altruist_results (list): Fixation probabilities for altruists.
        parochialist_results (list): Fixation probabilities for parochialists.
        xlabel (str): Label for the X-axis.
        title (str): Title of the plot.
        filename_prefix (str): Prefix for the saved file.
    """
    os.makedirs('plots', exist_ok=True)

    plt.plot(x_values, altruist_results, 'g-', label='Altruists')
    plt.plot(x_values, parochialist_results, 'r-', label='Parochialists')
    plt.axhline(y=0.01, color='black', linestyle='--', label='Neutral Threshold')

    plt.xlabel(xlabel)
    plt.ylabel('Fixation Probability')
    plt.title(title)
    plt.legend(loc='upper right')
    plt.grid(True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'plots/{filename_prefix}_{timestamp}.png'
    plt.savefig(output_file)
    plt.close()
    logging.info(f"Plot saved to {output_file}")

def fig2_fixation_vs_bc(runs=10, max_workers=4):
    """
    Generates Figure 2: Fixation probability vs b/c.
    """
    bc_values = np.arange(1.5, 5.1, 0.5)
    altruist_results = []
    parochialist_results = []

    for bc in bc_values:
        config.b, config.c = 1.0, 1 / bc
        logging.info(f"Configuring b/c ratio: b=1.0, c={config.c:.4f}")

        altruist_results.append(simulate_fixation_probabilities(runs, Strategy.ALTRUIST, max_workers))
        parochialist_results.append(simulate_fixation_probabilities(runs, Strategy.PAROCHIALIST, max_workers))

    generate_plot(bc_values, altruist_results, parochialist_results, 
                  'b/c (Benefit-to-Cost Ratio)', 
                  'Fixation Probability vs b/c', 
                  'fig2_fixation_vs_bc')

def fig5_fixation_vs_alpha(runs=10, max_workers=4):
    """
    Generates Figure 5: Fixation probability vs alpha.
    """
    alpha_values = np.arange(0, 1.1, 0.1)
    altruist_results = []
    parochialist_results = []

    for alpha in alpha_values:
        config.alpha = alpha
        logging.info(f"Setting ingroup interaction probability: alpha={alpha:.2f}")

        altruist_results.append(simulate_fixation_probabilities(runs, Strategy.ALTRUIST, max_workers))
        parochialist_results.append(simulate_fixation_probabilities(runs, Strategy.PAROCHIALIST, max_workers))

    generate_plot(alpha_values, altruist_results, parochialist_results, 
                  'Ingroup Interaction Probability (α)', 
                  'Fixation Probability vs α', 
                  'fig5_fixation_vs_alpha')

def fig7_fixation_vs_lambda(runs=10, max_workers=4):
    """
    Generates Figure 5: Fixation probability vs alpha.
    """
    lambda_values = np.arange(0, 1.1, 0.1)
    altruist_results = []
    parochialist_results = []

    for lambda_mig in lambda_values:
        config.lambda_mig = lambda_mig
        logging.info(f"Setting migration rate: lambda={lambda_mig:.2f}")

        altruist_results.append(simulate_fixation_probabilities(runs, Strategy.ALTRUIST, max_workers))
        parochialist_results.append(simulate_fixation_probabilities(runs, Strategy.PAROCHIALIST, max_workers))

    generate_plot(lambda_values, altruist_results, parochialist_results, 
                  'Migration Rate (lambda)', 
                  'Fixation Probability vs lambda', 
                  'fig7_fixation_vs_lambda')