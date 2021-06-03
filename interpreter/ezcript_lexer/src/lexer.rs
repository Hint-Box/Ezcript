use super::tokens::{Literal, Token, TokenKind};
use ezcript_result::Error;
use std::collections::{HashSet, VecDeque};
use std::ops::Index;
use std::str::Chars;

#[derive(Debug)]
struct Lexer<'a> {
    source: Chars<'a>,
    peeks: VecDeque<char>,
    lexeme: String,
    line: u64,
    offset: u64,
    eof: bool,
}

impl<'a> Lexer<'a> {
    pub fn new(c: Chars<'a>) -> Self {
        Self {
            source: c,
            peeks: VecDeque::with_capacity(2),
            lexeme: "".to_string(),
            line: 1,
            offset: 0,
            eof: false,
        }
    }

    fn advance(&mut self) -> Option<char> {
        if self.eof {
            return None;
        }

        match self.peeks.len() {
            0 => self.source.next(),
            _ => self.peeks.pop_front(),
        }
        .or_else(|| {
            self.eof = true;
            Some('\0')
        })
        .and_then(|c| {
            self.lexeme.push(c);
            self.offset += 1;
            Some(c)
        })
    }

    fn lookahead(&mut self, n: usize) -> char {
        assert!(n > 0, "lookahead must be greater than zero");

        while self.peeks.len() < n {
            if let Some(c) = self.source.next().or(Some('\0')) {
                self.peeks.push_back(c)
            }
        }

        *self.peeks.index(n - 1)
    }

    fn peek(&mut self) -> char {
        self.lookahead(1)
    }

    fn peek_next(&mut self) -> char {
        self.lookahead(2)
    }

    fn match_advance(&mut self, c: char) -> bool {
        if self.peek() == c {
            self.advance().unwrap();
            return true;
        }

        false
    }

    fn advance_until(&mut self, c: &[char]) -> char {
        let mut last = '\0';
        let chars: HashSet<&char> = c.iter().clone().collect();

        loop {
            match self.peek() {
                ch if chars.contains(&ch) || ch == '\0' => break,
                ch => {
                    last = ch;
                    self.advance()
                }
            };
        }
        last
    }

    fn static_token(&self, kind: TokenKind) -> Option<Result<Token>> {
        self.literal_token(kind, None)
    }

    fn literal_token(&self, kind: TokenKind, lit: Option<Literal>) -> Option<Result<Token>> {
        Some(Ok(Token {
            kind,
            literal: lit,
            line: self.line,
            offset: self.offset - self.lexeme.len() as u64,

            lexeme: self.lexeme.clone(),
        }))
    }

    fn err(&self, msg: &str) -> Option<Result<Token>> {
        Some(Err(Error::Lexical(
            self.line,
            msg.to_string(),
            self.lexeme.clone(),
        )))
    }

    fn match_static_token(&mut self, c: char, m: TokenKind, u: TokenKind) -> Option<Result<Token>> {
        if self.match_advance(c) {
            self.static_token(m)
        } else {
            self.static_token(u)
        }
    }

    fn string(&mut self) -> Option<Result<Token>> {
        loop {
            let last = self.advance_until(&['\n', '"', '\'']);

            match self.peek() {
                '\n' => self.line += 1,
                '"' if last == '\\' => { self.lexeme.pop(); }
                '\'' if last == '\\' => { self.lexeme.pop(); }
                '"' => break,
                '\'' => break,
                '\0' => return self.err("unterminated string"),
                _ => return self.err("unexpected character"),
            };

            self.advance();
        }

        self.advance();

        let lit: String = self.lexeme.clone()
            .chars()
            .skip(1)
            .take(self.lexeme.len() - 2)
            .collect();

        self.literal_token(Type::String, Some(Literal::String(lit)))
    }

    fn number(&mut self) -> Option<Result<Token>> {
        while self.peek().is_digit(10) { self.advance(); };

        if self.peek() == '.' && self.peek_next().is_digit(10) {
            self.advance();
            while self.peek().is_digit(10) { self.advance(); };
        }

        if let Ok(lit) = self.lexeme.clone().parse::<f64>() {
            return self.literal_token(Type::Number, Some(Literal::Number(lit)));
        }
        
        self.err("invalid numeric")
    }
    
    fn identifier(&mut self) -> Option<Result<Token>> {
        while is_alphanumeric(self.peek()) { self.advance(); }
        let lex: &str = self.lexeme.as_ref();
        let kind: TokenKind::reserved(lex).map_or(TokenKind::Ident, |t| *t);

        match kind {
            TokenKind::Null => self.literal_token(kind, Some(Literal::Null)),
            TokenKind::True => self.literal_token(kind, Some(Literal::Boolean)),
            TokenKind::False => self.literal_token(kind, Some(Literal::Boolean)),
            _ => self.static_token(kind)
        }
    }

    fn line_comment(&mut self) {
        self.advance_until(&['\n']);
        self.lexeme.clear();
    }

    fn block_comment(&mut self) {
        self.advance();

        loop {
            let last = self.advance_until(&['\n', '#']);
            let next = self.peek();
            match (last, next) {
                (_, '\n') => self.line += 1,
                ('*', '#') => {
                    self.advance();
                    self.advance();
                    break;
                }
                (_, '\0') => break,
                (_, _) => (),
            }
            self.advance();
        }

        self.lexeme.clear();
    }
}

impl Iterator for Lexer {
    type Item = Result<Token>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.eof {
            return None;
        }
        
        self.lexeme.clear();

        loop {
            match self.advance().unwrap() {
                '\0' => {
                    self.eof = true;
                    return self.static_token(TokenType::Eof);
                }
                '(' => return self.static_token(TokenType::LParen),
                ')' => return self.static_token(TokenType::RParen),
                '{' => return self.static_token(TokenType::LBrace),
                '}' => return self.static_token(TokenType::RBrace),
                '[' => return self.static_token(TokenType::LBracket),
                ']' => return self.static_token(TokenType::RBracket),
                ':' => return self.static_token(TokenType::Colon),
                ',' => return self.static_token(TokenType::Comma),
                '%' => return self.static_token(TokenType::Percent),
                '.' => match self.peek() {
                    '.' => match self.peek_next() {
                        '.'  => return self.static_token(TokenType::Ellipsis),
                    },
                    _ => return self.static_token(TokenType::Dot),
                },
                '-' => match self.peek() {
                    '-' => return self.static_token(TokenType::DoubleMinus),
                    '=' => return self.static_token(TokenType::MinEqual),
                    _ => return self.static_token(TokenType::Minus),
                },
                '+' => match self.peek() {
                    '+' => return self.static_token(TokenType::DoublePlus),
                    '=' => return self.static_token(TokenType::PlusEqual),
                    _ => return self.static_token(TokenType::Plus),
                },
                '*' => match self.peek() {
                    '*' => match self.peek_next() {
                        '=' => return self.static_token(TokenType::DoubleStarEqual),
                        _ => return self.static_token(TokenType::DoubleStar),
                    },
                    '=' => return self.static_token(TokenType::StarEqual),
                    _ => return self.static_token(TokenType::Star),
                },
                '/' => match self.peek() {
                    '/' => match self.peek_next() {
                        '=' => return self.static_token(TokenType::DoubleSlashEqual),
                        _ => return self.static_token(TokenType::DoubleSlash),
                    },
                    '=' => return self.static_token(TokenType::SlashEqual),
                    _ => return self.static_token(TokenType::Slash),
                },
                '=' => match self.peek() {
                    '>' => return self.static_token(TokenTyep::RArrow),
                    _ => return self.match_static_token('=', EqEqual, Equal),
                },
                '!' => return self.match_static_token('=', BangEqual, Not),
                '<' => return self.match_static_token('=', LessEqual, Less),
                '>' => return self.match_static_token('=', GreaterEqual, Greater),
                '"' => return self.string(),
                '\'' => return self.string(),
                '#' => match self.peek() {
                    '*' => self.block_comment(),
                    _ => self.line_comment(),
                }
                c if c.is_whitespace() => {
                    self.lexeme.clear();
                    if c == '\n' {
                        self.offset = 0;
                        self.line += 1;
                    }
                }
                c if c.is_digit(10) => return self.number(),
                c if is_alphanumeric(c) => return self.identifier(),
                _ => return self.err("unexpected character"),
            }
        }
    }
}

/// Describes a type that can be converted into a token Lexer.
pub trait TokenIterator<'a> {
    fn tokens(self) -> Lexer<'a>;
}

impl<'a> TokenIterator<'a> for Chars<'a> {
    fn tokens(self) -> Lexer<'a> {
        Lexer::new(self)
    }
}

fn is_alphanumeric(c: char) -> bool {
    c.is_digit(36) || c == '_'
}
