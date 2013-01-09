import config
import MySQLdb

def getconn():
	return MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASS, db=config.DB_NAME, charset=config.DB_CHARSET) 

def exists(sql):
	conn = getconn()
	cur = conn.cursor()
	n = cur.execute(sql)
	
	if cur.fetchone():
		return true

def execute(sql):
	conn = getconn()
	cur = conn.cursor()
	n = cur.execute(sql)
	cur.close()
	conn.close()
	return n

def scalar(sql):
	conn = getconn()
	cur = conn.cursor()
	n = cur.execute(sql)
	row = cur.fetchone()
	if row:
		return row[0]
	else:
		return 0

def query_dic(sql):
	conn = getconn()
	cur = conn.cursor()
	n = cur.execute(sql)
	dic = {}
	for row in cur.fetchall():
		dic[row[0]] = row[1]
	
	return dic
	