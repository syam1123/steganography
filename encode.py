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
import pickle
import binascii
import hashlib
#import bitarray


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
def md5Checksum(filePath):
  with open(filePath, 'rb') as fh:
    m = hashlib.md5()
    while True:
      data = fh.read(8192)
      if not data:
        break
      m.update(data)
    return m.hexdigest()
def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

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
    return [(i,j/7) for i, j in enumerate(xrange(slicing_start,img.size,slicing_diff))]

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
    print "String :" , string
    encrypted_home = project_home + 'encrypted'
    encrypted_file = encrypted_home + keyfilename
    shuffled_array = readImage(imagefilename)
    open(keyfilename,"w").close()
    chunks_str = chunks(string,32)
    for i in range (0, len(chunks_str)):
      string = chunks_str[i]
      encrypt_array = []
      #print string
      shuffled_array = shuffle_array(shuffled_array,key)
      string_as_bytearray = map(lambda x:map(int, bin(x)[2:]), bytearray(string, encoding = "utf-8", errors="strict"))
      #print string_as_bytearray
   
      for i in xrange(0, len(string_as_bytearray), 32):
          
          print "shuffledArrary :", len(shuffled_array)
          #print shuffled_array
          for str_index, str_byte in enumerate(string_as_bytearray[i:i+32]):
              write_byte = 0x00;
              #print str_byte
              if(len(str_byte) < 7):
              	while(len(str_byte) !=7):
              		str_byte = [0]+str_byte
              for bit_index, str_bit in enumerate(str_byte):
                bit_to_file = 0x01&(str_bit^(shuffled_array[8*(str_index+i)+bit_index][1]))
                
                write_byte = write_byte << 1 |  bit_to_file
                print str_bit,'^',shuffled_array[8*(str_index+i)+bit_index][1],", ",
                #print 8*(str_index+i)+bit_index
              #print bin(write_byte)[2:]
              write_byte = int(write_byte)
              encryptedfile = open(keyfilename, "a")
              encryptedfile.write('%s' % write_byte)
              encryptedfile.write("+")


            


def decode(imagefilename, key, keyfilename):
  encrypted_home = project_home + 'encrypted'
  encrypted_file = encrypted_home + keyfilename
  shuffled_array = readImage(imagefilename)
  encrypt_array = list()
  enc_array = list()
  open("output_steg.txt","w").close()
  shuffled_array = shuffle_array(shuffled_array, key)
  
  with open(keyfilename) as f:
    encrypted_array = f.readlines()
    encrypt_array = ''.join(encrypted_array)
  s = 0
  for i in xrange(0,len(encrypt_array)):
    if(encrypt_array[i] == "+"):
      i = i+1
      enc_str = ''.join(enc_array)##'''copy contents of file b/w two + symbols.which is the integer value##'''
      del enc_array[:]#'''clear the enc_array after copying it into the enc_str#'''
      enc_str = int(enc_str)
      enc_str = bin(enc_str)[2:]
      if(len(enc_str) < 7):
      	while(len(enc_str) != 7):
			enc_str = "0%s" %enc_str
      output_str = 0x00
      for j in range(0,7):
      	if(s > 255):
      		s = 0
      		shuffled_array = shuffle_array(shuffled_array,key)
        file_bit = enc_str[j:j+1]#'''getting by single bits at a time#'''
        file_bit = int(file_bit)
        bit_to_print = 0x01&(int(bin(file_bit)[2:])^(shuffled_array[s][1]))
        
        output_str = output_str << 1 | bit_to_print
        #print int(bin(file_bit)[2:]),'^',shuffled_array[s][1],", " ,
        #print s
        s = s + 1
      s = s+1
      output_str = chr(output_str)
      print output_str
      output_file = open("output_steg.txt", "a")
      output_file.write('%s' % output_str)


    else:
      enc_array.append(encrypt_array[i])
           
            
        
if __name__ == "__main__":

  encode('sarath is good boy and am also a very god boy', 'workhard.jpg', 1123, 'enc_syamsp.txt')
  print "successfully hide"
  decode('workhard.jpg', 1123,'enc_syamsp.txt')

