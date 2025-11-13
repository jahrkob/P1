import numpy as np

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

print(aes_mix_col(0x00112233445566778899aabbccddeeff))