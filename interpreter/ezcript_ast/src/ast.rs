use crate::expressions::Expressions;
use crate::statements::Statements;

/// The Expression Node
#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub enum Ast {
    Expression(Expressions),
    Statement(Statements),
    // Program(Program),
}

pub trait ASTNode {
    fn token_literal(&self) -> String;
}

// #[derive(Debug, Clone, PartialEq, Hash, Eq)]
// pub struct Program {
//     statements: Vec<Statements>,
// }

// impl Program {
//     pub fn new(statements: Vec<Statements>) -> Self {
//         Program { statements }
//     }

//     pub fn as_string(&self) -> String {
//         let mut out: Vec<String> = Vec::new();
//         for statement in self.statements.iter() {
//             out.push(statement.to_string());
//         }

//         return out.join("");
//     }
// }

// impl ASTNode for Program {
//     fn token_literal(&self) -> String {
//         if self.statements.len() > 0 {
//             return self.statements[0].token_literal();
//         }

//         String::from("")
//     }
// }
