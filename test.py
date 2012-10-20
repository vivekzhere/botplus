import scipy
import numpy as np
import random
from PIL import Image
from copy import deepcopy as copy
from dct import *

im=Image.open("image_cmyk.jpg")
img = scipy.misc.fromimage(im,flatten=0)
