"""
Database Test Manager
=====================

This module provides a TestManager class for managing test runs and tests in a database. It also includes functionality to reset the database and perform example test operations.

Classes:
- TestManager: Manages interactions with the database, including creating test runs, tests, finishing tests and test runs, printing tables, and more.

Functions:
- reset_and_test_with_example: Resets the database, performs example test operations, and prints tables.

Usage:
- Import this module and create an instance of the TestManager class to interact with the database.
- Use methods of the TestManager class to perform various database operations, such as creating test runs, tests, finishing tests, printing tables, and more.
- Call the reset_and_test_with_example function to reset the database, perform example test operations, and print tables.

Dependencies:
- uuid: Provides functions for generating and working with universally unique identifiers (UUIDs).
- logging: Allows logging of messages, errors, and other information.
- subprocess: Enables running shell commands from within Python.
- datetime: Provides classes for manipulating dates and times.
- sqlalchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- SetupDatabase: Contains the database models (TestRun, Test) and initialization logic.

Note:
- This module assumes the existence of a SetupDatabase module containing the database models and initialization logic.
"""

import uuid
import logging
import subprocess
from typing import Dict, Any
from datetime import datetime
from sqlalchemy import create_engine
from SetupDatabase import TestRun, Test
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add FileHandler to save logs to a file
file_handler = logging.FileHandler('logs/Database_TestManager.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class TestManager:
    """
    Manages interactions with the database for test runs and tests.

    Methods:
    - create_test_run: Creates a new test run in the database.
    - create_test: Creates a new test in the database.
    - finish_test: Marks a test as finished in the database.
    - finish_test_run: Marks a test run as finished in the database.
    - print_tables: Prints information from the database tables.
    - empty_table: Empties the specified database table.
    - get_tests_by_run_id: Retrieves tests associated with a specific test run ID.
    - get_all_tests: Retrieves all tests from the database.
    """
    def __init__(self, db):
        self.db = db
        
    def create_test_run(self, test_run_id: uuid.UUID, start_time: datetime):
        """
        Creates a new test run in the database.

        Parameters:
        - test_run_id (uuid.UUID): Unique identifier for the test run.
        - start_time (datetime): Start time of the test run.

        Returns:
        - TestRun: The created TestRun object.
        """
        try:
            self.db.begin()  # Begin a transaction

            test_run = TestRun(test_run_id=test_run_id, start_time=start_time)
            self.db.add(test_run)
            self.db.commit()  # Commit the transaction
            logger.info("Test run creation successful")
            return test_run

        except SQLAlchemyError as e:
            self.db.rollback()  # Rollback the transaction in case of error
            logger.error(f"Error occurred while creating test run: {e}")
            raise e

    def create_test(self, test_id: uuid.UUID, test_name: str, test_parameters: Dict[str, Any], timestamp: datetime,  test_run_id: uuid.UUID):
        """
        Creates a new test in the database.

        Parameters:
        - test_id (uuid.UUID): Unique identifier for the test.
        - test_name (str): Name of the test.
        - test_parameters (Dict[str, Any]): Parameters associated with the test.
        - timestamp (datetime): Timestamp of when the test was created.
        - test_run_id (uuid.UUID): ID of the test run associated with the test.

        Returns:
        - Test: The created Test object.
        """
        try:
            test = Test(test_id=test_id, test_name=test_name, test_run_id=test_run_id, test_parameters=test_parameters, timestamp=timestamp)
            self.db.add(test)
            self.db.commit()
            logger.info("Test creation successful")
            return test

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error occurred while creating test: {e}")
            raise e

    def finish_test(self, test_id: uuid.UUID, test_status: str, duration: int, error_exception: str = None):
        """
        Marks a test as finished in the database.

        Parameters:
        - test_id (uuid.UUID): Unique identifier for the test.
        - test_status (str): Status of the test (e.g., "PASSED", "FAILED").
        - duration (int): Duration of the test execution.
        - error_exception (str, optional): Exception message if the test encountered an error.

        Returns:
        - Test: The updated Test object.
        """
        try:
            test = self.db.query(Test).filter(Test.test_id == test_id).first()
            if test:
                test.test_status = test_status
                test.duration = duration
                test.error_exception = error_exception
                self.db.commit()
                logger.info("Test finished successfully")
                return test
            else:
                logger.warning("Test not found.")
                return None

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error occurred while finishing test: {e}")
            raise e

    def finish_test_run(self, test_run_id: int, finish_time: datetime):
        """
        Marks a test run as finished in the database.

        Parameters:
        - test_run_id (int): ID of the test run to finish.
        - finish_time (datetime): Finish time of the test run.

        Raises:
        - ValueError: If the test run ID is not found.

        Returns:
        - None
        """
        try:
            test_run = self.db.query(TestRun).filter(TestRun.test_run_id == test_run_id).first()
            if test_run:
                test_run.end_time = finish_time
                self.db.commit()
                logger.info("Test run finished successfully")
            else:
                raise ValueError("Test run ID not found")

        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            logger.error(f"Error occurred while finishing test run: {e}")
            raise e

    def print_tables(self):
        """
        Prints information from the database tables.
        """
        try:
            logger.info("Printing tables")
            test_runs = self.db.query(TestRun).all()
            for test_run in test_runs:
                logger.info(f"Test Run ID: {test_run.test_run_id}, Start Time: {test_run.start_time}, End Time: {test_run.end_time}")

            tests = self.db.query(Test).all()
            for test in tests:
                logger.info(f"Test ID: {test.test_id}, Name: {test.test_name}, Status: {test.test_status}, Test Run ID: {test.test_run_id}")

        except SQLAlchemyError as e:
            logger.error(f"Error occurred while printing tables: {e}")

    def empty_table(self, Model):
        """
        Empties the specified database table.

        Parameters:
        - Model: The SQLAlchemy model corresponding to the table to be emptied.

        Raises:
        - SQLAlchemyError: If an error occurs while emptying the table.

        Returns:
        - None
        """
        try:
            logger.info(f"Emptying {Model.__tablename__} table")
            self.db.query(Model).delete()
            self.db.commit()
            logger.info(f"Emptied {Model.__tablename__} table successfully")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error occurred while emptying {Model.__tablename__} table: {e}")
            raise e

    def get_tests_by_run_id(self, run_id):
        """
        Retrieves tests associated with a specific test run ID.

        Parameters:
        - run_id (str): ID of the test run.

        Returns:
        - List[Test]: List of Test objects associated with the specified test run ID, or None if an error occurs.
        """
        try:
            logger.info(f"Getting tests by run ID: {run_id}")
            try:
                run_id = uuid.UUID(run_id)
            except ValueError:
                logger.warning("Invalid UUID format")
                return None
            tests = self.db.query(Test).filter_by(test_run_id=run_id).all()
            return tests
        except SQLAlchemyError as e:
            logger.error(f"An error occurred: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

    def get_all_tests(self):
        """
        Retrieves all tests from the database.

        Returns:
        - List[Test]: List of all Test objects in the database, or None if an error occurs.
        """
        try:
            logger.info("Getting all tests")
            tests = self.db.query(Test).all()
            return tests
        except SQLAlchemyError as e:
            logger.error(f"An error occurred: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

def reset_and_test_with_example():
    """
    Resets the database, creates example test runs and tests, and prints table information.
    """
    SQLALCHEMY_DATABASE_URL = "sqlite:///plugin_app.sqlite"
    subprocess.call("python3 SetupDatabase.py", shell=True)

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    Session = sessionmaker(bind=engine)
    db = Session()
    
    test_manager = TestManager(db)

    test_run_id = uuid.uuid4()
    start_time = datetime.now()
    created_test_run = test_manager.create_test_run(test_run_id, start_time)
    print("Created Test Run:", created_test_run)

    for i in range(0, 4):
        test_id = uuid.uuid4()
        test_name = "Example Test"
        test_parameters = {"param1": "value1", "param2": "value2"}
        test_status = "PASSED"
        timestamp = datetime.now()
        test_run_id = created_test_run.test_run_id
        created_test = test_manager.create_test(test_id, test_name, test_parameters, timestamp, test_run_id)
        print("Created Test:", created_test)

        test_status = "PASSED"
        duration = i*10
        error_exception = "Something is wrong!!!"
        finished_test = test_manager.finish_test(created_test.test_id, test_status, duration, error_exception)
        if finished_test:
            print("Finished Test:", finished_test)
        else:
            print("Test not found.")

    finish_time = datetime.now()
    try:
        test_manager.finish_test_run(created_test_run.test_run_id, finish_time)
        print("Finished Test Run")
    except ValueError as e:
        print("Error:", e)

    test_manager.print_tables()

    test_manager.empty_table(Test)
    test_manager.empty_table(TestRun)

    db.close()

if __name__ == "__main__":
    reset_and_test_with_example()
