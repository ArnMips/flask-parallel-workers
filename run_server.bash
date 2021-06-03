echo off
source pyenv/bin/activate

cd server
python3 main_worker.py 127.0.0.1 5000
cd ..

# Deactivate python virtual env (with shell function from pyenv/bin/activate file)
deactivate