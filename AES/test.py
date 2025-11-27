
from shiftRow import shiftRow
from keyExpansion import keyExpansion
from mixColumn import mix_col
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
    print(a)
    b = subBytes(a)
    print(b)
    c = shiftRow(b)
    print(c)
    d = mix_col(c)
    print(d)
    e = addKey(d,keys[1])
    print(e)

print([hex(i) for i in keyExpansion(0x5468617473206D79204B756E67204675)])

key = 0x5468617473206D79204B756E67204675
initialText = 'Two One Nine Two'.encode()
singleRound(listToInt(bytes(initialText)),key)



