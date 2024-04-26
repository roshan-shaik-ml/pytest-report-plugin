import pytest
from _pytest._code.code import ExceptionInfo
import requests
from datetime import datetime 
import uuid
from _pytest.outcomes import skip

class ReportPlugin:

    def __init__(self, config: pytest.Config): 
        print("plugin initiated")
        self.enabled = config.getoption("reporting_enabled", False)
        self.api_url = config.getoption("reporting_api_url", "")
        self.auth_token = config.getoption("reporting_auth_token", "")

    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionstart(self):
        if self.enabled:
            self.run_id = self.start_test_run()

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        if self.enabled:
            self.test_id = self.start_test(item.name, self.run_id)

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_teardown(self, item):

        outcome = "Unknown"
        if not hasattr(item.session, 'last_testsfailed_status'):
            item.session.last_testsfailed_status = 0

        if item.session.testsfailed and item.session.testsfailed > item.session.last_testsfailed_status:
            outcome="Failed"
        else:
            outcome="Passed"

        self.finish_test(self.test_id, outcome)

    # @pytest.hookimpl(tryfirst=True)
    # def pytest_runtest_makereport(self, item, call):

    #     if call.when != "teardown":
    #         return "Exec Failed"
    #     excinfo = call.excinfo
    #     outcome = "unknown"
    #     if not call.excinfo:
    #         outcome = "passed"
    #     else:
    #         if not isinstance(excinfo, ExceptionInfo):
    #             outcome = "failed"
    #         elif isinstance(excinfo.value, skip.Exception):
    #             outcome = "skipped"
    #         else:
    #             outcome = "failed"
    #     self.finish_test(self.test_id, outcome)       
        
    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionfinish(self):
        print("session run completed")
        if self.enabled:
            self.finish_test_run(self.run_id)

    def start_test_run(self):
        if not self.enabled:
            return None
        
        run_id = str(uuid.uuid4())
        start_time = datetime.now()

        data = {

            "run_id" : run_id,
            "start_time": str(start_time)
        }
        start_test_run_response = requests.post(

            f"{self.api_url}/runs",
            headers={"Authorization": f"Bearer {self.auth_token}"},
            json=data
        )

        return run_id

    def finish_test_run(self, run_id):

        if not self.enabled or not run_id:
            return
        
        finish_time = str(datetime.now())

        data = {

            "finish_time": finish_time
        }
        finish_run_response = requests.post(

            f"{self.api_url}/runs/{run_id}/finish",
            headers={"Authorization": f"Bearer {self.auth_token}"},
            json=data
        )

    def start_test(self, test_name, run_id: str):

        if not self.enabled:
            return None
        
        test_id = str(uuid.uuid4())
        name = test_name
        
        data = {

            "test_id": test_id,
            "test_name": test_name,
            "test_run_id": run_id
        }

        start_test_response = requests.post(

            f"{self.api_url}/tests",
            headers={"Authorization": f"Bearer {self.auth_token}"},
            json=data
        )
        return test_id

    def finish_test(self, test_id, status):

        if not self.enabled or not test_id:
            return
        
        data = {

            "status": status
        }

        finish_test_response = requests.post(

            f"{self.api_url}/tests/{test_id}/finish",
            headers={"Authorization": f"Bearer {self.auth_token}"},
            json=data
        )
