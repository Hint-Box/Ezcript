from re import match

from utils.decorators import (
    one_char_token,
    two_char_token,
    three_char_token,
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

    @one_char_token(self._source)
    def get_one_char_token(self, token_type: TokenType, c1: str) -> Token:
        return Token(token_type, c1)

    @two_char_token(self._source)
    def get_two_char_token(self, token_type: TokenType, c1: str,
                           c2: str) -> Token:
        literal = c1 + c2
        return Token(token_type, literal)

    @three_char_token(self._source)
    def get_three_char_token(self, token_type: TokenType, c1: str, c2: str,
                             c3: str) -> Token:
        literal = c1 + c2 + c3
        return Token(token_type, literal)

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
