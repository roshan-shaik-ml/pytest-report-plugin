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

## Installation

To install **pytest-report-plugin**, clone the repository from GitHub and install the required dependencies:

```bash
git clone https://github.com/roshan-shaik-ml/pytest-report-plugin.git
cd pytest-report-plugin
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate      # On Unix or MacOS
venv\Scripts\activate         # On Windows
```
Then, install the required dependencies:

```bash
pip install -r requirements.txt
```
## Usage

Before using pytest-report-plugin, ensure that you have set up the necessary components:

1. **SetupDatabase.py**: Run this script located in the App folder to set up the SQLite database required for the plugin's functionality.
   > [!NOTE]
   > This script needs to be executed only during the initial setup or whenever you want to reset the database.

    ```bash
    python App/SetupDatabase.py
    ```

2. **FastAPI App**: Navigate to the App folder and run the FastAPI application using uvicorn. This app handles the requests from the plugin. It's crucial for the server to be running in order for the plugin to successfully communicate and send data to the FastAPI endpoints.
   > [!TIP]
   > Run this command in a separate terminal to ensure continuous operation.

    ```bash
    cd App
    uvicorn main:app
    ```

Keep the FastAPI server running while testing the plugin to ensure seamless communication between the plugin and the FastAPI endpoints.


Once you have set up the prerequisites by running these two files, you can then proceed to run the plugin with pytest by enabling it in your pytest configuration:

```bash
pytest --reporting-enabled --reporting-api-url=<API_URL> --reporting-auth-token=<AUTH_TOKEN>
```

Replace <API_URL> and <AUTH_TOKEN> with the appropriate values for your API endpoint and authentication token.
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
