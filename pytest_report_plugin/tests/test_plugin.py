# tests/test_plugin.py

import pytest
from hypothesis import strategies as st, given
from pytest_report_plugin.plugin import ReportPlugin 
import responses

@pytest.fixture
def report_plugin():
    # Mock the HTTP requests
    with responses.RequestsMock() as rsps:
        # Mock the responses for /runs/ endpoint
        rsps.add(responses.POST, "http://example.com/runs/", json={"run_id": 123}, status=201)
        # Mock the responses for /tests/ endpoint
        rsps.add(responses.POST, "http://example.com/tests/", json={"test_id": 456}, status=201)
        
        # Create an instance of the plugin
        plugin = ReportPlugin(enabled=True, api_url="http://example.com", auth_token="dummy_token")
        
        yield plugin

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

