"""
Helper functions for Chess Tournament Manager
"""
import os
import json
import csv
from datetime import datetime
from models.tournament import Tournament
from models.player import Player

def ensure_data_directories():
    """Ensure data directories exist"""
    dirs = ['data', 'data/players', 'data/tournaments']
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

def export_tournament_to_json(tournament_id, output_path=None):
    """
    Export tournament data to JSON file
    
    Args:
        tournament_id (str): Tournament ID
        output_path (str, optional): Output file path. Defaults to tournament_name.json.
        
    Returns:
        str: Path to exported file or None if failed
    """
    try:
        from controllers.tournament import get_tournament_report
        report = get_tournament_report(tournament_id)
        
        if not report:
            return None
        
        # Generate filename if not provided
        if not output_path:
            safe_name = report['tournament']['name'].replace(' ', '_').lower()
            output_path = f"{safe_name}_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return output_path
    except Exception as e:
        print(f"Error exporting tournament to JSON: {e}")
        return None

def export_tournament_to_csv(tournament_id, output_path=None):
    """
    Export tournament standings to CSV file
    
    Args:
        tournament_id (str): Tournament ID
        output_path (str, optional): Output file path. Defaults to tournament_name_standings.csv.
        
    Returns:
        str: Path to exported file or None if failed
    """
    try:
        from controllers.tournament import get_tournament_report
        report = get_tournament_report(tournament_id)
        
        if not report or not report['standings']:
            return None
        
        # Generate filename if not provided
        if not output_path:
            safe_name = report['tournament']['name'].replace(' ', '_').lower()
            output_path = f"{safe_name}_standings_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Write to CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Rank', 'Name', 'Rating', 'Score'])
            
            for i, player in enumerate(report['standings']):
                writer.writerow([
                    i + 1,
                    player['name'],
                    player['rating'] or 'N/A',
                    player['score']
                ])
        
        return output_path
    except Exception as e:
        print(f"Error exporting tournament to CSV: {e}")
        return None

def backup_all_data(output_dir=None):
    """
    Backup all tournament and player data
    
    Args:
        output_dir (str, optional): Output directory. Defaults to 'backups'.
        
    Returns:
        str: Path to backup directory or None if failed
    """
    try:
        # Default backup directory
        if not output_dir:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = f"backups/backup_{timestamp}"
        
        # Create backup directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Backup players
        players_dir = os.path.join(output_dir, 'players')
        os.makedirs(players_dir, exist_ok=True)
        
        for player in Player.get_all():
            player_path = os.path.join(players_dir, f"{player.player_id}.json")
            with open(player_path, 'w', encoding='utf-8') as f:
                json.dump(player.to_dict(), f, indent=2)
        
        # Backup tournaments
        tournaments_dir = os.path.join(output_dir, 'tournaments')
        os.makedirs(tournaments_dir, exist_ok=True)
        
        for tournament in Tournament.get_all():
            tournament_path = os.path.join(tournaments_dir, f"{tournament.tournament_id}.json")
            with open(tournament_path, 'w', encoding='utf-8') as f:
                json.dump(tournament.to_dict(), f, indent=2)
        
        return output_dir
    except Exception as e:
        print(f"Error backing up data: {e}")
        return None 