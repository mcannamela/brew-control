#!/bin/bash

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