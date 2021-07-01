pub mod ast;
mod expressions;
pub mod parser;
mod statements;

#[macro_use]
extern crate utils;

#[cfg(test)]
mod test {
    use super::*;
    use crate::ast::ASTNode;
    use crate::ast::Program;
    use crate::parser::Parser;
    use ezcript_lexer::lexer::Lexer;
    use utils::is_instance;

    #[test]
    fn test_parse_program() {
        let source: &str = "set x = 5\n";
        let lexer: Lexer = Lexer::new(source.chars());
        let mut parser: Parser = Parser::new(lexer);

        let program: Option<Program> = parser.parse_program();

        is_not_none!(program.as_ref());
        is_instance(&program, Program::new(Vec::new()))
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
                statements::Statements::SetStatement(statement) => {
                    assert_eq!(statement.token_lexeme(), "set");
                    is_instance(&Some(statement), Some(statements::SetStatement::default()))
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
                statements::Statements::SetStatement(ref statement) => {
                    is_instance(
                        &Some(statement.clone()),
                        Some(statements::SetStatement::default()),
                    );
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
}
