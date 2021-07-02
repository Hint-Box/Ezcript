use crate::ast::Program;
use crate::expressions::Identifier;
use crate::statements::{SetStatement, Statements};
use ezcript_lexer::lexer::Lexer;
use ezcript_lexer::tokens::{Token, TokenKind};
use ezcript_result::{EzcriptError, Result};

/// The Parser struct take a Lexer and then generate a program that generate an
/// Abstract Syntax Tree
#[derive(Debug)]
pub struct Parser<'a> {
    lexer: Lexer<'a>,
    current_token: Option<Token>,
    peek_token: Option<Token>,
    errors: Vec<Option<Result<()>>>,
    line: u64,
}

impl<'a> Parser<'a> {
    pub fn new(lexer: Lexer<'a>) -> Self {
        let mut parser = Self {
            lexer,
            current_token: None,
            peek_token: None,
            errors: Vec::new(),
            line: 1,
        };
        parser.advance_tokens();
        parser.advance_tokens();

        parser
    }

    /// This function is the most similar thing you can do for make a getter property.
    /// It is used to obtain all the errors that our parser has suffered from.
    pub fn errors(&self) -> &Vec<Option<Result<()>>> {
        &self.errors
    }

    /// This function is in charge of making the instance of the program and starts to see which
    /// are its statements
    pub fn parse_program(&mut self) -> Option<Program> {
        let mut program: Option<Program> = Program::new(Vec::new());

        is_not_none!(self.current_token.as_ref());
        while self.current_token.as_ref().unwrap().kind != TokenKind::Eof {
            let statement = self.parse_statement();
            match statement {
                Some(stmt) => match program {
                    Some(ref mut program) => program.statements.push(stmt),
                    None => (),
                },
                None => (),
            }

            self.advance_tokens();
        }

        program
    }

    fn err(&self, msg: &str) -> Option<Result<()>> {
        is_not_none!(self.current_token);
        Some(Err(EzcriptError::Parse(
            self.line,
            msg.to_string(),
            self.current_token.as_ref().unwrap().lexeme.clone(),
        )))
    }

    fn parse_statement(&mut self) -> Option<Statements> {
        is_not_none!(self.current_token.as_ref());
        if self.current_token.as_ref().unwrap().kind == TokenKind::Keyword
            && self.current_token.as_ref().unwrap().lexeme == "set".to_string()
        {
            self.parse_let_statement()
        } else {
            None
        }
    }

    fn parse_let_statement(&mut self) -> Option<Statements> {
        is_not_none!(self.current_token.as_ref());
        let mut set_statement =
            SetStatement::new(self.current_token.as_ref().unwrap().clone(), None, None);

        if !self.expected_token(TokenKind::Identifier) {
            return None;
        }

        set_statement.name = Some(Identifier::new(
            self.current_token.as_ref().unwrap().clone(),
            self.current_token.as_ref().unwrap().lexeme.as_str(),
            self.current_token.as_ref().unwrap().line,
        ));

        if !self.expected_token(TokenKind::Equal) {
            return None;
        }

        // TODO: Finish the parse expression later
        while self.current_token.as_ref().unwrap().kind != TokenKind::NewLine {
            self.advance_tokens();
        }

        Some(Statements::SetStatement(set_statement))
    }

    fn advance_tokens(&mut self) {
        if self.peek_token == None {
            self.current_token = Some(Token::default());
        } else {
            self.current_token = Some(self.peek_token.as_ref().unwrap().clone());
        }
        self.peek_token = match self.lexer.next_token() {
            Some(result) => match result {
                Ok(token) => Some(token),
                Err(_) => Some(Token::default()),
            },
            None => Some(Token::default()),
        };
    }

    fn expected_token_error(&mut self, kind: TokenKind) {
        is_not_none!(self.peek_token);
        let error = format!(
            "The following token should be of type '{:?}'. But got '{:?}'",
            kind,
            self.peek_token.as_ref().unwrap().kind
        );

        self.errors.push(self.err(error.as_str()));
    }

    fn expected_token(&mut self, kind: TokenKind) -> bool {
        is_not_none!(self.peek_token);
        if self.peek_token.as_ref().unwrap().kind == kind {
            self.advance_tokens();

            return true;
        }
        self.expected_token_error(kind);
        false
    }
}
