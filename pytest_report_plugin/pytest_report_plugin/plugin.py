import pytest
import requests

class ReportPlugin:

    def __init__(self, config):
        self.enabled = config.getoption("reporting_enabled", False)
        self.api_url = config.getoption("reporting_api_url", "")
        self.auth_token = config.getoption("reporting_auth_token", "")

    def start_test_run(self):
        if not self.enabled:
            return None
        response = requests.post(
            f"{self.api_url}/runs/",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

        print("start test run function is executed")
        return response.json()["run_id"] if response.status_code == 201 else None

    def finish_test_run(self, run_id):
        if not self.enabled:
            return
        requests.post(
            f"{self.api_url}/runs/{run_id}/finish/",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )
        print("finish test run function is executed")

    def start_test(self, test_name):
        if not self.enabled:
            return None
        response = requests.post(
            f"{self.api_url}/tests/",
            json={"name": test_name},
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )
        print("start test run is executed")
        return response.json()["test_id"] if response.status_code == 201 else None

    def finish_test(self, test_id, status):
        if not self.enabled:
            return
        requests.post(
            f"{self.api_url}/tests/{test_id}/finish/",
            json={"status": status},
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

        print("finish test function is executed")

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

@pytest.fixture(scope="session")
def report_plugin_config(request):
    return {
        "reporting_enabled": request.config.getoption("--reporting-enabled"),
        "reporting_api_url": request.config.getoption("--reporting-api-url"),
        "reporting_auth_token": request.config.getoption("--reporting-auth-token"),
    }

@pytest.fixture(scope="session")
def report_plugin(report_plugin_config):
    return ReportPlugin(report_plugin_config)
