
from subBytes import subBytesTable
import numpy as np
import doctest

# round constant
# note that for the initial round it is 0x00
RC = [0x01, 0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

def keyExpansion(key:int):
    """
    taken from here: https://www.kavaliro.com/wp-content/uploads/2014/03/AES.pdf
    >>> hex(keyExpansion(0x5468617473206D79204B756E67204675)[1])
    '0xe232fcf191129188b159e4e6d679a293'
    >>> hex(keyExpansion(0x5468617473206D79204B756E67204675)[2])
    '0x56082007c71ab18f76435569a03af7fa'
    """
    keys = [key]
    words = np.zeros(44)

    for index, constant in enumerate(RC):
        words = list(keys[index].to_bytes(16))
        w_1 = words[0]<<24 | words[1]<<16 | words[2]<<8 | words[3]
        w_2 = words[4]<<24 | words[5]<<16 | words[6]<<8 | words[7]
        w_3 = words[8]<<24 | words[9]<<16 | words[10]<<8 | words[11]
        w_4 = words[12]<<24 | words[13]<<16 | words[14]<<8 | words[15]
        g_val = g(w_4,constant)
        w_5 = w_1 ^ g_val
        w_6 = w_2 ^ w_5
        w_7 = w_3 ^ w_6
        w_8 = w_4 ^ w_7
        keys.append(w_5<<96 | w_6<<64 | w_7<<32 | w_8)
    return keys

def g(prevKey:int,constant):
    """
    These examples have 
    >>> g(0x12345678,0) # it has been validated by me step by step
    414301385
    >>> hex(g(0x12345678,1))
    '0x19b1bcc9'
    """
    a = list(prevKey.to_bytes(4))
    a.append(a.pop(0)) # shift left
    after_sub = [subBytesTable[byte] for byte in a]
    asInt = after_sub[0]<<24 | after_sub[1]<<16 | after_sub[2]<<8 | after_sub[3]
    asInt ^= constant<<24
    return asInt # convert to one integer

if __name__ == '__main__':
    print(doctest.testmod())

