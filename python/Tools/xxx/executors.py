import glob

def executor_lst():
	exes = {}
	for f in glob.glob('exe1000.py'):
		m = f[0:(len(f)-3)]
		s = __import__(m)
		if hasattr(s,m):
			t = getattr(s, m)
			o = t()
			exes[o.cmd_name()] = o
	return exes
