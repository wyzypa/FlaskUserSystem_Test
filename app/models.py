#!/usr/bin/env python
#coding=utf8
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    mailAdd = db.Column(db.String(64),primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    passwd_hash = db.Column(db.String(128),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    phone = db.Column(db.String(16),nullable=True)
    confirmed = db.Column(db.Boolean,nullable=False,default=False)

    @property
    def password(self):
        raise Exception('password is not a readable attribute')

    @password.setter
    def password(self,passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self,password):
        return check_password_hash(self.passwd_hash,password)

    def get_id(self):
        return self.mailAdd

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=3600)
        return s.dumps({'confirm':self.mailAdd})

    def confirm_token(self,token):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except Exception,e:
            return False
        if data.get('confirm') != self.mailAdd:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


@login_manager.user_loader
def load_user(user_id):
    # print user_id
    return User.query.filter_by(mailAdd=user_id).first()
    # return
