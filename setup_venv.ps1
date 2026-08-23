# PowerShell script to create and activate a virtual environment, then install requirements
# Usage: Open PowerShell, run: .\setup_venv.ps1

python -m venv .venv
Write-Host "Virtual environment created at .\.venv"

Write-Host "To activate (PowerShell): .\\.venv\\Scripts\\Activate.ps1"
Write-Host "After activation, install requirements: pip install -r requirements.txt"

# Optionally automate activation and install (uncomment to enable)
# & .\.venv\Scripts\Activate.ps1
# pip install -r requirements.txt
