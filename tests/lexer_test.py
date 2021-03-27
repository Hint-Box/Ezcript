from unittest import TestCase
from typing import List

from fol.token import (
    Token,
    TokenType,
)
from fol.lexer import Lexer


class LexerTest(TestCase):
    def test_illegal(self) -> None:
        source: str = "¿¡@;"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, "¿"),
            Token(TokenType.ILLEGAL, "¡"),
            Token(TokenType.ILLEGAL, "@"),
            Token(TokenType.ILLEGAL, ";"),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_one_character_operator(self) -> None:
        source: str = "=+-/*<>!"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

            expected_tokens: List[Token] = [
                Token(TokenType.ASSIGN, "="),
                Token(TokenType.PLUS, "+"),
                Token(TokenType.MINUS, "-"),
                Token(TokenType.DIVISION, "/"),
                Token(TokenType.MULTIPLICATION, "*"),
                Token(TokenType.LT, "<"),
                Token(TokenType.GT, ">"),
                Token(TokenType.NEGATION, "!"),
            ]

        self.assertEqual(tokens, expected_tokens)

    def test_line_break(self) -> None:
        source: str = """set five = 5
                        set six = 6
                        set seven = 7
                        set ocho = 8
                        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(21):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.SET, "set", 1),
            Token(TokenType.IDENTIFIER, "five", 1),
            Token(TokenType.ASSIGN, "=", 1),
            Token(TokenType.INTEGER, "5", 1),
            Token(TokenType.EOL, "", 1),
            Token(TokenType.SET, "set", 2),
            Token(TokenType.IDENTIFIER, "six", 2),
            Token(TokenType.ASSIGN, "=", 2),
            Token(TokenType.INTEGER, "6", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.SET, "set", 3),
            Token(TokenType.IDENTIFIER, "seven", 3),
            Token(TokenType.ASSIGN, "=", 3),
            Token(TokenType.INTEGER, "7", 3),
            Token(TokenType.EOL, "", 3),
            Token(TokenType.SET, "set", 4),
            Token(TokenType.IDENTIFIER, "eight", 4),
            Token(TokenType.ASSIGN, "=", 4),
            Token(TokenType.INTEGER, "8", 4),
            Token(TokenType.EOL, "", 4),
            Token(TokenType.EOF, "", 5),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_eol_eof(self) -> None:
        source: str = "+"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source) + 2):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.EOL, ""),
            Token(TokenType.EOF, ""),
        ]

        self.assertEqual(tokens, expected_tokens)

        def test_dot(self) -> None:
            source: str = "."
            lexer: Lexer = Lexer(source)

            tokens: List[Token] = []
            for i in range(len(source) + 2):
                tokens.append(lexer.next_token())

            expected_tokens: List[Token] = [
                Token(TokenType.DOT, ".", 1),
                Token(TokenType.EOL, "", 1),
                Token(TokenType.EOF, "", 2),
            ]

            self.assertEqual(tokens, expected_tokens)

    def test_delimeters(self) -> None:
        source: str = "(){}[],"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.LBRACKET, "["),
            Token(TokenType.RBRACKET, "]"),
            Token(TokenType.COMMA, ","),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_assigment(self) -> None:
        source: str = "set five = 5"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(6):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.SET, "set", 1),
            Token(TokenType.IDENTIFIER, "five", 1),
            Token(TokenType.ASSIGN, "=", 1),
            Token(TokenType.INTEGER, "5", 1),
            Token(TokenType.EOL, "", 1),
            Token(TokenType.EOF, "", 2),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_function_statement(self) -> None:
        source: str = """
            makeFunc sum(x, y) then
                x + y
            endfunc
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.FUNCTION, "makeFunc", 1),
            Token(TokenType.IDENTIFIER, "sum", 1),
            Token(TokenType.LPAREN, "(", 1),
            Token(TokenType.IDENTIFIER, "x", 1),
            Token(TokenType.COMMA, ",", 1),
            Token(TokenType.IDENTIFIER, "y", 1),
            Token(TokenType.RPAREN, ")", 1),
            Token(TokenType.THEN, "then", 1),
            Token(TokenType.EOL, "", 1),
            Token(TokenType.IDENTIFIER, "x", 2),
            Token(TokenType.PLUS, "+", 2),
            Token(TokenType.IDENTIFIER, "y", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.ENDFUNC, "endfunc", 3),
            Token(TokenType.EOL, "", 3),
            Token(TokenType.EOF, "", 4),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_function_declaration(self) -> None:
        source: str = """
            set sum = (x, y) then
                x + y
            endfunc
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.SET, "set", 1),
            Token(TokenType.IDENTIFIER, "sum", 1),
            Token(TokenType.EQ, "=", 1),
            Token(TokenType.LPAREN, "(", 1),
            Token(TokenType.IDENTIFIER, "x", 1),
            Token(TokenType.COMMA, ",", 1),
            Token(TokenType.IDENTIFIER, "y", 1),
            Token(TokenType.RPAREN, ")", 1),
            Token(TokenType.THEN, "then", 1),
            Token(TokenType.EOL, "", 1),
            Token(TokenType.IDENTIFIER, "x", 2),
            Token(TokenType.PLUS, "+", 2),
            Token(TokenType.IDENTIFIER, "y", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.ENDFUNC, "endfunc", 3),
            Token(TokenType.EOL, "", 3),
            Token(TokenType.EOF, "", 4),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_return_statement(self) -> None:
        source: str = """
            set sum = (x, y) then
                return x + y
            endfunc

            if 5 == 5 then
                return 5
            endif
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.SET, "set", 1),
            Token(TokenType.IDENTIFIER, "sum", 1),
            Token(TokenType.EQ, "=", 1),
            Token(TokenType.LPAREN, "(", 1),
            Token(TokenType.IDENTIFIER, "x", 1),
            Token(TokenType.COMMA, ",", 1),
            Token(TokenType.IDENTIFIER, "y", 1),
            Token(TokenType.RPAREN, ")", 1),
            Token(TokenType.THEN, "then", 1),
            Token(TokenType.EOL, "", 1),
            Token(TokenType.RETURN, "return", 2),
            Token(TokenType.IDENTIFIER, "x", 2),
            Token(TokenType.PLUS, "+", 2),
            Token(TokenType.IDENTIFIER, "y", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.ENDFUNC, "endfunc", 3),
            Token(TokenType.EOL, "", 3),
            Token(TokenType.IF, "if", 5),
            Token(TokenType.INTEGER, "5", 5),
            Token(TokenType.EQ, "==", 5),
            Token(TokenType.INTEGER, "5", 5),
            Token(TokenType.EOL, "", 5),
            Token(TokenType.RETURN, "return", 6),
            Token(TokenType.INTEGER, "5", 6),
            Token(TokenType.EOL, "", 6),
            Token(TokenType.ENDIF, "endif", 7),
            Token(TokenType.EOL, "", 7),
            Token(TokenType.EOF, "", 8),
        ]

    def test_function_call(self) -> None:
        source: str = "set result = sum(2, 3);"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(10):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.SET, "set", 1),
            Token(TokenType.IDENTIFIER, "result", 1),
            Token(TokenType.ASSIGN, "=", 1),
            Token(TokenType.IDENTIFIER, "sum", 1),
            Token(TokenType.LPAREN, "(", 1),
            Token(TokenType.INTEGER, "2", 1),
            Token(TokenType.COMMA, ",", 1),
            Token(TokenType.INTEGER, "3", 1),
            Token(TokenType.RPAREN, ")", 1),
            Token(TokenType.EOL, "", 1),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_control_statment(self) -> None:
        source: str = """
            if 5 < 10 then
                return true
            else
                return false
            endif
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IF, "if", 1),
            Token(TokenType.INTEGER, "5", 1),
            Token(TokenType.LT, "<", 1),
            Token(TokenType.INTEGER, "10", 1),
            Token(TokenType.THEN, "then", 1),
            Token(TokenType.EOL, "", 1),
            Token(TokenType.RETURN, "return", 2),
            Token(TokenType.TRUE, "true", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.ELSE, "else", 3),
            Token(TokenType.EOL, "", 3),
            Token(TokenType.RETURN, "return", 4),
            Token(TokenType.FALSE, "false", 4),
            Token(TokenType.EOL, "", 4),
            Token(TokenType.ENDIF, "enfif", 5),
            Token(TokenType.EOL, "", 5),
            Token(TokenType.EOF, "", 6),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_two_character_operator(self) -> None:
        source: str = """10 == 10;
                         10 != 9;
                         10 >= 4;
                         0 <= 11;
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INTEGER, "10", 1),
            Token(TokenType.EQ, "==", 1),
            Token(TokenType.INTEGER, "10", 1),
            Token(TokenType.EOL, "", 1),
            Token(TokenType.INTEGER, "10", 2),
            Token(TokenType.NOT_EQ, "!=", 2),
            Token(TokenType.INTEGER, "9", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.INTEGER, "10", 3),
            Token(TokenType.GE, ">=", 3),
            Token(TokenType.INTEGER, "4", 3),
            Token(TokenType.EOL, "", 3),
            Token(TokenType.INTEGER, "0", 4),
            Token(TokenType.LE, "<=", 4),
            Token(TokenType.INTEGER, "11", 4),
            Token(TokenType.EOL, "", 4),
            Token(TokenType.EOF, "", 5),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_identifier_with_numbers(self) -> None:
        source: str = """set num_1 = 1"""
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.SET, "set", 1),
            Token(TokenType.IDENTIFIER, "num_1", 1),
            Token(TokenType.ASSIGN, "=", 1),
            Token(TokenType.INTEGER, "1", 1),
            Token(TokenType.EOL, "", 1),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_assigment_with_floats(self) -> None:
        source: str = """
            set float_num = 1.5
            set num = 4.2
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(11):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.SET, "set", 2),
            Token(TokenType.IDENTIFIER, "float_num", 2),
            Token(TokenType.ASSIGN, "=", 2),
            Token(TokenType.FLOAT, "1.5", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.SET, "set", 2),
            Token(TokenType.IDENTIFIER, "num", 2),
            Token(TokenType.ASSIGN, "=", 2),
            Token(TokenType.FLOAT, "4.2", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.EOF, "", 3),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_string(self) -> None:
        source: str = """
            "foo";
            \'bar\';
            "Mucho texto xddd";
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(6):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, "foo", 2),
            Token(TokenType.EOL, "", 2),
            Token(TokenType.STRING, "bar", 3),
            Token(TokenType.EOL, "", 3),
            Token(TokenType.STRING, "Mucho texto xddd", 4),
            Token(TokenType.EOL, "", 4),
        ]

        self.assertEqual(tokens, expected_tokens)
