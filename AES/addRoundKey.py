"""
This file should hold both the take input function and the addKey function
"""

import doctest

def takeInput(key = 0x0102030405060708):
    userInput = input('Plaintext:\n>>> ')
    for chunk in splitIntoChunks(userInput):
        addKey(chunk,key)
        # <-----------------------------------------------

def addKey(text,key):
    return text^key

def splitIntoChunks(text:str, chunkSize : int = 16):
    """
    Splits text into chunks of 16 bytes (assuming each character is one byte). Uses the PKCS#7 padding method
    :param text: The text which will be split into chunks of 16 bytes
    :examples:
    >>> splitIntoChunks('1122334455667788aabbccddeeffgghha')
    [b'1122334455667788', b'aabbccddeeffgghh', b'\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f\\x0f']
    >>> splitIntoChunks('ab')
    [b'\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e\\x0e']
    """
    uniformCharacterLength = text.encode() # convert string into utf-8 which has uniform character length of one byte
    split = [uniformCharacterLength[i:i+16] for i in range(0,len(uniformCharacterLength),16)] # split into 16 byte chunks
    paddingNeeded = chunkSize - len(split[-1]) # check how much padding is needed for last chunk
    split[-1] = bytes([paddingNeeded]) * paddingNeeded # add the padding
    return split

if __name__ == '__main__':
    print(doctest.testmod())
