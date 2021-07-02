use ansi_term::Colour::RGB;
use std::fs::File;
use std::io::prelude::*;
use std::io::{stdin, stdout, BufReader};

use ezcript_lexer::{
    lexer::Lexer,
    tokens::{Token, TokenKind},
};
use ezcript_result::Result;

pub fn run_prompt() -> Result<()> {
    #[cfg(target_os = "windows")]
    ansi_term::enable_ansi_support();
    println!(
        "Welcom to Ezcript v1.0.0
Type \"help\" for more information"
    );
    loop {
        let mut source = String::new();
        print!("{}", RGB(31, 151, 116).bold().paint(">> "));
        stdout().flush()?;
        stdin().read_line(&mut source).expect("Failed to read line");
        let mut lexer = Lexer::new(source.chars());
        if source == "exit\n".to_string() {
            break;
        }
        loop {
            let token: Token = match lexer.next_token() {
                Some(result) => match result {
                    Ok(token) => token,
                    Err(e) => {
                        println!("{}", e.to_string());
                        break;
                    }
                },
                None => break,
            };

            if token.kind != TokenKind::Eof {
                println!("{}", token);
            } else {
                break;
            }
        }
    }
    Ok(())
}

pub fn run_file(file_name: Option<&str>) -> Result<()> {
    let file = File::open(file_name.unwrap())?;
    let mut buf_reader = BufReader::new(file);
    let mut contents = String::new();
    buf_reader.read_to_string(&mut contents)?;
    let mut lexer = Lexer::new(contents.chars());
    loop {
        let token: Token = match lexer.next_token() {
            Some(result) => match result {
                Ok(token) => token,
                Err(e) => {
                    println!("{}", e.to_string());
                    break;
                }
            },
            None => break,
        };

        if token.kind != TokenKind::Eof {
            println!("{}", token);
        } else {
            break;
        }
    }
    Ok(())
}
