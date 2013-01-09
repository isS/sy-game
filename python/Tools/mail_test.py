#-*- coding:UTF-8 -*-
__author__ = 'icestar'


import imaplib
import smtplib
import email

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


#from email import parser

def receiveMail():
    M = imaplib.IMAP4_SSL("mail.game-reign.com")
    M.login("shenyang", "smoon2011!")
    M.select()
    result, message = M.select()
    type,data = M.search(None, 'ALL')
    for num in data[0].split():
        try:
            type, data = M.fetch(num, '(RFC822)')
            data_str = data[0][1]
            #            from email.parser import Parser
            #            msg = Parser().parsestr(data[0][1])
            msg = email.message_from_string(data_str)
            print msg['subject']
        except Exception,e:
            print "get msg error:", e
    M.close()
    M.logout()

def sendMail():
    server = smtplib.SMTP()
    server.connect("mail.game-reign.com")
    server.docmd("EHLO server")
    server.ehlo()
    server.starttls()
    code, resp = server.login("shenyang", "smoon2011!")
    if code != 235:
        raise "帐号登录失败！"
    print resp
    sm = MIMEMultipart()
    sm['Subject'] = Header(u'Re: ' +"title", 'gb2312').encode()
    sm['To'] = Header("shenyang@game-reign.com",'gb2312').encode()
    sm['From'] = 'shenyang@game-reign.com'
    sm['cc'] = 'yupf@game-reign.com'
    sm.attach(MIMEText("test".encode('gbk')))
#    if res.has_key('file') and res['file']:
#        sm.attach(MIMEImage(file(res['file']).read()))
    server.sendmail('shenyang@game-reign.com', "shenyang@game-reign.com", sm.as_string())
    server.quit()


if __name__ == "__main__":
    sendMail()

