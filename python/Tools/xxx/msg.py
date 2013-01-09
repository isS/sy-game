import email,db,re
from email.Header import decode_header

def trim(body):
	prog = re.compile('([^\r\t\n]+)')
	res = prog.findall(body)
	if(res):
		return res[0]
	else:
		return None

def get_body(m):
    maintype = m.get_content_maintype()
    if maintype == 'multipart':
        for part in m.get_payload():
            if part.get_content_maintype() == 'text':
                return trim(part.get_payload())
    elif maintype == 'text':
        return trim(m.get_payload())

def get_first_image(m):
    maintype = m.get_content_maintype()
    if maintype == 'multipart':
        for part in m.get_payload():
            if part.get_content_maintype() == 'image':
                return part.get_payload(decode=True)
    elif maintype == 'image':
        return m.get_payload(decode=True)

def decode(x):
	b = decode_header(x)
	#print b
	u = u''

	for c in b:
		if c[1]:
			#print c[0].decode(c[1])
			u = u + c[0].decode(c[1])
		else:
			#print c[0]
			u = u + c[0]
	return u

class msg:
	id = 0
	subject = u''
	to = u''
	frm = u''
	cc = u''
	body = u''
	para = u''
	im = u''
	title = u''
	
	def __init__(self, id, message):
		m = email.message_from_string(message)
		#print m['from']
		self.id = int(id)
		self.title = decode(m['subject'])
		sub = decode(m['subject']).split('?')
		self.subject = sub[0].strip()
		if(len(sub) > 1): 
			self.para = sub[1].strip()
		self.to = decode(m['to'])
		self.frm = decode(m['from'])
		self.cc = decode(m['cc'])
		self.im = get_first_image(m)
		#if im:
		#	open('attachment.png', 'wb').write(im)
		#exit()
		

	def insert(self):
		sql = 'insert into msg (id, status) values (%d, 0)'	% self.id
		db.execute(sql)
	
	def ismarked(self):
		sql = 'select id from msg where id = %d and status = 1' % self.id
		if(db.exists(sql)):
			return True
		else:
			return False
		
	def mark(self):
		sql = 'update msg set status = 1 where id = %d'	% self.id
		db.execute(sql)
	
	@classmethod
	def last_msg(cls):
		sql = 'select max(id) from msg'
		return db.scalar(sql)
	
	def __str__(self):
		return unicode(self).encode('utf-8')
    
	def __unicode__(self):
		a = 'MessageID: %d' % self.id
		b = 'cmd      : %s' % self.subject
		c = 'To       : %s' % self.to
		d = 'From     : %s' % self.frm
		e = 'cc       : %s' % self.cc
		f = 'para     : %s' % self.para
		#f = 'body     : %s' % self.body
		return u'%s\n%s\n%s\n%s\n%s\n%s\n' % (a, b, c, d, e, f)
	

		
		
		