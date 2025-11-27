
import doctest

def listToInt(a,bytes):
    """
    Accepts a list with 4,16 bytes and makes it into one 4,16 byte integer
    Examples:
    >>> hex(listToInt([1,2,3,4],4))
    '0x1020304'
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
    >>> hex(shiftRow(0x0102030405060708090a0b0c0d0e0f))
    '0x10203050607040a0b08090f0c0d0e'
    """
    byteList = list(bigInt.to_bytes(16))
    return listToInt(byteList[0:4] + circularShiftLeft(byteList[4:8],1)+circularShiftLeft(byteList[8:12],2)+circularShiftLeft(byteList[12:16],3),16)

def circularShiftLeft(listThing:list, by = 1):
    """
    Both returns adajusted list and changes list in place
    Examples:
    >>> a = [1,2,3,4]
    >>> circularShiftLeft(a)
    [2, 3, 4, 1]
    >>> a
    [2, 3, 4, 1]
    >>> circularShiftLeft([1,2,3,4],2)
    [3, 4, 1, 2]
    """
    for _ in range(by):
        listThing.append(listThing.pop(0))
    return listThing

if __name__ == '__main__':
    print(doctest.testmod())