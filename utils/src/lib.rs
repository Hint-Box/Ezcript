// =============================================================================
//     * Utility functions *
// =============================================================================
pub fn is_instance<U, T>(_: &U, _: T) {
    let value = std::any::type_name::<U>();
    let real = std::any::type_name::<T>();

    if value != real {
        panic!("The value type of the two arguments are not the same!");
    }
}

// =============================================================================
//     * Utility macros *
// =============================================================================
/// Macro for testing purpose.
/// Ensures that the value passed as a parameter is not None.
#[macro_export]
macro_rules! is_not_none {
    ($value:expr) => {
        match $value {
            Some(val) => (),
            None => panic!("The value cannot be None"),
        }
    };
}

#[cfg(test)]
mod test {
    use super::*;

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
    fn test_is_instance() {
        let codo = Codo {
            codo: "mi codo".to_string(),
            num: 42,
        };

        is_instance(&codo, Codo::new());
    }

    #[test]
    fn test_not_none() {
        let not_none = Some("un string");
        is_not_none!(not_none);
    }

    #[test]
    #[should_panic]
    fn test_none() {
        let is_none: Option<&str> = None;
        is_not_none!(is_none);
    }
}
