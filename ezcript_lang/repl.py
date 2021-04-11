import readline
from os import system, name

from ezcript_lang.lexer import Lexer
from ezcript_lang.tokens import (
    Token,
    TokenType,
)

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def clear() -> None:

    # command for Windows
    if name == 'nt':
        system('cls')

    # command for MacOS and Linux
    else:
        system('clear')


def repl() -> None:
    try:
        while (source := input('>> ')) != 'exit()':
            lexer: Lexer = Lexer(source)

            if source == 'help()':
                print("Write \"clear()\" for clear the screen")
            elif source == 'clear()':
                clear()
            else:
                while (token := lexer.next_token()) != EOF_TOKEN:
                    print(token)
        print("Bye now")
    except KeyboardInterrupt:
        print("\nBye now")
