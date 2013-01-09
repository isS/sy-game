from executor import executor
from executors import executor_lst

class exe1000(executor):

	def cmd_name(self):
		return 'help'
	
	def help(self):
		return None
	
	def biz(self, m):
		exes  = executor_lst()
		t = 'Help\n\n'
		for (k,e) in exes.iteritems():
			if e.help():
				t = t + 'command: %s' % e.cmd_name() + '\n'
				t = t + e.help() + '\n\n'
		return {'body': t}		
	
