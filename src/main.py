import src.tools.tools as tools
import sys

def main(nbr_runs):
    # Check if an argument is provided
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <arg>")
        sys.exit(1)

    # Access the argument
    argument = int(sys.argv[1])
    
    # Process the argument (convert to integer, for example)
    try:
        if argument == 1:
            (bc_ratio_values,probabilities),x_label,y_label = tools.run_bc_simulation(nbr_runs)
            tools.save_graphs(bc_ratio_values,probabilities,x_label,y_label,nbr_runs)

        if argument == 2:
            (lambda_mig_values,probabilities),x_label,y_label = tools.run_lambda_simulation(nbr_runs)
            tools.save_graphs(lambda_mig_values,probabilities,x_label,y_label,nbr_runs)

        if argument == 3:
            (n_values,probabilities,x_label),y_label = tools.run_n_simulation(nbr_runs)
            tools.save_graphs(n_values,probabilities,x_label,y_label,nbr_runs)

        if argument == 4:
            (m_values,probabilities),x_label,y_label = tools.run_m_simulation(nbr_runs)
            tools.save_graphs(m_values,probabilities,x_label,y_label,nbr_runs)

        if argument == 5:
            (alpha_values,probabilities),x_label,y_label = tools.run_alpha_simulation(nbr_runs)
            tools.save_graphs(alpha_values,probabilities,x_label,y_label,nbr_runs)

    except ValueError:
        print("Error: Argument must be a valid integer.")


if __name__ == '__main__':
    nbr_runs = 10
    main(nbr_runs)