#!/usr/bin/env python
#coding=utf8

from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,HiddenField,SubmitField,BooleanField
from wtforms.validators import DataRequired,NumberRange,EqualTo

class UserForm(FlaskForm):
    # id = HiddenField(u'id')
    id = StringField(u'ID',validators=[DataRequired()])
    name = StringField(u'姓名',validators=[DataRequired()])
    passwd = PasswordField(u'密码',validators=[DataRequired()])
    passwd_recheck = PasswordField(u'确认密码',validators=[DataRequired(),EqualTo('passwd',message=u'两次密码输入不一致')])
    age = IntegerField(u'年龄',validators=[NumberRange(min=18,max=60,message=u'年龄必须在18到60岁间')])
    phone = StringField(u'联系电话')
    submit = SubmitField(u'提交')

class LoginForm(FlaskForm):
    name = StringField(u'姓名',validators=[DataRequired()])
    passwd = PasswordField(u'密码',validators=[DataRequired()])
    remember_me = BooleanField(u'记住我的登录状态')
    submit = SubmitField(u'登录')