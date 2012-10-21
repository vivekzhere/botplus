import glob
from os import path
from encode import encode
from decode import decode

m = "10abcd1234*#vivekzhere#G"
print m.__len__()
count = 1
picdir = path.expanduser("~/Pictures/")
for infile in glob.glob("*.jpg"):
    m2 = m #+ str(count)
    x=encode(infile,m2)
    print "******************Decoding******************"
    y=decode(infile,m2.__len__())
    count = count + 1
    print infile, " : ", y, "\n"
