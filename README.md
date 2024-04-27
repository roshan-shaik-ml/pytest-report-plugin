# pytest-report-plugin

## Description

**pytest-report-plugin** is a pytest plugin for reporting test execution progress and results to an external API.

## Features

- Report test execution progress and results during test runs.
- Seamlessly integrates with pytest.
- Provides detailed information about test execution.
- Supports custom configuration options for reporting.

## Installation

```bash
git clone https://github.com/roshan-shaik-ml/pytest-report-plugin.git
```
To install the required dependencies, navigate to the requirements.txt file in the repository.
```bash
cd pytest-report-plugin
```
Then install the dependencies:
```bash
pip install -r requirements.txt
```
## Usage

To use pytest-report-plugin, you need to enable it in your pytest configuration. You can do this by adding command-line options when running pytest:

```bash
pytest --reporting-enabled --reporting-api-url=<API_URL> --reporting-auth-token=<AUTH_TOKEN>
```
Make sure to replace <API_URL> and <AUTH_TOKEN> with the appropriate values for your API endpoint and authentication token.

## Contributing

Contributions are welcome! For bug reports or feature requests, please open an issue. For contributions, please follow the contribution guidelines.
## License

This project is licensed under the terms of the MIT license. See the [LICENSE](https://github.com/roshan-shaik-ml/pytest-report-plugin/blob/main/LICENSE) file for details.
## Credits

This plugin was developed by [Shaik Faizan Roshan Ali](https://github.com/roshan-shaik-ml/).

Feel free to modify and customize it according to your preferences and specific
