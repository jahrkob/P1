import numpy as np
import math

class gf28:
    def __init__(self, value: int):
        self.value = value
        self.prime = 2
        self.extensionDegree = 8
        self.irreduciblePolynomial = 0b100011011 # x^8+x^4+x^3+x+1
    
    def __add__(self, other):
        return gf28(int(self)^int(other))

    def __sub__(self,other):
        return gf28(int(self)^int(other))

    def __int__(self):
        return self.value
    
    def __str__(self):
        bitString = bin(self.value).split('b')[1]
        print(bitString)
        finalString = ""
        first = True
        for exponent,value in list(zip(range(len(bitString)-1,-1,-1),bitString)):
            if value == '1':
                if not first:
                    finalString += '+'
                else:
                    first = False
                finalString += f" x^{exponent} "
        return finalString

    def __mul__(self, other):
        mulProduct = gf28(int(self)*int(other))

        while math.log2(int(mulProduct)) >= 8:
            shiftBy = math.floor(math.log2(int(mulProduct)))-8
            mulProduct -= (self.irreduciblePolynomial << shiftBy)

        return mulProduct

    def __rmul__(self,other):
        return self.__mul__(other)


def aes_mix_col(hex_input):
    aes_standard = np.matrix([
        [2,3,1,1],
        [1,2,3,1],
        [1,1,2,3],
        [3,1,1,2]
    ])

    np.set_printoptions(formatter={'int':hex})

    input_bytes = hex_input.to_bytes(16)
    input_bytes = bytearray(input_bytes)

    result = np.matrix(
        input_bytes
    ) # creates a 1 dimeensional matrix
    print()
    result = result.reshape((4,4)) # makes the matrix 2 dimensional
    result = np.flip(result,axis=1) # part 1 of correcting the matrix layout
    result = np.rot90(result) # part 2 of correcting the matrix layout

    print(result)
    return result*aes_standard

#print(aes_mix_col(0x00112233445566778899aabbccddeeff))

print(
    gf28(0x87) + gf28(0x6E) + (gf28(0x2) * gf28(0x46)) + (gf28(0x3) * gf28(0xA6))
)
