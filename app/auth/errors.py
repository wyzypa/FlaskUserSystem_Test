#!/usr/bin/env python
#coding=utf8

from . import auth
from flask import render_template

@auth.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404

@auth.errorhandler(500)
def interval_server_error(error):
    return render_template('error/500.html'),500