#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, request, abort, redirect, session, escape

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'hello world'


@app.route('/user/<username>')
def show_user_profile(username):
    return 'user %s' % username


@app.route('/post/<int:post_id>')
def show_post_id(post_id):
    return 'post %d' % post_id


@app.route('/project/')
def project():
    return 'this is project page'


@app.route('/login')
def login():
    print(request.args)

    return render_template('login.html')
    pass


@app.route('/about')
def about():
    return 'this is about page'


if __name__ == '__main__':
    app.run(debug=True)
