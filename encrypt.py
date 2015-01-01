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

def shuffle_array(array, key):
    return array;#hey syam its your job bro...

'''
   This guy is the hero and the villain
      he assumes every string is ASCII [be nice to him or you are screwed]
      he takes an imagefilename , assuming file is placed in the img folder
         takes final encrypted file name and creates it in the folder encrypted
      key is the supreme power ...
      return False on failure or the obvious counter part :)        
'''
def encode(string, imagefilename, key, keyfilename):
    encrypted_home = project_home + 'encrypted'
    encrypted_file = encrypted_home + keyfilename
    shuffled_array = readImage(imagefilename)
    string_as_bytearray = map(lambda x:bin(x)[2:], bytearray(string, encoding = "utf-8", errors="strict"))
    for i in xrange(0, len(string_as_bytearray), 32):
        shuffled_array = shuffle_array(shuffle_array,key)
        for str_index, str_byte in enumerate(string_as_bytearray[i:i+32]):
            for bit_index, str_bit in enumerate(str_byte):
               bit_to_file = 0x01&(str_bit^(shuffle_array[8*(str_index+i)+bit_index]))
               #####Note : put this bit to file and you are done
               ###its 12:40 in the mid night good night bro
        
readImage('workhard.jpg')
