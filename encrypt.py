#!/usr/bin/python 
import Image
import numpy as np
import os


project_home = os.getcwd()
slicing_constant = 0x100
def readImage(filename):
    images_home = project_home + '/img/'
    img = (np.asarray(Image.open(images_home + filename))[:,:,0]).flatten()
    slicing_diff = img.size // slicing_constant 
    slicing_start = slicing_diff // 2
    return [(i,j) for i, j in enumerate(xrange(slicing_start,img.size,slicing_diff))]
    
    
readImage('workhard.jpg')
