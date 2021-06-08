use std::cmp::Ordering;
use std::collections::HashMap;
use std::fmt;
use std::hash::{Hash, Hasher};

/// All the tokens that the language accept
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TokenKind {
    Keyword,
    Ident,
    Number,
    String,
    Float,
    Boolean,
    Null,
    Not,

    // one char
    Plus,
    Minus,
    Star,
    Slash,
    Indent,
    Dedent,
    LParen,
    RParen,
    LBracket,
    RBracket,
    LBrace,
    RBrace,
    Colon,
    Comma,
    Equal,
    Less,
    Greater,
    Dot,
    Percent,
    Hashtag,
    EqEqual,
    BangEqual,
    LessEqual,
    GreaterEqual,
    DoublePlus,
    DoubleMinus,
    DoubleStar,
    DoubleSlash,
    PlusEqual,
    MinEqual,
    StarEqual,
    SlashEqual,
    PercentEqual,
    RArrow,
    Illegal,
    Eof,
}

impl TokenKind {
    /// The function return us a keyword if the argument we pass it is equal to a keyword in the
    /// RESERVED const
    pub fn reserved(keyword: &str) -> Option<&Self> {
        RESERVED.get(keyword)
    }
}

/// The Token structure, for create and manage the tokens from the Lexer
#[derive(Debug, Clone, PartialEq)]
pub struct Token {
    pub kind: TokenKind,
    pub lexeme: String,
    pub literal: Option<Literal>,
    pub line: u64,
}

impl Token {
    /// This function allow us to know if the type of the token that we pass it is a TokenKind
    /// variant or not
    pub fn in_types(&self, kinds: &[TokenKind]) -> bool {
        for kind in kinds {
            if &self.kind == kind {
                return true;
            }
        }
        false
    }
}

impl Default for Token {
    fn default() -> Self {
        Token {
            kind: TokenKind::Eof,
            lexeme: "".to_string(),
            literal: None,
            line: 1,
        }
    }
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "Type: {:?}, Lexeme: {}, Literal: {:?} : [line {}]",
            self.kind, self.lexeme, self.literal, self.line
        )
    }
}

/// Describe a Null, Boolean, Number or String value
#[derive(Debug, Clone)]
pub enum Literal {
    Null,
    Boolean(bool),
    Number(f64),
    String(String),
}

impl Eq for Literal {}

impl Hash for Literal {
    fn hash<H: Hasher>(&self, state: &mut H) {
        match *self {
            Literal::Null => "".hash(state),
            Literal::Boolean(b) => b.hash(state),
            Literal::Number(f) => f.to_bits().hash(state),
            Literal::String(ref s) => s.hash(state),
        }
    }
}

impl PartialEq for Literal {
    fn eq(&self, other: &Literal) -> bool {
        match *self {
            Literal::Null => match *other {
                Literal::Null => true,
                _ => false,
            },
            Literal::Boolean(ref a) => match *other {
                Literal::Boolean(ref b) => a.eq(b),
                _ => false,
            },
            Literal::Number(ref a) => match *other {
                Literal::Number(ref b) => a.eq(b),
                _ => false,
            },
            Literal::String(ref a) => match *other {
                Literal::String(ref b) => a.eq(b),
                _ => false,
            },
        }
    }
}

impl PartialOrd<Self> for Literal {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        match (self, other) {
            (&Literal::Null, &Literal::Null) => Some(Ordering::Equal),
            (&Literal::String(ref l), &Literal::String(ref r)) => l.partial_cmp(r),
            (&Literal::Number(ref l), &Literal::Number(ref r)) => l.partial_cmp(r),
            (&Literal::Boolean(ref l), &Literal::Boolean(ref r)) => l.partial_cmp(r),
            _ => None,
        }
    }
}

impl fmt::Display for Literal {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            Literal::Null => write!(f, "null"),
            Literal::Boolean(b) => write!(f, "{}", b),
            Literal::Number(n) => write!(f, "{}", n),
            Literal::String(ref s) => write!(f, "{}", s),
        }
    }
}

lazy_static! {
    static ref RESERVED: HashMap<&'static str, TokenKind> = [
        ("set", TokenKind::Keyword),
        ("const", TokenKind::Keyword),
        ("use", TokenKind::Keyword),
        ("from", TokenKind::Keyword),
        ("true", TokenKind::Boolean),
        ("false", TokenKind::Boolean),
        ("if", TokenKind::Keyword),
        ("else", TokenKind::Keyword),
        ("elseif", TokenKind::Keyword),
        ("and", TokenKind::Keyword),
        ("or", TokenKind::Keyword),
        ("not", TokenKind::Not),
        ("is", TokenKind::Keyword),
        ("in", TokenKind::Keyword),
        ("do", TokenKind::Keyword),
        ("while", TokenKind::Keyword),
        ("break", TokenKind::Keyword),
        ("for", TokenKind::Keyword),
        ("each", TokenKind::Keyword),
        ("func", TokenKind::Keyword),
        ("return", TokenKind::Keyword),
        ("match", TokenKind::Keyword),
        ("class", TokenKind::Keyword),
        ("inherit", TokenKind::Keyword),
        ("null", TokenKind::Null),
    ]
    .iter()
    .cloned()
    .collect();
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_tokens() {
        for (key, value) in RESERVED.iter() {
            let kind: TokenKind = *TokenKind::reserved(key).unwrap();
            assert_eq!(kind, *value);
        }
    }
}
