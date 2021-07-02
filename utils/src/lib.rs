// =============================================================================
//     * Utility functions *
// =============================================================================
/// Function that let us know if the type of the first argument is equal to the type of the second
/// argumen.
///
/// **Examples**
/// ```
/// use utils::is_instance;
/// use std::collections::HashMap;
/// let text: String = String::from("Hola");
/// is_instance(&text, String::new());
/// ```
pub fn is_instance<U, T>(_: &U, _: T) -> bool {
    let value = std::any::type_name::<U>();
    let real = std::any::type_name::<T>();

    if value != real {
        panic!("The value {} is not the same as value {}!", value, real);
    }
    true
}

// =============================================================================
//     * Utility macros *
// =============================================================================
/// Macro for testing purpose. The macro ensures that the value passed as a parameter is not None.
/// The argument of the macro must be an Option<T> value.
/// **Examples**
/// ```
/// use utils::is_not_none;
/// is_not_none!(Some(5));
/// is_not_none!(Some("Hello"));
/// // If you use something like: "is_not_none(None);" the program will panic.
/// ```
#[macro_export]
macro_rules! is_not_none {
    ($value:expr) => {
        match $value {
            Some(_) => (),
            None => panic!("The value cannot be None"),
        }
    };
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_is_instance() {
        is_instance(&"hola".to_string(), String::new());
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
