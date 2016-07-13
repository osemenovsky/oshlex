class UnacceptableTokenCount(Exception):
    pass

class UnacceptableToken(Exception):
    pass


def text(tokens):
    if len(tokens) > 1:
        raise UnacceptableTokenCount("This handler accepts 1 token at most")

    return tokens[0]

def integer(tokens):
    if len(tokens) > 1:
        raise UnacceptableTokenCount("This handler accepts 1 token at most")

    return int(tokens[0])
