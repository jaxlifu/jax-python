#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


def clone_awesome():
    os.chdir('/home/jax/python')
    os.system('git clone git@github.com:RainliFu/awesome-python-webapp.git')
    os.chdir('./awesome-python-webapp')
    os.system('mysql -u root -p < schema.sql')

    os.system('cp ./conf/supervisor/awesome.conf /etc/supervisor/conf.d/')
    #os.system('sudo supervisorctl reload')
    #os.system('sudo supervisorctl status')

    os.system('cp ./conf/nginx/awesome /etc/nginx/sites-available/')
    os.chdir('/etc/nginx/sites-enabled')
    os.system('sudo ln -s /etc/nginx/sites-available/awesome')
    #os.system('sudo /etc/init.d/nginx reload')


def clone_lizi():
    os.chdir('/home/jax/python')
    os.system('git clone git@github.com:RainliFu/lizhi.git')
    os.chdir('./lizhi')
    os.system('pip3 install -r require.text')
    os.system('mysql -u root -p < schema.sql')
    os.system('python3 manage.py migrate')
    os.system('python3 manage.py makemigrations Student')
    os.system('python3 manage.py migrate')

    #os.system('cp ./conf/supervisor/lizhi.conf /etc/supervisor/conf.d/')
    os.system('cp ./conf/nginx/lizhi /etc/nginx/sites-available/')
    os.chdir('/etc/nginx/sites-enabled')
    os.system('sudo ln -s /etc/nginx/sites-available/lizhi')


def config_git():
    os.system('git config --global user.name "jax"')
    os.system('git config --global user.email "fuliby2loveyou@gmail.com"')
    os.system('ssh-keygen -t rsa -C "fuliby2loveyou@gmail.com"')
    pass


if __name__ == '__main__':
    if not os.path.exists('/home/jax/python'):
        os.system('mkdir -p /home/jax/python')

    config_git()
    clone_lizi()
    clone_awesome()
