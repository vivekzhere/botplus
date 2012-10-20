import glob
from os import path
from encode import encode
from decode import decode

m = "vivekzhere@gmail.com#mis"
print m.__len__()
count = 1
picdir = path.expanduser("~/Pictures/")
for infile in glob.glob(picdir + "*.jpg"):
    m2 = m + str(count)
    encode(infile,m2)
    print decode(infile,m2.__len__())
    print ""
    count = count + 1
