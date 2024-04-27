"""
File: plugin.py
Author: Shaik Faizan Roshan Ali
Date: April 27 2024
Description: This module contains a pytest plugin for reporting test results to an API.

Usage:
    This plugin can be used to report test results to an external API during test execution.

    To enable reporting, use the following command-line options when running pytest:
        pytest --reporting_enabled --reporting_api_url <API_URL> --reporting_auth_token <AUTH_TOKEN>

    The API URL and authentication token must be provided for reporting to work properly.
"""
import uuid
import pytest
import requests
from datetime import datetime
from typing import Union, Dict, Any

from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.reports import CollectReport


class ReportPlugin:

    def __init__(self, config: pytest.Config): 
        """
        Initialize the ReportPlugin with configuration options.

        Args:
            config (pytest.Config): The pytest configuration object.
        """

        self.enabled = config.getoption("reporting_enabled", False)
        self.api_url = config.getoption("reporting_api_url", "")
        self.auth_token = config.getoption("reporting_auth_token", "")

    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionstart(self):
        """
        Hook function called at the beginning of the test session.
        Starts the test run if reporting is enabled.
        """

        # Reporting Enabled
        if self.enabled:
            self.run_id = self.start_test_run()
        
        return None

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item: Item):
        """
        Hook function called before each test setup.
        Starts a new test if reporting is enabled.
        """
        # reporting enabled 
        if self.enabled:

            test_name = item.name
            test_params = dict()
            timestamp = datetime.now()
            # Check if the test item has parameters
            if hasattr(item, "callspec") and hasattr(item.callspec, "params"):
                # Access the test parameters
                test_params = item.callspec.params
            
            self.test_id = self.start_test(test_name, test_params, timestamp, self.run_id)
        
        return None

    def pytest_report_teststatus(self, report: Union[CollectReport, TestReport]):
        """
        Hook function called when reporting test status.
        Reports the status of each test.
        """
        # reporting the test status
        duration = None
        test_status = None
        error_exception = None

        if report.when == "call":

            test_status = report.outcome
            duration = report.duration

            if hasattr(report.longrepr, 'reprcrash'):
                
                error_exception = str(report.longrepr.reprcrash) 

            # print(f"\nStatus at call: {test_status.capitalize()}\nDuration: {duration}")
            self.finish_test(self.test_id, test_status, error_exception, duration)

        if report.when == "setup" and report.outcome=="skipped":

            test_status = report.outcome
            #print(f"@ Setup {report.outcome}")
            self.finish_test(self.test_id, test_status, error_exception, duration)    
        
    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionfinish(self):
        """
        Hook function called at the end of the test session.
        Finishes the test run if reporting is enabled.
        """
        # At the end of session finish
        if self.enabled:

            self.finish_test_run(self.run_id)
            #print("Session run completed")

    def start_test_run(self) -> str:
        """
        Start a new test run and return its ID.

        Returns:
            str: The ID of the newly started test run.
        """
        # Check if reporting is enabled
        if self.enabled:
            # Generate a unique run ID
            run_id = str(uuid.uuid4())
            # Get the current time as the start time
            start_time = datetime.now()
            # Prepare the data for the request
            data = {
                "run_id": run_id,
                "start_time": start_time.isoformat()
            }
            # Send a POST request to start the test run
            start_test_run_endpoint = f"{self.api_url}/runs"
            start_test_run_response = requests.post(
                start_test_run_endpoint,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                json=data
            )
            # Return the ID of the started test run
            return run_id
        # Return None if reporting is disabled
        return None

    def finish_test_run(self, run_id: str) -> None:
        """
        Finish the test run identified by the given run ID.

        Args:
            run_id (str): The ID of the test run.

        Returns:
            None
        """
        # Check if reporting is enabled and run ID is provided
        if self.enabled and run_id:
            # Get the current time as the finish time
            finish_time = datetime.now()

            # Prepare the data for the request
            data = {
                "run_id": run_id,
                "finish_time": finish_time.isoformat()
            }

            # Send a POST request to finish the test run
            finish_test_run_endpoint = f"{self.api_url}/runs/{run_id}/finish"
            finish_run_response = requests.post(
                finish_test_run_endpoint,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                json=data
            )

        # Return None if reporting is disabled or run ID is not provided
        return None
    
    def replace_nan(self, obj: Dict) -> Any:
        """
        Replace NaN values in the object with None.

        Args:
            obj (Any): The object to process.

        Returns:
            Any: The object with NaN values replaced by None.
        """
        if isinstance(obj, dict):
            return {k: self.replace_nan(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.replace_nan(item) for item in obj]
        elif isinstance(obj, float) and obj != obj:  # Check for NaN
            return None
        else:
            return obj
        
    def start_test(self, test_name:str, test_param:Dict[str, Any], timestamp: datetime, run_id: str) -> Union[str, None]:
        """
        Starts a new test with the given parameters and returns the test ID.

        Args:
            test_name (str): The name of the test.
            test_param (Dict[str, Any]): The parameters of the test.
            timestamp (datetime): The timestamp when the test started.
            run_id (str): The ID of the test run to which the test belongs.

        Returns:
            Union[str, None]: The ID of the newly started test, or None if reporting is disabled.
        """

        if self.enabled:
            # Generate a unique test ID
            test_id = str(uuid.uuid4())

            # Replace NaN values in the test parameters with None
            test_param = self.replace_nan(test_param)

            # Prepare the data to be sent in the request
            data = {
                "test_id": test_id,
                "test_name": test_name,
                "test_param": test_param,
                "timestamp": timestamp.isoformat(),
                "test_run_id": run_id,
            }

            # Send a POST request to start the test
            start_test_endpoint = f"{self.api_url}/tests"
            start_test_response = requests.post(
                start_test_endpoint,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                json=data
            )

            # Return the test ID
            return test_id

        # Return None if reporting is disabled
        return None
  
    def finish_test(self, test_id: str, test_status: str, error_exception: str=None, duration: int=None) -> None:
        """
        Finishes the test with the given test ID and reports its status.

        Args:
            test_id (str): The ID of the test to finish.
            test_status (str): The status of the test (e.g., 'passed', 'failed', 'skipped').
            error_exception (str, optional): Any error or exception message associated with the test. Defaults to None.
            duration (int, optional): The duration of the test in milliseconds. Defaults to None.
        Returns:
            None
        """

        if self.enabled and test_id:
            # Prepare the data to be sent in the request
            data = {
                "test_id": test_id,
                "test_status": test_status,
                "error_exception": error_exception,
                "duration": duration
            }

            # Send a POST request to finish the test
            finish_test_run_endpoint = f"{self.api_url}/tests/{test_id}/finish"
            finish_test_response = requests.post(
                finish_test_run_endpoint,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                json=data
            )

        # Return None if reporting is disabled or test ID is not provided
        return None
