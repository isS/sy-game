import config,db
from msg import msg

import imaplib,smtplib,email
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import re,os.path,urllib,urllib2,sys
from executors import executor_lst
from email.Header import Header


def get_new_mail(exes):
	
	max_id = msg.last_msg()
	#print 'checking mail from id %d' % (max_id + 1)
	
	M = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
	M.login(config.EMAIL_USER, config.EMAIL_PASS)
	M.select()
	typ, data = M.search(None, 'ALL')
	#print data[0]
	for num in data[0].split():
		n = int(num)
		if n > max_id:
			typ, data = M.fetch(num, '(RFC822)')
			for response_part in data:
				if isinstance(response_part, tuple):
					m = msg(n, response_part[1])
					m.insert()
					
					res = None
					
					if exes.has_key(m.subject):
						res = exes[m.subject].process(m)
					
					if not res:		
						res = {'body':'command not found'}
						print 'processing message %d from %s command not found' % (m.id, m.frm)

										
					if res:
						server = smtplib.SMTP()
						server.connect(config.SMTP_SERVER, config.SMTP_PORT)
						server.ehlo()
						server.starttls()
						server.login(config.EMAIL_USER, config.EMAIL_PASS)
						sm = MIMEMultipart()
						sm['Subject'] = Header(u'Re: ' + m.title, 'gb2312').encode()
						sm['To'] = Header(m.frm,'gb2312').encode()
						sm['From'] = 'Q <yupf@game-reign.com>'
						sm['cc'] = 'yupf@game-reign.com'
						sm.attach(MIMEText(res['body'].encode('gbk')))
						if res.has_key('file') and res['file']:
							sm.attach(MIMEImage(file(res['file']).read()))
						server.sendmail('Q <yupf@game-reign.com>', m.frm.encode('gbk'), sm.as_string())
						server.quit()

					
	M.close()
	M.logout()
	
if __name__ == "__main__":
	es = executor_lst()
	if(len(sys.argv)>1) and sys.argv[1] == 'debug':
		print 'debug mode'
		get_new_mail(es)
	else:
		print 'server mode'
		while(True):
			get_new_mail(es)
