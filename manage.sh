#!/usr/bin/env bash

# Exit script on any error
set -e

# Define variables
REPO_URL="https://github.com/alinchet/Learning-Dynamics.git"
REPO_DIR="Learning-Dynamics"
ENV_DIR="env"
LOG_DIR="logs"

# Check for arguments
case "$1" in
    "clone")
        # Clone the repository
        echo "Cloning the repository..."
        git clone $REPO_URL
        echo "Repository cloned successfully."
        ;;

    "setup")
        # Set up a Python environment
        echo "Setting up the Python environment..."
        python3 -m venv $ENV_DIR
        source $ENV_DIR/bin/activate
        pip install -r requirements.txt
        echo "Python environment set up successfully."

        # Create a log folder if it doesn't exist
        if [ ! -d "$LOG_DIR" ]; then
            mkdir -p $LOG_DIR
            echo "Log directory created successfully."
        else
            echo "Log directory already exists."
        fi

        # Provide activation reminder
        echo "To activate the environment, run: source $ENV_DIR/bin/activate"
        ;;

    "run")
        # Run a single simulation
        if [ ! -d "$ENV_DIR" ]; then
            echo "Error: Virtual environment not found. Run './bash.sh setup' first."
            exit 1
        fi

        source $ENV_DIR/bin/activate
        echo "Running the simulation..."
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        python -m src.main 1 | tee $LOG_DIR/run_1_$TIMESTAMP.log
        echo "Simulation completed successfully. Logs saved to $LOG_DIR/run_1_$TIMESTAMP.log."
        ;;

    "run_all")
        # Run all simulations
        if [ ! -d "$ENV_DIR" ]; then
            echo "Error: Virtual environment not found. Run './bash.sh setup' first."
            exit 1
        fi

        source $ENV_DIR/bin/activate
        echo "Running all simulations..."
        for i in {1..5}; do
            TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
            python -m src.main $i | tee $LOG_DIR/run_${i}_$TIMESTAMP.log
            echo "Simulation $i completed. Logs saved to $LOG_DIR/run_${i}_$TIMESTAMP.log."
        done
        echo "All simulations completed successfully."
        ;;

    "clean")
        # Clean up virtual environment and logs
        if [ -d "$ENV_DIR" ]; then
            deactivate || true
            rm -rf $ENV_DIR
            echo "Removed virtual environment."
        fi

        if [ -d "$LOG_DIR" ]; then
            rm -rf $LOG_DIR/*
            echo "Cleared logs in $LOG_DIR."
        fi

        echo "Cleaned up temporary files."
        ;;

    *)
        # Display usage instructions
        echo -e "Usage:
    ./manage.sh clone
    ./manage.sh setup
    ./manage.sh run
    ./manage.sh run_all
    ./manage.sh clean"
        ;;
esac