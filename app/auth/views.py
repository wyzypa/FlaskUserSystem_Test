#!/usr/bin/env python
# coding=utf8

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from . import auth
from .forms import LoginForm, UserForm
from .. import db
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(name=loginForm.name.data).first()
        if not user:
            flash(u'没有找到相关用户，请先注册')
            return redirect(url_for('auth.register'))
        elif not user.verify_passwd(loginForm.passwd.data):
            flash(u'密码错误')
        else:
            login_user(user, loginForm.remember_me.data)  # TODO 如果remember_me是True，那么走cookie保存信息，如果是False走session保存信息
            return redirect(request.args.get('next') or url_for('main.index'))

    return render_template('auth/login.html', form=loginForm)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    userForm = UserForm()
    if userForm.validate_on_submit():
        name = User.query.filter_by(name=userForm.name.data).first()
        if name:
            flash(u'该用户名已经被注册')
            return redirect(url_for('auth.register'))
        else:
            new_user = User(id=userForm.id.data, name=userForm.name.data, age=userForm.age.data,
                            phone=userForm.phone.data)
            new_user.password = userForm.passwd.data
            db.session.add(new_user)
            db.session.commit()
            return render_template('auth/success.html')
    return render_template('auth/register.html', form=userForm)
