#!/usr/bin/env bash

# Exit script on any error
set -e

# Define constants
REPO_URL="https://github.com/alinchet/Learning-Dynamics.git"
REPO_DIR="Learning-Dynamics"
ENV_DIR="env"
LOG_DIR="logs"

# Functions

clone_repo() {
    echo "Cloning the repository..."
    if [ -d "$REPO_DIR" ]; then
        echo "Repository directory already exists. Skipping clone."
    else
        git clone "$REPO_URL" "$REPO_DIR"
        echo "Repository cloned successfully."
    fi
}

setup_env() {
    echo "Setting up the Python environment..."
    if [ -d "$ENV_DIR" ]; then
        echo "Virtual environment already exists. Skipping setup."
    else
        python3 -m venv "$ENV_DIR"
        source "$ENV_DIR/bin/activate"
        pip install -r requirements.txt
        echo "Python environment set up successfully."
    fi

    echo "Creating log directory..."
    mkdir -p "$LOG_DIR"
    echo "Log directory is ready."

    echo "To activate the environment, run: source $ENV_DIR/bin/activate"
}

run_simulation() {
    if [ ! -d "$ENV_DIR" ]; then
        echo "Error: Virtual environment not found. Run './manage.sh setup' first."
        exit 1
    fi

    source "$ENV_DIR/bin/activate"
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    LOG_FILE="$LOG_DIR/simulation_$TIMESTAMP.log"
    
    echo "Running the simulation..."
    python -m src.main 1 >> "$LOG_FILE" 2>&1
    echo "Simulation completed successfully. Logs saved to $LOG_FILE"
}

clean_env() {
    if [ -d "$ENV_DIR" ]; then
        deactivate || true
        rm -rf "$ENV_DIR"
        echo "Removed virtual environment."
    else
        echo "No virtual environment found to clean."
    fi

    echo "Logs are preserved and not deleted."
}

# Main script
case "$1" in
    clone)
        clone_repo
        ;;
    setup)
        setup_env
        ;;
    run)
        run_simulation
        ;;
    clean)
        clean_env
        ;;
    *)
        echo -e "Usage:
    ./manage.sh clone   # Clone the repository
    ./manage.sh setup   # Set up the Python environment and logs
    ./manage.sh run     # Run a single simulation
    ./manage.sh clean   # Clean up the virtual environment (logs are preserved)"
        ;;
esac