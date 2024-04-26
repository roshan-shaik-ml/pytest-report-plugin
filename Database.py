import subprocess
from datetime import datetime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from DatabaseModels import TestRun, Test  # Import your TestRun and Test models

class TestManager:
    def __init__(self, db: Session):
        self.db = db

    def create_test_run(self):
        try:
            self.db.begin()  # Begin a transaction

            # Check if there's an ongoing test run that hasn't ended yet
            ongoing_test_run = self.db.query(TestRun).filter(TestRun.end_time == None).first()

            if ongoing_test_run:
                return ongoing_test_run
            else:
                test_run = TestRun(start_time=datetime.now())
                self.db.add(test_run)
                self.db.commit()  # Commit the transaction
                self.db.refresh(test_run)
                return test_run

        except SQLAlchemyError as e:
            self.db.rollback()  # Rollback the transaction in case of error
            raise e

    def create_test(self, name: str, test_run_id: int):
        # Create a new test associated with the given test run and set the name
        test = Test(name=name, test_run_id=test_run_id, status=None)
        self.db.add(test)
        self.db.commit()
        self.db.refresh(test)
        return test

    def finish_test(self, test_id: int, status: str):
        # Retrieve the test from the database based on its ID
        test = self.db.query(Test).filter(Test.id == test_id).first()
        if test:
            # Update the status of the test
            test.status = status
            # Commit the changes
            self.db.commit()
            # Return the updated test
            return test
        else:
            # Handle the case where the test ID is not found
            return None
        
        # Function to finish a test run
    def finish_test_run(self, test_run_id: int):
        # Retrieve the test run from the database
        test_run = self.db.query(TestRun).filter(TestRun.id == test_run_id).first()
        if test_run:
            # Update the end time of the test run
            test_run.end_time = datetime.now()
            self.db.commit()
        else:
            # Handle the case where the test run ID is not found
            raise ValueError("Test run ID not found")

    def print_tables(self):
        try:
            # Print TestRun table
            print("TestRun Table:")
            test_runs = self.db.query(TestRun).all()
            for test_run in test_runs:
                print(f"Test Run ID: {test_run.id}, Start Time: {test_run.start_time}, End Time: {test_run.end_time}")

            # Print Test table
            print("\nTest Table:")
            tests = self.db.query(Test).all()
            for test in tests:
                print(f"Test ID: {test.id}, Name: {test.name}, Status: {test.status}, Test Run ID: {test.test_run_id}")

        except Exception as e:
            print("Error:", e)

    def empty_table(self, Model):
        try:
            self.db.query(Model).delete()
            # Commit the transaction
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()  # Rollback the transaction in case of error
            raise e



if __name__ == "__main__":

    SQLALCHEMY_DATABASE_URL = "sqlite:///plugin_app.sqlite"
    # create tables
    subprocess.call("python3 DatabaseModels.py", shell=True)

    # Set up the database connection
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a session
    db = SessionLocal()

    try:
        # Create an instance of the TestManager
        manager = TestManager(db)

        # Empty tables
        manager.empty_table(TestRun)
        manager.empty_table(Test)

        # Create a new test run
        test_run = manager.create_test_run()

        # Create tests associated with the test run
        for i in range(3):
            test = manager.create_test(name="Example Test", test_run_id=test_run.id)
            print("Created Test:", test.id)

            # Finish the test
            finished_test = manager.finish_test(test_id=test.id, status="PASSED")
            if finished_test:
                print("Finished Test:", finished_test.id)
            else:
                print("Test not found.")

        # Finish the test run
        manager.finish_test_run(test_run.id)

        # Print tables
        manager.print_tables()

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the session
        db.close()
