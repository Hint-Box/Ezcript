from ezcript.lexer import Lexer
from ezcript.tokens import (
    Token,
    TokenType,
)


class TestLexer:
    def test_one_char_token(self) -> None:
        source: str = "=%()*+,-./:<>[]{}!"
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.EQUAL, "="),
            Token(TokenType.PERCENT, "%"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.STAR, "*"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DOT, "."),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.LESS, "<"),
            Token(TokenType.GREATER, ">"),
            Token(TokenType.LBRACKET, "["),
            Token(TokenType.RBRACKET, "]"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.NEGATION, "!"),
        ]

        assert expected_tokens == tokens
