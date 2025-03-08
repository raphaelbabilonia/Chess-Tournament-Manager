"""
Tournament model for Chess Tournament Manager
"""
import uuid
import json
import os
from datetime import datetime
from enum import Enum
from models.player import Player

class TournamentType(Enum):
    """Tournament types"""
    SWISS = "Swiss"
    ROUND_ROBIN = "Round Robin"
    KNOCKOUT = "Knockout"

class Result(Enum):
    """Game result types"""
    WHITE_WIN = "1-0"
    BLACK_WIN = "0-1"
    DRAW = "1/2-1/2"
    FORFEIT_WHITE = "1-0F"  # White wins by forfeit
    FORFEIT_BLACK = "0-1F"  # Black wins by forfeit
    DOUBLE_FORFEIT = "0-0F"  # Both forfeit
    ONGOING = "*"
    # Aliases for GUI usage
    PLAYER1_WIN = "1-0"     # Same as WHITE_WIN
    PLAYER2_WIN = "0-1"     # Same as BLACK_WIN
    NOT_PLAYED = "*"        # Same as ONGOING

class Pairing:
    """Class representing a game pairing"""
    def __init__(self, white_id=None, black_id=None, board_number=None, result=Result.ONGOING):
        self.white_id = white_id
        self.black_id = black_id
        self.board_number = board_number
        self.result = result if isinstance(result, Result) else Result(result)
    
    def to_dict(self):
        """Convert pairing to dictionary"""
        return {
            'white_id': self.white_id,
            'black_id': self.black_id,
            'board_number': self.board_number,
            'result': self.result.value if self.result else Result.ONGOING.value
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create pairing from dictionary"""
        return cls(
            white_id=data.get('white_id'),
            black_id=data.get('black_id'),
            board_number=data.get('board_number'),
            result=data.get('result', Result.ONGOING.value)
        )
    
    def __str__(self):
        """String representation of pairing"""
        white_name = Player.load(self.white_id).name if self.white_id else "BYE"
        black_name = Player.load(self.black_id).name if self.black_id else "BYE"
        return f"Board {self.board_number}: {white_name} vs {black_name} [Result: {self.result.value}]"

class Round:
    """Class representing a tournament round"""
    def __init__(self, number, pairings=None, start_time=None, end_time=None):
        self.number = number
        self.pairings = pairings or []
        self.start_time = start_time
        self.end_time = end_time
    
    def to_dict(self):
        """Convert round to dictionary"""
        return {
            'number': self.number,
            'pairings': [p.to_dict() for p in self.pairings],
            'start_time': self.start_time,
            'end_time': self.end_time
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create round from dictionary"""
        round_obj = cls(
            number=data['number'],
            start_time=data.get('start_time'),
            end_time=data.get('end_time')
        )
        round_obj.pairings = [Pairing.from_dict(p) for p in data.get('pairings', [])]
        return round_obj

class Tournament:
    """
    Class representing a chess tournament
    """
    def __init__(self, name, tournament_type=TournamentType.SWISS, 
                 num_rounds=0, location="", start_date=None, end_date=None,
                 description="", tournament_id=None):
        """
        Initialize a tournament
        
        Args:
            name (str): Tournament name
            tournament_type (TournamentType): Type of tournament
            num_rounds (int): Number of rounds
            location (str): Tournament location
            start_date (str): Start date (ISO format)
            end_date (str): End date (ISO format)
            description (str): Tournament description
            tournament_id (str): Unique tournament ID
        """
        self.tournament_id = tournament_id if tournament_id else str(uuid.uuid4())
        self.name = name
        self.tournament_type = tournament_type if isinstance(tournament_type, TournamentType) else TournamentType(tournament_type)
        self.num_rounds = num_rounds
        self.location = location
        self.start_date = start_date or datetime.now().isoformat()
        self.end_date = end_date
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        
        # Player management
        self.players = []  # List of player IDs
        
        # Round management
        self.rounds = []  # List of Round objects
        self.current_round = 0  # Index of current round (0 = not started)
        
        # Tournament status
        self.is_finished = False
    
    def to_dict(self):
        """Convert tournament object to dictionary for serialization"""
        return {
            'tournament_id': self.tournament_id,
            'name': self.name,
            'tournament_type': self.tournament_type.value,
            'num_rounds': self.num_rounds,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'players': self.players,
            'rounds': [r.to_dict() for r in self.rounds],
            'current_round': self.current_round,
            'is_finished': self.is_finished
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create tournament object from dictionary"""
        tournament = cls(
            name=data['name'],
            tournament_type=data['tournament_type'],
            num_rounds=data['num_rounds'],
            location=data['location'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            description=data['description'],
            tournament_id=data['tournament_id']
        )
        tournament.created_at = data['created_at']
        tournament.updated_at = data['updated_at']
        tournament.players = data.get('players', [])
        tournament.rounds = [Round.from_dict(r) for r in data.get('rounds', [])]
        tournament.current_round = data.get('current_round', 0)
        tournament.is_finished = data.get('is_finished', False)
        return tournament
    
    def save(self):
        """Save tournament to file"""
        data_dir = os.path.join('data', 'tournaments')
        os.makedirs(data_dir, exist_ok=True)
        
        self.updated_at = datetime.now().isoformat()
        
        filename = os.path.join(data_dir, f"{self.tournament_id}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, tournament_id):
        """Load tournament from file"""
        filename = os.path.join('data', 'tournaments', f"{tournament_id}.json")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls.from_dict(data)
        except FileNotFoundError:
            return None
    
    @classmethod
    def get_all(cls):
        """Get all tournaments"""
        tournaments = []
        data_dir = os.path.join('data', 'tournaments')
        os.makedirs(data_dir, exist_ok=True)
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                tournament_id = filename.replace('.json', '')
                tournament = cls.load(tournament_id)
                if tournament:
                    tournaments.append(tournament)
        
        # Sort tournaments with most recent first
        return sorted(tournaments, key=lambda t: t.start_date, reverse=True)
    
    def add_player(self, player_id):
        """Add player to tournament"""
        if player_id not in self.players:
            self.players.append(player_id)
            # Add tournament to player's history
            player = Player.load(player_id)
            if player:
                player.add_tournament(self.tournament_id)
            self.save()
            return True
        return False
    
    def remove_player(self, player_id):
        """Remove player from tournament"""
        if player_id in self.players:
            self.players.remove(player_id)
            self.save()
            return True
        return False
    
    def start_tournament(self):
        """Start the tournament"""
        if not self.is_finished and self.current_round == 0:
            self.current_round = 1
            self.save()
            return True
        return False
    
    def finish_tournament(self):
        """Mark tournament as finished"""
        self.is_finished = True
        self.end_date = datetime.now().isoformat()
        self.save()
    
    def add_round(self, round_obj):
        """Add a round to the tournament"""
        self.rounds.append(round_obj)
        self.save()
    
    def get_player_score(self, player_id):
        """Calculate player's score in the tournament"""
        score = 0.0
        for round_obj in self.rounds:
            for pairing in round_obj.pairings:
                if pairing.white_id == player_id:
                    if pairing.result == Result.WHITE_WIN or pairing.result == Result.FORFEIT_WHITE:
                        score += 1.0
                    elif pairing.result == Result.DRAW:
                        score += 0.5
                elif pairing.black_id == player_id:
                    if pairing.result == Result.BLACK_WIN or pairing.result == Result.FORFEIT_BLACK:
                        score += 1.0
                    elif pairing.result == Result.DRAW:
                        score += 0.5
        return score
    
    def get_standings(self):
        """Get current tournament standings"""
        standings = []
        for player_id in self.players:
            player = Player.load(player_id)
            if player:
                score = self.get_player_score(player_id)
                standings.append({
                    'player_id': player_id,
                    'name': player.name,
                    'rating': player.rating,
                    'score': score
                })
        
        # Sort by score (descending) and then by rating (descending)
        return sorted(standings, key=lambda x: (-x['score'], -x['rating']))
    
    def get_player_opponents(self, player_id):
        """Get all opponents a player has faced"""
        opponents = []
        for round_obj in self.rounds:
            for pairing in round_obj.pairings:
                if pairing.white_id == player_id and pairing.black_id:
                    opponents.append(pairing.black_id)
                elif pairing.black_id == player_id and pairing.white_id:
                    opponents.append(pairing.white_id)
        return opponents
    
    def __str__(self):
        return f"{self.name} ({self.tournament_type.value}, {self.num_rounds} rounds)" 