extern crate clap;
use clap::{App, Arg};
use ezcript_result::Result;
use ezcript_runner::{run_file, run_prompt};

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
