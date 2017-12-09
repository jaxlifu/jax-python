#!/usr/bin/env python
# -*- coding: utf-8 -*-

# install.py
#
import os
import sys


def update():

    os.system('sudo apt-get update')
    os.system('sudo apt-get -y upgrade')
    pass


def install():
    os.system(
        'sudo apt-get install -y nginx supervisor python3 mysql-server git python3-pip python-dev python3-dev libmysqlclient-dev')
    os.system('sudo pip3 install --upgrade pip')
    os.system('wget -qO- https://raw.github.com/ma6174/vim/master/setup.sh | sh -x')
    pass


def install_omz():
    os.system('sudo apt-get install -y zsh')
    os.system(
        'curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh')
    os.system('pip install powerline-status')
    os.system(
        'git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting')
    try:
        os.chdir('/etc')
        os.system('hostname jax')
        hosts = open('hosts','a+')
        hosts.write('127.0.0.1              jax')
        hosts.close()

        os.chdir('/root')
        zshrc = open('.zshrc', 'a+')
        zshrc.write('plugins=(zsh-syntax-highlighting)')
        zshrc.close()
    except Exception as e:
        print('write file %s' % e)
    pass
    
if __name__ == '__main__':
    update()
    install()
    install_omz()
    config_git()
