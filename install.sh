#!/bin/sh


# install nodejs & npm, fix any error or warning
sudo apt-get install -y build-essential
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v
npm -v
npm install npm@latest -g

# install blockchain wallet service
npm install -g blockchain-wallet-service
blockchain-wallet-service -V
npm update -g blockchain-wallet-service
blockchain-wallet-service -V
blockchain-wallet-service -h

# install pip 
python --version
pip --version
sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip 
pip --version

# install blockchain library
pip install blockchain

# install coinbase library
pip install coinbase

# Install pycurl
pip install --upgrade setuptools
sudo apt-get install python-pycurl

# install Tor
sudo apt-get install tor
sudo apt-get install python-stem



