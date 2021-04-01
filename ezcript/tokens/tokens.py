from enum import (
    Enum,
    auto,
    unique,
)


@unique
class TokenType(Enum):
    """Define all the token types that the language have"""

    ENDMARKER = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = ()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COLON = auto()
    COMMA = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LESS = auto()
    GRATER = auto()
    EQUAL = auto()
    DOT = auto()
    PERCENT = auto()
    EQEQUAL = auto()
    NOTEQUAL = auto()
    LESSEQUAL = auto()
    GREATEREQUAL = auto()
    DOUBLESTAR = auto()
    DOUBLEPLUS = auto()
    DOUBLEMINUS = auto()
    PLUSEQUAL = auto()
    MINEQUAL = auto()
    STAREQUAL = auto()
    SLASHEQUAL = auto()
    PERCENTEQUAL = auto()
    DOUBLESLASH = auto()
    DOUBLESLASHEQUAL = auto()
    RARROW = auto()  # this => not this ->
    ELLIPSIS = auto()
    OP = auto()
    TYPE_IGNORE = auto()
    TYPE_COMMENT = auto()
    ERRORTOKEN = auto()
    N_TOKENS = 63

    ISEOF = ENDMARKER
    ISWHITESPACE = ENDMARKER\
        or NEWLINE\
        or INDENT\
        or DEDENT
