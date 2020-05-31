import seq
import pytest


########################
# Test data
########################

# 5-tuples representing each figurate number function and the first 5 numbers of that type
figurate_test_params = (
    # label (id), generation function, inverse function, inclusion function, first 5 values
    ('triangle', seq.triangle_num, seq.which_triangle_num, seq.is_triangular, (1, 3, 6, 10, 15)),
    ('square', seq.square_num, seq.which_square_num, seq.is_square, (1, 4, 9, 16, 25)),
    ('pentagonal', seq.pentagonal_num, seq.which_pentagonal_num, seq.is_pentagonal, (1, 5, 12, 22, 35)),
    ('hexagonal', seq.hexagonal_num, seq.which_hexagonal_num, seq.is_hexagonal, (1, 6, 15, 28, 45)),
    ('heptagonal', seq.heptagonal_num, seq.which_heptagonal_num, seq.is_heptagonal, (1, 7, 18, 34, 55)),
    ('octagonal', seq.octagonal_num, seq.which_octagonal_num, seq.is_octagonal, (1, 8, 21, 40, 65)),
)


########################
# Tests
########################
@pytest.mark.parametrize(
    "label, func, inverse_func, incl_func, args",
    figurate_test_params,
    ids=(f[0] for f in figurate_test_params)
)
def test_figurate(label, func, inverse_func, incl_func, args):
    """Test figurate number functions with the first 5 numbers of each given type."""
    for k, n in enumerate(args, start=1):
        assert func(k) == n, f"Failed to calculate {k}th {label} number"
        assert inverse_func(n) == k, f"Failed to invert {k}th {label} number"
        assert incl_func(n), f"Failed to verify inclusion of {n} in {label} numbers"
