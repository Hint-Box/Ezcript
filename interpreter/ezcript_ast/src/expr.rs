use ezcript_lexer::tokens::Token;

/// The Expression Node
#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub enum Expr {
    Literal(Token),
    Grouping(Box<Expr>),
    Prefix(Token, Box<Expr>),
    Infix(Box<Expr>, Token, Box<Expr>),
}

/// Implement the visitor trait
///
/// An implementor of Visitor<T> should recursively walk
/// a `Expr` and returns `T`.
pub trait Visitor<T> {
    /// Visit an expression
    fn visit_expr(&mut self, _expr: &Expr) -> T {
        unimplemented!()
    }

    fn visit_literal(&mut self, _expr: &Expr, _lit: &Token) -> T {
        self.visit_expr(_expr)
    }

    fn visit_grouping(&mut self, _expr: &Expr, _inside: &Expr) -> T {
        self.visit_expr(_expr)
    }

    fn visit_prefix(&mut self, _expr: &Expr, _op: &Token, _rhs: &Expr) -> T {
        self.visit_expr(_expr)
    }

    fn visit_infix(&mut self, _expr: &Expr, _lhs: &Expr, _op: &Token, _rhs: &Expr) -> T {
        self.visit_expr(_expr)
    }
}

impl Expr {
    pub fn accept<T>(&self, v: &mut dyn Visitor<T>) -> T {
        match *self {
            Expr::Literal(ref lit) => v.visit_literal(self, lit),
            Expr::Grouping(ref inside) => v.visit_grouping(self, inside.as_ref()),
            Expr::Prefix(ref op, ref rhs) => v.visit_prefix(self, op, rhs.as_ref()),
            Expr::Infix(ref lhs, ref op, ref rhs) => {
                v.visit_infix(self, lhs.as_ref(), op, rhs.as_ref())
            }
        }
    }
}
