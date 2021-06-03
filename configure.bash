echo off

# Prepare virtual python env
python3 -m venv pyenv

# Execute commands from a file in the current shell.
source pyenv/bin/activate

# Install requirements
pip3 install -r requirements.txt