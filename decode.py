""" Encode a image with the given data
"""
import scipy
import numpy as np
import random
import binascii
from binascii import unhexlify
from PIL import Image
from copy import deepcopy as copy
from dct import *

def decode(filename,l):
	im=Image.open(filename)
	img_src = scipy.misc.fromimage(im,flatten=0)

	if im.mode != 'L':
		img_component = img_src[...,1]
	else:
		img_component = img_src
	if(img_component.shape[0] < 256 or img_component.shape[1] < 256):
		print "Error"
	else:
		img = img_component[0:256,0:256]

	# Set a seed for random number generator
	random.seed("agRJJHoiefxn8328D24kg")

	q = 5        #Rate of enccoding for RA Codes
#	l = 29        # Length of encoded string

	#Finding the same random permutation
	permvector = range(q*l*8)
	random.shuffle(permvector)

	#Finding inverse permuation vector
	ipermvector = copy(permvector)
	for i in range(q*l*8):
		ipermvector[permvector[i]] = i
		
	M = img.shape[0]
	N = img.shape[1]
	B = 10			#Block Size 
	Mb =  np.uint8(np.floor(M/B))
	Nb =  np.uint8(np.floor(N/B))
	Qf = 50;

	QM = [[16,  11,  10,  16,  24,   40,   51,   61],   
	[12,  12,  14,  19,  26,   58,   60,   55],   
	[14,  13,  16,  24,  40,   57,   69,   56],   
	[14,  17,  22,  29,  51,   87,   80,   62],   
	[18,  22,  37,  56,  68,   109,  103,  77],   
	[24,  35,  55,  64,  81,   104,  113,  92],   
	[49,  64,  78,  87,  103,  121,  120,  101], 
	[72,  92,  95,  98,  112,  100,  103,  99]]

	if Qf < 50:	
		S = 5000/Qf
	else:
		S = 200 - 2*Qf

	newQM = QM
	if S !=	0:
		newQM = np.divide(np.multiply(QM,S),100)
	######
	bitstream=[]
	bitCount = 0;

	for I in range(Mb):
		if(bitCount >= q*l*8):  
			break  
		for J in range(Nb):
			if(bitCount >= q*l*8):  
				break  
			Sx = random.randrange(0,B-7)
			Sy = random.randrange(0,B-7)
		
			randBlock = copy(img[((I)*B+Sx):((I)*B+Sx+8), ((J)*B+Sy):((J)*B+Sy+8)])
			randBlock = np.add(randBlock,-128)
			randBlockDCT = dct2(randBlock)
			randBlockQ = np.divide(randBlockDCT,newQM)
			##Decoding
			rowstep = -1		
			colstep = 1
			i = 0
			j = 0
			#Travelling zigzag
			for n in range(1,20):      
				i = i + rowstep
				j = j + colstep
				if (i < 0):
					i = i + 1	
					colstep = colstep * -1
					rowstep = rowstep * -1
				if ( j < 0 ):
					j = j + 1
					colstep = colstep * -1
					rowstep = rowstep * -1
				absval = abs(round(randBlockQ[i][j]))
				if (absval > 0):
					if (absval%2 == 0):
						bitstream.append(0)
						bitCount = bitCount + 1
					else:
						bitstream.append(1)
						bitCount = bitCount + 1
					
	if bitstream.__len__() >= q*l*8:				
		bitstream = bitstream[:q*l*8]
		drepbitstream = copy(bitstream)
		for i in range(bitstream.__len__()):
			drepbitstream[i] = bitstream[ipermvector[i]]

		#Finding the correct bit per block 
		obitstream = []
		for i in range(l*8):
			if(drepbitstream[i*q:(i+1)*q].count(1) >= 3):
				obitstream.append('1')
			elif(drepbitstream[i*q:(i+1)*q].count(0) >= 3):
				obitstream.append('0')
			else:
				print "Error\n"

		decodestream="".join(obitstream)
		decodestream='0b'+decodestream
		n = int(decodestream, 2)
		decodestr=unhexlify('%x' % n)
		print decodestr
