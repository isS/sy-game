import telnetlib
from executor import executor

class exe6000(executor):

	def cmd_name(self):
		return 'alert'
	
	def help(self):
		return None
	
	def biz(self, m):
		tn = telnetlib.Telnet('192.168.26.80',55555)
		tn.write('#alert#\n')
		return {'body': 'alert sent'}
	
	

