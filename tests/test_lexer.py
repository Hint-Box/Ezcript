from ezcript.lexer import Lexer
from ezcript.tokens import (
    Token,
    TokenType,
)


class TestLexer:
    def test_illegal_char(self) -> None:
        source: str = "@~¿¡ºªçÇ"
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.ILLEGAL, "@"),
            Token(TokenType.ILLEGAL, "~"),
            Token(TokenType.ILLEGAL, "¿"),
            Token(TokenType.ILLEGAL, "¡"),
            Token(TokenType.ILLEGAL, "º"),
            Token(TokenType.ILLEGAL, "ª"),
            Token(TokenType.ILLEGAL, "ç"),
            Token(TokenType.ILLEGAL, "Ç"),
        ]

        assert expected_tokens == tokens

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

    def test_two_char_token(self) -> None:
        source: str = """
            2 ** 3
            num1 *= 1
            4++
            num2 += 1
            4--
            num3 -= 1
            23 // 2
            num4 /= 1
            3 <= 4
            5 == 5
            5 >= 1
            true != false
        """
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(34):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.DOUBLESTAR, "**"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.IDENTIFIER, "num1"),
            Token(TokenType.STAREQUAL, "*="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.NUMBER, "4"),
            Token(TokenType.DOUBLEPLUS, "++"),
            Token(TokenType.IDENTIFIER, "num2"),
            Token(TokenType.PLUSEQUAL, "+="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.NUMBER, "4"),
            Token(TokenType.DOUBLEMINUS, "--"),
            Token(TokenType.IDENTIFIER, "num3"),
            Token(TokenType.MINEQUAL, "-="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.NUMBER, "23"),
            Token(TokenType.DOUBLESLASH, "//"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.IDENTIFIER, "num4"),
            Token(TokenType.SLASHEQUAL, "/="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.LESSEQUAL, "<="),
            Token(TokenType.NUMBER, "4"),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.EQEQUAL, "=="),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.GREATEREQUAL, ">="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.BOOLEAN, "true"),
            Token(TokenType.NOTEQUAL, "!="),
            Token(TokenType.BOOLEAN, "false"),
        ]

        assert expected_tokens == tokens

    def test_booleans(self) -> None:
        source: str = """
            true == true
            false == false
            true != false
        """
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(9):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.BOOLEAN, "true"),
            Token(TokenType.EQEQUAL, "=="),
            Token(TokenType.BOOLEAN, "true"),
            Token(TokenType.BOOLEAN, "false"),
            Token(TokenType.EQEQUAL, "=="),
            Token(TokenType.BOOLEAN, "false"),
            Token(TokenType.BOOLEAN, "true"),
            Token(TokenType.NOTEQUAL, "!="),
            Token(TokenType.BOOLEAN, "false"),
        ]

        assert expected_tokens == tokens

    def test_keywords(self) -> None:
        source: str = """
            set
            if
            then
            elseif
            else
            endif
            while
            do
            break
            endwhile
            for
            each
            endfor
            makeFunc
            return
            endfunc
            class
            endclass
            inherit
            interface
            endinterface
        """
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(21):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.KEYWORD, "if"),
            Token(TokenType.KEYWORD, "then"),
            Token(TokenType.KEYWORD, "elseif"),
            Token(TokenType.KEYWORD, "else"),
            Token(TokenType.KEYWORD, "endif"),
            Token(TokenType.KEYWORD, "while"),
            Token(TokenType.KEYWORD, "do"),
            Token(TokenType.KEYWORD, "break"),
            Token(TokenType.KEYWORD, "endwhile"),
            Token(TokenType.KEYWORD, "for"),
            Token(TokenType.KEYWORD, "each"),
            Token(TokenType.KEYWORD, "endfor"),
            Token(TokenType.KEYWORD, "makeFunc"),
            Token(TokenType.KEYWORD, "return"),
            Token(TokenType.KEYWORD, "endfunc"),
            Token(TokenType.KEYWORD, "class"),
            Token(TokenType.KEYWORD, "endclass"),
            Token(TokenType.KEYWORD, "inherit"),
            Token(TokenType.KEYWORD, "interface"),
            Token(TokenType.KEYWORD, "endinterface"),
        ]

        assert expected_tokens == tokens
