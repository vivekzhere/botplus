import glob
from encode import encode
from decode import decode

m = "vivekzhere@gmail.com#mississippi"
print m.__len__()
count = 1
for infile in glob.glob("*.jpg"):
    m2 = m + str(count)
    encode(infile,m2)
    decode(infile,m2.__len__())
    count = count + 1
