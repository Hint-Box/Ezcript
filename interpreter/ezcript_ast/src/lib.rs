mod ast;
mod expressions;
mod parser;
mod statements;

#[macro_use]
extern crate utils;

#[cfg(test)]
mod test {
    use super::*;
    use crate::ast::Program;
    use crate::parser::Parser;
    use ezcript_lexer::lexer::Lexer;
    use utils::is_instance;

    #[test]
    fn test_parse_program() {
        let source: &str = "set x = 5";
        let lexer: Lexer = Lexer::new(source.chars());
        let parser: Parser = Parser::new(lexer);

        let program: Program = parser.parse_program();

        is_not_none!(Some(program));
    }
}
