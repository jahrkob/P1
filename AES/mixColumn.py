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
    elif type(poly) == int:
        while math.log2(int(poly)) >= 8:
            shiftBy = math.floor(math.log2(int(poly)))-8
            poly = poly ^ (0b100011011 << shiftBy)
    else:
        raise("Unsupported argument type")
    return poly

# def aes_mix_col(hex_input):
#     aes_standard = np.matrix([
#         [2,3,1,1],
#         [1,2,3,1],
#         [1,1,2,3],
#         [3,1,1,2]
#     ])

#     np.set_printoptions(formatter={'int':hex})

#     input_bytes = hex_input.to_bytes(16)
#     input_bytes = bytearray(input_bytes)

#     result = np.matrix(
#         input_bytes
#     ) # creates a 1 dimeensional matrix
#     print()
#     result = result.reshape((4,4)) # makes the matrix 2 dimensional
#     result = np.flip(result,axis=1) # part 1 of correcting the matrix layout
#     result = np.rot90(result) # part 2 of correcting the matrix layout

#     print(result)
#     return result*aes_standard

# #print(aes_mix_col(0x00112233445566778899aabbccddeeff))

print(doctest.testmod())

print(
    GF2_8(0b11101101) * GF2_8(0b110010)
)
