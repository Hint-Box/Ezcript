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
