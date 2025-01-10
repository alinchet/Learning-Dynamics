import logging

from src.plots import fig2_fixation_vs_bc, fig5_fixation_vs_alpha, fig7_fixation_vs_lambda
from src.simulation import single_simulation
from src.settings.constants import Strategy

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """
    Entry point of the script. Runs simulations and generates figures.
    """
    runs = 10  # Adjust as needed
    max_workers = 8  # Adjust based on system capabilities

    # Uncomment to run all simulations and generate plots
    fig2_fixation_vs_bc(runs, max_workers)
    # fig5_fixation_vs_alpha(runs, max_workers)
    # fig7_fixation_vs_lambda(runs, max_workers)

    # Uncomment to run a single simulation
    # single_simulation(10, 10, Strategy.ALTRUIST)
    # single_simulation(10, 10, Strategy.PAROCHIALIST)

if __name__ == "__main__":
    main()