echo off
source pyenv/bin/activate

cd client
python3 runner.py http://127.0.0.1 5000 10
cd ..

# Deactivate python virtual env (with shell function from pyenv/bin/activate file)
deactivate