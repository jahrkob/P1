import numpy as np
import doctest
import math

class GF2_8:
    def __init__(self, value: int):
        # Prime: 2
        # Extension degree 8
        self.irreduciblePolynomial = 0b100011011 # x^8+x^4+x^3+x+1
        self.value = modPoly(value)

    def __add__(self, other):
        return GF2_8(int(self)^int(other))

    def __sub__(self,other):
        return GF2_8(int(self)^int(other))

    def __int__(self):
        return self.value
    
    def __str__(self):
        bitString = bin(self.value).split('b')[1]
        finalString = ""
        first = True
        for exponent,value in list(zip(range(len(bitString)-1,-1,-1),bitString)):
            if value == '1':
                if not first:
                    finalString += '+'
                else:
                    first = False
                finalString += f" x^{exponent} "
            else:
                finalString += "    " + len(str(exponent)) * ' ' # exponents can be several digits long
        return finalString.strip() # remove the leading and trailing spaces

    def __mul__(self, other):
        SoP = 0
        for digitPlace, value in enumerate(bin(int(other)).split('b')[1][::-1]): # i want the digits to come from smallest to biggest with the smallets digitPlace being 0
            if value == '1':
                SoP ^= (self.value << digitPlace)
        return GF2_8(SoP)

    def __rmul__(self,other):
        return self.__mul__(other)

def modPoly(poly : int | GF2_8):
    """
    The examples showcase both multiplication AND modPoly at the same time
    Examples:
    >>> str(modPoly(GF2_8(0b10100101) * GF2_8(0b110)))
    'x^7 + x^6 + x^5 + x^4           + x^1 + x^0'
    >>> str(modPoly(GF2_8(0b10101010) * GF2_8(0b110)))
    'x^7 + x^6      + x^4                + x^0'
    >>> str(modPoly(GF2_8(0b10111010) * GF2_8(0b110)))
    'x^7      + x^5 + x^4                + x^0'
    """
    if type(poly) == GF2_8:
        while math.log2(int(poly)) >= 8:
            shiftBy = math.floor(math.log2(int(poly)))-8
            poly -= (0b100011011 << shiftBy)
    else:
        poly = int(poly)
    if type(poly) == int:
        while math.log2(int(poly)) >= 8:
            shiftBy = math.floor(math.log2(int(poly)))-8
            poly = poly ^ (0b100011011 << shiftBy)
    else:
        raise("Unsupported argument type")
    return poly

print(doctest.testmod())

class AES_Array:
    def __init__(self,input):
        self.aes_standard = [
            [GF2_8(2),GF2_8(3),GF2_8(1),GF2_8(1)],
            [GF2_8(1),GF2_8(2),GF2_8(3),GF2_8(1)],
            [GF2_8(1),GF2_8(1),GF2_8(2),GF2_8(3)],
            [GF2_8(3),GF2_8(1),GF2_8(1),GF2_8(2)]
        ]

    def __mul__(self, other):
        return 2

    def EncryptBlock(self, block:int):
        blockString = hex(block).strip('x')[1]
        if len(blockString) != 32:
            raise("invalid input length")
        self.table = [
            [blockString[0:2],blockString[8:10],blockString[16:18],blockString[24:26]],
            [blockString[2:4],blockString[10:12],blockString[18:20],blockString[26:28]],
            [blockString[4:6],blockString[12:14],blockString[20:22],blockString[28:30]],
            [blockString[6:8],blockString[14:16],blockString[22:24],blockString[30:]]
        ]
        print("Still lacks encryption")

    def aes_mix_col(hex_input : list[list[GF2_8]]):
        aes_standard = [
            [GF2_8(2),GF2_8(3),GF2_8(1),GF2_8(1)],
            [GF2_8(1),GF2_8(2),GF2_8(3),GF2_8(1)],
            [GF2_8(1),GF2_8(1),GF2_8(2),GF2_8(3)],
            [GF2_8(3),GF2_8(1),GF2_8(1),GF2_8(2)]
        ]



print()
