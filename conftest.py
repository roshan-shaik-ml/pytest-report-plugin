import pytest
from pytest_report_plugin.plugin import ReportPlugin

# Allows plugins and conftest files to perform initial configuration.
def pytest_configure(config):

    config.pluginmanager.register(ReportPlugin(config))

# Used to register options and settings.
def pytest_addoption(parser):
    parser.addoption(
        "--reporting-enabled",
        action="store_true",
        help="Enable reporting to the test report service",
    )
    parser.addoption(
        "--reporting-api-url",
        action="store",
        default="",
        help="URL of the test report service API",
    )
    parser.addoption(
        "--reporting-auth-token",
        action="store",
        default="",
        help="Authorization token for accessing the test report service",
    )

@pytest.fixture(scope="class")
def report_plugin_config(request):
    # Get option values or use defaults
    reporting_enabled = request.config.option.reporting_enabled
    reporting_api_url = request.config.option.reporting_api_url
    reporting_auth_token = request.config.option.reporting_auth_token

    # Validate option values if needed

    return {
        "reporting_enabled": reporting_enabled,
        "reporting_api_url": reporting_api_url,
        "reporting_auth_token": reporting_auth_token,
    }

@pytest.fixture(scope="class")
def report_plugin(report_plugin_config):
    print("Initializing ReportPlugin...")
    plugin = ReportPlugin(report_plugin_config)
    print("ReportPlugin initialized successfully.")
    return plugin
