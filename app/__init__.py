#!/usr/bin/env python
#coding=utf-8

from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()

def create_app(config_mode=None):
    app = Flask(__name__)
    app.config.from_object(config.get(config_mode,'default'))
    config.get(config_mode,'default').init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login' #TODO 这句语句设置了login的界面，后面所有@login_required的验证不通过时就跳转到这个界面
    login_manager.login_message = u'访问此页面需要登录'  #TODO 这句设置了当跳转过去之后显示的flash消息
    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as authorization_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(authorization_blueprint,url_prefix='/auth')

    return app


