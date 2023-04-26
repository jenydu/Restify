#!/bin/bash
cd restify
sudo add-apt-repository universe
sudo apt install -y python3-pip
sudo apt install -y python3.8-venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install phonenumbers
pip install django-phonenumber-field
pip install Pillow
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py loaddata db2.json
pip install django-cors-headers