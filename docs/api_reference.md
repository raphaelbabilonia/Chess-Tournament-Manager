# Chess Tournament Manager - API Reference

This document provides detailed information about the API of the Chess Tournament Manager.

## Table of Contents

-  [Models](#models)
   -  [Player](#player)
   -  [Tournament](#tournament)
-  [Controllers](#controllers)
   -  [PlayerController](#playercontroller)
   -  [TournamentController](#tournamentcontroller)
   -  [PairingEngine](#pairingengine)
-  [Utilities](#utilities)
   -  [Data Storage](#data-storage)
   -  [Validation](#validation)

## Models

### Player

The `Player` class represents a chess player in the system.

#### Properties

| Property      | Type | Description                            |
| ------------- | ---- | -------------------------------------- |
| `id`          | str  | Unique identifier for the player       |
| `name`        | str  | Player's full name                     |
| `rating`      | int  | Player's rating (FIDE, national, etc.) |
| `federation`  | str  | Chess federation or country            |
| `birth_date`  | date | Player's date of birth                 |
| `title`       | str  | Chess title (GM, IM, FM, etc.)         |
| `performance` | dict | Performance statistics                 |
| `history`     | list | Tournament history                     |

#### Methods

```python
def update_rating(self, new_rating: int) -> None:
    """Update player's rating and record history"""

def add_tournament_result(self, tournament_id: str, score: float, performance: int) -> None:
    """Add a tournament result to player's history"""

def calculate_average_performance(self) -> int:
    """Calculate player's average performance"""

def to_dict(self) -> dict:
    """Convert player object to dictionary for serialization"""

@classmethod
def from_dict(cls, data: dict) -> Player:
    """Create player object from dictionary"""
```

### Tournament

The `Tournament` class represents a chess tournament with its configuration and state.

#### Properties

| Property           | Type | Description                                      |
| ------------------ | ---- | ------------------------------------------------ |
| `id`               | str  | Unique identifier for the tournament             |
| `name`             | str  | Tournament name                                  |
| `start_date`       | date | Start date                                       |
| `end_date`         | date | End date                                         |
| `location`         | str  | Tournament venue                                 |
| `format`           | enum | Tournament format (SWISS, ROUND_ROBIN, KNOCKOUT) |
| `rounds`           | int  | Number of rounds                                 |
| `players`          | list | List of players                                  |
| `current_round`    | int  | Current round number                             |
| `pairings`         | dict | Pairings by round                                |
| `results`          | dict | Results by round                                 |
| `standings`        | list | Current standings                                |
| `tiebreak_systems` | list | List of tiebreak systems in order                |

#### Methods

```python
def add_player(self, player: Player) -> bool:
    """Add a player to the tournament"""

def remove_player(self, player_id: str) -> bool:
    """Remove a player from the tournament"""

def start_tournament(self) -> bool:
    """Start the tournament"""

def generate_pairings(self, round_num: int = None) -> list:
    """Generate pairings for a specific round"""

def record_result(self, round_num: int, board_num: int, result: str) -> bool:
    """Record a game result"""

def update_standings(self) -> list:
    """Update tournament standings"""

def complete_round(self, round_num: int = None) -> bool:
    """Complete a round and prepare for the next"""

def to_dict(self) -> dict:
    """Convert tournament object to dictionary for serialization"""

@classmethod
def from_dict(cls, data: dict) -> Tournament:
    """Create tournament object from dictionary"""
```

## Controllers

### PlayerController

The `PlayerController` class manages player-related operations.

#### Methods

```python
def create_player(self, name: str, rating: int = 0, **kwargs) -> Player:
    """Create a new player"""

def get_player(self, player_id: str) -> Player:
    """Get a player by ID"""

def get_all_players(self) -> list:
    """Get all players"""

def update_player(self, player_id: str, **updates) -> Player:
    """Update player information"""

def delete_player(self, player_id: str) -> bool:
    """Delete a player"""

def import_players(self, file_path: str, format: str = 'csv') -> int:
    """Import players from a file"""

def export_players(self, file_path: str, format: str = 'csv') -> bool:
    """Export players to a file"""

def search_players(self, query: str) -> list:
    """Search for players by name or other criteria"""
```

### TournamentController

The `TournamentController` class manages tournament-related operations.

#### Methods

```python
def create_tournament(self, name: str, start_date: date, **kwargs) -> Tournament:
    """Create a new tournament"""

def get_tournament(self, tournament_id: str) -> Tournament:
    """Get a tournament by ID"""

def get_all_tournaments(self) -> list:
    """Get all tournaments"""

def update_tournament(self, tournament_id: str, **updates) -> Tournament:
    """Update tournament information"""

def delete_tournament(self, tournament_id: str) -> bool:
    """Delete a tournament"""

def add_player_to_tournament(self, tournament_id: str, player_id: str) -> bool:
    """Add a player to a tournament"""

def remove_player_from_tournament(self, tournament_id: str, player_id: str) -> bool:
    """Remove a player from a tournament"""

def start_tournament(self, tournament_id: str) -> bool:
    """Start a tournament"""

def generate_pairings(self, tournament_id: str, round_num: int = None) -> list:
    """Generate pairings for a tournament round"""

def record_result(self, tournament_id: str, round_num: int,
                 board_num: int, result: str) -> bool:
    """Record a game result"""

def get_standings(self, tournament_id: str) -> list:
    """Get current tournament standings"""

def complete_round(self, tournament_id: str, round_num: int = None) -> bool:
    """Complete a tournament round"""

def finalize_tournament(self, tournament_id: str) -> bool:
    """Finalize a tournament"""

def generate_report(self, tournament_id: str, report_type: str,
                   file_format: str = 'pdf') -> str:
    """Generate a tournament report"""
```

### PairingEngine

The `PairingEngine` class handles pairing generation for different tournament formats.

#### Methods

```python
def generate_swiss_pairings(self, tournament: Tournament, round_num: int) -> list:
    """Generate Swiss system pairings"""

def generate_round_robin_pairings(self, tournament: Tournament, round_num: int) -> list:
    """Generate round-robin pairings"""

def generate_knockout_pairings(self, tournament: Tournament, round_num: int) -> list:
    """Generate knockout/elimination pairings"""

def assign_colors(self, player1: Player, player2: Player,
                 tournament: Tournament) -> tuple:
    """Assign colors to players in a pairing"""

def handle_odd_players(self, players: list, tournament: Tournament,
                      round_num: int) -> tuple:
    """Handle odd number of players (bye assignment)"""

def avoid_repeat_pairings(self, candidate_pairings: list,
                         tournament: Tournament) -> list:
    """Adjust pairings to avoid repeats"""
```

## Utilities

### Data Storage

The `DataStorage` class handles data persistence.

#### Methods

```python
def save_player(self, player: Player) -> bool:
    """Save player data"""

def load_player(self, player_id: str) -> Player:
    """Load player data"""

def load_all_players(self) -> list:
    """Load all players"""

def save_tournament(self, tournament: Tournament) -> bool:
    """Save tournament data"""

def load_tournament(self, tournament_id: str) -> Tournament:
    """Load tournament data"""

def load_all_tournaments(self) -> list:
    """Load all tournaments"""

def backup_data(self, backup_path: str = None) -> bool:
    """Create a backup of all data"""

def restore_data(self, backup_path: str) -> bool:
    """Restore data from a backup"""
```

### Validation

The `Validator` class provides data validation utilities.

#### Methods

```python
def validate_player_data(self, data: dict) -> tuple:
    """Validate player data"""

def validate_tournament_data(self, data: dict) -> tuple:
    """Validate tournament data"""

def validate_pairing(self, player1: Player, player2: Player,
                    tournament: Tournament) -> bool:
    """Validate if a pairing is legal"""

def validate_result(self, result: str) -> bool:
    """Validate a game result"""

def validate_import_file(self, file_path: str, format: str) -> bool:
    """Validate player import file"""
```

---

This API reference provides details about the main classes and methods in the Chess Tournament Manager. For implementation details, please refer to the source code.
