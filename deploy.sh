#!/bin/bash

echo "installing system dependencies, must sudo:"
sudo apt-get install python-traits libfreetype6-dev

echo "ensure we have the most up to date pip and virtualenv"
sudo apt-get remove python-pip
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
sudo -H python get-pip.py
rm ./get-pip.py

sudo -H pip install virtualenv


if [ -d "./brew_env" ]; then
  echo "removing existing virtualenv brew_env"
  sudo rm -rf ./brew_env;
fi


echo "creating and activating virtualenv brew_env"
virtualenv --system-site-packages brew_env
source ./brew_env/bin/activate
ln -s ./brew_env/bin/activate ./activate_brew_env


pip install -r requirements.txt