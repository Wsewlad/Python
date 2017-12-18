#!/usr/bin/env python3

# A little program for sending e-mail me, when my pc turn on

import smtplib
import time
import socket

# Get current time in format mm/dd/yyyy hh:mm:ss
t = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(time.time()))

# Get local ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 0))
ip = s.getsockname()[0]
s.close()

sender = 'wladyslawfil@gmail.com'
receivers = ['wladyslawfil@gmail.com']

# Form some e-mail header and html content
message = """From: vfil-pc <vfil@pc.ua>
To: me <wladyslawfil@gmail.com>
MIME-Version: 1.0
Content-type: text/html
Subject: [vfil-pc][Login]

<div style="padding:50px;text-align:center;margin:auto;">
<h1 style="color:#686766;">You login vfil-pc from %s<br />at %s</h1>
</div>
""" % (ip, t)

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print ("Successfully sent email")
except SMTPException:
   print ("Error: unable to send email")