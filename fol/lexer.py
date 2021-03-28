from re import match

from fol.token import (
    Token,
    TokenType,
    lookup_token_type,
)


class Lexer:
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ""
        self._read_position: int = 0
        self._position: int = 0
        self._line: int = 1

        self._read_character()

    def next_token(self) -> Token:
        self._skip_whitespace()
        # Token '='
        if match(r"^=$", self._character):
            if self._peek_character() == "=":
                token = self._make_two_character_token(TokenType.EQ)
            else:
                token = Token(TokenType.ASSIGN, self._character, self._line)
        # Token '+'
        elif match(r"^\+$", self._character):
            token = Token(TokenType.PLUS, self._character, self._line)
        # Token '-'
        elif match(r"^-$", self._character):
            token = Token(TokenType.MINUS, self._character, self._line)
        # Token '*'
        elif match(r"^\*$", self._character):
            token = Token(TokenType.MULTIPLICATION, self._character,
                          self._line)
        # Token '/'
        elif match(r"^\/$", self._character):
            if self._peek_character() == "/":
                token = self._make_two_character_token(TokenType.COMMENTS)
            token = Token(TokenType.DIVISION, self._character, self._line)
        # Token EOL
        elif match(r"^$", self._character) and self._peek_character() != "":
            token = Token(TokenType.EOL, self._character, self._line)
        # Token EOF
        elif match(r"^$", self._character):
            token = Token(TokenType.EOF, self._character, self._line)
        # Token '('
        elif match(r"^\($", self._character):
            token = Token(TokenType.LPAREN, self._character, self._line)
        # Token ')'
        elif match(r"^\)$", self._character):
            token = Token(TokenType.RPAREN, self._character, self._line)
        # Token '{'
        elif match(r"^\{$", self._character):
            token = Token(TokenType.LBRACE, self._character, self._line)
        # Token '}'
        elif match(r"^\}$", self._character):
            token = Token(TokenType.RBRACE, self._character, self._line)
        # Token '['
        elif match(r"^\[$", self._character):
            token = Token(TokenType.LBRACKET, self._character, self._line)
        # Token ']'
        elif match(r"^\]$", self._character):
            token = Token(TokenType.RBRACKET, self._character, self._line)
        # Token ','
        elif match(r"^\,$", self._character):
            token = Token(TokenType.COMMA, self._character, self._line)
        # Token '.'
        elif match(r"^\.$", self._character):
            token = Token(TokenType.DOT, self._character, self._line)
        # Token ':0
        elif match(r"^:$", self._character):
            token = Token(TokenType.COLON, self._character, self._line)
        # Token '<'
        elif match(r"^<$", self._character):
            if self._peek_character() == "=":
                token = self._make_two_character_token(TokenType.LE)
            else:
                token = Token(TokenType.LT, self._character, self._line)
        # Token '>'
        elif match(r"^>$", self._character):
            if self._peek_character() == "=":
                token = self._make_two_character_token(TokenType.GE)
            else:
                token = Token(TokenType.GT, self._character, self._line)
        # Token '!'
        elif match(r"^!$", self._character):
            if self._peek_character() == "=":
                token = self._make_two_character_token(TokenType.NOT_EQ)
            else:
                token = Token(TokenType.NEGATION, self._character, self._line)
        # Token for any letter
        elif self._is_letter(self._character):
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)

            return Token(token_type, literal, self._line)
        # Token for read numbers
        elif self._is_number(self._character):
            literal = self._read_number()

            if self._character == ".":
                self._read_character()
                sufix = self._read_number()
                return Token(TokenType.FLOAT, f"{literal}.{sufix}", self._line)

            return Token(TokenType.INTEGER, literal, self._line)
        elif match(r"^\"|'$", self._character):
            literal = self._read_string()

            return Token(TokenType.STRING, literal, self._line)
        # Illegal Token
        else:
            token = Token(TokenType.ILLEGAL, self._character, self._line)
        self._read_character()

        return token

    def _is_letter(self, character: str) -> bool:
        # Expresión regular para obtener todas las letras del alfabeto español
        return bool(match(r"^[a-zA-Z_]$", character))

    def _is_number(self, character: str) -> bool:
        # Expresión regular para objeter todos los digitos
        return bool(match(r"^\d$", character))

    def _make_two_character_token(self, token_type: TokenType) -> Token:
        prefix = self._character
        self._read_character()
        suffix = self._character

        return Token(token_type, f"{prefix}{suffix}", self._line)

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ""
        else:
            self._character = self._source[self._read_position]
            # Los \n son contados como caracteres, son skipeados por
            # _skip_whitespace, pero los interceptamos aquí para sumar
            # una línea
            if self._character == "\n":
                self._line += 1

        self._position = self._read_position
        self._read_position += 1

    def _read_identifier(self) -> str:
        initial_position = self._position

        while self._is_letter(self._character) or self._is_number(
                self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_number(self) -> str:
        initial_position = self._position

        while self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_string(self) -> str:
        # Vemos en cual tipo de comilla está el caracter actual
        quote_type = self._character

        # Como antes de esto estamos en la comilla, leemos un caracter,
        # para así ir hacia el string
        self._read_character()

        initial_position = self._position

        # Segumos leyendo el string hasta que encontremos otra comilla o se
        # acabe el archivo
        while self._character != quote_type and self._read_position <= len(
                self._source):
            self._read_character()

        string = self._source[initial_position:self._position]

        self._read_character()

        return string

    def _peek_character(self, skip=1) -> str:
        if self._read_position >= len(self._source):
            return ""

        return (self._source[self._read_position] if skip == 1 else
                self._source[self._read_position + (skip - 1)])

    def _skip_whitespace(self) -> None:
        while match(r"^\s$", self._character):
            self._read_character()
