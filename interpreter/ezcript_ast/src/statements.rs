use crate::ast::ASTNode;
use crate::expressions::{Boolean, Expressions, Float, Identifier, Integer};
use ezcript_lexer::tokens::Token;
use std::fmt;

impl fmt::Display for dyn ASTNode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.token_lexeme())
    }
}

/// Statements enum where we will locate all the statements of our language
#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub enum Statements {
    SetStatement,
    ReturnStatement,
}

/// The SetStatement will look like
/// `set var_name = 4`
#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct SetStatement {
    token: Token,
    name: Identifier,
    value: Option<Expressions>,
}

impl SetStatement {
    pub fn new(token: Token, name: Identifier, value: Option<Expressions>) -> Self {
        Self { token, name, value }
    }
}

impl ASTNode for SetStatement {
    fn token_lexeme(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for SetStatement {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let lexeme = self.token_lexeme();
        // We use the trait ASTNode like a type because we want all the types tha implement it
        // trait.
        let value: Box<dyn ASTNode> = match self.value.as_ref().unwrap() {
            Expressions::Identifier => Box::new(Identifier::new(
                self.token.clone(),
                lexeme.as_str(),
                self.token.line,
            )),
            Expressions::Integer => Box::new(Integer::new(
                self.token.clone(),
                lexeme.clone().parse::<i64>().unwrap(),
                self.token.line,
            )),
            Expressions::Float => Box::new(Float::new(
                self.token.clone(),
                lexeme.clone().parse::<f64>().unwrap(),
                self.token.line,
            )),
            Expressions::Boolean => {
                let value: bool;
                if lexeme == "true".to_string() {
                    value = true;
                } else {
                    value = false;
                }

                Box::new(Boolean::new(self.token.clone(), value, self.token.line))
            }
        };

        write!(f, "{} {} = {}", lexeme, self.name.to_string(), value)
    }
}

/// The return statement that will look like
/// `return "hello"`
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
    fn token_lexeme(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for ReturnStatement {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let lexeme = self.token_lexeme();
        // We use the trait ASTNode like a type because we want all the types tha implement the
        // trait.
        let return_value: Box<dyn ASTNode> = match self.return_value.as_ref().unwrap() {
            Expressions::Identifier => Box::new(Identifier::new(
                self.token.clone(),
                lexeme.as_str(),
                self.token.line,
            )),
            Expressions::Integer => Box::new(Integer::new(
                self.token.clone(),
                lexeme.clone().parse::<i64>().unwrap(),
                self.token.line,
            )),
            Expressions::Float => Box::new(Float::new(
                self.token.clone(),
                lexeme.clone().parse::<f64>().unwrap(),
                self.token.line,
            )),
            Expressions::Boolean => {
                let value: bool;
                if lexeme == "true".to_string() {
                    value = true;
                } else {
                    value = false;
                }

                Box::new(Boolean::new(self.token.clone(), value, self.token.line))
            }
        };
        write!(f, "{} {}", self.token_lexeme(), return_value)
    }
}
