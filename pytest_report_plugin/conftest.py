import pytest
from pytest_report_plugin.plugin import ReportPlugin


@pytest.fixture
def report_plugin_config(request):

    # Get option values or use defaults
    reporting_enabled = request.config.getoption("--reporting-enabled", default=False)
    reporting_api_url = request.config.getoption("--reporting-api-url", default="")
    reporting_auth_token = request.config.getoption("--reporting-auth-token", default="")
    
    # Validate option values if needed
    
    return {
        "reporting_enabled": reporting_enabled,
        "reporting_api_url": reporting_api_url,
        "reporting_auth_token": reporting_auth_token
    }

def pytest_addoption(parser):
    parser.addoption("--reporting-enabled", action="store_true", help="Enable reporting to the test report service")
    parser.addoption("--reporting-api-url", action="store", default="", help="URL of the test report service API")
    parser.addoption("--reporting-auth-token", action="store", default="", help="Authorization token for accessing the test report service")

@pytest.fixture
def report_plugin(report_plugin_config):
    return ReportPlugin(report_plugin_config)