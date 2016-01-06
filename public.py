# -*- coding:utf8 -*- #
import smtplib,email,email.MIMEMultipart,email.MIMEBase,email.MIMEText
import email.MIMEImage,base64,sys,re

def sendMail(mailmsg,tomail,title):
    mail_recv=re.split('[,;]',tomail)
    femail=('no-reply@server.com')
    temail =tomail
    msg=email.MIMEMultipart.MIMEMultipart()
    msg['From'] = femail
    msg['To'] = ';'.join(mail_recv)
    msg['Subject'] = title
    msg['Reply-To'] = femail
    body=email.MIMEText.MIMEText(mailmsg,_charset='utf8')
    msg.attach(body)
    smtp = smtplib.SMTP('your mail sev ip','25')
    smtp.login('user@server.com', 'password') 
    smtp.sendmail(femail,mail_recv,msg.as_string())
    smtp.close()
    print 'All mail were sended!'

def sendHtmlMail(mailmsg,tomail,title):
    mail_recv=re.split('[,;]',tomail)
    femail=('noreply@server.com')
    msg=email.MIMEMultipart.MIMEMultipart()

    msg['From'] = femail
    msg['To'] = ';'.join(mail_recv)
    msg['Subject'] = title
    msg['Reply-To'] = femail
    body=email.MIMEText.MIMEText(mailmsg,_subtype='html',_charset='utf8')
    msg.attach(body)
    smtp = smtplib.SMTP('your mail srv ip','25')
    smtp.login('user@server.com', 'password') 
    smtp.sendmail(femail,mail_recv,msg.as_string())
    smtp.close()
    print 'All mail were sended!'
