#!/usr/bin/env python3

# The Ezcript interpreter.

from sys import platform as cwos  # Current Working OS
from os import system

from ezcript_lang.tokens import Token, TokenType
from ezcript_lang.lexer import Lexer


def repl() -> None:
    EOF_TOKEN: Token = Token(TokenType.EOF, '')
    try:
        while (source := input(">> ")) != "exit":
            lexer: Lexer = Lexer(source)

            if source == 'help':
                print('Type "clear" to clear the console.')

            elif source == 'clear':
                system("cls") if cwos[:5] == "win32" else system("clear")

            else:
                while (token := lexer.next_token()) != EOF_TOKEN:
                    print(token)
        print("\nGoodbye!")

    except KeyboardInterrupt:
        print("\nGoodbye!")
