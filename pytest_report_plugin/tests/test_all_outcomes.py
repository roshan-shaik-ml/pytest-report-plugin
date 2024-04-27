import pytest

def test_passing():
    assert 1 + 1 == 2
    
def test_error():
    with pytest.raises(ZeroDivisionError):
        1 / 0

@pytest.mark.skip(reason="Test is skipped for a reason")
def test_skipped():
    assert False


@pytest.mark.xfail(reason="Expected failure")
def test_expected_failure():
    assert False

def test_unexpected_failure():
    assert False
