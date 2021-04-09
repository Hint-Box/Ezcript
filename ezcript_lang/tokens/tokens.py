from enum import (
    Enum,
    auto,
    unique,
)
from typing import (NamedTuple)


@unique
class TokenType(Enum):
    """Define all the token types that the language have"""

    ENDMARKER = auto()
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COLON = auto()
    COMMA = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LESS = auto()
    GREATER = auto()
    NEGATION = auto()
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
    DOUBLESTAREQUAL = auto()
    DOUBLESLASH = auto()
    DOUBLESLASHEQUAL = auto()
    RARROW = auto()  # this => not this ->
    ELLIPSIS = auto()
    ILLEGAL = auto()
    COMMENT = auto()
    ERRORTOKEN = auto()
    EOF = auto()


class Token(NamedTuple):
    """The Token created with a token type and it literal"""
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type {self.token_type} [Literal {self.literal}]'


def lookup_token_type(literal: str) -> TokenType:
    keywords: dict[str:TokenType] = {
        "set": TokenType.KEYWORD,
        "const": TokenType.KEYWORD,
        "true": TokenType.BOOLEAN,
        "false": TokenType.BOOLEAN,
        "if": TokenType.KEYWORD,
        "then": TokenType.KEYWORD,
        "elseif": TokenType.KEYWORD,
        "else": TokenType.KEYWORD,
        "and": TokenType.KEYWORD,
        "or": TokenType.KEYWORD,
        "not": TokenType.KEYWORD,
        "is": TokenType.KEYWORD,
        "while": TokenType.KEYWORD,
        "do": TokenType.KEYWORD,
        "break": TokenType.KEYWORD,
        "for": TokenType.KEYWORD,
        "each": TokenType.KEYWORD,
        "in": TokenType.KEYWORD,
        "makeFunc": TokenType.KEYWORD,
        "return": TokenType.KEYWORD,
        "class": TokenType.KEYWORD,
        "inherit": TokenType.KEYWORD,
        "interface": TokenType.KEYWORD,
        "null": TokenType.NULL,
        "end": TokenType.KEYWORD,
    }

    return keywords.get(literal, TokenType.IDENTIFIER)
