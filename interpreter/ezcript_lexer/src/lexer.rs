use std::collections::{HashSet, VecDeque};
use std::ops::Index;
use std::str::Chars;

use super::tokens::{Literal, Token, TokenKind};
use ezcript_result::{Error, Result};

#[derive(Debug, Clone)]
pub struct Lexer<'a> {
    source: Chars<'a>,
    tokens: VecDeque<char>,
    lexeme: String,
    line: u64,
    eof: bool,
}

impl<'a> Lexer<'a> {
    pub fn new(source: Chars<'a>) -> Self {
        Self {
            source,
            tokens: VecDeque::with_capacity(2),
            lexeme: String::from(""),
            line: 1,
            eof: false,
        }
    }

    pub fn next_token(&mut self) -> Option<Result<Token>> {
        if self.eof {
            return None;
        }

        self.lexeme.clear();

        loop {
            match self.advance().unwrap() {
                '\0' => {
                    self.eof = true;
                    return self.static_token(TokenKind::Eof);
                }
                '(' => return self.static_token(TokenKind::LParen),
                ')' => return self.static_token(TokenKind::RParen),
                '{' => return self.static_token(TokenKind::LBrace),
                '}' => return self.static_token(TokenKind::RBrace),
                '[' => return self.static_token(TokenKind::LBracket),
                ']' => return self.static_token(TokenKind::RBracket),
                ':' => return self.static_token(TokenKind::Colon),
                ',' => return self.static_token(TokenKind::Comma),
                '%' => return self.static_token(TokenKind::Percent),
                '.' => return self.static_token(TokenKind::Dot),
                '-' => match self.peek(1) {
                    '-' => {
                        return self.match_static_token(
                            '-',
                            TokenKind::DoubleMinus,
                            TokenKind::Minus,
                        )
                    }
                    '>' => {
                        return self.match_static_token('>', TokenKind::RArrow, TokenKind::Minus)
                    }
                    '=' => {
                        return self.match_static_token('=', TokenKind::MinEqual, TokenKind::Minus)
                    }
                    _ => return self.static_token(TokenKind::Minus),
                },
                '+' => match self.peek(1) {
                    '+' => {
                        return self.match_static_token('+', TokenKind::DoublePlus, TokenKind::Plus)
                    }
                    '=' => {
                        return self.match_static_token('=', TokenKind::PlusEqual, TokenKind::Plus)
                    }
                    _ => return self.static_token(TokenKind::Plus),
                },
                '*' => match self.peek(1) {
                    '*' => {
                        return self.match_static_token('*', TokenKind::DoubleStar, TokenKind::Star)
                    }
                    '=' => {
                        return self.match_static_token('=', TokenKind::StarEqual, TokenKind::Star)
                    }
                    _ => return self.static_token(TokenKind::Star),
                },
                '/' => match self.peek(1) {
                    '/' => {
                        return self.match_static_token(
                            '/',
                            TokenKind::DoubleSlash,
                            TokenKind::Slash,
                        )
                    }
                    '=' => {
                        return self.match_static_token(
                            '=',
                            TokenKind::SlashEqual,
                            TokenKind::Slash,
                        )
                    }
                    _ => return self.static_token(TokenKind::Slash),
                },
                '=' => return self.match_static_token('=', TokenKind::EqEqual, TokenKind::Equal),
                '!' => return self.match_static_token('=', TokenKind::BangEqual, TokenKind::Not),
                '<' => return self.match_static_token('=', TokenKind::LessEqual, TokenKind::Less),
                '>' => {
                    return self.match_static_token(
                        '=',
                        TokenKind::GreaterEqual,
                        TokenKind::Greater,
                    )
                }
                '"' => return self.string(),
                '\'' => return self.string(),
                '#' => match self.peek(1) {
                    '*' => self.block_comment(),
                    _ => self.line_comment(),
                },
                c if c.is_whitespace() => {
                    self.lexeme.clear();
                    if c == '\n' {
                        self.line += 1;
                        return self.static_token(TokenKind::NewLine);
                    }
                }
                c if c.is_digit(10) => return self.number(),
                c if is_alphanumeric(c) => return self.identifier(),
                _ => return self.err("unexpected character"),
            }
        }
    }

    fn static_token(&mut self, kind: TokenKind) -> Option<Result<Token>> {
        self.literal_token(kind, None)
    }

    fn literal_token(&self, kind: TokenKind, literal: Option<Literal>) -> Option<Result<Token>> {
        Some(Ok(Token {
            kind,
            literal,
            line: self.line,
            lexeme: self.lexeme.clone(),
        }))
    }

    fn advance(&mut self) -> Option<char> {
        if self.eof {
            return None;
        }

        match self.tokens.len() {
            0 => self.source.next(),
            _ => self.tokens.pop_front(),
        }
        .or_else(|| {
            self.eof = true;
            Some('\0')
        })
        .and_then(|c| {
            self.lexeme.push(c);
            Some(c)
        })
    }

    fn advance_until(&mut self, c: &[char]) -> char {
        let mut last = '\0';
        let chars: HashSet<&char> = c.iter().clone().collect();

        loop {
            match self.peek(1) {
                ch if chars.contains(&ch) || ch == '\0' => break,
                ch => {
                    last = ch;
                    self.advance()
                }
            };
        }
        last
    }

    fn line_comment(&mut self) {
        self.advance_until(&['\n']);
        self.lexeme.clear();
    }

    fn block_comment(&mut self) {
        self.advance(); // *

        loop {
            let last = self.advance_until(&['\n', '#']);
            let next = self.peek(1);
            match (last, next) {
                (_, '\n') => self.line += 1,
                ('*', '#') => {
                    self.advance(); // *
                    self.advance(); // /
                    break;
                }
                (_, '\0') => break,
                (_, _) => (), // noop
            }
            self.advance();
        }

        self.lexeme.clear();
    }

    fn err(&self, msg: &str) -> Option<Result<Token>> {
        Some(Err(Error::Lexical(
            self.line,
            msg.to_string(),
            self.lexeme.clone(),
        )))
    }

    fn peek(&mut self, skip: usize) -> char {
        assert!(skip > 0, "Skip must be greater than zero");

        while self.tokens.len() < skip {
            if let Some(c) = self.source.next().or(Some('\0')) {
                self.tokens.push_back(c)
            }
        }

        *self.tokens.index(skip - 1)
    }

    fn match_advance(&mut self, c: char) -> bool {
        if self.peek(1) == c {
            self.advance().unwrap();
            return true;
        }

        false
    }

    fn match_static_token(
        &mut self,
        c: char,
        first: TokenKind,
        second: TokenKind,
    ) -> Option<Result<Token>> {
        if self.match_advance(c) {
            self.static_token(first)
        } else {
            self.static_token(second)
        }
    }

    fn string(&mut self) -> Option<Result<Token>> {
        loop {
            let last = self.advance_until(&['\n', '"', '\'']);

            match self.peek(1) {
                '\n' => self.line += 1,
                '"' if last == '\\' => {
                    self.lexeme.pop();
                }
                '"' => break,
                '\'' if last == '\\' => {
                    self.lexeme.pop();
                }
                '\'' => break,
                '\0' => return self.err("unterminated string"),
                _ => return self.err("unexpected character"),
            };

            self.advance();
        }

        self.advance();

        let literal: String = self
            .lexeme
            .clone()
            .chars()
            .skip(1)
            .take(self.lexeme.len() - 2)
            .collect();

        self.literal_token(TokenKind::String, Some(Literal::String(literal)))
    }

    fn number(&mut self) -> Option<Result<Token>> {
        while self.peek(1).is_digit(10) {
            self.advance();
        }

        if self.peek(1) == '.' && self.peek(2).is_digit(10) {
            self.advance();
            while self.peek(1).is_digit(10) {
                self.advance();
            }
        }

        if let Ok(literal) = self.lexeme.clone().parse::<f64>() {
            return self.literal_token(TokenKind::Number, Some(Literal::Number(literal)));
        }

        self.err("invalid numeric")
    }

    fn identifier(&mut self) -> Option<Result<Token>> {
        while is_alphanumeric(self.peek(1)) || self.peek(1).is_digit(10) {
            self.advance();
        }
        let lexeme: &str = self.lexeme.as_ref();
        let kind = TokenKind::reserved(lexeme).map_or(TokenKind::Ident, |t| *t);

        match kind {
            TokenKind::Null => self.literal_token(kind, Some(Literal::Null)),
            TokenKind::Boolean => {
                if lexeme == "true" {
                    return self.literal_token(kind, Some(Literal::Boolean(true)));
                } else {
                    return self.literal_token(kind, Some(Literal::Boolean(false)));
                }
            }
            _ => self.static_token(kind),
        }
    }
}

fn is_alphanumeric(c: char) -> bool {
    c.is_digit(36) || c == '_' || c == '$'
}
