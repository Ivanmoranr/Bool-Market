# SETUP PYTHON
  # install python
sudo apt update
sudo apt install python3 python3-dev python3-venv

  # install pip
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
pip3 --version

  # package management
cd <project_name>
python3 -m venv .venv/<env_name>

source .venv/<env_name>/bin/activate
deactivate
