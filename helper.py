from redef import symbols


def isSymbol(char):
    for symbol in symbols:
        if symbol == char:
            return True
    return False
