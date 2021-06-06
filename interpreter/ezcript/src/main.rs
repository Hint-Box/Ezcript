extern crate clap;
use clap::{App, Arg};
use std::fs::File;
use std::io::prelude::*;
use std::io::{stdin, stdout, BufReader};
use std::process::exit;

use ezcript_lexer::{
    lexer::Lexer,
    tokens::{Token, TokenKind},
};
use ezcript_result::{Error, Result};

fn main() -> Result<()> {
    let args = App::new("Ezcript-lang")
        .version("[1.0]")
        .author("Author: DaBitwisersWay")
        .about("\"A friendly programming language whose purpose is to teach new users in the tech world about the basics of programming languages and their use.\"")
        .arg(Arg::with_name("file")
            .short("f")
            .long("file")
            .value_name("FILE")
            .help("Sets the script for execute by the interpreter")
            .required(false)
            .takes_value(true))
        .get_matches();

    let file_name = args.value_of("file");

    if file_name == None {
        // run_prompt()?;
        println!("Hola, no hay file");
    } else {
        run_file(file_name)?;
    }

    Ok(())
}

fn run_file(file_name: Option<&str>) -> Result<()> {
    let file = File::open(file_name.unwrap())?;
    let mut buf_reader = BufReader::new(file);
    let mut contents = String::new();
    buf_reader.read_to_string(&mut contents)?;
    let mut lexer = Lexer::new(contents.chars());
    for i in 0..contents.len() {
        let token = lexer.next_token().unwrap().unwrap();
        if token.kind != TokenKind::Eof {
            println!("{}", token);
        } else {
            break;
        }
    }
    Ok(())
}
