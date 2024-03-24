import sys
import math

hash_valss = [1779033703,3144124277,1013904242,2773480762,1359893119,2600822924,528734635,1541459225]
constants_k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

class padding:

  def __init__(self) -> None:
     pass
  
  # tools
  def big_edian(arr, len):
      #edian = ['00000000','00000000','00000000','00000000','00000000','00000000','00000000']
      #edian.append(str(bin(len)))
      #print(edian)
      arr.append(str(bin(len)))
      return arr

  def to_binary(word):
     return ''.join(format(ord(c), '08b') for c in word)
      
  def add_padding(bin_str, origin_len):
      bin_str += '1'
      pad_amount = (448 - len(bin_str) % 512) % 512
      bin_str += '0' * pad_amount

      bin_len = format(origin_len * 8, '064b')
      return bin_str+bin_len

  def b2d(n):
     return int(n,2)

  # function
  def pad_word(text):
      p = padding
      bin_text = p.to_binary(text)
      pad_text = p.add_padding(bin_text, len(text))
      return pad_text

class pre_processing :
  
  def __init__(self) -> None:
     pass
 
  # tools
  def arr_sep(word):
      new_arr = []
      start = 0
      end = len(word) 
      step = 32
      for i in range(start, end, step): 
          x = i 
          new_arr.append(word[x:x+step])
      temp = new_arr
      for i in range(16) :
        new_arr[i] = "".join(temp[i])
      return new_arr

  def r_shift(bits,n):
      bin_shift = int(bits, 2) >> n
      return format(bin_shift, '032b')
      
  def r_rotate(bits,n):
      bin_rotate = (int(bits,2) >> n)|(int(bits,2) << (32 - n)) & 0xFFFFFFFF
      return format(bin_rotate, '032b')

  def xor(bin_a , bin_b):
      xored = int(bin_a,2) ^ int(bin_b,2)
      return format(xored,'032b')

  # pre-processing functions
  def sig_n0(msg):
    p = pre_processing
    a = p.r_rotate(msg,7)
    b = p.r_rotate(msg,18)
    c = p.r_shift(msg,3)
    xored_1 = p.xor(a,b)
    return p.xor(xored_1, c)
  
  def sig_n1(msg):
    p = pre_processing
    a = p.r_rotate(msg,17)
    b = p.r_rotate(msg,19)
    c = p.r_shift(msg,10)
    xored_1 = p.xor(a,b)
    return p.xor(xored_1, c)
  
  def sum_n0(msg):
    p = pre_processing
    a = p.r_rotate(msg,2)
    b = p.r_rotate(msg,13)
    c = p.r_rotate(msg,22)
    xored_1 = p.xor(a,b)
    return p.xor(xored_1, c)
  
  def sum_n1(msg):
    p = pre_processing
    a = p.r_rotate(msg,6)
    b = p.r_rotate(msg,11)
    c = p.r_shift(msg,25)
    xored_1 = p.xor(a,b)
    return p.xor(xored_1, c)
   
  def choice(x, y, z):
     final = ''
     for i in range(32):
        if(x[i] == '1'):
           final += y[i]
        else:
           final += z[i]
     return final
  
  def majority(x,y,z):
     final = ''
     for i in range(32):
      ones = sum([x[i] == '1',y[i] == '1',z[i] == '1'])
      if(ones > 1) :
        final += '1'
      else :
         final += '0'
     return final

  def add_bin(x,y):
     x = int(x,2)
     y = int(y,2)
     final = (x+y) % (2**32)
     return format(final, '032b')

class scheduling :
  
  def hash_shift():
     pass
  
  def get_cnst64(cnst):
     for i in range(64):
        cnst[i] = format(cnst[i], '032b')
     return cnst
  
  def msgSchd(word) :
    prp = pre_processing
    for i in range(16,64):
       n_word = prp.add_bin(
          prp.add_bin(prp.add_bin(prp.sig_n1(word[i-2]), 
          word[i-7]), prp.sig_n0(word[i-15])), word[i-16]
          )
       word.append(n_word)
    return word
   
  def get32(cnst):
     return format(cnst, '032b')

  def toHex(val):
     hex_string = format(val, 'x')
     hex_string = hex_string.zfill(8)
     return hex_string

  def compression(msg_scd,hash_vals):
     #T1 = Σ1(e) + Ch(e, f, g) + h + Kt + Wt
     scd = scheduling
     prp = pre_processing
     cnst = scd.get_cnst64(constants_k)
     for i in range(64):
        msg = msg_scd[i]
        t_cnst = cnst[i]
        sig1 = prp.sig_n1(scd.get32(hash_vals[4]))
        choice = prp.choice(scd.get32(hash_vals[4]),scd.get32(hash_vals[5]),scd.get32(hash_vals[6]))
        h = scd.get32(hash_vals[7])
        p1 = prp.add_bin(sig1,choice)
        p2 = prp.add_bin(p1,h)
        p3 = prp.add_bin(p2,msg)
        T1 = prp.add_bin(p3,t_cnst)
        
        #T2 = Σ0(a) + Maj(a, b, c)
        sig0 = prp.sig_n0(scd.get32(hash_vals[0]))
        maj = prp.majority(scd.get32(hash_vals[0]),scd.get32(hash_vals[1]),scd.get32(hash_vals[2]))
        T2 = prp.add_bin(sig0,maj)
        hash_vals[0] = int(prp.add_bin(T1,T2),2)
        hash_vals[4] = int(prp.add_bin(T1,scd.get32(hash_vals[4])),2)
     return hash_vals
     
  def final_hash(cmp):
     for i in range(8):
        cmp[i] = cmp[scheduling.toHex(cmp[i])]
     return cmp

# variables
prp = pre_processing
pad = padding
scd = scheduling



def final_hash(input_string) :
   # word ready to be scheduled
   pad_word = padding.pad_word(input_string)
   sep_pad_word = pre_processing.arr_sep(pad_word)

   # trying the scheduling
   msg_scd = scheduling.msgSchd(sep_pad_word)

   cmp = scd.compression(msg_scd, hash_valss)
   hashh = ''
   for i in range(8):
      cmp[i] = scd.toHex(cmp[i])
      hashh += cmp[i]
   return hashh


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python shah265.py <string_to_hash>")
        sys.exit(1)
    
    input_string = sys.argv[1]
    hash_result = final_hash(input_string)
    print(hash_result)












     

