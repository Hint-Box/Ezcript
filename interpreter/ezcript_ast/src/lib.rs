mod ast;
mod expressions;
mod statements;

// TODO: Convert this into a macro creating a lib just for macros and also create a macro for know
// if a value is not None
// fn is_instance<U, T>(_: &U, _: T) -> bool {
//     let value_type = std::any::type_name::<U>();
//     let the_type = std::any::type_name::<T>();

//     if value_type != the_type {
//         panic!("The value type of the two arguments are not the same!");
//     }

//     true
// }

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

    #[derive(Debug)]
    struct Codo {
        codo: String,
        num: u64,
    }

    impl Codo {
        pub fn new() -> Self {
            Self {
                codo: "".to_string(),
                num: 0,
            }
        }
    }

    #[test]
    fn testing() {
        let codo = Codo {
            codo: "mi codo".to_string(),
            num: 42,
        };

        is_instance(&codo, Codo::new());
    }
}
