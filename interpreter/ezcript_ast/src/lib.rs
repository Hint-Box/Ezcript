mod ast;
mod expressions;
mod statements;

#[macro_use]
extern crate utils;

#[cfg(test)]
mod test {
    use super::*;
    use utils::is_instance;

    // #[test]
    // fn test_parse_program() {
    //     let source: &str = "set x = 5";
    //     let lexer: Lexer = Lexer::new(source);
    //     let parser: Parser = Parser::new(lexer);

    //     let program: Program = parser.parse_program();

    //     if program == None {
    //         panic!("This value shouldn't be None");
    //     }
    // }
}
