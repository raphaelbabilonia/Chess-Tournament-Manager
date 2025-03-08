"""
Tournament management controller
"""
from datetime import datetime
from models.tournament import Tournament, Round, Pairing, Result, TournamentType
from models.player import Player
from controllers.pairing import generate_pairings

def create_tournament(name, tournament_type, num_rounds, location="", 
                      start_date=None, end_date=None, description=""):
    """
    Create a new tournament
    
    Args:
        name (str): Tournament name
        tournament_type (str): Tournament type (Swiss, Round Robin, Knockout)
        num_rounds (int): Number of rounds
        location (str): Tournament location
        start_date (str, optional): Tournament start date. Defaults to today.
        end_date (str, optional): Tournament end date
        description (str, optional): Tournament description
        
    Returns:
        str: Tournament ID if created, None otherwise
    """
    try:
        # Convert tournament_type string to enum
        t_type = None
        for tt in TournamentType:
            if tt.value.lower() == tournament_type.lower():
                t_type = tt
                break
        
        if t_type is None:
            return None
        
        # Create tournament
        tournament = Tournament(
            name=name,
            tournament_type=t_type,
            num_rounds=int(num_rounds),
            location=location,
            start_date=start_date or datetime.now().isoformat(),
            end_date=end_date,
            description=description
        )
        tournament.save()
        
        return tournament.tournament_id
    except Exception as e:
        print(f"Error creating tournament: {e}")
        return None

def update_tournament(tournament_id, **kwargs):
    """
    Update tournament details
    
    Args:
        tournament_id (str): Tournament ID
        **kwargs: Tournament attributes to update
        
    Returns:
        bool: True if updated, False otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament:
            return False
        
        # Handle tournament_type conversion
        if 'tournament_type' in kwargs:
            t_type = None
            for tt in TournamentType:
                if tt.value.lower() == kwargs['tournament_type'].lower():
                    t_type = tt
                    break
            
            if t_type is not None:
                tournament.tournament_type = t_type
                del kwargs['tournament_type']
        
        # Update other attributes
        for key, value in kwargs.items():
            if hasattr(tournament, key) and key not in ['tournament_id', 'created_at', 'updated_at']:
                setattr(tournament, key, value)
        
        tournament.save()
        return True
    except Exception as e:
        print(f"Error updating tournament: {e}")
        return False

def start_tournament(tournament_id):
    """
    Start a tournament
    
    Args:
        tournament_id (str): Tournament ID
        
    Returns:
        bool: True if started, False otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament:
            return False
        
        # Start tournament
        return tournament.start_tournament()
    except Exception as e:
        print(f"Error starting tournament: {e}")
        return False

def finish_tournament(tournament_id):
    """
    Finish a tournament
    
    Args:
        tournament_id (str): Tournament ID
        
    Returns:
        bool: True if finished, False otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament:
            return False
        
        tournament.finish_tournament()
        return True
    except Exception as e:
        print(f"Error finishing tournament: {e}")
        return False

def add_player_to_tournament(tournament_id, player_id):
    """
    Add a player to a tournament
    
    Args:
        tournament_id (str): Tournament ID
        player_id (str): Player ID
        
    Returns:
        bool: True if added, False otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament or tournament.current_round > 0:
            return False
        
        player = Player.load(player_id)
        if not player:
            return False
        
        return tournament.add_player(player_id)
    except Exception as e:
        print(f"Error adding player to tournament: {e}")
        return False

def remove_player_from_tournament(tournament_id, player_id):
    """
    Remove a player from a tournament
    
    Args:
        tournament_id (str): Tournament ID
        player_id (str): Player ID
        
    Returns:
        bool: True if removed, False otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament or tournament.current_round > 0:
            return False
        
        return tournament.remove_player(player_id)
    except Exception as e:
        print(f"Error removing player from tournament: {e}")
        return False

def start_next_round(tournament_id):
    """
    Start the next round of a tournament
    
    Args:
        tournament_id (str): Tournament ID
        
    Returns:
        bool: True if started, False otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament or tournament.is_finished:
            return False
        
        # If tournament hasn't started yet
        if tournament.current_round == 0:
            if not tournament.start_tournament():
                return False
        else:
            # Move to next round
            tournament.current_round += 1
            tournament.save()
        
        # Generate pairings for the current round
        return generate_pairings(tournament_id)
    except Exception as e:
        print(f"Error starting next round: {e}")
        return False

def update_result(tournament_id, round_number, board_number, result):
    """
    Update the result of a game
    
    Args:
        tournament_id (str): Tournament ID
        round_number (int): Round number
        board_number (int): Board number
        result (str): Game result (1-0, 0-1, 1/2-1/2, etc.)
        
    Returns:
        bool: True if updated, False otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament:
            return False
        
        # Find the round
        round_obj = None
        for r in tournament.rounds:
            if r.number == round_number:
                round_obj = r
                break
        
        if not round_obj:
            return False
        
        # Find the pairing
        pairing = None
        for p in round_obj.pairings:
            if p.board_number == board_number:
                pairing = p
                break
        
        if not pairing:
            return False
        
        # Update result
        try:
            pairing.result = Result(result)
            tournament.save()
            return True
        except ValueError:
            return False
    except Exception as e:
        print(f"Error updating result: {e}")
        return False

def get_tournament_report(tournament_id):
    """
    Generate a report for a tournament
    
    Args:
        tournament_id (str): Tournament ID
        
    Returns:
        dict: Tournament report or None
    """
    try:
        tournament = Tournament.load(tournament_id)
        if not tournament:
            return None
        
        # Get player details
        players = {}
        for player_id in tournament.players:
            player = Player.load(player_id)
            if player:
                players[player_id] = {
                    'name': player.name,
                    'rating': player.rating,
                    'federation': player.federation
                }
        
        # Get standings
        standings = tournament.get_standings()
        
        # Get round details
        rounds = []
        for round_obj in tournament.rounds:
            pairings = []
            for pairing in round_obj.pairings:
                # Skip byes in detailed report
                if pairing.white_id and pairing.black_id:
                    white_name = players.get(pairing.white_id, {}).get('name', 'Unknown')
                    black_name = players.get(pairing.black_id, {}).get('name', 'Unknown')
                    
                    pairings.append({
                        'board': pairing.board_number,
                        'white': white_name,
                        'black': black_name,
                        'result': pairing.result.value
                    })
            
            rounds.append({
                'number': round_obj.number,
                'pairings': pairings,
                'start_time': round_obj.start_time,
                'end_time': round_obj.end_time
            })
        
        # Build report
        report = {
            'tournament': {
                'id': tournament.tournament_id,
                'name': tournament.name,
                'type': tournament.tournament_type.value,
                'rounds': tournament.num_rounds,
                'location': tournament.location,
                'start_date': tournament.start_date,
                'end_date': tournament.end_date,
                'description': tournament.description,
                'current_round': tournament.current_round,
                'is_finished': tournament.is_finished
            },
            'players': len(players),
            'standings': standings,
            'rounds': rounds
        }
        
        return report
    except Exception as e:
        print(f"Error generating tournament report: {e}")
        return None

def delete_tournament(tournament_id):
    """
    Delete a tournament
    
    Args:
        tournament_id (str): Tournament ID
        
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        # First load the tournament to ensure it exists
        tournament = Tournament.load(tournament_id)
        if not tournament:
            return False
        
        # Remove tournament from players' histories
        for player_id in tournament.players:
            player = Player.load(player_id)
            if player and tournament_id in player.tournaments:
                player.tournaments.remove(tournament_id)
                player.save()
        
        # Delete tournament file
        import os
        filename = os.path.join('data', 'tournaments', f"{tournament_id}.json")
        if os.path.exists(filename):
            os.remove(filename)
            return True
        
        return False
    except Exception as e:
        print(f"Error deleting tournament: {e}")
        return False

def get_all_tournaments():
    """
    Get all tournaments
    
    Returns:
        list: List of tournament dictionaries
    """
    try:
        tournaments = Tournament.get_all()
        return [tournament.to_dict() for tournament in tournaments]
    except Exception as e:
        print(f"Error getting tournaments: {e}")
        return []

def get_tournament(tournament_id):
    """
    Get a tournament by ID
    
    Args:
        tournament_id (str): Tournament ID
        
    Returns:
        dict: Tournament data if found, None otherwise
    """
    try:
        tournament = Tournament.load(tournament_id)
        if tournament:
            return tournament.to_dict()
        return None
    except Exception as e:
        print(f"Error getting tournament: {e}")
        return None 