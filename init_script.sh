# script d'initialisation sur une vm ubuntu sur gcp

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8
sudo apt-get install python3.8-venv
python3.8 -m venv env
source env/bin/activate
pip install -r requirements_webapp.txt

