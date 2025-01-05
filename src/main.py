import src.tools as tools
import os


if __name__ == '__main__':
    nbr_runs = 2
    winner_strategy = []
    tools.create_logs_folder()

    #tools.main(nbr_runs,winner_strategy)
    bc_ratios,probabilities,x_label,y_label = tools.run_bc_simulation(nbr_runs)
    tools.plot_graph(bc_ratios,probabilities,x_label,y_label,"r--")
    