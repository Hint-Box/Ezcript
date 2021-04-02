from functools import wraps

from ezcript.tokens import (
    Token,
    TokenType,
)


def one_char_token(func: Token, c1: str) -> Token:
    """
    Decorator that return one character token from the function decorated

    :param func: The function that return the token
    :type func: Token
    :param c1: The character
    :type c1: str
    :return: Return the token that match with the character
    :rtype: Token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if c1 == '%':
            return func(TokenType.PERCENT, c1)
        elif c1 == '(':
            return func(TokenType.LPAREN, c1)
        elif c1 == ')':
            return func(TokenType.RPAREN, c1)
        elif c1 == '*':
            return func(TokenType.STAR, c1)
        elif c1 == '+':
            return func(TokenType.PLUS, c1)
        elif c1 == ',':
            return func(TokenType.COMMA, c1)
        elif c1 == '-':
            return func(TokenType.MINUS, c1)
        elif c1 == '.':
            return func(TokenType.DOT, c1)
        elif c1 == '/':
            return func(TokenType.SLASH, c1)
        elif c1 == ':':
            return func(TokenType.COLON, c1)
        elif c1 == '<':
            return func(TokenType.LESS, c1)
        elif c1 == '=':
            return func(TokenType.EQUAL, c1)
        elif c1 == '>':
            return func(TokenType.GRATER, c1)
        elif c1 == '[':
            return func(TokenType.LBRACKET, c1)
        elif c1 == ']':
            return func(TokenType.RBRACKET, c1)
        elif c1 == '{':
            return func(TokenType.LBRACE, c1)
        elif c1 == '}':
            return func(TokenType.RBRACE, c1)
        elif c1 == '!':
            return func(TokenType.NEGATION, c1)
        else:
            return func(TokenType.OP, c1)

    return wrapper


def two_char_token(func: Token, c1: str, c2: str) -> Token:
    """
    Decorator that return two character token from the function decorated

    :param func: The function that return the token
    :type func: Token
    :param c1: The first character
    :type c1: str
    :param c2: The second character
    :type c2: str
    :return: Return the token that match with the two characters
    :rtype: Token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if c1 == '!':
            if c2 == '=':
                return func(TokenType.NOTEQUAL, c1, c2)
        elif c1 == '%':
            if c2 == '=':
                return func(TokenType.PERCENTEQUAL, c1, c2)
        elif c1 == '*':
            if c2 == '*':
                return func(TokenType.DOUBLESTAR, c1, c2)
            elif c2 == '=':
                return func(TokenType.STAREQUAL, c1, c2)
        elif c1 == '+':
            if c2 == '=':
                return func(TokenType.PLUSEQUAL, c1, c2)
            elif c2 == '+':
                return func(TokenType.DOUBLEPLUS, c1, c2)
        elif c1 == '-':
            if c2 == '=':
                return func(TokenType.MINEQUAL, c1, c2)
            elif c2 == '-':
                return func(TokenType.DOUBLEMINUS, c1, c2)
        elif c1 == '/':
            if c2 == '/':
                return func(TokenType.DOUBLESLASH, c1, c2)
            elif c2 == '=':
                return func(TokenType.SLASHEQUAL, c1, c2)
        elif c1 == '<':
            if c2 == '=':
                return func(TokenType.LESSEQUAL, c1, c2)
        elif c1 == '=':
            if c2 == '=':
                return func(TokenType.EQEQUAL, c1, c2)
            elif c2 == '>':
                return func(TokenType.RARROW, c1, c2)
        elif c1 == '>':
            if c2 == '=':
                return func(TokenType.GREATEREQUAL, c1, c2)
        else:
            return func(TokenType.OP, c1, c2)

    return wrapper


def three_char_token(func: Token, c1: str, c2: str, c3: str) -> Token:
    """
    Decorator that return a three characters token from the function decorated

    :param func: The function that return the token
    :type func: Token
    :param c1: The first character
    :type c1: str
    :param c2: The second character
    :type c2: str
    :param c3: The third character
    :type c3: str
    :return: Return the token that match with the character
    :rtype: Token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if c1 == '*':
            if c2 == '*':
                if c3 == '=':
                    return func(TokenType.DOUBLESTAREQUAL, c1, c2, c3)
        elif c1 == '.':
            if c2 == '.':
                if c3 == '.':
                    return func(TokenType.ELLIPSIS, c1, c2, c3)
        elif c1 == '/':
            if c2 == '/':
                if c3 == '=':
                    return func(TokenType.DOUBLESLASHEQUAL, c1, c2, c3)
        else:
            return func(TokenType.OP, c1, c2, c3)

    return wrapper
