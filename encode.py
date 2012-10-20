""" Encode a image with the given data
"""
import scipy
import numpy as np
import random
import os
from PIL import Image
from copy import deepcopy as copy
from dct import *

def encode(filename,message):
	im = Image.open(filename)
	img_src = scipy.misc.fromimage(im,flatten=0)

	if im.mode == 'RGB':
		img_component = img_src[...,1]
	elif im.mode == 'L':
		img_component = img_src
	else:
		print "Error"
	if(img_component.shape[0] < 256 or img_component.shape[1] < 256):
		print "Error"
	else:
		img = img_component[0:256,0:256]
	
	#Set a seed for random number generator
	random.seed("agRJJHoiefxn8328D24kg")

	asciilist = [ord(c) for c in message]
	binlist = ['{0:08b}'.format(i) for i in asciilist]
	binstr = "".join(binlist)
	q = 5
	repbitstream = [bit*q for bit in binstr]
	repbitstring = "".join(repbitstream)
	repbitstream = [b for b in repbitstring]


	permvector = range(repbitstream.__len__())
	random.shuffle(permvector)
	permbitstream = copy(repbitstream)
	for i in range(repbitstream.__len__()):
		permbitstream[i] = repbitstream[permvector[i]]

	accbitstream = permbitstream
	bitCount=0	# no of bit encoded
		
		
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

	newimg = copy(img)


	for I in range(Mb):
		if(bitCount >= accbitstream.__len__()):  
			break   
		for J in range(Nb):
			if(bitCount >= accbitstream.__len__()):  
				break  
			Sx = random.randrange(0,B-7)
			Sy = random.randrange(0,B-7)	

			randBlock = copy(img[((I)*B+Sx):((I)*B+Sx+8), ((J)*B+Sy):((J)*B+Sy+8)])
			randBlock = np.add(randBlock,-128)
			randBlockDCT = dct2(randBlock)
			randBlockQ = np.divide(randBlockDCT,newQM)
		
			##Embedding
			zigzag = np.zeros(20)
			zigzag[0] = randBlockQ[0][0]
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
				zigzag[n] = abs(round(randBlockQ[i][j]))
				if (randBlockQ[i][j] > 0):
					sgn = '+'
	 			else:
					sgn = '-'
			
				if(zigzag[n] > 0):                                                #Checking for threshold
					if( randBlockQ[i][j] > 0.5 and randBlockQ[i][j] < 0.7):
						randBlockQ[i][j] = 0.7
					if(randBlockQ[i][j] < -0.5 and randBlockQ[i][j] > -0.7):
						randBlockQ[i][j] = -0.7
				
					if(bitCount < accbitstream.__len__()):           
						if (accbitstream[bitCount] == '1'):                               #If bit to be encoded is 1
							if (zigzag[n] % 2 == 0):                                    #Converting to odd if it is an even reconstruction point			
								if sgn == '+':											#Incrementing to next step size to get odd							
									randBlockQ[i][j] = (randBlockDCT[i][j] + newQM[i][j]) / newQM[i][j]							
								else:
									randBlockQ[i][j] = (randBlockDCT[i][j] - newQM[i][j]) / newQM[i][j]
								   
														
						elif (accbitstream[bitCount] == '0'):								#If bit to be encoded is 0
							if (zigzag[n] % 2 != 0):									#Converting to even if it is an odd reconstruction point
								if sgn == '+':											#Incrementing to next step size to get even
									randBlockQ[i][j] = (randBlockDCT[i][j] + newQM[i][j]) / newQM[i][j]
								else:
									randBlockQ[i][j] = (randBlockDCT[i][j] - newQM[i][j]) / newQM[i][j]   
			
					bitCount = bitCount + 1
				elif (zigzag[n] == 0):
					randBlockQ[i][j]=zigzag[n]
				
					
			irandBlockDCT = np.multiply(randBlockQ,newQM)
			irandBlock = idct2(irandBlockDCT)
			irandBlock = np.add(irandBlock,128)
			newimg[((I)*B+Sx):((I)*B+Sx+8), ((J)*B+Sy):((J)*B+Sy+8)] = np.uint8(irandBlock)



	img_component[0:256,0:256] = newimg
	if im.mode != 'L':
		img_src[...,1] = img_component
	else:
		img_src = img_component

	newim = scipy.misc.toimage(img_src,255,0,mode=im.mode)
	img_src2 = scipy.misc.fromimage(newim,flatten=0)
	destfile = filename
	newim.save(destfile,'PNG', quality=100)
	shellcommand = "convert " + destfile + " -quality 100 " + destfile
	os.system(shellcommand)
