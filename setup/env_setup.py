import os
import subprocess
import sys

"""Sets up the virtual environment and installs required packages for the Gethub application."""

# Create a virtual environment if it doesn't exist
def create_virtualenv():
    venv_path = ".venv"
    if not os.path.exists(venv_path):
        print("[SETUP] Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        return True
    return False

# Install requirements from requirements.txt
def install_requirements():
    pip_path = os.path.join(".venv", "Scripts", "pip.exe")
    if not os.path.exists(pip_path):
        raise FileNotFoundError("[SETUP] pip not found. Virtual environment may be broken.")

    print("[SETUP] Installing dependencies...")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
