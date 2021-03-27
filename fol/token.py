"""
This module create two classes, TokenType and Token for create a Token,
you have to pass it the token type, the literal and  the line where the
token is, just for the case an error occurs.

Classes:

    TokenType(Enum)
    Token(NamedTuple)

Function:

    lookup_token_type(literal: str) -> TokenType
"""

from enum import Enum, unique, auto
from typing import (
    Dict,
    NamedTuple,
)


@unique
class TokenType(Enum):
    """Define all the tokens types that the language have"""

    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    FALSE = auto()
    TRUE = auto()
    ARRAY = auto()
    OBJECT = auto()
    TUPLE = auto()
    NULL = auto()
    SET = auto()
    IDENTIFIER = auto()
    IF = auto()
    ENDIF = auto()
    ELSEIF = auto()
    ELSE = auto()
    AND = auto()
    OR = auto()
    WHILE = auto()
    ENDWHILE = auto()
    DO = auto()
    FOR = auto()
    EACH = auto()
    ENDFOR = auto()
    FUNCTION = auto()
    RETURN = auto()
    ENDFUNC = auto()
    CLASS = auto()
    ENDCLASS = auto()
    THEN = auto()
    INTERFACE = auto()
    ENDINTERFACE = auto()
    MINUS = auto()
    NEGATION = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    PLUS = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    ASSIGN = auto()
    LT = auto()  # <
    GT = auto()  # >
    LE = auto()  # <=
    GE = auto()  # >=
    EQ = auto()  # ==
    NOT_EQ = auto()  # !=
    DOT = auto()
    COMMA = auto()
    TPOINTS = auto()  # :
    LARROW = auto()
    ILLEGAL = auto()
    COMMENTS = auto()  # //
    EOL = auto()
    EOF = auto()


class Token(NamedTuple):
    """Define a Token. Everytime a token is created, the token you have to pass it
    three arguments, which are:

        token_type: TokenType
        literal: str
        line: int (default=1)"""

    token_type: TokenType
    literal: str
    line: int = 1

    def __str__(self) -> str:
        return f"Type {self.token_type}, Literal {self.literal}, Line {self.line}"


def lookup_token_type(literal: str) -> TokenType:
    """
    This function take the literal of the token and return the TokenType
    that matches with the literal.

    :param literal: The token itself
    :type literal: str
    :return: The TokenType that matches with the literal
    :rtype: TokenType
    """
    keywords: Dict[str, TokenType] = {
        "set": TokenType.SET,
        "false": TokenType.FALSE,
        "true": TokenType.TRUE,
        "null": TokenType.NULL,
        "if": TokenType.IF,
        "elseif": TokenType.ELSEIF,
        "else": TokenType.ELSE,
        "endif": TokenType.ENDIF,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "while": TokenType.WHILE,
        "do": TokenType.DO,
        "endwhile": TokenType.ENDWHILE,
        "for": TokenType.FOR,
        "each": TokenType.EACH,
        "endfor": TokenType.ENDFOR,
        "makeFunc": TokenType.FUNCTION,
        "then": TokenType.THEN,
        "return": TokenType.RETURN,
        "endfunc": TokenType.ENDFUNC,
        "class": TokenType.CLASS,
        "endclass": TokenType.ENDCLASS,
        "interface": TokenType.INTERFACE,
        "endinterface": TokenType.ENDINTERFACE,
    }

    return keywords.get(literal, TokenType.IDENTIFIER)
