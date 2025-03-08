"""
Integration tests for the Chess Tournament Manager application
"""
import unittest
import os
import sys
import tempfile
import shutil
import json
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.player import Player
from models.tournament import Tournament, TournamentType, Result
import controllers.player as player_controller
import controllers.tournament as tournament_controller
from utils.helpers import ensure_data_directories


class TestApplicationFlow(unittest.TestCase):
    """Integration tests for the entire application flow"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for test data
        self.test_data_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_data_dir, "data", "players"), exist_ok=True)
        os.makedirs(os.path.join(self.test_data_dir, "data", "tournaments"), exist_ok=True)
        
        # Set data directory for saving/loading
        Player._data_dir = os.path.join(self.test_data_dir, "data")
        Tournament._data_dir = os.path.join(self.test_data_dir, "data")
        
        # Create test players
        self.players = []
        for i in range(1, 9):
            player_data = {
                "first_name": f"Player{i}",
                "last_name": f"Last{i}",
                "rating": 2000 + i * 50,
                "federation": "TEST"
            }
            player_id = player_controller.create_player(**player_data)
            self.players.append(player_id)
    
    def tearDown(self):
        """Clean up after tests"""
        shutil.rmtree(self.test_data_dir)
    
    def test_complete_tournament_flow(self):
        """Test a complete tournament flow from creation to completion"""
        # 1. Create a tournament
        tournament_data = {
            "name": "Integration Test Tournament",
            "tournament_type": "Swiss",
            "num_rounds": 3,
            "location": "Test Location",
            "start_date": "2023-12-01",
            "end_date": "2023-12-10",
            "description": "Tournament for integration testing"
        }
        
        tournament_id = tournament_controller.create_tournament(**tournament_data)
        self.assertIsNotNone(tournament_id)
        
        # 2. Add players to the tournament
        for player_id in self.players:
            result = tournament_controller.add_player_to_tournament(tournament_id, player_id)
            self.assertTrue(result)
        
        # 3. Start the tournament
        result = tournament_controller.start_tournament(tournament_id)
        self.assertTrue(result)
        
        # 4. Run three rounds
        for round_num in range(1, 4):
            # Start the next round
            round_result = tournament_controller.start_next_round(tournament_id)
            self.assertTrue(round_result)
            
            # Get the tournament data to examine the pairings
            tournament = tournament_controller.get_tournament(tournament_id)
            self.assertIsNotNone(tournament)
            
            # Get the current round
            current_round = tournament["rounds"][-1]
            self.assertEqual(current_round["number"], round_num)
            
            # Enter results - alternate between white wins and black wins
            for i, pairing in enumerate(current_round["pairings"]):
                board_number = pairing["board_number"]
                if i % 2 == 0:
                    # White wins
                    result_str = Result.WHITE_WIN.value
                else:
                    # Black wins
                    result_str = Result.BLACK_WIN.value
                
                # Update the result
                update_result = tournament_controller.update_result(
                    tournament_id, round_num, board_number, result_str
                )
                self.assertTrue(update_result)
        
        # 5. Get tournament report
        from controllers.tournament import get_tournament_report
        report = get_tournament_report(tournament_id)
        self.assertIsNotNone(report)
        
        # Check tournament data
        self.assertEqual(report["tournament"]["name"], "Integration Test Tournament")
        self.assertEqual(len(report["rounds"]), 3)
        
        # Check standings
        self.assertEqual(len(report["standings"]), 8)
        
        # The total points should add up to the correct number
        # (4 games per round, 3 rounds = 12 total points)
        total_points = sum(float(player["score"]) for player in report["standings"])
        self.assertEqual(total_points, 12.0)
    
    def test_player_management_flow(self):
        """Test the player management flow"""
        # 1. Check if all players were added correctly
        all_players = player_controller.get_all_players()
        self.assertEqual(len(all_players), 8)
        
        # 2. Update a player's rating
        player_id = self.players[0]
        original_player = player_controller.get_player(player_id)
        original_rating = original_player["rating"]
        
        # Update rating
        result = player_controller.update_player(player_id, rating=original_rating + 100)
        self.assertTrue(result)
        
        # Get updated player
        updated_player = player_controller.get_player(player_id)
        self.assertEqual(updated_player["rating"], original_rating + 100)
        
        # 3. Delete a player
        player_to_delete = self.players[7]
        result = player_controller.delete_player(player_to_delete)
        self.assertTrue(result)
        
        # Check player was deleted
        all_players_after = player_controller.get_all_players()
        self.assertEqual(len(all_players_after), 7)
        
        # 4. Add a new player
        new_player_data = {
            "first_name": "New",
            "last_name": "Player",
            "rating": 2100,
            "federation": "TEST"
        }
        new_player_id = player_controller.create_player(**new_player_data)
        self.assertIsNotNone(new_player_id)
        
        # Check new player was added
        all_players_final = player_controller.get_all_players()
        self.assertEqual(len(all_players_final), 8)
        
        # Check new player exists
        new_player = player_controller.get_player(new_player_id)
        self.assertEqual(new_player["first_name"], "New")
        self.assertEqual(new_player["last_name"], "Player")
    
    def test_tournament_management_flow(self):
        """Test the tournament management flow"""
        # 1. Create two tournaments
        tournament1_data = {
            "name": "First Tournament",
            "tournament_type": "Swiss",
            "num_rounds": 5,
            "location": "Location 1",
            "start_date": "2023-11-01",
            "end_date": "2023-11-10",
            "description": "First test tournament"
        }
        
        tournament2_data = {
            "name": "Second Tournament",
            "tournament_type": "Round Robin",
            "num_rounds": 7,
            "location": "Location 2",
            "start_date": "2023-12-01",
            "end_date": "2023-12-10",
            "description": "Second test tournament"
        }
        
        tournament1_id = tournament_controller.create_tournament(**tournament1_data)
        tournament2_id = tournament_controller.create_tournament(**tournament2_data)
        
        self.assertIsNotNone(tournament1_id)
        self.assertIsNotNone(tournament2_id)
        
        # 2. Add players to tournaments (first 4 to tournament1, last 4 to tournament2)
        for i, player_id in enumerate(self.players):
            if i < 4:
                result = tournament_controller.add_player_to_tournament(tournament1_id, player_id)
            else:
                result = tournament_controller.add_player_to_tournament(tournament2_id, player_id)
            self.assertTrue(result)
        
        # 3. Get all tournaments
        all_tournaments = tournament_controller.get_all_tournaments()
        self.assertEqual(len(all_tournaments), 2)
        
        # 4. Update tournament
        result = tournament_controller.update_tournament(
            tournament1_id, description="Updated description"
        )
        self.assertTrue(result)
        
        # Check update
        updated_tournament = tournament_controller.get_tournament(tournament1_id)
        self.assertEqual(updated_tournament["description"], "Updated description")
        
        # 5. Delete tournament
        result = tournament_controller.delete_tournament(tournament2_id)
        self.assertTrue(result)
        
        # Check deletion
        remaining_tournaments = tournament_controller.get_all_tournaments()
        self.assertEqual(len(remaining_tournaments), 1)
        self.assertEqual(remaining_tournaments[0]["tournament_id"], tournament1_id)


if __name__ == "__main__":
    unittest.main() 