#!/usr/bin/env bash
# Create and activate a virtual environment, then install requirements
# Usage: bash setup_venv.sh
python3 -m venv .venv
echo "Virtual environment created at ./.venv"

echo "To activate (bash): source .venv/bin/activate"
echo "After activation, install requirements: pip install -r requirements.txt"

# Optionally automate activation and install (uncomment to enable)
# source .venv/bin/activate
# pip install -r requirements.txt
