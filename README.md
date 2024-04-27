# pytest-report-plugin

[![GitHub license](https://img.shields.io/github/license/roshan-shaik-ml/pytest-report-plugin)](https://github.com/roshan-shaik-ml/pytest-report-plugin/blob/main/LICENSE)

## Description

**pytest-report-plugin** is a pytest plugin for reporting test execution progress and results to an external API.

## Features

- Report test execution progress and results during test runs.
- Seamlessly integrates with pytest.
- Provides detailed information about test execution.
- Supports custom configuration options for reporting.

## Installation

You can install `pytest-report-plugin` via pip:

```bash
pip install pytest-report-plugin
```
To install the required dependencies, download the requirements.txt file from the repository:

```
bash
wget https://raw.githubusercontent.com/roshan-shaik-ml/pytest-report-plugin/main/requirements.txt
```

Then install the dependencies:
```
bash
pip install -r requirements.txt
```
Usage

To use pytest-report-plugin, you need to enable it in your pytest configuration. You can do this by adding command-line options when running pytest:

bash

pytest --reporting_enabled --reporting_api_url <API_URL> --reporting_auth_token <AUTH_TOKEN>

Make sure to replace <API_URL> and <AUTH_TOKEN> with the appropriate values for your API endpoint and authentication token.

Contributing

Contributions are welcome! For bug reports or feature requests, please open an issue. For contributions, please follow the contribution guidelines.
License

This project is licensed under the terms of the MIT license. See the LICENSE file for details.
Credits

This plugin was developed by Shaik Faizan Roshan Ali.

css
Feel free to modify and customize it according to your preferences and specific
