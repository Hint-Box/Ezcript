use ezcript_lexer::tokens::Token;
use std::fmt;

/// The Expression Node
#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub enum Ast {
    Expression(Expression),
    Statement(Statement),
    Program(Program),
}

pub trait ASTNode {
    fn token_literal(&self) -> String;
}

pub trait AsString {
    fn as_string(&self) -> String;
}

#[derive(Debug, Clone, PartialEq, Hash, Eq)]
pub struct Expression {
    token: Token,
}

impl Expression {
    pub fn new(token: Token) -> Self {
        Expression { token }
    }
}

impl ASTNode for Expression {
    fn token_literal(&self) -> String {
        self.token.lexeme.clone()
    }
}

#[derive(Debug, Clone, PartialEq, Hash, Eq)]
pub struct Statement {
    token: Token,
}

impl Statement {
    pub fn new(token: Token) -> Self {
        Statement { token }
    }
}

impl ASTNode for Statement {
    fn token_literal(&self) -> String {
        self.token.lexeme.clone()
    }
}

impl fmt::Display for Statement {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.token)
    }
}

#[derive(Debug, Clone, PartialEq, Hash, Eq)]
pub struct Program {
    statements: Vec<Statement>,
}

impl Program {
    pub fn new(statements: Vec<Statement>) -> Self {
        Program { statements }
    }
}

impl ASTNode for Program {
    fn token_literal(&self) -> String {
        if self.statements.len() > 0 {
            return self.statements[0].token_literal();
        }

        String::from("")
    }
}

impl AsString for Program {
    fn as_string(&self) -> String {
        let mut out: Vec<String> = Vec::new();
        for statement in self.statements.iter() {
            out.push(statement.to_string());
        }

        return out.join("");
    }
}
