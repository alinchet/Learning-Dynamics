import src.tools as tools

if __name__ == '__main__':
    nbr_runs = 1
    winner_strategy = []
    tools.create_logs_folder()

    tools.main(nbr_runs,winner_strategy)
    tools.run_bc_simulation(nbr_runs)