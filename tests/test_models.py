"""
Tests for the models module
"""
import unittest
import os
import sys
import json
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.player import Player
from models.tournament import Tournament, TournamentType


class TestPlayer(unittest.TestCase):
    """Test cases for the Player class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.player = Player(
            first_name="Magnus",
            last_name="Carlsen",
            rating=2850,
            federation="FIDE",
            email="magnus@example.com",
            player_id="12345"
        )
    
    def test_player_creation(self):
        """Test player creation with valid data"""
        self.assertEqual(self.player.first_name, "Magnus")
        self.assertEqual(self.player.last_name, "Carlsen")
        self.assertEqual(self.player.rating, 2850)
        self.assertEqual(self.player.federation, "FIDE")
        self.assertEqual(self.player.player_id, "12345")
    
    def test_player_full_name(self):
        """Test player full name property"""
        self.assertEqual(self.player.full_name, "Magnus Carlsen")
    
    def test_player_to_dict(self):
        """Test player to_dict method"""
        player_dict = self.player.to_dict()
        self.assertIsInstance(player_dict, dict)
        self.assertEqual(player_dict["first_name"], "Magnus")
        self.assertEqual(player_dict["last_name"], "Carlsen")
        self.assertEqual(player_dict["player_id"], "12345")
    
    def test_player_from_dict(self):
        """Test player from_dict method"""
        player_dict = {
            "first_name": "Hikaru",
            "last_name": "Nakamura",
            "rating": 2750,
            "federation": "USCF",
            "email": "hikaru@example.com",
            "player_id": "54321",
            "phone": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "tournaments": []
        }
        player = Player.from_dict(player_dict)
        self.assertEqual(player.first_name, "Hikaru")
        self.assertEqual(player.last_name, "Nakamura")
        self.assertEqual(player.player_id, "54321")


class TestTournament(unittest.TestCase):
    """Test cases for the Tournament class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tournament = Tournament(
            name="World Chess Championship",
            tournament_type=TournamentType.SWISS,
            num_rounds=14,
            location="London",
            start_date="2023-11-01",
            end_date="2023-11-30",
            description="The ultimate chess championship"
        )
        
        # Add some players to the tournament
        self.player1_id = "12345"
        self.player2_id = "23456"
        self.tournament.add_player(self.player1_id)
        self.tournament.add_player(self.player2_id)
    
    def test_tournament_creation(self):
        """Test tournament creation with valid data"""
        self.assertEqual(self.tournament.name, "World Chess Championship")
        self.assertEqual(self.tournament.location, "London")
        self.assertEqual(self.tournament.start_date, "2023-11-01")
        self.assertEqual(self.tournament.num_rounds, 14)
    
    def test_add_player(self):
        """Test adding a player to the tournament"""
        player3_id = "34567"
        self.tournament.add_player(player3_id)
        self.assertEqual(len(self.tournament.players), 3)
        self.assertIn(player3_id, self.tournament.players)
    
    def test_remove_player(self):
        """Test removing a player from the tournament"""
        self.tournament.remove_player(self.player1_id)
        self.assertEqual(len(self.tournament.players), 1)
        self.assertNotIn(self.player1_id, self.tournament.players)
    
    def test_tournament_to_dict(self):
        """Test tournament to_dict method"""
        tournament_dict = self.tournament.to_dict()
        self.assertIsInstance(tournament_dict, dict)
        self.assertEqual(tournament_dict["name"], "World Chess Championship")
        self.assertEqual(tournament_dict["location"], "London")
        self.assertEqual(len(tournament_dict["players"]), 2)
    
    def test_tournament_from_dict(self):
        """Test tournament from_dict method"""
        tournament_dict = {
            "name": "Candidates Tournament",
            "tournament_type": "Swiss",
            "num_rounds": 8,
            "location": "Berlin",
            "start_date": "2023-10-01",
            "end_date": "2023-10-15",
            "description": "Qualifier for the World Championship",
            "tournament_id": "tourn123",
            "players": [],
            "rounds": [],
            "status": "upcoming",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        tournament = Tournament.from_dict(tournament_dict)
        self.assertEqual(tournament.name, "Candidates Tournament")
        self.assertEqual(tournament.location, "Berlin")
        self.assertEqual(tournament.num_rounds, 8)


if __name__ == "__main__":
    unittest.main() 