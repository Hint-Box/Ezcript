use std::error::Error;
use std::fmt;
use std::io;
use std::result;
// #[macro_use]
// extern crate lazy_static;

/// A Ezcript-Specific Result Type
pub type Result<T> = result::Result<T, EzcriptError>;

/// A Lox-Specific Error
#[derive(Debug)]
pub enum EzcriptError {
    // /// Returned if the CLI command is used incorrectly
    // Usage,
    /// Returned if there is an error reading from a file or stdin
    IO(io::Error),
    /// Returned if the scanner encounters an error
    Lexical(u64, String, String),
    /// Returned if the parser encounters an error
    Parse(u64, String, String),
}

impl From<io::Error> for EzcriptError {
    fn from(err: io::Error) -> EzcriptError {
        EzcriptError::IO(err)
    }
}

impl fmt::Display for EzcriptError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            // EzcriptError::Usage => write!(f, "{:?}", USAGE),
            EzcriptError::IO(ref e) => e.fmt(f),
            EzcriptError::Lexical(ref line, ref msg, ref whence) => {
                write!(f, "Lexical Error [line {}] {}: {}", line, msg, whence)
            }
            EzcriptError::Parse(ref line, ref msg, ref near) => {
                write!(f, "Parse Error [line {}] {}: near {}", line, msg, &near)
            }
        }
    }
}

impl Error for EzcriptError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match *self {
            EzcriptError::IO(ref e) => e.source(),
            _ => None,
        }
    }
}

// lazy_static! {
//     #[derive(Debug)]
//     pub static ref USAGE: String = "usage: ezcript [option]
// Options and Arguments

//     file:   read program from an script file".to_string();
// }
