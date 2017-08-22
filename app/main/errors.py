#!/usr/bin/env python
#coding=utf8

from flask import render_template

from . import main

@main.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404

@main.errorhandler(500)
def server_interval_error(error):
    return render_template('error/500.html'),500