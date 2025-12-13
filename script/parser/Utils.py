


def detectType(startingBytes:bytes) -> str:
    if startingBytes == b'\xaa':
        return "BIN"
    elif startingBytes == b'$':
        return "ASCII"
    else:
        return None