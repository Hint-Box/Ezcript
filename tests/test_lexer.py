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
            and
            or
            not
            is
            endif
            while
            do
            break
            endwhile
            for
            each
            in
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
        for i in range(26):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.KEYWORD, "if"),
            Token(TokenType.KEYWORD, "then"),
            Token(TokenType.KEYWORD, "elseif"),
            Token(TokenType.KEYWORD, "else"),
            Token(TokenType.KEYWORD, "and"),
            Token(TokenType.KEYWORD, "or"),
            Token(TokenType.KEYWORD, "not"),
            Token(TokenType.KEYWORD, "is"),
            Token(TokenType.KEYWORD, "endif"),
            Token(TokenType.KEYWORD, "while"),
            Token(TokenType.KEYWORD, "do"),
            Token(TokenType.KEYWORD, "break"),
            Token(TokenType.KEYWORD, "endwhile"),
            Token(TokenType.KEYWORD, "for"),
            Token(TokenType.KEYWORD, "each"),
            Token(TokenType.KEYWORD, "in"),
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

    def test_set_statement(self) -> None:
        source: str = """
            set num_1
            set var
            set otra_var
        """
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(6):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.IDENTIFIER, "num_1"),
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.IDENTIFIER, "var"),
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.IDENTIFIER, "otra_var"),
        ]

        assert expected_tokens == tokens

    def test_string(self) -> None:
        source: str = '''
            "text"
            \'coso\'
            "Texto largo ajam"
        '''
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(3):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.STRING, 'text'),
            Token(TokenType.STRING, 'coso'),
            Token(TokenType.STRING, 'Texto largo ajam'),
        ]

        assert expected_tokens == tokens

    def test_assigment(self) -> None:
        source: str = """
            set var
            var = 1
            set num = 5
            set result = 6 + 6
        """
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(15):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.IDENTIFIER, "var"),
            Token(TokenType.IDENTIFIER, "var"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.IDENTIFIER, "num"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.IDENTIFIER, "result"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.NUMBER, "6"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "6"),
        ]

        assert expected_tokens == tokens

    def test_eof(self) -> None:
        source: str = "5"
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.EOF, ""),
        ]

        assert expected_tokens == tokens

    def test_if_expression(self) -> None:
        source: str = """
            if 5 < 10 then
                print("si")
            elseif 10 == 10 then
                print("si también")
            else then
                print("no")
            endif

            set resultado = if true then
                print("ostras")
            endif
        """
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(36):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.KEYWORD, "if"),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.LESS, "<"),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.KEYWORD, "then"),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, "si"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.KEYWORD, "elseif"),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.EQEQUAL, "=="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.KEYWORD, "then"),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, "si también"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.KEYWORD, "else"),
            Token(TokenType.KEYWORD, "then"),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, "no"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.KEYWORD, "endif"),
            Token(TokenType.KEYWORD, "set"),
            Token(TokenType.IDENTIFIER, "resultado"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.KEYWORD, "if"),
            Token(TokenType.BOOLEAN, "true"),
            Token(TokenType.KEYWORD, "then"),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.STRING, "ostras"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.KEYWORD, "endif"),
        ]

        assert expected_tokens == tokens
