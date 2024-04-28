"""
Database Models and Initialization
==================================

This module defines SQLAlchemy models for the database tables related to test runs and tests. It also provides functionality to initialize the database and drop existing tables.

Classes:
- TestRun: Represents a test run entity, with attributes such as test_run_id, start_time, end_time, and tests.
- Test: Represents a test entity, with attributes such as test_id, test_name, test_status, duration, error_exception, test_parameters, timestamp, and test_run_id.

Functions:
- drop_all_tables: Drops all tables from the database.
- main: Main function to initialize the database by dropping existing tables (if any) and creating new ones.

Usage:
- Import this module and use the TestRun and Test classes to interact with the database.
- Call the main function to initialize the database.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import create_engine, Column, CHAR, String, ForeignKey, Enum, JSON, DateTime, Float, text

Base =  declarative_base()
load_dotenv()

class TestRun(Base):
    """
    Represents a test run entity in the database.

    Attributes:
    - test_run_id: Unique identifier for the test run.
    - start_time: Start time of the test run.
    - end_time: End time of the test run.
    - tests: Relationship attribute linking TestRun to Test entities.
    """
    __tablename__ = "test_runs"
    
    test_run_id = Column(CHAR(36), index=True, primary_key=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    tests = relationship("Test", back_populates="test_run")

class Test(Base):
    """
    Represents a test entity in the database.

    Attributes:
    - test_id: Unique identifier for the test.
    - test_name: Name of the test.
    - test_status: Status of the test (e.g., PASSED, FAILED).
    - duration: Duration of the test.
    - error_exception: Error message or exception encountered during the test.
    - test_parameters: Parameters of the test stored as JSON.
    - timestamp: Timestamp of the test.
    - test_run_id: Foreign key referencing the associated TestRun.
    - test_run: Relationship attribute linking Test to TestRun entity.
    """
    __tablename__ = "tests"
    
    test_id = Column(CHAR(36), index=True, primary_key=True)
    test_name = Column(String(length=80))
    test_status = Column(Enum("PASSED", "FAILED", "SKIPPED", "ERROR", "UNKNOWN"), nullable=True)
    duration = Column(Float, nullable=True)
    error_exception = Column(String(length=120), nullable=True)
    test_parameters = Column(JSON)  # Store parameters as JSON
    timestamp = Column(DateTime)
    test_run_id = Column(CHAR(36), ForeignKey("test_runs.test_run_id"))
    test_run = relationship("TestRun", back_populates="tests")

def create_mysql_database(username: str, password: str, database_name: str, host: str="localhost", port: str=3306):
    """
    Create a MySQL database using SQLAlchemy.

    Args:
        username (str): MySQL username.
        password (str): MySQL password.
        host (str, optional): MySQL host. Defaults to "localhost".
        port (int, optional): MySQL port. Defaults to 3306.
        database_name (str): Name of the database to create.
    """
    # Construct the SQLAlchemy URL
    url = f"mysql+pymysql://{username}:{password}@{host}:{port}/"

    # Create the engine without specifying the database name
    engine = create_engine(url)

    # Connect to the engine
    conn = engine.connect()

    try:
        # Check if the database exists by querying the list of databases
        show_databases = "SHOW DATABASES"
        databases = conn.execute(text(show_databases))
        database_names = [row[0] for row in databases]
        if database_name in database_names:
            print(f"Database '{database_name}' already exists. Dropping it...")

            # Drop the database
            drop_statement = f"DROP DATABASE {database_name}"
            conn.execute(text(drop_statement))
            print(f"Database '{database_name}' dropped successfully.")
        else:
            print(f"Database '{database_name}' does not exist. Proceeding to create...")
    except ProgrammingError as e:
        # If an error occurs during the query, raise it
        raise e
    finally:
        # Close the connection
        conn.close()

    # Create the database
    conn = engine.connect()
    create_database_statement = f"CREATE DATABASE {database_name}"
    conn.execute(text(create_database_statement))
    print(f"Database '{database_name}' created successfully.")
    conn.close()

def drop_all_tables(database_url: str):
    """
    Drop all tables from the specified database.

    Parameters:
    - database_url (str): URL of the database to drop tables from.
    """
    # Create an engine
    engine = create_engine(database_url)

    # Create a metadata object
    metadata = MetaData()

    # Reflect database tables
    metadata.reflect(bind=engine)

    # Drop all tables
    metadata.drop_all(engine)

def main():
    """
    Main function to initialize the database.

    Drops existing tables (if any) and creates new ones.
    """

    USERNAME = os.getenv('DB_USER')
    PASSWORD = os.getenv('PASSWORD')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    
    # create MySQL database (drops the old one if exists)
    create_mysql_database(USERNAME, PASSWORD, database_name=DATABASE_NAME)
    # Create an engine
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Drop all tables
    print("Dropping existing tables.")
    drop_all_tables(database_url=SQLALCHEMY_DATABASE_URL)

    # Create tables again if needed
    Base.metadata.create_all(bind=engine)
    print("Creating new tables.")
if __name__ == "__main__":
    
    main()