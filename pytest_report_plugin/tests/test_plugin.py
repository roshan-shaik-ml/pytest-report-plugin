# tests/test_plugin.py
import pytest
from hypothesis import strategies as st, given

@pytest.mark.parametrize(
    "left, right",
    (
        (2, 2),
        pytest.param(3.14, 5.55, marks=pytest.mark.skip("Skipped!")),
        (float("nan"), 42),
    ),
)
def test_examples(left, right):
    assert left + right == right + left


NUMBER = st.integers() | st.floats()

@given(left=NUMBER, right=NUMBER)
def test_properties(left, right):
    assert left + right == right + left
