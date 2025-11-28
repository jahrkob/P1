
import doctest
import math
from shiftRow import listToInt

class GF2_8:
    def __init__(self, value: int):
        # Prime: 2
        # Extension degree 8
        self.value = modPoly(value)

    def __add__(self, other):
        return GF2_8(modPoly(int(self)^int(other)))

    def __sub__(self,other):
        return GF2_8(modPoly(int(self)^int(other)))

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
    
    def __repr__(self):
        return hex(self.value)

    def __mul__(self, other):
        SoP = 0
        for digitPlace, value in enumerate(bin(int(other)).split('b')[1][::-1]): # i want the digits to come from smallest to biggest with the smallets digitPlace being 0
            if value == '1':
                SoP ^= (self.value << digitPlace)
        return GF2_8(modPoly(SoP))

    def __rmul__(self,other):
        return self.__mul__(other)

def modPoly(poly : int):
    """
    :Description: Used in GF2_8 to reduce by the aes standard polynomial

    The examples showcase both multiplication AND modPoly at the same time
    Examples:
    >>> str(GF2_8(modPoly(GF2_8(0b10100101) * GF2_8(0b110))))
    'x^7 + x^6 + x^5 + x^4           + x^1 + x^0'
    >>> str(GF2_8(modPoly(GF2_8(0b10101010) * GF2_8(0b110))))
    'x^7 + x^6      + x^4                + x^0'
    >>> str(GF2_8(modPoly(GF2_8(0b10111010) * GF2_8(0b110))))
    'x^7      + x^5 + x^4                + x^0'
    """
    poly = int(poly)
    if poly == 0:
        return 0
    elif type(poly) == int:
        while math.log2(int(poly)) >= 8:
            shiftBy = math.floor(math.log2(int(poly)))-8
            poly = poly ^ (0b100011011 << shiftBy)
            if poly == 0:
                break
    else:
        raise("Unsupported argument type")
    return poly

def mix_col(col):
    """
    >>> mix_col([0x87, 0x6e, 0x46, 0xa6])
    [0x47, 0x37, 0x94, 0xed]
    """
    return [
        2*GF2_8(col[0])+3*GF2_8(col[1])+1*GF2_8(col[2])+1*GF2_8(col[3]),
        1*GF2_8(col[0])+2*GF2_8(col[1])+3*GF2_8(col[2])+1*GF2_8(col[3]),
        1*GF2_8(col[0])+1*GF2_8(col[1])+2*GF2_8(col[2])+3*GF2_8(col[3]),
        3*GF2_8(col[0])+1*GF2_8(col[1])+1*GF2_8(col[2])+2*GF2_8(col[3])
    ]
std::throw
def inv_mix_col(col):
    """
    >>> inv_mix_col([0x47,0x37,0x94,0xed])
    [0x87, 0x6e, 0x46, 0xa6]
    """
    return [
        0xe*GF2_8(col[0])+0xb*GF2_8(col[1])+0xd*GF2_8(col[2])+0x9*GF2_8(col[3]),
        0x9*GF2_8(col[0])+0xe*GF2_8(col[1])+0xb*GF2_8(col[2])+0xd*GF2_8(col[3]),
        0xd*GF2_8(col[0])+0x9*GF2_8(col[1])+0xe*GF2_8(col[2])+0xb*GF2_8(col[3]),
        0xb*GF2_8(col[0])+0xd*GF2_8(col[1])+0x9*GF2_8(col[2])+0xe*GF2_8(col[3])
    ]

def aes_mix_col(hex_input:int):
    """
    >>> hex(aes_mix_col(0x632fafa2eb93c7209f92abcba0c0302b))
    '0xba75f47a84a48d32e88d060e1b407d5d'
    """

    r = list(hex_input.to_bytes(16))
    # print(list(hex(i) for i in r[0:4]))
    # print(list(hex(i) for i in r[4:8]))
    # print(list(hex(i) for i in r[8:12]))
    # print(list(hex(i) for i in r[12:]))

    return listToInt([int(i) for i in mix_col(r[0:4]) + mix_col(r[4:8]) + mix_col(r[8:12]) + mix_col(r[12:])],16)

def aes_inv_mix_col(hex_input:int):
    """
    >>> hex(aes_inv_mix_col(0xba75f47a84a48d32e88d060e1b407d5d))
    '0x632fafa2eb93c7209f92abcba0c0302b'
    """
    r = list(hex_input.to_bytes(16))

    return listToInt([int(i) for i in inv_mix_col(r[0:4]) + inv_mix_col(r[4:8]) + inv_mix_col(r[8:12]) + inv_mix_col(r[12:])],16)

if __name__ == '__main__':
    print(doctest.testmod())
    # print(modPoly(0b100000011))
    # print(modPoly(0b1000110110))
    # print(modPoly(0b10001101101))
    # print(modPoly(0b111011011))
    print(mix_col([1,2,3,4]))