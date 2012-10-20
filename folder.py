import glob
from encode import encode
from decode import decode

m = "vivekzhere@gmail.com#mississippi"
print m.__len__()
for infile in glob.glob("~/Pictures/*.jpg"):
    encode(infile,m)
for infile in glob.glob("~/Pictures/*.jpg"):
    decode(infile,m.__len__())
    




