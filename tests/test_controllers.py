"""
Tests for the controllers module
"""
import unittest
import os
import sys
import json
import tempfile
import shutil
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.player import Player
from models.tournament import Tournament, TournamentType
import controllers.player as player_controller
import controllers.tournament as tournament_controller
import controllers.pairing as pairing_controller


class TestPlayerController(unittest.TestCase):
    """Test cases for the player controller functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for test data
        self.test_data_dir = tempfile.mkdtemp()
        self.players_dir = os.path.join(self.test_data_dir, "data", "players")
        os.makedirs(self.players_dir, exist_ok=True)
        
        # Set data directory for saving/loading
        Player._data_dir = os.path.join(self.test_data_dir, "data")
        
        # Create test player data
        self.player1_data = {
            "first_name": "Magnus",
            "last_name": "Carlsen",
            "rating": 2850,
            "federation": "FIDE",
            "email": "magnus@example.com"
        }
        
        self.player2_data = {
            "first_name": "Fabiano",
            "last_name": "Caruana",
            "rating": 2800,
            "federation": "USCF",
            "email": "fabiano@example.com"
        }
    
    def tearDown(self):
        """Clean up after tests"""
        shutil.rmtree(self.test_data_dir)
    
    def test_create_player(self):
        """Test creating a player"""
        player_id = player_controller.create_player(**self.player1_data)
        self.assertIsNotNone(player_id)
        
        # Check if the player file exists
        player_file = os.path.join(self.players_dir, f"{player_id}.json")
        self.assertTrue(os.path.exists(player_file))
    
    def test_get_player(self):
        """Test getting a player by ID"""
        # First create the player
        player_id = player_controller.create_player(**self.player1_data)
        
        # Then get the player
        player = player_controller.get_player(player_id)
        self.assertIsNotNone(player)
        self.assertEqual(player["first_name"], "Magnus")
        self.assertEqual(player["last_name"], "Carlsen")
    
    def test_update_player(self):
        """Test updating a player"""
        # First create the player
        player_id = player_controller.create_player(**self.player1_data)
        
        # Update the player's rating
        result = player_controller.update_player(player_id, rating=2860)
        self.assertTrue(result)
        
        # Get the updated player
        updated_player = player_controller.get_player(player_id)
        self.assertEqual(updated_player["rating"], 2860)
    
    def test_delete_player(self):
        """Test deleting a player"""
        # First create the player
        player_id = player_controller.create_player(**self.player1_data)
        
        # Check that the player exists
        player_file = os.path.join(self.players_dir, f"{player_id}.json")
        self.assertTrue(os.path.exists(player_file))
        
        # Delete the player
        result = player_controller.delete_player(player_id)
        self.assertTrue(result)
        
        # Check that the player file no longer exists
        self.assertFalse(os.path.exists(player_file))
    
    def test_get_all_players(self):
        """Test getting all players"""
        # Create multiple players
        player_id1 = player_controller.create_player(**self.player1_data)
        player_id2 = player_controller.create_player(**self.player2_data)
        
        # Get all players
        all_players = player_controller.get_all_players()
        self.assertIsInstance(all_players, list)
        self.assertEqual(len(all_players), 2)
        
        # Check if both players are in the list
        player_ids = [p["player_id"] for p in all_players]
        self.assertIn(player_id1, player_ids)
        self.assertIn(player_id2, player_ids)


class TestTournamentController(unittest.TestCase):
    """Test cases for the tournament controller functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for test data
        self.test_data_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.test_data_dir, "data")
        self.tournaments_dir = os.path.join(self.data_dir, "tournaments")
        self.players_dir = os.path.join(self.data_dir, "players")
        
        os.makedirs(self.tournaments_dir, exist_ok=True)
        os.makedirs(self.players_dir, exist_ok=True)
        
        # Set data directory for saving/loading
        Tournament._data_dir = self.data_dir
        Player._data_dir = self.data_dir
        
        # Create test tournament data
        self.tournament_data = {
            "name": "Test Tournament",
            "tournament_type": "Swiss",
            "num_rounds": 5,
            "location": "Test Location",
            "start_date": "2023-12-01",
            "end_date": "2023-12-10",
            "description": "Test tournament for unit tests"
        }
        
        # Create test players
        player1 = Player(
            first_name="Magnus",
            last_name="Carlsen",
            rating=2850,
            federation="FIDE"
        )
        player1.save()
        
        player2 = Player(
            first_name="Fabiano",
            last_name="Caruana",
            rating=2800,
            federation="USCF"
        )
        player2.save()
        
        self.player1_id = player1.player_id
        self.player2_id = player2.player_id
    
    def tearDown(self):
        """Clean up after tests"""
        shutil.rmtree(self.test_data_dir)
    
    def test_create_tournament(self):
        """Test creating a tournament"""
        tournament_id = tournament_controller.create_tournament(**self.tournament_data)
        self.assertIsNotNone(tournament_id)
        
        # Check if the tournament file exists
        tournament_file = os.path.join(self.tournaments_dir, f"{tournament_id}.json")
        self.assertTrue(os.path.exists(tournament_file))
    
    def test_get_tournament(self):
        """Test getting a tournament by ID"""
        # First create the tournament
        tournament_id = tournament_controller.create_tournament(**self.tournament_data)
        
        # Then get the tournament
        tournament = tournament_controller.get_tournament(tournament_id)
        self.assertIsNotNone(tournament)
        self.assertEqual(tournament["name"], "Test Tournament")
        self.assertEqual(tournament["location"], "Test Location")
    
    def test_update_tournament(self):
        """Test updating a tournament"""
        # First create the tournament
        tournament_id = tournament_controller.create_tournament(**self.tournament_data)
        
        # Update the tournament description
        result = tournament_controller.update_tournament(tournament_id, description="Updated description")
        self.assertTrue(result)
        
        # Get the updated tournament
        updated_tournament = tournament_controller.get_tournament(tournament_id)
        self.assertEqual(updated_tournament["description"], "Updated description")
    
    def test_add_player_to_tournament(self):
        """Test adding a player to a tournament"""
        # First create the tournament
        tournament_id = tournament_controller.create_tournament(**self.tournament_data)
        
        # Add a player to the tournament
        result = tournament_controller.add_player_to_tournament(tournament_id, self.player1_id)
        self.assertTrue(result)
        
        # Get the updated tournament
        tournament = tournament_controller.get_tournament(tournament_id)
        self.assertIn(self.player1_id, tournament["players"])
    
    def test_remove_player_from_tournament(self):
        """Test removing a player from a tournament"""
        # First create the tournament and add players
        tournament_id = tournament_controller.create_tournament(**self.tournament_data)
        tournament_controller.add_player_to_tournament(tournament_id, self.player1_id)
        tournament_controller.add_player_to_tournament(tournament_id, self.player2_id)
        
        # Remove a player
        result = tournament_controller.remove_player_from_tournament(tournament_id, self.player1_id)
        self.assertTrue(result)
        
        # Get the updated tournament
        tournament = tournament_controller.get_tournament(tournament_id)
        self.assertNotIn(self.player1_id, tournament["players"])
        self.assertIn(self.player2_id, tournament["players"])
    
    def test_delete_tournament(self):
        """Test deleting a tournament"""
        # First create the tournament
        tournament_id = tournament_controller.create_tournament(**self.tournament_data)
        
        # Delete the tournament
        result = tournament_controller.delete_tournament(tournament_id)
        self.assertTrue(result)
        
        # Check that the tournament file no longer exists
        tournament_file = os.path.join(self.tournaments_dir, f"{tournament_id}.json")
        self.assertFalse(os.path.exists(tournament_file))
    
    def test_get_all_tournaments(self):
        """Test getting all tournaments"""
        # Create multiple tournaments
        tournament_data2 = self.tournament_data.copy()
        tournament_data2["name"] = "Second Tournament"
        
        tournament_id1 = tournament_controller.create_tournament(**self.tournament_data)
        tournament_id2 = tournament_controller.create_tournament(**tournament_data2)
        
        # Get all tournaments
        all_tournaments = tournament_controller.get_all_tournaments()
        self.assertIsInstance(all_tournaments, list)
        self.assertEqual(len(all_tournaments), 2)
        
        # Check if both tournaments are in the list
        tournament_ids = [t["tournament_id"] for t in all_tournaments]
        self.assertIn(tournament_id1, tournament_ids)
        self.assertIn(tournament_id2, tournament_ids)


if __name__ == "__main__":
    unittest.main() 