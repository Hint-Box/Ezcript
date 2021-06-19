use crate::ast::Program;
use ezcript_lexer::lexer::Lexer;

/// The Parser struct take a Lexer and then generate a program that generate an
/// Abstract Syntax Tree
#[derive(Debug, Clone)]
pub struct Parser<'a> {
    lexer: Lexer<'a>,
}

impl<'a> Parser<'a> {
    pub fn new(lexer: Lexer<'a>) -> Self {
        Self { lexer }
    }

    /// This function is in charge of making the instance of the program and starts to see which
    /// are its statements
    pub fn parse_program(&self) -> Program {
        let program: Program = Program::new(Vec::new());
        program
    }
}
