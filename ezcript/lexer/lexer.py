from re import match

from ezcript.tokens import (
    Token,
    TokenType,
)


class Lexer:
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ''
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()

    def next_token(self) -> Token:
        self._skip_whitespace()

        # Getting the tokens
        if match(r'^%$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.PERCENTEQUAL)
            token = Token(TokenType.PERCENT, self._character)
        elif match(r'^\($', self._character):
            token = Token(TokenType.LPAREN, self._character)
        elif match(r'^\)$', self._character):
            token = Token(TokenType.RPAREN, self._character)
        elif match(r'^\*$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.STAREQUAL)
            elif self._peek_character() == '*':
                token = self._make_two_character_token(TokenType.DOUBLESTAR)
            elif self._peek_character() == '*':
                if self._peek_character(2) == '=':
                    token = self._make_three_character_token(
                        TokenType.DOUBLESTAREQUAL)
            else:
                token = Token(TokenType.STAR, self._character)
        elif match(r'^\+$', self._character):
            if self._peek_character() == '+':
                token = self._make_two_character_token(TokenType.DOUBLEPLUS)
            elif self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.PLUSEQUAL)
            else:
                token = Token(TokenType.PLUS, self._character)
        elif match(r'^,$', self._character):
            token = Token(TokenType.COMMA, self._character)
        elif match(r'^-$', self._character):
            if self._peek_character() == '-':
                token = self._make_two_character_token(TokenType.DOUBLEMINUS)
            elif self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.MINEQUAL)
            else:
                token = Token(TokenType.MINUS, self._character)
        elif match(r'^\.$', self._character):
            if self._peek_character() == '.':
                if self._peek_character(2) == '.':
                    token = self._make_three_character_token(
                        TokenType.ELLIPSIS)
            else:
                token = Token(TokenType.DOT, self._character)
        elif match(r'^\/$', self._character):
            if self._peek_character() == '/':
                if self._peek_character(2) == '=':
                    token = self._make_three_character_token(
                        TokenType.DOUBLESLASHEQUAL)
                else:
                    token = Token(TokenType.DOUBLESLASH, self._character)
            elif self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.SLASHEQUAL)
            else:
                token = Token(TokenType.SLASH, self._character)
        elif match(r'^:$', self._character):
            token = Token(TokenType.COLON, self._character)
        elif match(r'^<$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.LESSEQUAL)
            else:
                token = Token(TokenType.LESS, self._character)
        elif match(r'^=$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.EQEQUAL)
            else:
                token = Token(TokenType.EQUAL, self._character)
        elif match(r'^>$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.GREATEREQUAL)
            else:
                token = Token(TokenType.GREATER, self._character)
        elif match(r'^\[$', self._character):
            token = Token(TokenType.LBRACKET, self._character)
        elif match(r'^\]$', self._character):
            token = Token(TokenType.RBRACKET, self._character)
        elif match(r'^\{$', self._character):
            token = Token(TokenType.LBRACE, self._character)
        elif match(r'^\}$', self._character):
            token = Token(TokenType.RBRACE, self._character)
        elif match(r'^!$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.NOTEQUAL)
            else:
                token = Token(TokenType.NEGATION, self._character)
        else:
            token = Token(TokenType.OP, self._character)
        self._read_character()

        return token

    def _make_three_character_token(self, token_type: TokenType) -> Token:
        first = self._character
        self._read_character()
        second = self._character
        self._read_character()
        third = self._character

        return Token(token_type, f'{first}{second}{third}')

    def _make_two_character_token(self, token_type: TokenType) -> Token:
        prefix = self._character
        self._read_character()
        suffix = self._character

        return Token(token_type, f'{prefix}{suffix}')

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def _peek_character(self, skip: int = 1) -> str:
        if self._read_position >= len(self._source):
            return ''

        return self._source[self._read_position] if skip == 1\
            else self._source[self._read_position + (skip - 1)]

    def _skip_whitespace(self) -> None:
        while match(r'^\s$', self._character):
            self._read_character()
