# Chess Tournament Manager - User Guide

This guide provides detailed instructions on how to use the Chess Tournament Manager application.

## Table of Contents

-  [Installation](#installation)
-  [Getting Started](#getting-started)
-  [Managing Players](#managing-players)
-  [Creating Tournaments](#creating-tournaments)
-  [Managing Tournaments](#managing-tournaments)
-  [Generating Reports](#generating-reports)
-  [Advanced Features](#advanced-features)
-  [Troubleshooting](#troubleshooting)

## Installation

### System Requirements

-  Python 3.8 or higher
-  2GB RAM minimum
-  100MB disk space

### Installation Steps

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/chess-tournament-manager.git
   cd chess-tournament-manager
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## Getting Started

### First Launch

When you first launch the application, you'll see the main dashboard with options for:

-  Player Management
-  Tournament Management
-  Reports
-  Settings

### Initial Setup

Before creating your first tournament, you should:

1. Import or create player profiles
2. Configure application settings (optional)

## Managing Players

### Adding Players

1. Navigate to "Player Management"
2. Click "Add New Player"
3. Fill in the required fields:
   -  Name
   -  Rating (if applicable)
   -  ID (FIDE ID, national ID, etc.)
   -  Contact information (optional)
4. Click "Save"

### Importing Players

1. Navigate to "Player Management"
2. Click "Import Players"
3. Select the file format (CSV, JSON, or FIDE format)
4. Browse for the file
5. Map the columns if using CSV
6. Confirm the import

### Editing Player Information

1. Find the player in the player list
2. Click on the player's name
3. Modify the information
4. Click "Save"

### Player History

Each player profile tracks:

-  Tournament participation
-  Game results
-  Rating history
-  Performance statistics

## Creating Tournaments

### New Tournament

1. Navigate to "Tournament Management"
2. Click "Create New Tournament"
3. Enter tournament details:
   -  Name
   -  Dates
   -  Location
   -  Description
   -  Format (Swiss, Round-robin, Knockout)
   -  Number of rounds
   -  Time control
   -  Rating type (FIDE, national, unrated)
4. Click "Create"

### Tournament Formats

#### Swiss System

-  Best for large groups of players
-  Players meet opponents with similar scores
-  All players play in each round
-  Configure number of rounds and tiebreak criteria

#### Round-robin

-  Each player plays against every other player
-  Best for small groups (typically <12 players)
-  Can be single or double round-robin

#### Knockout/Elimination

-  Players who lose are eliminated
-  Configure with or without consolation brackets

### Adding Players to Tournament

1. Open the tournament
2. Click "Add Players"
3. Select players from the database
4. Assign starting rank numbers if needed
5. Click "Add Selected Players"

## Managing Tournaments

### Starting a Tournament

1. Open the tournament
2. Verify all settings and players
3. Click "Start Tournament"

### Generating Pairings

1. Click "Generate Pairings" for the current round
2. Review the pairings
3. Make manual adjustments if necessary
4. Finalize pairings

### Entering Results

1. Navigate to the current round
2. Click on a pairing
3. Enter the result (1-0, 0-1, ½-½, +/-, -/+, etc.)
4. Save the result

### Advancing to Next Round

1. Ensure all results for the current round are entered
2. Click "Complete Round"
3. Generate pairings for the next round

### Standings

View current standings at any time by clicking "Standings" in the tournament view.

## Generating Reports

### Tournament Reports

1. Navigate to "Reports"
2. Select the tournament
3. Choose report type:
   -  Standings
   -  Pairings
   -  Cross table
   -  Player results
   -  Rating changes
4. Select format (PDF, HTML, CSV)
5. Generate and save the report

### Exporting for Rating Submission

1. Open the tournament
2. Click "Export for Rating"
3. Select the rating organization format (FIDE, USCF, etc.)
4. Save the file

## Advanced Features

### Manual Pairing Adjustments

1. Generate automatic pairings
2. Click "Edit Pairings"
3. Make changes as needed
4. Click "Save Changes"

### Handling Special Cases

-  **Byes**: Assigned automatically or manually in Swiss tournaments
-  **Late Entries**: Add players after tournament starts
-  **Withdrawals**: Mark players as withdrawn
-  **Forfeits**: Report as +/- or -/+ results

### Custom Tiebreak Systems

1. Go to tournament settings
2. Select "Tiebreak Systems"
3. Choose and order tiebreak methods

## Troubleshooting

### Common Issues

#### Pairing Problems

-  Ensure all results from previous rounds are entered
-  Check for duplicate players
-  Verify tournament format settings

#### Data Not Saving

-  Check disk space
-  Ensure proper permissions for data directory

#### Application Won't Start

-  Verify Python version (3.8+)
-  Check all dependencies are installed
-  Review error logs

### Getting Help

For additional support:

-  Check the GitHub repository issues page
-  Contact your system administrator
-  Review error logs in the `data/logs/` directory

---

This user guide covers the basic functionality of the Chess Tournament Manager. For more detailed information on specific features, please refer to the other documentation files.
