
from shiftRow import shiftRow,listToInt,invShiftRow
from keyExpansion import keyExpansion
from mixColumn import aes_mix_col,aes_inv_mix_col
from subBytes import *
from addRoundKey import *
import base64

def singleRound(text:str,initialKey:int|str):
    """
    This is NOT the encryption the sole purpose of this is to simulate ONE round:
    Examples:
    >>> hex(singleRound('Two One Nine Two',0x5468617473206D79204B756E67204675))
    '0x5847088b15b61cba59d4e2e8cd39dfce'
    """
    #print(hex(text))
    textIntFormat = listToInt(list(text.encode()),16)
    if type(initialKey) != int:
        initialKey.encode('ascii')
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

def AES_encrypt(text:str,initialKey:int,debug:bool = False):
    """
    Examples:
    >>> AES_encrypt('Two One Nine Two',0x5468617473206D79204B756E67204675,debug=True)
    0x5847088b15b61cba59d4e2e8cd39dfce
    0x43c6a9620e57c0c80908ebfe3df87f37
    0x29c3505f571420f6402299b31a02d73a
    0xd8bbae0fc510ef90ef52a9a4f4060029
    0xa72dc2ec856f4bf1e61596587679dc87
    0xb3e46f11ba8d2b97c18769449a89e868
    b'KcNQX1cUIPZAIpmzGgLXOrPkbxG6jSuXwYdpRJqJ6Gg='
    """
    encryptedText = bytes()
    for textChunk in splitIntoChunks(text):
        textIntFormat = listToInt(list(textChunk.encode()),16)
        keys = keyExpansion(initialKey)
        #print([hex(i) for i in keys])
        for round,key in enumerate(keys):
            if round == 0:
                a = addKey(textIntFormat,key)
                continue
            #print(hex(a))
            a = subBytes(a)
            #print(hex(a))
            a = shiftRow(a)
            #print(hex(a))
            if round != 10:
                a = aes_mix_col(a)
                #print(hex(a))
            a = addKey(a,key)
            if debug and round in [1,2,10]:
                print(hex(a))
        encryptedText += a.to_bytes(16)
    return base64.b64encode(encryptedText)

def base64Decode(b64EncodedText):
    """
    Examples:
    >>> list(hex(i) for i in base64Decode(b'KcNQX1cUIPZAIpmzGgLXOrPkbxG6jSuXwYdpRJqJ6Gg='))
    ['0x29c3505f571420f6402299b31a02d73a', '0xb3e46f11ba8d2b97c18769449a89e868']
    """
    byteList = base64.b64decode(b64EncodedText)
    return list(listToInt(list(byteList[i:i+16]),16) for i in range(0,len(byteList),16))

def AES_decrypt(base64EncodedText,initialKey:int):
    """
    >>> AES_decrypt(b'KcNQX1cUIPZAIpmzGgLXOrPkbxG6jSuXwYdpRJqJ6Gg=',0x5468617473206D79204B756E67204675)
    'Two One Nine Two'
    """
    encryptedText = base64Decode(base64EncodedText)
    keys = keyExpansion(initialKey)
    keys.reverse() # we have to use the keys in opposite order now
    
    plaintext = []

    for textChunk in encryptedText:
        for round,key in enumerate(keys):
            if round == 0:
                a = addKey(textChunk,key)
                continue
            a = invShiftRow(a)
            a = invSubBytes(a)
            a = addKey(a,key)
            if round != 10:
                a = aes_inv_mix_col(a) # i know that these are different naming convention but i lost my mind when i made this function
        if textChunk is encryptedText[-1]:
            padding = a.to_bytes(16)[-1]
            if padding == 16:
                plaintext.append('')
            else:
                plaintext.append(a.to_bytes(16).decode()[0:16-padding])
        else:
            plaintext.append(a.to_bytes(16).decode())
    return ''.join(plaintext)





if __name__ == '__main__':
    print(doctest.testmod(),end='\n\n')

    key = 0x6162636465666768696a6b6C6D6E6F70
    print(f'Key: {hex(key)}',end='\n\n')
    initialText = 'Two One Nine Two'
    cipherText = AES_encrypt(initialText,key)
    print(f'Cipher text: {cipherText}')
    plaintext = AES_decrypt(cipherText,key)
    print(f'Plaintext: {plaintext}',end='\n\n')
    newText = 'Some big booty latinas bouncing on my dick'
    cipherText = AES_encrypt(newText,key)
    print(f'Cipher text: {cipherText}')
    plaintext = AES_decrypt(cipherText,key)
    print(f'Plaintext: {plaintext}',end='\n\n')
