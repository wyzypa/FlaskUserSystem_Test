#!/usr/bin/env python
#coding=utf8

import smtplib
from email.mime.text import MIMEText

SERVER = 'smtp.126.com'
USER = 'test@126.com'
PASSWD = 'test'
PORT = 25

def send_mail(sender,receiver,subject,message):
    smtp = smtplib.SMTP()
    smtp.connect(SERVER,PORT)
    smtp.login(USER,PASSWD)
    msg = MIMEText(message,'plain','utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    content = msg.as_string()
    smtp.sendmail(USER,receiver,content)
    smtp.quit()