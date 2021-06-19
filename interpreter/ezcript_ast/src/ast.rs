// use crate::expressions::Expressions;
use crate::statements::Statements;
use std::fmt;

// /// The Ast enum, containing all the nodes
// #[derive(Debug, PartialEq, Eq, Clone, Hash)]
// pub enum Ast {
//     Expression(Expressions),
//     Statement(Statements),
//     // Program(Program),
// }

/// Trait for structs that will be a Node for the Abstract syntaxt tree
pub trait ASTNode: fmt::Display {
    /// Get the lexeme of the Node token
    fn token_lexeme(&self) -> String;
}

/// Our general program that contain all the statements
#[derive(Debug, Clone, PartialEq, Hash, Eq)]
pub struct Program {
    statements: Vec<Statements>,
}

impl Program {
    pub fn new(statements: Vec<Statements>) -> Self {
        Self { statements }
    }
}

impl ASTNode for Program {
    fn token_lexeme(&self) -> String {
        if self.statements.len() > 0 {
            // Here we are using the match expression for get the lexeme of the token depending on
            // which statement it is
            match &self.statements[0] {
                Statements::SetStatement(statement) => statement.token_lexeme(),
                Statements::ReturnStatement(statement) => statement.token_lexeme(),
            };
        }

        "".to_string()
    }
}

impl fmt::Display for Program {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut out: Vec<String> = Vec::new();
        for statement in self.statements.clone() {
            match statement {
                Statements::SetStatement(statement) => out.push(statement.to_string()),
                Statements::ReturnStatement(statement) => out.push(statement.to_string()),
            }
        }

        write!(f, "{}", out.join(""))
    }
}
