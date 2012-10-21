import glob
from os import path
import stepic
import Image

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


# Function to decrypt passwords from the browser and save in a file
def decrypt_passwords():
	print "decrypt"
	
# Main Functiion

picdir = path.expanduser("~/Pictures/Pictures/")
i=0
for infile in glob.glob(picdir+"*.jpg"):
	i = i+1;
	#encode(infile,"06qwerty"+str(i)+"shamilcm#G############");
	print decode(infile)
