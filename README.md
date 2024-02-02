# govtech-csg-xcg-dangerousrequests

This package belongs to the **eXtended Code Guardrails (XCG)** project, which consists of a series of packages that harden the Django web framework to prevent common web application vulnerabilities.

The Dangerous Requests package contains a Django app that protects your application against dangerous requests. More specifically, this package protects against SSRF attempts when you use the [`requests` library](https://requests.readthedocs.io/en/latest/) in your application. This is achieved by (transparently) leveraging on the [`advocate` library](https://github.com/JordanMilne/Advocate) under the hood.

*Do note that the README in this repository is intentionally limited in scope and is catered towards developers. For detailed instructions on installation, usage, and community guidelines, please refer to the published documentation at https://xcg.tech.gov.sg.*

## Security-related matters

For instructions on how to **report a vulnerability**, refer to the [official documentation website](https://xcg.tech.gov.sg/community/vulnerabilities).

Additionally, **enable email alerts for security issues by "watching" this repository**. The "watch" button can be found near the top right corner of this repo's home page, and there are various options for configuring notification volume. To receive security alerts, either enable notifications for **"All Activity"** or **"Custom -> Security alerts"**.

## Installing development dependencies

Before building or testing the package, or committing changes, install the development dependencies into a virtual environment:

```sh
# In the project root directory
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Building

The package can be built using [`build`](https://pypa-build.readthedocs.io/en/latest/) as the build frontend and [`setuptools`](https://setuptools.pypa.io/en/latest/) as the build backend.

Run the build command below:

```sh
# In the project root directory
python -m build .
```

This creates a directory named `dist/`, which should contain 2 files:

1. A `.whl` (wheel) file, which is a [binary distribution format](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) for Python packages
2. A `.tar.gz` file, which is a [source distribution format](https://packaging.python.org/en/latest/specifications/source-distribution-format/) for Python packages

To view the source files included in the source distribution, use the `tar` utility as follows:

```sh
tar --list -f dist/<filename>.tar.gz
```

To install the package directly from either distribution files:

```sh
pip install <name_of_distribution_file>
```

## Testing

As the tests for this package use multiple variants of the Django settings module, a [convenience script](./tests/run_all_tests.sh) has been provided for ease of running all test methods. Execute the tests using the commands below:

```bash
pip install -e . # Performs an "editable install" of the govtech-csg-xcg-dangerousrequests package
cd tests/
DANGEROUS_REQUESTS_RUN_FLAKY_TESTS=true /bin/bash run_all_tests.sh
```

### Note on potentially flaky tests

There are a few test methods within the test suite that make HTTP requests over the internet. These are non-ideal from an automated testing perspective as they can fail intermittently due to issues such as network error.

Until these are replaced with better means of testing, developers can choose to skip those tests by dropping `DANGEROUS_REQUESTS_RUN_FLAKY_TESTS=true` from the command given above.

## Running pre-commit hooks

*Note: This section is only relevant if you intend to contribute code*

This project uses the [`pre-commit` tool](https://pre-commit.com) to run Git pre-commit hooks for linting and code quality checks. The `pre-commit` tool itself should have been installed along with the [development dependencies](#installing-development-dependencies). After cloning the repository **for the first time**, run the command below to "install" the Git hooks:

```sh
pre-commit install
```

The command above creates a file `.git/hooks/pre-commit`, which defines the shell commands to run before any Git commit is created.

Subsequently, any invocation of `git commit` will trigger the commands, rejecting the commit if there are linting errors. Issues should be automatically fixed, but you will need to re-stage the changes before attempting the commit again.

For a list of hooks run by `pre-commit`, see its [configuration file](.pre-commit-config.yaml).
