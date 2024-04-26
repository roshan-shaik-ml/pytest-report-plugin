import json
import uuid
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from Models import Response
from Database import *

app = FastAPI()

'''
    Root: /
    Start Test Run: POST /runs/
    Finished Test Run: POST /runs/{run_id}/finish/
    Individual Test: POST/tests/
    Finished Test: POST/{test_id}/finish

'''

# routes
@app.get("/")
def index():

    return {"Content": "Hello World!"}

@app.post("/runs", response_model=Response, tags=['TestRuns'], summary="Create a new test run")
async def create_run(request_body: dict):


    with open("openapi/create_run.json", "r") as file:

        openapi_spec = json.load(file)
    # Access data from the request body
    run_id = None
    start_time = None
    try:
        run_id = request_body['run_id']
        start_time = request_body['start_time']
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields in request body")

    print(run_id, start_time)
    # Modify the description field with the updated run_id
    openapi_spec["paths"]["/runs/"]["post"]["responses"]["201"]["description"] = f"A new test run is created. Contains a unique `{run_id}`"

    return openapi_spec


@app.post("/runs/{run_id}/finish", response_model=Response, tags=['TestRuns'], summary="Finished a test run")
async def finish_run(request_body: dict):

    try:
        finish_time = request_body["finish_time"]
        print(finish_time)
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields in request body")

    # return test resport schema
    with open("openapi/finish_run.json", "r") as file:

        openapi_spec = json.load(file)

    return openapi_spec

@app.post("/tests", response_model=Response, tags=["Tests"], summary="Start a new test")
async def create_test(request_body: dict):
    
    try:
        test_id = request_body["test_id"]
        test_name = request_body["test_name"]
        test_run_id = request_body["test_run_id"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields in request body")
    
    with open("openapi/create_test.json", "r") as file:

        openapi_spec = json.load(file)

    # Modify the description field with the updated run_id
    openapi_spec["paths"]["/tests/"]["post"]["responses"]["201"]["description"] = f"A new test run is created. Contains a unique `{test_id}`"

     # Replace with your logic to generate test_id
    return openapi_spec

@app.post("/tests/{test_id}/finish", response_model=Response, tags=["Tests"], summary="Finished a test")
async def finish_test(request_body: dict):

    try:
        status = request_body["status"]
        print(status)
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields in request body")
        
    with open("openapi/finish_test.json", "r") as file:

        openapi_spec = json.load(file)

    return openapi_spec


