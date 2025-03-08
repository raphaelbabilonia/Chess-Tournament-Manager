# Chess Tournament Manager - Database Schema

This document describes the data storage structure used by the Chess Tournament Manager application.

## Overview

The Chess Tournament Manager uses a file-based JSON storage system. Data is organized into separate files by type and identifier. This approach was chosen for simplicity, portability, and ease of backup.

## Data Directory Structure

```
data/
├── players/
│   ├── {player_id}.json  # Individual player data
│   └── index.json        # Player index with basic info
├── tournaments/
│   ├── {tournament_id}.json  # Individual tournament data
│   └── index.json            # Tournament index with basic info
├── settings/
│   └── app_settings.json     # Application settings
└── backups/
    └── {timestamp}/          # Data backups by timestamp
```

## Schema Definitions

### Player Data

Each player is stored in a separate JSON file with the following structure:

```json
{
   "id": "string", // Unique identifier
   "name": "string", // Player's full name
   "rating": 0, // Player's rating (integer)
   "federation": "string", // Chess federation or country
   "birth_date": "YYYY-MM-DD", // ISO date format
   "title": "string", // Chess title (GM, IM, etc.)
   "email": "string", // Contact email
   "phone": "string", // Contact phone
   "created_at": "YYYY-MM-DD HH:MM:SS", // Creation timestamp
   "updated_at": "YYYY-MM-DD HH:MM:SS", // Last update timestamp
   "performance": {
      "games_played": 0,
      "wins": 0,
      "draws": 0,
      "losses": 0,
      "rating_change": 0,
      "performance_rating": 0
   },
   "history": [
      {
         "tournament_id": "string",
         "tournament_name": "string",
         "start_date": "YYYY-MM-DD",
         "end_date": "YYYY-MM-DD",
         "score": 0.0, // Total score
         "games": 0, // Games played
         "performance": 0, // Performance rating
         "rating_change": 0, // Rating change
         "standing": 0 // Final standing
      }
   ],
   "rating_history": [
      {
         "date": "YYYY-MM-DD",
         "rating": 0,
         "event": "string" // Tournament name or reason
      }
   ]
}
```

### Player Index

The player index provides a quick lookup of all players:

```json
{
   "last_updated": "YYYY-MM-DD HH:MM:SS",
   "count": 0,
   "players": [
      {
         "id": "string",
         "name": "string",
         "rating": 0,
         "federation": "string",
         "title": "string"
      }
   ]
}
```

### Tournament Data

Each tournament is stored in a separate JSON file:

```json
{
   "id": "string", // Unique identifier
   "name": "string", // Tournament name
   "start_date": "YYYY-MM-DD", // Start date
   "end_date": "YYYY-MM-DD", // End date
   "location": "string", // Venue
   "description": "string", // Description
   "format": "SWISS|ROUND_ROBIN|KNOCKOUT", // Tournament format
   "rounds": 0, // Number of rounds
   "current_round": 0, // Current round (0 = not started)
   "time_control": "string", // Time control description
   "created_at": "YYYY-MM-DD HH:MM:SS", // Creation timestamp
   "updated_at": "YYYY-MM-DD HH:MM:SS", // Last update timestamp
   "status": "PENDING|ACTIVE|COMPLETED|CANCELLED", // Tournament status
   "tiebreak_systems": [
      // List of tiebreak systems in order
      "DIRECT_ENCOUNTER",
      "BUCHHOLZ",
      "SONNEBORN_BERGER"
   ],
   "players": [
      {
         "id": "string", // Player ID
         "name": "string", // Player name
         "rating": 0, // Player rating
         "title": "string", // Player title
         "starting_rank": 0, // Starting rank
         "federation": "string", // Player federation
         "status": "ACTIVE|WITHDRAWN|EXPELLED" // Player status
      }
   ],
   "pairings": {
      "1": [
         // Round 1 pairings
         {
            "board": 1,
            "white_id": "string",
            "black_id": "string",
            "result": "1-0|0-1|1/2-1/2|+/-|-/+|*/*", // Game result
            "scheduled_time": "YYYY-MM-DD HH:MM:SS"
         }
      ]
   },
   "standings": [
      {
         "rank": 1,
         "player_id": "string",
         "player_name": "string",
         "score": 0.0,
         "tiebreaks": {
            "DIRECT_ENCOUNTER": 0.0,
            "BUCHHOLZ": 0.0,
            "SONNEBORN_BERGER": 0.0
         },
         "games_played": 0,
         "wins": 0,
         "draws": 0,
         "losses": 0,
         "forfeits_won": 0,
         "forfeits_lost": 0,
         "byes": 0,
         "color_balance": 0, // Positive = more whites, negative = more blacks
         "opponents": ["string"] // IDs of opponents faced
      }
   ],
   "rounds_data": {
      "1": {
         // Round 1 data
         "start_time": "YYYY-MM-DD HH:MM:SS",
         "end_time": "YYYY-MM-DD HH:MM:SS",
         "status": "PENDING|ACTIVE|COMPLETED"
      }
   }
}
```

### Tournament Index

The tournament index provides a quick lookup of all tournaments:

```json
{
   "last_updated": "YYYY-MM-DD HH:MM:SS",
   "count": 0,
   "tournaments": [
      {
         "id": "string",
         "name": "string",
         "start_date": "YYYY-MM-DD",
         "end_date": "YYYY-MM-DD",
         "format": "SWISS|ROUND_ROBIN|KNOCKOUT",
         "rounds": 0,
         "current_round": 0,
         "status": "PENDING|ACTIVE|COMPLETED|CANCELLED",
         "player_count": 0
      }
   ]
}
```

### Application Settings

Application settings are stored in a single JSON file:

```json
{
   "app_version": "string",
   "last_backup": "YYYY-MM-DD HH:MM:SS",
   "auto_backup": true,
   "auto_backup_interval_days": 7,
   "default_tournament_format": "SWISS",
   "default_rounds": 7,
   "default_tiebreak_systems": [
      "DIRECT_ENCOUNTER",
      "BUCHHOLZ",
      "SONNEBORN_BERGER"
   ],
   "ui_theme": "LIGHT|DARK|SYSTEM",
   "language": "en",
   "date_format": "YYYY-MM-DD",
   "organizer_info": {
      "name": "string",
      "contact": "string",
      "organization": "string"
   }
}
```

## Data Operations

### Creating Data

When new data is created:

1. A unique ID is generated
2. The data is serialized to JSON
3. The file is saved to the appropriate directory
4. The index file is updated

### Reading Data

When data is read:

1. The appropriate file is loaded
2. JSON is deserialized into objects
3. Objects are used in the application

### Updating Data

When data is updated:

1. The file is read and deserialized
2. Changes are applied to the object
3. The object is serialized back to JSON
4. The file is saved
5. Index files are updated if necessary

### Deleting Data

When data is deleted:

1. The file is removed from the filesystem
2. The entry is removed from the index file

## Data Integrity

To ensure data integrity:

1. Writes are atomic (write to temp file, then rename)
2. Backups are created automatically at configurable intervals
3. Indices are rebuilt if inconsistencies are detected
4. Data validation occurs before saving

## Data Migration

When the application is upgraded:

1. The data schema version is checked
2. Migration scripts are run if needed
3. A backup is created before migration

---

This document describes the data storage approach of the Chess Tournament Manager. While not a traditional database, this file-based approach provides simplicity and portability while meeting the application's needs.
