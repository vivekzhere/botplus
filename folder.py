import glob
from encode import encode
from decode import decode

m = "vivekzhere@gmail.com#missippi4"
print m.__len__()
count = 1
for infile in glob.glob("*.jpg"):
    m2 = m #+ str(count)
    x=encode(infile,m2)
    y=decode(infile,m2.__len__())
    count = count + 1
