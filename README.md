# Chess Tournament Manager

A comprehensive Python-based application for managing chess tournaments, designed for tournament organizers, arbiters, and chess clubs.

## Overview

Chess Tournament Manager is an easy-to-use, feature-rich application for organizing and managing chess tournaments of various formats. The software handles player registration, tournament creation, automated pairings, result recording, standings calculation, and reporting.

## Features

-  **Player Management**

   -  Register and manage player profiles with ratings and history
   -  Import/export player data from/to various formats
   -  Track player performance and rating changes

-  **Tournament Configuration**

   -  Support for multiple tournament formats:
      -  Swiss System (variable rounds)
      -  Round-robin
      -  Knockout/Elimination
   -  Customizable tiebreak systems
   -  Configurable time controls and scheduling

-  **Pairing Engine**

   -  Automated pairings based on tournament format
   -  Advanced Swiss pairing algorithm with color balancing
   -  Manual override capabilities for arbiters
   -  Handling of byes, forfeits, and special cases

-  **Result Management**

   -  Simple interface for inputting game results
   -  Support for different scoring systems (1-0-½, 3-1-0, etc.)
   -  Partial result entry and validation

-  **Standings and Statistics**

   -  Real-time standings with multiple tiebreak criteria
   -  Performance statistics and rating calculations
   -  Cross tables and crosstabs generation

-  **Reporting**
   -  Generate tournament reports in various formats
   -  Export results for rating submission
   -  Customizable report templates

## Requirements

-  Python 3.8 or higher
-  Dependencies (automatically installed):
   -  tabulate 0.9.0 (for formatted table output)
   -  tqdm 4.66.1 (for progress bars)
   -  rich 13.6.0 (for enhanced terminal output)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/chess-tournament-manager.git
   cd chess-tournament-manager
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application

Run the application with GUI (default):

```
python main.py
```

For command-line interface only:

```
python -m views.cli
```

### Quick Start Guide

1. Launch the application
2. Create/import player profiles
3. Create a new tournament
4. Configure tournament settings
5. Add registered players to the tournament
6. Start the tournament and generate first-round pairings
7. Enter game results as they complete
8. Generate pairings for subsequent rounds
9. Finalize tournament and export reports

## Project Structure

-  `models/`: Core data models

   -  `player.py`: Player data structure and operations
   -  `tournament.py`: Tournament management and configuration

-  `controllers/`: Business logic

   -  `player.py`: Player registration and management
   -  `tournament.py`: Tournament creation and management
   -  `pairing.py`: Pairing algorithms for different tournament formats

-  `views/`: User interfaces

   -  `gui.py`: Graphical user interface
   -  `cli.py`: Command-line interface

-  `utils/`: Helper functions and utilities

   -  Data validation
   -  File operations
   -  General helpers

-  `data/`: Data storage

   -  Player database
   -  Tournament records
   -  Application settings

-  `tests/`: Unit and integration tests

-  `main.py`: Application entry point

## Development

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

### Testing

Run the test suite:

```
python -m unittest discover tests
```

## Documentation

Detailed documentation is available in the `docs/` directory.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For bug reports and feature requests, please [open an issue](https://github.com/yourusername/chess-tournament-manager/issues) on GitHub.
