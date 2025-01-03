#!/bin/bash

# Exit script on any error
set -e

# Define variables
REPO_URL="https://github.com/alinchet/Learning-Dynamics.git"
REPO_DIR="Learning-Dynamics"
ENV_DIR="env"

# Check for arguments
if [ "$1" == "clone" ]; then
    # Step 1: Clone the Repository
    echo "Cloning the repository..."
    git clone $REPO_URL
    echo "Repository cloned successfully."

elif [ "$1" == "setup" ]; then
    # Step 2: Set up a Python Environment

    echo "Setting up the Python environment..."
    python3 -m venv $ENV_DIR
    source $ENV_DIR/bin/activate
    pip install -r requirements.txt
    echo "Python environment set up successfully."


elif [ "$1" == "run" ]; then
    # Step 3: Run the Simulation

    source $ENV_DIR/bin/activate
    echo "Running the simulation..."
    python -m src.main
    echo "Simulation completed successfully."


elif [ "$1" == "clean" ]; then
    # Step 5: Clean Up (optional)
    deactivate || true
    rm -rf $ENV_DIR
    echo "Cleaned up temporary files."

else
    echo "Usage: ./bash.sh <clone|setup|run|clean>"
fi
