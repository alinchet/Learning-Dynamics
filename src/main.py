import src.tools.tools as tools
import os


if __name__ == '__main__':
    nbr_runs = 10
    winner_strategy = []
    tools.create_logs_folder()

    #tools.main(nbr_runs,winner_strategy)

    (bc_ratio_values,probabilities),x_label,y_label = tools.run_bc_simulation(nbr_runs)
    tools.save_graphs(bc_ratio_values,probabilities,x_label,y_label)
    """
        (lambda_mig_values,probabilities),x_label,y_label = tools.run_lambda_mig_simulation(nbr_runs)
        tools.save_graphs(lambda_mig_values,probabilities,x_label,y_label)

        (n_values,probabilities,x_label),y_label = tools.run_n_simulation(nbr_runs)
        tools.save_graphs(n_values,probabilities,x_label,y_label)

        (m_values,probabilities),x_label,y_label = tools.run_m_simulation(nbr_runs)
        tools.save_graphs(m_values,probabilities,x_label,y_label)

        (alpha_values,probabilities),x_label,y_label = tools.run_alpha_simulation(nbr_runs)
        tools.save_graphs(alpha_values,probabilities,x_label,y_label)

        """
        