#!/bin/bash

#
# Initial bootstrapping script for elCID server setups
#

#
# Make Bash play nice with our requirement for setting proxies from variablescase
#
alias sudo='sudo '

#
# Required Ubuntu Packages
#
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install git \
     python-pip \
     libssl-dev \
     python-dev \
     postgresql \
     libpq-dev -y

#
# Pick up on environment variables
#
if [ -z "$HTTP_PROXY" ]; then
    echo "Found an HTTP Proxy environment variable - settng pip and git up to use it.sour"
    alias pip="pip --proxy $HTTP_PROXY"
    git config --global http.proxy $HTTP_PROXY
fi

sudo pip install --upgrade pip
pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv elcid-setup
