# Chess Tournament Manager - Developer Guide

This guide provides technical information for developers who want to understand, modify, or contribute to the Chess Tournament Manager project.

## Table of Contents

-  [Architecture Overview](#architecture-overview)
-  [Code Organization](#code-organization)
-  [Key Components](#key-components)
-  [Development Environment](#development-environment)
-  [Contributing Guidelines](#contributing-guidelines)
-  [Testing](#testing)
-  [Building and Packaging](#building-and-packaging)
-  [API Documentation](#api-documentation)

## Architecture Overview

Chess Tournament Manager follows the Model-View-Controller (MVC) architectural pattern:

-  **Model**: Defines data structures and business objects
-  **View**: Handles user interface elements and interactions
-  **Controller**: Implements business logic and connects models with views

The application uses a file-based data storage system with JSON serialization for persistence.

## Code Organization

### Directory Structure

```
chess-tournament-manager/
├── models/            # Data models
├── views/             # User interfaces
├── controllers/       # Business logic
├── utils/             # Helper utilities
├── data/              # Data storage
├── tests/             # Unit and integration tests
├── docs/              # Documentation
├── main.py            # Application entry point
└── requirements.txt   # Dependencies
```

### Key Files

-  `models/player.py`: Player data model
-  `models/tournament.py`: Tournament data model
-  `controllers/pairing.py`: Pairing algorithms
-  `controllers/tournament.py`: Tournament management logic
-  `views/gui.py`: Graphical user interface
-  `views/cli.py`: Command-line interface

## Key Components

### Player Management System

The player management system handles:

-  Player registration
-  Profile management
-  Rating tracking
-  Player history

Key classes:

-  `Player` (models/player.py)
-  `PlayerController` (controllers/player.py)

### Tournament Engine

The tournament engine manages:

-  Tournament creation
-  Player registration
-  Round management
-  Pairing generation
-  Result recording
-  Standings calculation

Key classes:

-  `Tournament` (models/tournament.py)
-  `TournamentController` (controllers/tournament.py)
-  `PairingEngine` (controllers/pairing.py)

### Pairing Algorithms

The application implements several pairing algorithms:

#### Swiss System

-  Based on FIDE Dutch System
-  Color balancing
-  Score group pairing
-  Avoid repeat pairings

Implementation: `SwissPairing` class in `controllers/pairing.py`

#### Round-robin

-  Berger tables for optimal scheduling
-  Color balancing

Implementation: `RoundRobinPairing` class in `controllers/pairing.py`

#### Knockout

-  Seeding algorithm
-  Bracket generation
-  Handling byes

Implementation: `KnockoutPairing` class in `controllers/pairing.py`

### User Interfaces

The application provides two user interfaces:

-  **GUI**: Built with standard Python UI libraries
-  **CLI**: Text-based interface for command-line operation

## Development Environment

### Setting Up

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/chess-tournament-manager.git
   cd chess-tournament-manager
   ```

2. Install development dependencies:

   ```
   pip install -r requirements-dev.txt
   ```

3. Set up pre-commit hooks:
   ```
   pre-commit install
   ```

### Coding Standards

-  Follow PEP 8 for Python code style
-  Use docstrings for all modules, classes, and functions
-  Include type hints for function parameters and return values
-  Maximum line length: 100 characters

### Branching Strategy

-  `main`: Production-ready code
-  `develop`: Integration branch for feature development
-  Feature branches: `feature/feature-name`
-  Bug fix branches: `bugfix/issue-description`

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Ensure all tests pass
5. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Testing

The project uses Python's `unittest` framework for testing.

### Running Tests

Run all tests:

```
python -m unittest discover tests
```

Run specific test suite:

```
python -m unittest tests.test_pairing
```

### Test Structure

-  Unit tests: Test individual functions and classes
-  Integration tests: Test component interactions
-  Functional tests: Test complete workflows

### Test Coverage

Run test coverage report:

```
coverage run -m unittest discover
coverage report
coverage html  # Generates HTML report
```

## Building and Packaging

### Building a Standalone Application

1. Install PyInstaller:

   ```
   pip install pyinstaller
   ```

2. Build the executable:
   ```
   pyinstaller --onefile --windowed main.py
   ```

### Creating Distribution Packages

Create a source distribution:

```
python setup.py sdist
```

Create a wheel package:

```
python setup.py bdist_wheel
```

## API Documentation

### Data Models

#### Player

```python
Player(
    name: str,
    rating: int = 0,
    id: str = None,
    federation: str = None,
    birth_date: date = None,
    title: str = None
)
```

#### Tournament

```python
Tournament(
    name: str,
    start_date: date,
    end_date: date = None,
    location: str = None,
    description: str = None,
    format: TournamentFormat = TournamentFormat.SWISS,
    rounds: int = 7,
    players: List[Player] = None
)
```

### Controller APIs

See `api_reference.md` for detailed API documentation of controller classes.

---

This developer guide provides an overview of the technical aspects of the Chess Tournament Manager. For more detailed API documentation, refer to the API Reference file.
