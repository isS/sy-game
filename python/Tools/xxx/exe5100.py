from executor import executor

class exe5100(executor):

	def cmd_name(self):
		return 'add girl'
	
	def help(self):
		return 'usage => to:yupf@game-reign.com subject:add girl?[girl name] attachement:[girl.png]'
	
	def biz(self, m):
		return self.add_girl(m)
	
	def add_girl(self, m): 
		path = m.para + ".png"
		open(path,'wb').write(m.im)
		return {'body': 'add girl %s success' % m.para}
	
	