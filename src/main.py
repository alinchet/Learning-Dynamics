import src.tools.tools as tools
import os


if __name__ == '__main__':
    nbr_runs = 10
    winner_strategy = []
    tools.create_logs_folder()

    #tools.main(nbr_runs,winner_strategy)

    bc_ratio_values,probabilities,x_label,y_label = tools.run_bc_simulation(nbr_runs)
    tools.save_graph(bc_ratio_values,probabilities,x_label,y_label,"r--")

    lambda_mig_values,probabilities,x_label,y_label = tools.run_lambda_mig_simulation(nbr_runs)
    tools.save_graph(lambda_mig_values,probabilities,x_label,y_label,"r--")

    n_values,probabilities,x_label,y_label = tools.run_n_simulation(nbr_runs)
    tools.save_graph(n_values,probabilities,x_label,y_label,"r--")

    m_values,probabilities,x_label,y_label = tools.run_m_simulation(nbr_runs)
    tools.save_graph(m_values,probabilities,x_label,y_label,"r--")

    alpha_values,probabilities,x_label,y_label = tools.run_alpha_simulation(nbr_runs)
    tools.save_graph(alpha_values,probabilities,x_label,y_label,"r--")

    
    