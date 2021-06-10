use crate::ast::ASTNode;
use crate::expressions::{Expressions, Identifier, Integer};
use ezcript_lexer::tokens::Token;
use std::fmt;

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub enum Statements {
    SetStatement(SetStatement),
    ReturnStatement(ReturnStatement),
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct SetStatement {
    token: Token,
    name: Option<Identifier>,
    value: Option<Expressions>,
}

impl SetStatement {
    pub fn new(token: Token, name: Option<Identifier>, value: Option<Expressions>) -> Self {
        Self { token, name, value }
    }
}

impl ASTNode for SetStatement {
    fn token_literal(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for dyn ASTNode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.token_literal())
    }
}

impl fmt::Display for SetStatement {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let lexeme = self.token_literal();
        let value: Box<dyn ASTNode> = match self.value.as_ref().unwrap() {
            Expressions::Identifier(_ident) => {
                Box::new(Identifier::new(self.token.clone(), lexeme.as_str()))
            }
            Expressions::Integer(_int) => Box::new(Integer::new(
                self.token.clone(),
                Some(lexeme.parse::<i64>()),
            )),
        };
        write!(
            f,
            "{} {} = {}",
            lexeme,
            self.name.as_ref().unwrap().to_string(),
            value,
        )
    }
}

impl fmt::Display for ReturnStatement {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let lexeme = self.token_literal();
        let return_value: Box<dyn ASTNode> = match self.return_value.as_ref().unwrap() {
            Expressions::Identifier(_ident) => {
                Box::new(Identifier::new(self.token.clone(), lexeme.as_str()))
            }
            Expressions::Integer(_int) => Box::new(Integer::new(
                self.token.clone(),
                Some(lexeme.parse::<i64>()),
            )),
        };
        write!(f, "{} {}", self.token_literal(), return_value)
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct ReturnStatement {
    token: Token,
    return_value: Option<Expressions>,
}

impl ReturnStatement {
    pub fn new(token: Token, return_value: Option<Expressions>) -> Self {
        Self {
            token,
            return_value,
        }
    }
}

impl ASTNode for ReturnStatement {
    fn token_literal(&self) -> String {
        self.token.lexeme.clone()
    }
}
