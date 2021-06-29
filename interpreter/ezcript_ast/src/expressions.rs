use crate::ast::ASTNode;
use ezcript_lexer::tokens::Token;
use std::fmt;

/// An enum that contain all expressions
#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub enum Expressions {
    Identifier,
    Integer,
    Float,
    Boolean,
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct Null {
    pub token: Token,
    pub value: String,
    pub line: u64,
}

impl Null {
    pub fn new(token: Token, value: &str, line: u64) -> Self {
        Self {
            token,
            value: value.to_string(),
            line,
        }
    }
}

impl ASTNode for Null {
    fn token_lexeme(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for Null {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct Identifier {
    pub token: Token,
    pub value: String,
    pub line: u64,
}

impl Identifier {
    pub fn new(token: Token, value: &str, line: u64) -> Self {
        Self {
            token,
            value: value.to_string(),
            line,
        }
    }
}

impl ASTNode for Identifier {
    fn token_lexeme(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for Identifier {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct Integer {
    pub token: Token,
    pub value: i64,
    pub line: u64,
}

impl Integer {
    pub fn new(token: Token, value: i64, line: u64) -> Self {
        Self { token, value, line }
    }
}

impl ASTNode for Integer {
    fn token_lexeme(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for Integer {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, PartialEq, Clone)]
pub struct Float {
    pub token: Token,
    pub value: f64,
    pub line: u64,
}

impl Float {
    pub fn new(token: Token, value: f64, line: u64) -> Self {
        Self { token, value, line }
    }
}

impl ASTNode for Float {
    fn token_lexeme(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for Float {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct Boolean {
    pub token: Token,
    pub value: bool,
    pub line: u64,
}

impl Boolean {
    pub fn new(token: Token, value: bool, line: u64) -> Self {
        Self { token, value, line }
    }
}

impl ASTNode for Boolean {
    fn token_lexeme(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for Boolean {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}
