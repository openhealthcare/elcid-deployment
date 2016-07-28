sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python-pip -y
sudo apt-get install libssl-dev -y
sudo apt-get install python-dev -y
sudo apt-get install postgresql
sudo apt-get install libq-dev
sudo pip install --upgrade pip
pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv elcid-setup
sudo pip install fabric
