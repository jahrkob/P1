
from shiftRow import shiftRow
from keyExpansion import keyExpansion
from mixColumn import aes_mix_col
from subBytes import *
from addRoundKey import *

def listToInt(a):
    """
    Accepts a list with 4 bytes and makes it into one 4 byte integer
    """
    return a[0]<<12 | a[1]<<8 | a[2]<<4 | a[3]

def singleRound(text,key):
    keys = keyExpansion(key)
    a = addKey(text,key)
    print(hex(a))
    b = subBytes(a)
    print(hex(b))
    c = shiftRow(b)
    print(hex(c))
    d = aes_mix_col(c)
    print(hex(d))
    e = addKey(d,keys[1])
    print(hex(e))

print([hex(i) for i in keyExpansion(0x5468617473206D79204B756E67204675)])

key = 0x5468617473206D79204B756E67204675
initialText = 'Two One Nine Two'.encode()
singleRound(listToInt(list(initialText)),key)



