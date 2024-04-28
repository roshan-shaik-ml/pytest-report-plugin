import json
import uuid
import logging
from datetime import datetime
from Database import TestManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse, JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create file handlers for each logger
http_handler = logging.FileHandler(filename='logs/http.log')
generic_handler = logging.FileHandler(filename='logs/generic.log')
action_handler = logging.FileHandler(filename='logs/action.log')

# Set log levels for each handler
http_handler.setLevel(logging.ERROR)
generic_handler.setLevel(logging.ERROR)
action_handler.setLevel(logging.INFO)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
http_handler.setFormatter(formatter)
generic_handler.setFormatter(formatter)
action_handler.setFormatter(formatter)

# Attach handlers to loggers
http_logger = logging.getLogger('http_logger')
http_logger.addHandler(http_handler)

generic_logger = logging.getLogger('generic_logger')
generic_logger.addHandler(generic_handler)

action_logger = logging.getLogger('action_logger')
action_logger.addHandler(action_handler)

# Create SQLAlchemy session
SQLALCHEMY_DATABASE_URL = "sqlite:///plugin_app.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Initialize TestManager with the session
test_manager = TestManager(db)

# Initialize FastAPI app and Jinja2 environment
app = FastAPI()
templates = Environment(loader=FileSystemLoader("templates"))


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Exception handler for HTTPException.

    Parameters:
    - request: The request object.
    - exc (HTTPException): The raised HTTPException.

    Returns:
    - JSONResponse: Response with error details.
    """
    http_logger.error(f"HTTPException: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """
    Generic exception handler for unhandled exceptions.

    Parameters:
    - request: The request object.
    - exc (Exception): The raised exception.

    Returns:
    - JSONResponse: Response with error details.
    """
    generic_logger.exception("Unhandled Exception occurred")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"}
    )


@app.get("/")
def index():
    """
    Default endpoint. Returns a simple greeting message.
    """
    return {"Content": "Hello World!"}


@app.post("/runs", tags=['TestRuns'], summary="Create a new test run")
async def create_run(request_body: dict):
    """
    Endpoint to create a new test run.

    Parameters:
    - request_body (dict): Request body containing run details.

    Returns:
    - dict: OpenAPI specification.
    """
    try:
        run_id = uuid.UUID(request_body.get('run_id'))
        start_time = datetime.fromisoformat(request_body.get('start_time'))
        created_test_run = test_manager.create_test_run(test_run_id=run_id, start_time=start_time)
        action_logger.info(f"Test run created with ID: {run_id}")
    except Exception as e:
        generic_logger.exception("Exception occurred while creating test run")
        raise HTTPException(status_code=400, detail="Missing required fields in request body") from e

    with open("openapi/create_run.json", "r") as file:
        openapi_spec = json.load(file)

    updated_value = f"A new test run is created. Contains a unique `{run_id}`"
    openapi_spec["paths"]["/runs/"]["post"]["responses"]["201"]["description"] = updated_value

    return openapi_spec


@app.get("/runs/{run_id}")
async def get_tests_for_run(run_id: str):
    """
    Endpoint to retrieve tests for a specific run.

    Parameters:
    - run_id (str): ID of the test run.

    Returns:
    - HTMLResponse: Rendered HTML content.
    """
    try:
        tests = test_manager.get_tests_by_run_id(run_id)
        if not tests:
            raise HTTPException(status_code=404, detail="Tests not found for the specified run ID")

        template = templates.get_template("tests.html")
        html_content = template.render(run_id=run_id, tests=tests)
        return HTMLResponse(content=html_content)

    except Exception as e:
        generic_logger.exception("Exception occurred while retrieving tests for a run")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@app.get("/full-report")
async def get_full_report():
    """
    Endpoint to retrieve a full test report.

    Returns:
    - HTMLResponse: Rendered HTML content.
    """
    try:
        tests = test_manager.get_all_tests()
        if not tests:
            raise HTTPException(status_code=404, detail="Tests not found")

        template = templates.get_template("full-report.html")
        html_content = template.render(tests=tests)
        return HTMLResponse(content=html_content)

    except Exception as e:
        generic_logger.exception("Exception occurred while retrieving full test report")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@app.post("/runs/{run_id}/finish", tags=['TestRuns'], summary="Finish a test run")
async def finish_run(request_body: dict):
    """
    Endpoint to finish a test run.

    Parameters:
    - request_body (dict): Request body containing run details.

    Returns:
    - dict: OpenAPI specification.
    """
    try:
        run_id = uuid.UUID(request_body.get("run_id"))
        finish_time = datetime.fromisoformat(request_body.get("finish_time"))
        test_manager.finish_test_run(run_id, finish_time)
        action_logger.info(f"Test run finished with ID: {run_id}")
    except Exception as e:
        generic_logger.exception("Exception occurred while finishing test run")
        raise HTTPException(status_code=400, detail="Missing required fields in request body") from e

    with open("openapi/finish_run.json", "r") as file:
        openapi_spec = json.load(file)

    return openapi_spec


@app.post("/tests", tags=["Tests"], summary="Start a new test")
async def create_test(request_body: dict):
    """
    Endpoint to start a new test.

    Parameters:
    - request_body (dict): Request body containing test details.

    Returns:
    - dict: OpenAPI specification.
    """
    try:
        test_id = uuid.UUID(request_body.get("test_id"))
        test_name = request_body.get("test_name")
        test_parameters = request_body.get("test_parameters")
        timestamp = request_body.get("timestamp")
        test_run_id = request_body.get("test_run_id")

        timestamp_formatted = datetime.fromisoformat(timestamp)
        test_run_id = uuid.UUID(test_run_id)
        test_manager.create_test(test_id, test_name, test_parameters, timestamp_formatted, test_run_id)
        action_logger.info(f"Test created with ID: {test_id}")
    except Exception as e:
        generic_logger.exception("Exception occurred while creating test")
        raise HTTPException(status_code=400, detail="Missing required fields in request body") from e

    with open("openapi/create_test.json", "r") as file:
        openapi_spec = json.load(file)

    updated_value = f"A new test is created. Contains a unique `{test_id}`"
    openapi_spec["paths"]["/tests/"]["post"]["responses"]["201"]["description"] = updated_value

    return openapi_spec


@app.post("/tests/{test_id}/finish", tags=["Tests"], summary="Finish a test")
async def finish_test(request_body: dict):
    """
    Endpoint to finish a test.

    Parameters:
    - request_body (dict): Request body containing test details.

    Returns:
    - dict: OpenAPI specification.
    """
    try:
        test_id = uuid.UUID(request_body.get("test_id"))
        test_status = request_body.get("test_status")
        error_exception = request_body.get("error_exception")
        duration = request_body.get("duration")

        test_manager.finish_test(test_id, test_status, duration, error_exception)
        action_logger.info(f"Test finished with ID: {test_id}")
    except Exception as e:
        generic_logger.exception("Exception occurred while finishing test")
        raise HTTPException(status_code=400, detail="Missing required fields in request body") from e

    with open("openapi/finish_test.json", "r") as file:
        openapi_spec = json.load(file)

    return openapi_spec
