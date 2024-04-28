from SetupDatabase import Test
from SetupDatabase import TestRun
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def main():
    
    Base = declarative_base()
    # Create SQLite database engine
    engine = create_engine('sqlite:///plugin_app.sqlite')

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Retrieve all test records from the database
    tests = session.query(Test).all()

    # Print retrieved test records
    for test in tests:
        print("Test ID:", test.test_id)
        print("Test Name:", test.test_name)
        print("Status:", test.test_status)
        print("Duration:", test.duration)
        print("Error/Exception:", test.error_exception)
        print("Test Parameters:", test.test_parameters)
        print("Timestamp:", test.timestamp)
        print("Test Run ID:", test.test_run_id)
        print("---------------------------")

    # Query all test runs
    test_runs = session.query(TestRun).all()

    # Print retrieved test run records
    for test_run in test_runs:

        print("Test Run ID:", test_run.test_run_id)
        print("Start Time:", test_run.start_time)
        print("End Time:", test_run.end_time)
        print("---------------------------")

    session.close()

if __name__ == "__main__":

    main()