#!/usr/bin/env python
#coding=utf8
'''
v1.0 modified@20170822
@author:weiyz

'''

from flask import render_template
from flask_login import login_required

from . import main

@main.route('/',methods=['GET'])
def index():
    return render_template('main/index.html')

@main.route('/userinfo',methods=['GET'])
@login_required
def show_userinfo():
    return render_template('main/userinfo.html')
