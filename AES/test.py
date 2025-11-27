
from shiftRow import shiftRow,listToInt
from keyExpansion import keyExpansion
from mixColumn import aes_mix_col
from subBytes import *
from addRoundKey import *

def singleRound(text:str,initialKey:int):
    """
    This is NOT the encryption the sole purpose of this is to simulate ONE round:
    Examples:
    >>> hex(singleRound('Two One Nine Two',0x5468617473206D79204B756E67204675))
    '0x5847088b15b61cba59d4e2e8cd39dfce'
    """
    #print(hex(text))
    textIntFormat = listToInt(list(text.encode()),16)
    keys = keyExpansion(initialKey)
    a = addKey(textIntFormat,initialKey)
    #print(hex(a))
    b = subBytes(a)
    #print(hex(b))
    c = shiftRow(b)
    #print(hex(c))
    d = aes_mix_col(c)
    #print(hex(d))
    e = addKey(d,keys[1])
    #print(hex(e))
    return e

key = 0x5468617473206D79204B756E67204675
initialText = 'Two One Nine Two'
singleRound(initialText,key)

if __name__ == '__main__':
    print(doctest.testmod())
