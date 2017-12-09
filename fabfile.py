#!/usr/bin/env python
# coding=utf-8

from fabric.api import env, local, cd, run, settings, abort
from fabric.context_managers import prefix


def build():
    '''
    设置build环境
    '''
    env.user = 'root'
    env.sudo_user = 'root'
    env.hosts = ['60.205.190.223']
    env.password = 'Jax@gmail.com'


def prepare():
    '''
    提交本地代码,准备部署,remote 和 branch更据自己需求修改
    '''
    with settings(warn_only=True):
        result = local("git pull webapp master")
        #手动添加依赖文件比较好
        #result = local("pip freeze > requirements.txt")
        result = local("git add . -A && git commit")
        result = local("git push webapp master")
    if result.failed and not confirm("put file failed, Continue[Y/N]?"):
        abort("Aborting file put task!")


def update():
    '''
    服务器上更新代码
    '''
    with cd("/home/jax/python/awesome-python-webapp"):
        run("git pull")
        run("pip3 install -r requirements.txt")
        run("supervisorctl restart awesome")


def deploy():
    prepare()
    update()
