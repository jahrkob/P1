
import doctest

def listToInt(a,bytes):
    """
    Accepts a list with 4,16 bytes and makes it into one 4,16 byte integer
    Examples:
    >>> hex(listToInt([1,2,3,4],4))
    '0x1020304'
    >>> hex(listToInt([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],16))
    '0x102030405060708090a0b0c0d0e0f10'
    """
    if (len(a) != bytes):
        raise('ListToInt only accepts a list with a length equal to amount of bytes integer should have')

    if bytes == 4:
        return a[0]<<24 | a[1]<<16 | a[2]<<8 | a[3]
    elif bytes == 16:
        return a[0]<<120 | a[1]<<112 | a[2]<<104 | a[3]<<96 | a[4]<<88 | a[5]<<80 | a[6]<<72 | a[7]<<64 | a[8]<<56 | a[9]<<48 | a[10]<<40 | a[11]<<32 | a[12]<<24 | a[13]<<16 | a[14]<<8 | a[15]
    else:
        raise('Unsupported amount of bytes')

def shiftRow(bigInt:int):
    """
    remember that this accepts one big int and not rows
    >>> hex(shiftRow(0x63c0ab20eb2f30cb9f93af2ba092c7a2))
    '0x632fafa2eb93c7209f92abcba0c0302b'
    """
    BL = list(bigInt.to_bytes(16)) # ByteList
    return listToInt([BL[0],BL[5],BL[10],BL[15],
            BL[4],BL[9],BL[14],BL[3],
            BL[8],BL[13],BL[2],BL[7],
            BL[12],BL[1],BL[6],BL[11]],16)

def invShiftRow(bigInt:int):
    """
    remember that this accepts one big int and not rows
    >>> hex(invShiftRow(0x632fafa2eb93c7209f92abcba0c0302b))
    '0x63c0ab20eb2f30cb9f93af2ba092c7a2'
    """
    BL = list(bigInt.to_bytes(16)) # ByteList
    return listToInt([BL[0],BL[13],BL[10],BL[7],
                     BL[4],BL[1],BL[14],BL[11],
                     BL[8],BL[5],BL[2],BL[15],
                     BL[12],BL[9],BL[6],BL[3]],16)

if __name__ == '__main__':
    print(doctest.testmod())