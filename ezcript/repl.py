import readline

from ezcript.lexer import Lexer
from ezcript.tokens import (
    Token,
    TokenType,
)

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def start_repl() -> None:
    try:
        while (source := input('>> ')) != 'exit()':
            lexer: Lexer = Lexer(source)

            if source == 'help()':
                print("This is a provicional help")
            else:
                while (token := lexer.next_token()) != EOF_TOKEN:
                    print(token)
        print("Bye now")
    except KeyboardInterrupt:
        print("\nBye now")
