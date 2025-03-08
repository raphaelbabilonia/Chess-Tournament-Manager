# Contributing to Chess Tournament Manager

Thank you for your interest in contributing to the Chess Tournament Manager! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

-  [Code of Conduct](#code-of-conduct)
-  [Getting Started](#getting-started)
-  [How to Contribute](#how-to-contribute)
-  [Development Workflow](#development-workflow)
-  [Coding Standards](#coding-standards)
-  [Testing Guidelines](#testing-guidelines)
-  [Documentation](#documentation)
-  [Issue Reporting](#issue-reporting)
-  [Pull Requests](#pull-requests)
-  [Review Process](#review-process)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. By participating, you are expected to uphold this code. Please report unacceptable behavior.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```
   git clone https://github.com/raphaelbabilonia/Chess-Tournament-Manager.git
   cd Chess-Tournament-Manager
   ```
3. Set up the development environment:
   ```
   pip install -r requirements.txt
   ```
4. Create a branch for your work:
   ```
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

There are many ways to contribute to this project:

-  **Code contributions**: Implement new features or fix bugs
-  **Documentation**: Improve or create documentation
-  **Bug reports**: Submit detailed bug reports
-  **Feature requests**: Suggest new features or improvements
-  **Testing**: Help improve test coverage or report test failures
-  **Translations**: Help translate the application to other languages

## Development Workflow

1. Ensure you're working on the latest version:
   ```
   git pull origin main
   ```
2. Create a feature branch:
   ```
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run tests:
   ```
   python -m unittest discover tests
   ```
5. Commit your changes with a descriptive message:
   ```
   git commit -m "Add feature: description of your changes"
   ```
6. Push to your fork:
   ```
   git push origin feature/your-feature-name
   ```
7. Create a Pull Request on GitHub

## Coding Standards

This project follows PEP 8 Python style guidelines with a few exceptions:

-  Maximum line length is 100 characters
-  Use 4 spaces for indentation (no tabs)
-  Use docstrings for all modules, classes, and functions
-  Include type hints for function parameters and return values

We use `pylint` and `flake8` for linting. Run these before submitting a PR:

```
pylint --rcfile=.pylintrc .
flake8
```

## Testing Guidelines

-  Write tests for all new features and bug fixes
-  Maintain or improve test coverage
-  Tests should be independent and repeatable
-  Follow the existing test structure in the `tests` directory
-  Include both unit tests and integration tests where appropriate

Run tests with:

```
python -m unittest discover tests
```

Check test coverage with:

```
coverage run -m unittest discover
coverage report
```

## Documentation

-  Update documentation for all changes
-  Use clear, concise language
-  Include examples where appropriate
-  Document API changes in the API reference
-  Update user guides for user-facing changes

## Issue Reporting

When reporting issues, please include:

-  A clear, descriptive title
-  A detailed description of the issue
-  Steps to reproduce the problem
-  Expected behavior
-  Actual behavior
-  Screenshots if applicable
-  Environment information:
   -  Operating System
   -  Python version (use `python --version`)
   -  Package versions (from requirements.txt)
   -  Any relevant configuration settings

## Pull Requests

When submitting a pull request:

1. Reference any related issues using GitHub's #issue-number syntax
2. Include a clear description of the changes
3. Update relevant documentation
4. Add or update tests
5. Ensure all tests pass
6. Follow the coding standards
7. Update the CHANGELOG.md file if applicable

## Review Process

All submissions require review before being merged:

1. Automated checks must pass (tests, linting)
2. At least one maintainer must approve the changes
3. Address review feedback promptly
4. Once approved, a maintainer will merge your PR

## Branch Naming Convention

Please follow these branch naming conventions:

-  `feature/` - for new features
-  `bugfix/` - for bug fixes
-  `docs/` - for documentation updates
-  `test/` - for test additions or updates
-  `refactor/` - for code refactoring

Example: `feature/add-swiss-pairing-algorithm`

## Commit Message Guidelines

Follow these guidelines for commit messages:

-  Use the present tense ("Add feature" not "Added feature")
-  Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
-  Limit the first line to 72 characters or less
-  Reference issues and pull requests liberally after the first line

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [GNU General Public License v3.0](LICENSE).

---

Thank you for contributing to the Chess Tournament Manager project! If you have any questions, feel free to open an issue for discussion.
