#!/usr/bin/env python
#coding=utf8
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager

class User(UserMixin,db.Model):
    __tablename__ = 'users_old'
    id = db.Column(db.String(8),primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    passwd_hash = db.Column(db.String(128),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    phone = db.Column(db.String(16),nullable=True)

    @property
    def password(self):
        raise Exception('password is not a readable attribute')

    @password.setter
    def password(self,passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self,password):
        return check_password_hash(self.passwd_hash,password)

    def get_id(self):
        return self.name



@login_manager.user_loader
def load_user(user_id): #todo 这个回调函数再每次页面变更或者浏览器重启之类的场景时调用，接受当前用户的一个标识，由用户类所继承或自己重载的get_id方法决定，返回user对象以保证始终保持用户的登录状态
    print user_id
    return User.query.filter_by(name=user_id).first()
    # return
