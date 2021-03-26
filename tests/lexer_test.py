from unittest import TestCase
from typing import List

from fol.token import (
    Token,
    TokenType,
)
from fol.lexer import Lexer


class LexerTest(TestCase):

    def test_illegal(self) -> None:
        source: str = "¿¡@"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.Illegal, "¿"),
            Token(TokenType.Illegal, "¡"),
            Token(TokenType.Illegal, "@"),
        ]

        self.assertEquals(tokens, expected_tokens)
