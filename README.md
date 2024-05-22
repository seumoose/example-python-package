# Example Python Package

Example Python Package (EPP) provides example utility functions.

[![Testing](https://github.com/seumoose/example-python-package/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/seumoose/example-python-package/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/seumoose/example-python-package/badge.svg?branch=main)](https://coveralls.io/github/seumoose/example-python-package?branch=main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Python](https://img.shields.io/badge/Python-3.9.18-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3918)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Table of Contents

- [Installation](#installation)
- [Top Level Functionality](#top-level-functionality)
- [Quick Start](#quick-start)
- [Developer Information](#developer-information)
  - [Setup & Installation](#setup--installation)
  - [Code Formatting, Type Hinting & Comment Styling](#code-formatting-type-hinting--comment-styling)
  - [Testing](#testing)
  - [Making a Release](#making-a-release)

## Installation <a name="installation"></a>

Install the example-python-package the package:

```bash
pip install example-python-package
```

## Top Level Functionality <a name="top-level-functionality"></a>

The package, by default, exposes top level functionality of several top-level classes that can be imported to perform utility based functions. These include:

- `Multiplier`: For multiplying numbers.

## Quick Start <a name="quick-start"></a>

To use the utilities, simply import the desired class and call the exposed method i.e.

```python
from example_python_package import Multiplier

utility: Multiplier = Multiplier()

# > 6
utility.multiply([3,2])
```

## Developer Information <a name="developer-information"></a>

The following section contains information useful for developers.

### Setup & Installation <a name="setup--installation"></a>

The following commands need to be in-order when setting up the repository for the first time.

- Install project dependencies for local development:

  ```bash
  pip install -e ".[dev,test]"
  ```

- Install the pre-commit hooks to automatically format and lint your code before commit:

  ```bash
  pre-commit install
  ```

Remember to select the correct Python interpreter if using Visual Studio Code with cmd + shift + P > `Python: Select Interpreter`.

It is also suggested that developers install the recommended extensions found in [extensions.json](./.vscode/extensions.json).

_Note_: it is also possible to setup virtual environments using pyenv.

### Code Formatting, Type Hinting & Comment Styling <a name="code-formatting-type-hinting--comment-styling"></a>

Use `black .` to automatically fix code according to the opinionated formatting style.

While type hinting doesn't normally provide any added benefit at runtime using a combination of mypy's static typing analysis and the `@typechecked` decorator from typeguard we can greatly improve type safety both locally and during runtime. It is also best practice to use type hinting as it can help developers better understand methods etc. at a glance and can further allow IDEs to provide better suggestions / warnings if something is unlikely to work though static code analysis.

Commenting is an important step to help developers pickup where others have left off, this repository describes each method through a combination of class/method docstrings and in-line comments around any potentially confusing business logic i.e.:

```python
def foo(foo: Dict[str, int]) -> Dict[str, int]
    """Main method for foo.
    Args:
        foo (bar): an object of type Bar to process.

    Returns:
        List[Bar]: a list of processed Bar objects.
    """

    .
    .
    .
    # build the newline character array by joining newlines characters of length N (distance between paragraphs)
    newlines = ["\n" * newline_characters for newline_characters in number_of_newlines]
    .
    .
    .
    return [Bar()]
```

### Testing <a name="testing"></a>

All tests can be ran by using the [test script](./.sh/test) - this will set up a virtual environment and install needed dependencies.

If users want to manually run the tests, install the required dependencies using `pip install -e ".[dev]"` and then refer to each respective testing section below.

_Note_: additional permissions may need to be granted to the scripts.

#### Pylint

Run pylint linting:

```bash
pylint ./example_python_package
```

Once ran, the generate linting reports can be found [here](./reports/pylint).

_Note_: because pylint cannot create directories itself, on clone of the repository the /bandit directory will have an empty .report placeholder file.

#### mypy

Run `mypy` static code type checking:

```bash
mypy .
```

Once ran, reporting will be viewable in the terminal.

#### Pytest

Run pytest tests:

```bash
pytest
```

Once ran, the generated coverage reports can be found [here](./reports/pytest). To view the report in interactive mode, right click -> Show Preview on the [index.html](reports/pytest/html/index.html) file or run the [server start script](.sh/reports/pytest/serve).

#### Bandit

Run Bandit static vulnerability reporting:

```bash
bandit -v -r ./example_python_package -f json -o reports/bandit/report.json
```

Once ran, the generated JSON report can be found [here](./reports/bandit).

_Note_: because bandit cannot create directories itself, on clone of the repository the /bandit directory will have an empty .report placeholder file.

### Vulnerability Scanning <a name="vulnerability-scanning">

#### Sonarqube

docker run --rm --name sonarqube -p 9000:9000 sonarqube:latest

#### Trivy

Once an image is made, Trivy scanning can be ran with:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/Library/Caches:/root/.cache/ aquasec/trivy:latest image <image>
```

### Making a Release <a name="making-a-release"></a>

Once the version and other functional changes have been merged to master, and the commit tagged, the package needs to be uploaded to the PyPI repository:

- Locally run the (build script)[./.sh/build] with `sh ./.sh/build` to build the package under the `./dist` directory - all dependencies will be installed.
- Push the build artifacts to the PyPI repository using: `python -m twine upload --verbose -r PyPI dist/*`.
  - _Note:_ this requires a `.pypirc` file to be setup following the [example file](.pypirc.example) in the home directory so the user is not prompted for their username & password each time.
    - Username: your email.
    - Password: your https://pypi.org/ password.
  - Alternatively the command `python -m twine upload --verbose --repository-url https://pypi.org/ dist/*` can be used to push files using the same information as described above.
  - _Note:_ if during the upload process see errors like _urllib3 v2.0 only supports OpenSSL 1.1.1+_ are observed, the installed Python version will need to be reinstalled and recompiled with updated OpenSSL libraries:
    - Uninstall the current Python version, if using pyenv simply uninstall the version i.e. `pyenv uninstall 3.8.10` - for other installs you'll need to completely uninstall Python from the EC2 instance.
      - _Note:_ if using pyenv this will only half-uninstall all currently installed pyenvs - to completely remove them (to be able to recreate them post-Python update) navigate to ~/.pyenv/versions/ and remove them with `rm -rf`.
    - Remove the current OpenSSL library with `sudo yum remove openssl`.
    - Reinstall the OpenSSL libraries with `sudo yum install openssl11 openssl11-devel`.
    - Reinstall Python, recreate virtual environments if using pyenv, and reinstall project dependencies.
    - Retry the upload, if correctly updated twine should now push the package build to PyPI.
- Confirm that the new version of example-python-package has been uploaded to [PyPI](https://pypi.org/) as expected.

_Note_: additional permissions may need to be granted to the scripts.
