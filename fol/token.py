from enum import (
    Enum,
    unique,
    auto
)
from typing import (
    Dict,
    NamedTuple,
)


@unique
class TokenType(Enum):
    """Define all the tokens types that the language have"""

    String = auto()
    Integer = auto()
    Float = auto()
    Boolean = auto()
    false = auto()
    true = auto()
    Array = auto()
    Object = auto()
    Tuple = auto()
    Null = auto()
    Set = auto()
    Identifier = auto()
    If = auto()
    Endif = auto()
    Elseif = auto()
    Else = auto()
    And = auto()
    Or = auto()
    While = auto()
    Endwhile = auto()
    Do = auto()
    For = auto()
    Each = auto()
    Endfor = auto()
    MakeFunc = auto()
    Return = auto()
    Endfunc = auto()
    Class = auto()
    Endclass = auto()
    Then = auto()
    Interface = auto()
    Endinterface = auto()
    Minus = auto()
    Negation = auto()
    LParen = auto()
    RParen = auto()
    LBrace = auto()
    RBrace = auto()
    LBracket = auto()
    RBracket = auto()
    Plus = auto()
    Multiplication = auto()
    Division = auto()
    Assign = auto()
    LT = auto() # <
    GT = auto() # >
    LE = auto() # <=
    GE = auto() # >=
    Equals = auto()
    NotEq = auto()
    Dot = auto()
    Comma = auto()
    TPoints = auto() # :
    LArrow = auto()
    Illegal = auto()
    Comments = auto() # //
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
    keywords: Dict[str, TokenType] = {
        "set": TokenType.Set,
        "false": TokenType.false,
        "true": TokenType.false,
        "null": TokenType.Null,
        "if": TokenType.If,
        "elseif": TokenType.Elseif,
        "else": TokenType.Else,
        "endif": TokenType.Endif,
        "and": TokenType.And,
        "or": TokenType.Or,
        "while": TokenType.While,
        "do": TokenType.Do,
        "endwhile": TokenType.Endwhile,
        "for": TokenType.For,
        "each": TokenType.Each,
        "endfor":  TokenType.Endfor,
        "makeFunc": TokenType.MakeFunc,
        "then": TokenType.Then,
        "return": TokenType.Return,
        "endfunc": TokenType.Endfunc,
        "class": TokenType.Class,
        "endclass": TokenType.Endclass,
        "interface": TokenType.Interface,
        "endinterface": TokenType.Endinterface,
    }

    return keywords.get(literal, TokenType.Identifier)
