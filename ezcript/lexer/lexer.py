from re import match

from ezcript.tokens import (
    Token,
    TokenType,
    lookup_token_type,
)


class Lexer:
    """The Lexer is the one who convert all the source code you write in the
    interpreter into tokens for pass it to the parser later on"""
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ''
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()

    def next_token(self) -> Token:
        """
        Get the current character the lexer are reading and convert it in a
        Token and return it

        :return: Return the Token of the current character
        :rtype: Token
        """
        self._skip_whitespace()

        # Getting the tokens
        if match(r'^%$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.PERCENTEQUAL)
            else:
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
                    token = self._make_two_character_token(
                        TokenType.DOUBLESLASH)
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
        elif self._is_letter(self._character):
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)

            return Token(token_type, literal)
        elif self._is_number(self._character):
            literal = self._read_number()

            if self._character == '.':
                self._read_character()
                sufix = self._read_number()
                return Token(TokenType.NUMBER, f'{literal}.{sufix}')

            return Token(TokenType.NUMBER, literal)
        elif match(r"^\"|'$", self._character):
            literal = self._read_string()

            return Token(TokenType.STRING, literal)
        elif match(r"^$", self._character):
            token = Token(TokenType.EOF, self._character)
        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_character()
        return token

    def _make_three_character_token(self, token_type: TokenType) -> Token:
        """
        This function take the token type of the current character and return
        a token with three characters

        :param token_type: The token type of the current character
        :type token_type: TokenType
        :return: return the token for the "next_token" function
        :rtype: Token
        """
        first = self._character
        self._read_character()
        second = self._character
        self._read_character()
        third = self._character

        return Token(token_type, f'{first}{second}{third}')

    def _make_two_character_token(self, token_type: TokenType) -> Token:
        """
        This function take the token type of the current character and return
        a token with two characters

        :param token_type: The token type of the current character
        :type token_type: TokenType
        :return: return the roken for the "next_token" function
        :rtype: Token
        """
        prefix = self._character
        self._read_character()
        suffix = self._character

        return Token(token_type, f'{prefix}{suffix}')

    def _read_character(self) -> None:
        """
        This function read each character of the source that we pass to the
        class. We use this function specifically for save some character
        and do something with it or for skip one character.

        :return: The function don't return anything
        :rtype: None
        """
        if self._read_position >= len(self._source):
            # If the lexer finish to read the source, the current caracter is
            # a empty string again
            self._character = ''
        else:
            # if not, the character will be the current character
            self._character = self._source[self._read_position]

        # Save the position of the current character readed
        self._position = self._read_position
        # And then aument in one the actual position
        self._read_position += 1

    def _peek_character(self, skip: int = 1) -> str:
        """
        This function return the character after the current, and if you pass
        an argument that have to be an integer, the function will skip the
        number of character you pass

        :param skip: The numbers of character the function will skip, defaults to 1
        :type skip: int, optional
        :return: Return the next token to the current
        :rtype: str
        """
        if self._read_position >= len(self._source):
            return ''

        return self._source[self._read_position] if skip == 1\
            else self._source[self._read_position + (skip - 1)]

    def _skip_whitespace(self) -> None:
        """
        This function is used for the other function "next_token" for skip
        any whitespace that the source have for just center to the tokens

        :return: None
        :rtype: None
        """
        while match(r'^\s$', self._character):
            self._read_character()

    def _read_string(self) -> str:

        # With this, we can know which type of quote is the current character
        quote_type = self._character

        # We have to move one character more for get the string content
        self._read_character()

        # Save the current position for later save all the sting in a
        # variable
        initial_position = self._position

        # We keep reading the string content until we find the closing
        # quotation mark or the file end
        while self._character != quote_type \
                and self._read_position <= len(self._source):
            self._read_character()

        # After we read until the final of the string or the file, we
        # save the content on the initial position until the current position
        string = self._source[initial_position:self._position]

        # Go to the last character which is the closing quotation mark
        self._read_character()

        return string

    def _is_letter(self, character: str) -> bool:
        # Expresión regular para obtener todas las letras del alfabeto español
        return bool(match(r'^[a-zA-Z_]$', character))

    def _is_number(self, character: str) -> bool:
        # Expresión regular para objeter todos los digitos
        return bool(match(r'^\d$', character))

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
