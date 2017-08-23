#!/usr/bin/env python
#coding utf-8

class Config(object):
    SECRET_KEY = 'franknihao'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(self):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql://weiyz:123456@192.168.191.112:3306/flask_DB'
    SQLALCHEMY_DATABASE_URI = 'mysql://weiyz:123456@192.168.191.112:3306/flask_DB'
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

config = {
    'default':DevelopmentConfig,
    'development':DevelopmentConfig,
    'producntion':ProductionConfig
}

MailSiteMap = {
    '126':'https://www.126.com/',
    '163':'https://mail.163.com',
    'qq':'https://mail.qq.com/',
    'hotmail':'https://www.hotmail.com/',
    'gmail':'https://mail.google.com/'
}