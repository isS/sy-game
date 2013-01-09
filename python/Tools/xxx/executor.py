
class executor:

	def cmd_name(self):
		return '[command]'

	def help(self):
		return None
	
	def process(self, m):
		print 'processing message %d from %s using executor %s for %s' % (m.id, m.frm, self.cmd_name(), m.para)
		if not m.ismarked():
			if m.subject == self.cmd_name():
				r = self.biz(m)
				m.mark()
				return r
			else:
				print 'command error'
				return
		else:
			print 'message already processed'
			return
	
	def biz(self, m):
		return True	

