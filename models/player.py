"""
Player model for Chess Tournament Manager
"""
import uuid
import json
import os
from datetime import datetime

class Player:
    """
    Class representing a chess player
    """
    def __init__(self, first_name, last_name, rating=None, federation=None, email=None, phone=None, player_id=None):
        """
        Initialize a player with required attributes
        
        Args:
            first_name (str): First name of the player
            last_name (str): Last name of the player
            rating (int, optional): Chess rating
            federation (str, optional): Chess federation (e.g., FIDE, USCF)
            email (str, optional): Contact email
            phone (str, optional): Contact phone number
            player_id (str, optional): Unique player ID (generated if not provided)
        """
        self.player_id = player_id if player_id else str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.rating = rating or 0
        self.federation = federation or ""
        self.email = email or ""
        self.phone = phone or ""
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        
        # Tournament history
        self.tournaments = []
        
    def to_dict(self):
        """Convert player object to dictionary for serialization"""
        return {
            'player_id': self.player_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'rating': self.rating,
            'federation': self.federation,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'tournaments': self.tournaments
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create player object from dictionary"""
        # Handle backward compatibility with old data format
        if 'name' in data and 'first_name' not in data and 'last_name' not in data:
            # Split the name into first and last name (best effort)
            name_parts = data['name'].split(maxsplit=1)
            first_name = name_parts[0] if name_parts else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""
        else:
            first_name = data.get('first_name', "")
            last_name = data.get('last_name', "")
            
        player = cls(
            first_name=first_name,
            last_name=last_name,
            rating=data.get('rating', 0),
            federation=data.get('federation', ""),
            email=data.get('email', ""),
            phone=data.get('phone', ""),
            player_id=data.get('player_id', "")
        )
        player.created_at = data.get('created_at', datetime.now().isoformat())
        player.updated_at = data.get('updated_at', player.created_at)
        player.tournaments = data.get('tournaments', [])
        return player
    
    def save(self):
        """Save player to file"""
        data_dir = os.path.join('data', 'players')
        os.makedirs(data_dir, exist_ok=True)
        
        self.updated_at = datetime.now().isoformat()
        
        filename = os.path.join(data_dir, f"{self.player_id}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, player_id):
        """Load player from file"""
        filename = os.path.join('data', 'players', f"{player_id}.json")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls.from_dict(data)
        except FileNotFoundError:
            return None
    
    @classmethod
    def get_all(cls):
        """Get all players"""
        players = []
        data_dir = os.path.join('data', 'players')
        os.makedirs(data_dir, exist_ok=True)
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                player_id = filename.replace('.json', '')
                player = cls.load(player_id)
                if player:
                    players.append(player)
        
        return sorted(players, key=lambda p: p.last_name)
    
    def update(self, **kwargs):
        """Update player attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['player_id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        
        self.updated_at = datetime.now().isoformat()
        self.save()
    
    def add_tournament(self, tournament_id):
        """Add tournament to player's history"""
        if tournament_id not in self.tournaments:
            self.tournaments.append(tournament_id)
            self.save()
    
    def delete(self):
        """Delete player from storage"""
        filename = os.path.join('data', 'players', f"{self.player_id}.json")
        if os.path.exists(filename):
            os.remove(filename)
            return True
        return False
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rating})"
    
    @property
    def full_name(self):
        """Get player's full name"""
        return f"{self.first_name} {self.last_name}" 