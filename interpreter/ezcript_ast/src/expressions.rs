use crate::ast::ASTNode;
use ezcript_lexer::tokens::Token;
use std::fmt;

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub enum Expressions {
    Identifier(Identifier),
    Integer(Integer),
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct Identifier {
    pub token: Token,
    pub value: String,
}

impl Identifier {
    pub fn new(token: Token, value: &str) -> Self {
        Self {
            token,
            value: value.to_string(),
        }
    }
}

impl ASTNode for Identifier {
    fn token_literal(&self) -> String {
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
    pub value: Option<i64>,
}

impl Integer {
    pub fn new(token: Token, value: Option<Result<i64, std::num::ParseIntError>>) -> Self {
        if value != None {
            let value = Some(value.unwrap().unwrap());
            Self { token, value }
        } else {
            Self { token, value: None }
        }
    }
}

impl ASTNode for Integer {
    fn token_literal(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for Integer {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{}",
            if self.value != None {
                self.value.unwrap().to_string()
            } else {
                String::from("null")
            }
        )
    }
}
