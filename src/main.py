import src.tools.tools as tools
import os
import sys

"""

def main(nbr_runs):
    # Check if an argument is provided
    if len(sys.argv) < 2:
        print("Usage: python src.main <arg>")
        sys.exit(1)

    # Access the argument
    argument = int(sys.argv[1])
    
    # Process the argument (convert to integer, for example)
    try:
        if argument == 1:
            (bc_ratio_values,probabilities),x_label,y_label = tools.run_bc_simulation(nbr_runs)
            tools.save_graphs(bc_ratio_values,probabilities,x_label,y_label,nbr_runs)

        if argument == 2:
            (lambda_mig_values,probabilities),x_label,y_label = tools.run_lambda_mig_simulation(nbr_runs)
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
    nbr_runs = 15
    winner_strategy = []
    tools.create_logs_folder()

    #tools.main(nbr_runs,winner_strategy)

    main(nbr_runs)



"""



import os
import sys
import threading

import src.tools.tools as tools


def run_simulation(argument: int, nbr_runs: int):
    """
    Runs the simulation corresponding to `argument`.
    """
    try:
        if argument == 1:
            (bc_ratio_values, probabilities), x_label, y_label = tools.run_bc_simulation(nbr_runs)
            tools.save_graphs(bc_ratio_values, probabilities, x_label, y_label, nbr_runs)

        elif argument == 2:
            (lambda_mig_values, probabilities), x_label, y_label = tools.run_lambda_mig_simulation(nbr_runs)
            tools.save_graphs(lambda_mig_values, probabilities, x_label, y_label, nbr_runs)

        elif argument == 3:
            (n_values, probabilities, x_label), y_label = tools.run_n_simulation(nbr_runs)
            tools.save_graphs(n_values, probabilities, x_label, y_label, nbr_runs)

        elif argument == 4:
            (m_values, probabilities), x_label, y_label = tools.run_m_simulation(nbr_runs)
            tools.save_graphs(m_values, probabilities, x_label, y_label, nbr_runs)

        elif argument == 5:
            (alpha_values, probabilities), x_label, y_label = tools.run_alpha_simulation(nbr_runs)
            tools.save_graphs(alpha_values, probabilities, x_label, y_label, nbr_runs)

        else:
            print(f"[WARNING] Argument {argument} is not recognized. Skipping.")

    except ValueError:
        print(f"[ERROR] Argument {argument} must be a valid integer.")


def main(nbr_runs: int):
    """
    Parse all arguments from sys.argv and run each simulation in a separate thread.
    """
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <arg1> <arg2> ...")
        print("  e.g. python -m src.main 1 2 3")
        sys.exit(1)

    # Create logs folder if needed
    tools.create_logs_folder()

    # Gather all arguments
    arguments = sys.argv[1:]

    threads = []
    for arg_str in arguments:
        try:
            arg_int = int(arg_str)
        except ValueError:
            print(f"[ERROR] Cannot convert '{arg_str}' to integer. Skipping.")
            continue

        # Launch each simulation in a separate thread
        t = threading.Thread(target=run_simulation, args=(arg_int, nbr_runs))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("All requested simulations have completed.")


if __name__ == '__main__':
    # Adjust default number of runs as needed
    nbr_runs = 15
    main(nbr_runs)