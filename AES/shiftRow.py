
import doctest

def shiftRow(byteList):
    """
    :Input: Takes a bytelist and outputs a bytelist

    >>> shiftRow([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    [0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14]
    """
    return byteList[0:4]+circularShiftLeft(byteList[4:8],1)+circularShiftLeft(byteList[8:12],2)+circularShiftLeft(byteList[12:16],3)

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