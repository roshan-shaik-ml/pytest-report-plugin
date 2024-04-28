bash

# pytest-report-plugin

## Description

**pytest-report-plugin** is a pytest plugin designed to report test execution progress and results to an external API. This plugin seamlessly integrates with pytest, offering runtime logging for easy debugging and detailed insights into test execution.

## Features

- Report test execution progress and results during test runs.
- Seamless integration with pytest.
- Provides detailed runtime logging for debugging purposes.
- Supports custom configuration options for reporting.
- Detailed information about test execution.

## Prerequisite
- [python3](https://www.python.org/downloads/)
- [virtualenv](https://pypi.org/project/virtualenv/)
- [git](https://git-scm.com/downloads)
- MySQL (version: mysql  Ver 8.0.36-0ubuntu0.20.04.1 for Linux on x86_64 ((Ubuntu)))
> [!NOTE]
> Make sure MySQL is installed and MySQL service is running.

## Installation

To install **pytest-report-plugin**, clone the repository from GitHub and install the required dependencies:

```bash
git clone https://github.com/roshan-shaik-ml/pytest-report-plugin.git
cd pytest-report-plugin
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate      # On Linux or MacOS
venv\Scripts\activate         # On Windows
```
Then, install the required dependencies:

```bash
pip install -r requirements.txt
```
## Usage

Before using pytest-report-plugin, ensure that you have set up the necessary components:
1. **Add database credentials**: Navigate into the App folder. In the .env file, set the following variables:
```bash
# To navigate into App folder
cd App
```


```plaintext
# set the following variable in .env
DB_USER=your_database_username
PASSWORD=your_database_password
DATABASE_NAME=your_database_name
SQLALCHEMY_DATABASE_URL=mysql+pymysql://${DB_USER}:${PASSWORD}@localhost/${DATABASE_NAME}
```

Replace your_database_username, your_database_password, and your_database_name with your actual database credentials.


2. **SetupDatabase.py**: Run this script located in the App folder to set up the MySQL database required for the plugin's functionality.
> [!NOTE]
> This script needs to be executed only during the initial setup or whenever you want to reset the database.

```bash
python SetupDatabase.py
```

3. **FastAPI App**: From within the App folder and run the FastAPI application using uvicorn. This app handles the requests from the plugin. It's crucial for the server to be running in order for the plugin to successfully communicate and send data to the FastAPI endpoints.
> [!TIP]
> Run this command in a separate terminal to ensure continuous operation.

```bash
uvicorn main:app
```

Keep the FastAPI server running while testing the plugin to ensure seamless communication between the plugin and the FastAPI endpoints.

### Finally, Run The Tests.

Once you have set up the prerequisites by running these two files, you can then proceed to run the plugin with pytest by enabling it in your pytest configuration:
```bash
# Navigate to the pytest-report-plugin/pytest_report_plugin directory containing conftest.py, then execute pytest with reporting enabled
pytest --reporting-enabled --reporting-api-url=<API_URL> --reporting-auth-token=<AUTH_TOKEN>
```

## Examples
For testing use the FastAPI hosted url we have setup earlier
### Example 1 (Sequential Execution Testing)

```bash 
pytest --reporting-enabled --reporting-api-url="http://127.0.0.1:8000" --reporting-auth-token="password"
```
### Example 2 (Parllel Execution Testing)
You can change the -n flag based on the CPU count required. `-n auto` uses all the CPUs
```bash

pytest --reporting-enabled --reporting-api-url="http://127.0.0.1:8000" --reporting-auth-token="password" -n 3
```
## Output

After running the tests with pytest-report-plugin, you can access the following endpoints to view the output using a broswer:

    full-report: Endpoint to view a comprehensive report of the all test runs execution.
    runs/run_id: Endpoint to view detailed information about a specific test run identified by run_id.

## Contributing

Contributions to pytest-report-plugin are welcomed! For bug reports or feature requests, please open an issue. If you plan to contribute code, please follow the contribution guidelines.
License

This project is licensed under the terms of the MIT license. For more details, refer to the [LICENSE](https://github.com/roshan-shaik-ml/pytest-report-plugin/blob/main/LICENSE) file.

## Credits

This plugin was developed by [Shaik Faizan Roshan Ali](https://github.com/roshan-shaik-ml/). Feel free to modify and customize it according to your preferences and specific requirements.
