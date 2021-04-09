import readline
from os import system, name

from ezcript_lang.lexer import Lexer
from ezcript_lang.tokens import (
    Token,
    TokenType,
)

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def clear() -> None:

    # command for windows
    if name == 'nt':
        system('cls')

    # commanf for mac and linux
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
