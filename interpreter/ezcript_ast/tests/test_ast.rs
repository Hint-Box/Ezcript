use ezcript_ast::ast::Program;
use ezcript_ast::expressions::{Expressions, Identifier, Integer};
use ezcript_ast::statements::{ReturnStatement, SetStatement, Statements};
use ezcript_lexer::tokens::{Literal, Token, TokenKind};

#[macro_use]
extern crate utils;

#[test]
fn test_ast_set_statement() {
    let program: Option<Program> = Program::new(vec![Statements::SetStatement(SetStatement::new(
        Token {
            kind: TokenKind::Keyword,
            lexeme: "set".to_string(),
            literal: None,
            line: 1,
        },
        Some(Identifier::new(
            Token {
                kind: TokenKind::Identifier,
                lexeme: "var".to_string(),
                literal: None,
                line: 1,
            },
            "var",
            1,
        )),
        Some(Expressions::Identifier(Identifier::new(
            Token {
                kind: TokenKind::Identifier,
                lexeme: "other_var".to_string(),
                literal: None,
                line: 1,
            },
            "other_var",
            1,
        ))),
        1,
    ))]);
    is_not_none!(program);
    let program = program.unwrap();

    let program_str = program.to_string();

    assert_eq!(program_str, String::from("set var = other_var"));
}

#[test]
fn test_() {
    let program: Option<Program> =
        Program::new(vec![Statements::ReturnStatement(ReturnStatement::new(
            Token {
                kind: TokenKind::Keyword,
                lexeme: "return".to_string(),
                literal: None,
                line: 1,
            },
            Some(Expressions::Integer(Integer::new(
                Token {
                    kind: TokenKind::Number,
                    lexeme: "0".to_string(),
                    literal: Some(Literal::Number(0.0)),
                    line: 1,
                },
                0,
                1,
            ))),
            1,
        ))]);

    is_not_none!(program);
    let program_str = program.unwrap().to_string();

    assert_eq!(program_str, "return 0".to_string());
}
