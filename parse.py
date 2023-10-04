import re
from enum import IntEnum

tokenMatchers = [
    ("const", r"\d+(\.\d+)?"),
    ("punct", r"[()+\-*/^]"),
    ("space", r"\s+"),  # Tokenizer never emits "space" token
    # Tokenizer also produces "eof" token
]
tokenMatchers = [(tokType, re.compile(regex)) for (tokType, regex) in tokenMatchers]


class ParseError(ValueError):
    pass


class Tokenizer:
    string: str
    index: int = 0
    peeked: tuple[str, str] | None = None

    def __init__(self, string):
        self.string = string

    def _next(self) -> tuple[str, str]:
        if self.index >= len(self.string):
            return ("eof", "")
        for (tokType, pattern) in tokenMatchers:
            m = pattern.match(self.string, self.index)
            if m:
                self.index += len(m.group(0))
                if tokType == "space":
                    return self._next()
                return (tokType, m.group(0))
        raise ParseError(
            f"Invalid character at column {self.index}: {self.string[self.index]}"
        )

    def peek(self) -> tuple[str, str]:
        if not self.peeked:
            self.peeked = self._next()
        return self.peeked

    def consume(self) -> tuple[str, str]:
        if self.peeked:
            p = self.peeked
            self.peeked = None
            return p
        else:
            return self._next()

    def consumePunct(self, expected):
        match self.consume():
            case ("punct", expected):  # TODO: does this not bind expected?
                pass
            case token:
                raise ParseError(f"Expected {expected} but got {token}")


class Power(IntEnum):
    top = 0
    plus = 10
    times = 20
    pow = 30


def parse(string: str) -> float:
    tok = Tokenizer(string)
    result = parseMain(tok, Power.top)
    if tok.peek() != ("eof", ""):
        # TODO: check trailing spaces
        raise ParseError(f"Full string not parsed: reached column {tok.index}")
    return result


# Parse some stuff, and only allow operators with power at least maxPower
def parseMain(tok: Tokenizer, maxPower: Power) -> float:
    left = parseInitial(tok)
    return parseConsequent(tok, left, maxPower)


def parseConsequent(tok: Tokenizer, left: float, maxPower: Power) -> float:
    match tok.peek():
        case ("punct", "+"):
            if Power.plus < maxPower:
                # Example break: expression is 2*3+4, left=3, maxPower=Power.times
                # We don't want to do 3+4. So just return 3 and move on.
                return left
            tok.consume()
            newLeft = left + parseMain(tok, Power.plus + 1)
            return parseConsequent(tok, newLeft, maxPower)
        case ("punct", "-"):
            if Power.plus < maxPower:
                return left
            tok.consume()
            # Add 1 because we don't want to parse 1-2+3 as 1-(2+3).
            newLeft = left - parseMain(tok, Power.plus + 1)
            return parseConsequent(tok, newLeft, maxPower)
        case ("punct", "*"):
            if Power.times < maxPower:
                return left
            # Example keep going: expression is 2+3*4, left=3, maxPower=Power.plus
            tok.consume()
            newLeft = left * parseMain(tok, Power.times + 1)
            return parseConsequent(tok, newLeft, maxPower)
        case ("punct", "/"):
            if Power.times < maxPower:
                return left
            tok.consume()
            newLeft = left / parseMain(tok, Power.times + 1)
            return parseConsequent(tok, newLeft, maxPower)
        case ("punct", "^"):
            if Power.pow < maxPower:
                return left
            tok.consume()
            # Don't add 1 here: we want to parse 2^3^4 as 2^(3^4)
            newLeft = left ** parseMain(tok, Power.pow)
            return parseConsequent(tok, newLeft, maxPower)
        case _:
            # This isn't a consequent, e.g. a close-paren ")".
            return left


def parseInitial(tok: Tokenizer) -> float:
    match tok.consume():
        case ("const", string):
            return float(string)
        case ("punct", "("):
            p = parseMain(tok, Power.top)
            tok.consumePunct(")")
            return p
        case ("eof", ""):
            raise ParseError("Unexpected end of file")
        case token:
            raise ParseError(f"Invalid token here: {token}")


if __name__ == "__main__":
    while True:
        string = input("Expr: ")
        print(parse(string))
