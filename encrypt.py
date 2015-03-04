#!/usr/bin/python 
try:
  import Image
except ImportError, e:
  from PIL import Image
try:
  import pylab
except ImportError, e:
  print 'pylab is not imported '
import numpy as np
import os


project_home = os.getcwd()
slicing_constant = 0x100

def memoize(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        """ The dictionary that will act as hashmap for Memoization """
        def __missing__(self, key):
            #print 'no memo'
            ret = self[key] = f(key)
            return ret 
    return memodict().__getitem__

@memoize
def prime(n):
  """ Returns prime number below n  using seive of eratosthenas"""
  np1 = n + 1
  s = list(range(np1)) # leave off `list()` in Python 2
  s[1] = False
  sqrtn = int(round(n**0.5))
  for i in xrange(sqrtn + 1):
      if s[i]:
          s[i*i: np1: i] = [False] * len(xrange(i*i, np1, i))
  return  filter(lambda x:x is not False, s)[-1]

def readImage(filename):
    '''
    reads image as given by the filename
    1 . The function searches for the file in the directory images_home + filename
        on succes proceeds and on falure raise exception
    2.  Then the read file is returned as an array of 256 elements which are 
        the red value of pixels in equal spaced dffrence
        eg : for image of 256*256 size t may start at 128th pixel and ..
             128, 256, 384, 512, 640, 768, 896 ...........
    '''
    images_home = project_home + '/img/'
    img = (np.asarray(Image.open(images_home + filename))[:,:,0]).flatten()
    slicing_diff = img.size // slicing_constant 
    slicing_start = slicing_diff // 2
    return [(i,j) for i, j in enumerate(xrange(slicing_start,img.size,slicing_diff))]

def shuffle_array(array, key):
    for x in range(key,0,-1):
        if prime(x)==1:
            pprime = x
            break;
        else:
            continue;
    pprime = prime(key)
    sh_array = list()
    fact = len(array)   
    #prime = 17
    while fact>0:
        div = pprime
        while div>0:
            div = fact%div
            div = div/3
            sh_array.append(array[div])
            array.pop(div)
            fact = fact-1
            div = div*2
    return sh_array



def encode(string, imagefilename, key, keyfilename):
    '''
       This guy is the hero and the villain
          he assumes every string is ASCII [be nice to him or you are screwed]
          he takes an imagefilename , assuming file is placed in the img folder
             takes final encrypted file name and creates it in the folder encrypted
          key is the supreme power ...
          return False on failure or the obvious counter part :)        
    '''
    encrypted_home = project_home + 'encrypted'
    encrypted_file = encrypted_home + keyfilename
    shuffled_array = readImage(imagefilename)
    string_as_bytearray = map(lambda x:map(int, bin(x)[2:]), bytearray(string, encoding = "utf-8", errors="strict"))
    for i in xrange(0, len(string_as_bytearray), 32):
        shuffled_array = shuffle_array(shuffled_array,key)
        for str_index, str_byte in enumerate(string_as_bytearray[i:i+32]):
            write_byte = 0x00;
            for bit_index, str_bit in enumerate(str_byte):
               bit_to_file = 0x01&(str_bit^(shuffled_array[8*(str_index+i)+bit_index][1]))
               write_byte = write_byte << 1 |  bit_to_file
            print write_byte
        
if __name__ == "__main__":
    encode('sarath','workhard.jpg',11235,'enc_sarath')
