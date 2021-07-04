#![feature(type_name_of_val)]
use ezcript_ast::ast::ASTNode;
use ezcript_ast::ast::Program;
use ezcript_ast::expressions::{Expressions, Identifier};
use ezcript_ast::parser::Parser;
use ezcript_ast::statements::{ExpressionStatement, ReturnStatement, SetStatement, Statements};
use ezcript_lexer::lexer::Lexer;
use std::any::{type_name_of_val, Any};
use utils::is_instance;

#[macro_use]
extern crate utils;

#[test]
fn test_parse_program() {
    let source: &str = "set x = 5\n";
    let lexer: Lexer = Lexer::new(source.chars());
    let mut parser: Parser = Parser::new(lexer);

    let program: Option<Program> = parser.parse_program();

    is_not_none!(program.as_ref());
    is_instance(&program, Program::new(Vec::new()));
}

#[test]
fn test_let_statements() {
    let source: &str = "
            set x = 5
            set y = 10
            set foo = 20
        ";
    let lexer: Lexer = Lexer::new(source.chars());
    let mut parser: Parser = Parser::new(lexer);

    let program: Option<Program> = parser.parse_program();

    is_not_none!(program.as_ref());

    let program = program.unwrap();

    assert_eq!(program.statements.len(), 3);

    for statement in program.statements.clone() {
        match statement {
            Statements::SetStatement(statement) => {
                assert_eq!(statement.token_lexeme(), "set");
                is_instance(&Some(statement), Some(SetStatement::default()));
            }
            _ => continue,
        }
    }
}

#[test]
fn test_variable_name() {
    let source: &str = "set string = \"hola\"
            set num = 5
            set bool = true
        ";
    let lexer: Lexer = Lexer::new(source.chars());
    let mut parser: Parser = Parser::new(lexer);

    let program: Option<Program> = parser.parse_program();
    is_not_none!(program.as_ref());

    let program = program.unwrap();

    let mut statements_name: Vec<String> = Vec::new();

    for statement in program.statements.clone() {
        match statement {
            Statements::SetStatement(ref statement) => {
                is_instance(&Some(statement.clone()), Some(SetStatement::default()));
                is_not_none!(statement.name);
                statements_name.push(statement.name.as_ref().unwrap().value.clone());
            }
            _ => continue,
        }
    }
    let expected_names: Vec<String> =
        vec!["string".to_string(), "num".to_string(), "bool".to_string()];
    assert_eq!(statements_name, expected_names);
}

#[test]
fn test_parse_errors() {
    let source: &str = "set x 5\n";
    let lexer: Lexer = Lexer::new(source.chars());
    let mut parser: Parser = Parser::new(lexer);

    let _program: Option<Program> = parser.parse_program();
    println!("{:?}", parser.errors());

    assert_eq!(parser.errors().len(), 1);
}

#[test]
fn test_return_statement() {
    let source: &str = "
            return 5
            return foo
        ";
    let lexer: Lexer = Lexer::new(source.chars());
    let mut parser: Parser = Parser::new(lexer);

    let program: Option<Program> = parser.parse_program();
    is_not_none!(program.as_ref());

    let program = program.unwrap();

    assert_eq!(program.statements.len(), 2);

    for statement in program.statements.clone() {
        match statement {
            Statements::ReturnStatement(statement) => {
                assert_eq!(statement.token_lexeme(), "return");
                is_instance(&Some(statement), Some(ReturnStatement::default()));
            }
            _ => continue,
        }
    }
}

#[test]
fn test_identifier_expression() {
    let source: &str = "foobar\n";
    let lexer: Lexer = Lexer::new(source.chars());
    let mut parser: Parser = Parser::new(lexer);

    let program: Option<Program> = parser.parse_program();
    is_not_none!(program);
    let program = program.unwrap();

    test_program_statements(parser, &program, 1);

    let expression_statement: &ExpressionStatement = match &program.statements[0] {
        Statements::ExpressionStatement(statement) => statement,
        _ => panic!("Must be a expression statement"),
    };

    is_not_none!(expression_statement.expression);
    let expected_value = "foobar";
    test_literal_expression(
        expression_statement.expression.as_ref().unwrap().clone(),
        &expected_value,
    );
}

fn test_program_statements(parser: Parser, program: &Program, expected_statement_count: u64) {
    assert_eq!(parser.errors().len(), 0);
    assert_eq!(program.statements.len() as u64, expected_statement_count);
    match &program.statements.clone()[0] {
        Statements::ExpressionStatement(statement) => {
            is_instance(&statement, ExpressionStatement::default());
        }
        _ => panic!("Must be a expression statement"),
    }
}

fn test_literal_expression(expression: Expressions, expected_value: &dyn Any) {
    if expected_value.is::<&str>() {
        if let Some(lit_str) = expected_value.downcast_ref::<&str>() {
            test_identifier(expression, lit_str);
        }
    } else {
        panic!(
            "Unhandled type of expression. Got={}",
            type_name_of_val(expected_value)
        );
    }
}

fn test_identifier(expression: Expressions, expected_value: &str) {
    match &expression {
        Expressions::Identifier(expression) => is_instance(&expression, Identifier::default()),
        _ => panic!("The expression must be an Identifier"),
    }

    let identifier = Identifier::from(expression);
    assert_eq!(identifier.value, expected_value.to_string());
    assert_eq!(identifier.token.lexeme, expected_value.to_string());
}
