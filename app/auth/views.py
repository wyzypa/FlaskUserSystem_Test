#!/usr/bin/env python
# coding=utf8

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required,current_user

from . import auth
from .tools.MailAdaptor import send_mail
from .config import MailSiteMap
from .forms import LoginForm, UserForm
from .. import db
from ..models import User


@auth.before_app_request
def before_request():
    if (current_user.is_authenticated) and (not current_user.confirmed) and (not request.endpoint.startswith('auth')):
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed_user')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    import re
    flag = re.match('^.+@(\w+?)\.[a-z]+$',current_user.mailAdd).group(1)
    mail_site = MailSiteMap.get(flag)
    return render_template('auth/unconfirmed.html',mail_site=mail_site)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(mailAdd=loginForm.mailAdd.data).first()
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

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_token(token):
        flash(u'认证成功!')
    else:
        flash(u'认证失败！')

    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    userForm = UserForm()
    if userForm.validate_on_submit():
        mailAdd = User.query.filter_by(mailAdd=userForm.mailAdd.data).first()
        if mailAdd:
            flash(u'该邮箱已经被注册')
            return redirect(url_for('auth.register'))
        else:
            new_user = User(mailAdd=userForm.mailAdd.data, name=userForm.name.data, age=userForm.age.data,
                            phone=userForm.phone.data)
            new_user.password = userForm.passwd.data
            db.session.add(new_user)
            db.session.commit()
            token = new_user.generate_confirmation_token()
            link = url_for('auth.confirm',token=token,_external=True)
            message = render_template('mail/confirm_mail.txt',confirm_link=link)
            print message
            # send_mail('User System Admin', new_user.mailAdd, u'用户认证', message)
            login_user(new_user)
            return render_template('auth/success.html',new_user=new_user)
    return render_template('auth/register.html', form=userForm)

@auth.route('/resend_confirm')
@login_required
def resend_confirm():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    token = current_user.generate_confirmation_token()
    link = url_for('auth.confirm',token=token,_external=True)
    message = render_template('mail/confirm_mail.txt',confirm_link=link)
    print message
    # send_mail('User System Admin', current_user.mailAdd, u'用户认证', message)
    return render_template('auth/success.html',new_user=current_user)
