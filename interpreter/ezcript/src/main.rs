extern crate clap;
use clap::{App, Arg};
use std::fs::File;
use std::io::prelude::*;
use std::io::{stdin, stdout, BufReader};

use ezcript_lexer::{
    lexer::Lexer,
    tokens::{Token, TokenKind},
};
use ezcript_result::Result;

fn main() -> Result<()> {
    let args = App::new("Ezcript-lang")
        .version("[1.0]")
        .author("Author: DaBitwisersWay")
        .about("\"A friendly programming language whose purpose is to teach new users in the tech world about the basics of programming languages and their use.\"")
        .arg(Arg::with_name("file")
            .value_name("FILE")
            .help("Sets the script for execute by the interpreter")
            .required(false)
            .takes_value(true))
        .get_matches();

    let file_name = args.value_of("file");

    if file_name == None {
        run_prompt()?;
    } else {
        run_file(file_name)?;
    }

    Ok(())
}

fn run_prompt() -> Result<()> {
    println!(
        "Welcom to Ezcript v1.0.0
Type \"help\" for more information"
    );
    loop {
        let mut source = String::new();
        print!(">> ");
        stdout().flush()?;
        stdin().read_line(&mut source).expect("Failed to read line");
        source.remove(source.len() - 1);
        let mut lexer = Lexer::new(source.chars());
        if source == "exit".to_string() {
            break;
        } else if source == "help" {
            println!("Some help message");
        } else {
            let mut tokens: Vec<Token> = Vec::new();
            for _i in 0..source.len() {
                let token: Token = lexer.next_token().unwrap().unwrap();
                if token.kind == TokenKind::Eof {
                    break;
                }
                tokens.push(token);
            }
            for token in tokens {
                println!("{}", token);
            }
        }
    }
    Ok(())
}

fn run_file(file_name: Option<&str>) -> Result<()> {
    let file = File::open(file_name.unwrap())?;
    let mut buf_reader = BufReader::new(file);
    let mut contents = String::new();
    buf_reader.read_to_string(&mut contents)?;
    let mut lexer = Lexer::new(contents.chars());
    for _i in 0..contents.len() {
        let token = lexer.next_token().unwrap().unwrap();
        if token.kind != TokenKind::Eof {
            println!("{}", token);
        } else {
            break;
        }
    }
    Ok(())
}
