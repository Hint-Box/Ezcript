mod ast;

/// Boxer converts a type its Boxed form
pub trait Boxer {
    /// Convert to a boxed version
    fn boxed(self) -> Box<Self>
    where
        Self: Sized,
    {
        Box::new(self)
    }
}
