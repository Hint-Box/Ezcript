use crate::ast::Program;
use crate::statements::Statements;
use ezcript_lexer::{
    lexer::Lexer,
    tokens::{Token, TokenKind},
};

/// The Parser struct take a Lexer and then generate a program that generate an
/// Abstract Syntax Tree
#[derive(Debug, Clone)]
pub struct Parser<'a> {
    lexer: Lexer<'a>,
    current_token: Option<Token>,
    peek_token: Option<Token>,
}

impl<'a> Parser<'a> {
    pub fn new(lexer: Lexer<'a>) -> Self {
        Self {
            lexer,
            current_token: None,
            peek_token: None,
        }
    }

    /// This function is in charge of making the instance of the program and starts to see which
    /// are its statements
    pub fn parse_program(&self) -> Option<Program> {
        let program: Option<Program> = Program::new(Vec::new());

        is_not_none!(self.current_token.as_ref());
        while self.current_token.unwrap().kind != TokenKind.Eof {
            let statement = self.parse_statement();
            match statement {
                Some(stmt) => match program {
                    Some(program) => program.statements.push(stmt),
                    None => continue,
                },
                None => continue,
            }
        }

        program
    }

    fn parse_statement(&self) -> Option<Statement> {
        is_not_none!(self.current_token.as_ref());
        if self.current_token.unwrap().kind == TokenKind.Keyword
            && self.current_token.unwrap().lexem == "set".to_string()
        {
            return self.parse_let_statement();
        } else {
            return None;
        }
    }

    fn parse_let_statement(&self) -> Option<LetStatement> {
        is_not_none!(self.current_token.as_ref());
        let let_statement = SetStatement::new(self.current_token, None, None);

        if !self.expected_token(TokenKind::Identifier) {
            return None;
        }

        let_statement.name = Identifier::new(
            self.current_token.unwrap(),
            self.current_token.unwrap().lexeme.as_str(),
            self.current_token.unwrap().line,
        );

        if !self.expected_token(TokenKind.Equal) {
            return None;
        }

        // TODO: Finish the parse expression later
        while self.current_token.unwrap().kind != TokenType.NewLine {
            self.advance_tokens();
        }

        Some(let_statement)
    }
}
