mod ast;
mod expressions;
mod parser;
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
        let source: &str = "set x = 5";
        let lexer: Lexer = Lexer::new(source.chars());
        let parser: Parser = Parser::new(lexer);

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
        let parser: Parser = Parser::new(lexer);

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
}
