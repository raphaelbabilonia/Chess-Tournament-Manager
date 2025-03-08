"""
Player management controller
"""
from models.player import Player

def create_player(first_name, last_name, rating=None, federation=None, email=None, phone=None):
    """
    Create a new player
    
    Args:
        first_name (str): Player's first name
        last_name (str): Player's last name
        rating (int, optional): Player rating
        federation (str, optional): Chess federation
        email (str, optional): Contact email
        phone (str, optional): Contact phone
        
    Returns:
        str: Player ID if created, None otherwise
    """
    try:
        player = Player(
            first_name=first_name,
            last_name=last_name,
            rating=int(rating) if rating else None,
            federation=federation,
            email=email,
            phone=phone
        )
        player.save()
        
        return player.player_id
    except Exception as e:
        print(f"Error creating player: {e}")
        return None

def get_player(player_id):
    """
    Get a player by ID
    
    Args:
        player_id (str): Player ID
        
    Returns:
        dict: Player details or None
    """
    try:
        player = Player.load(player_id)
        if not player:
            return None
        
        return player.to_dict()
    except Exception as e:
        print(f"Error getting player: {e}")
        return None

def get_all_players():
    """
    Get all players
    
    Returns:
        list: List of player dictionaries
    """
    try:
        players = []
        for player in Player.get_all():
            players.append(player.to_dict())
        
        return players
    except Exception as e:
        print(f"Error getting all players: {e}")
        return []

def update_player(player_id, **kwargs):
    """
    Update player details
    
    Args:
        player_id (str): Player ID
        **kwargs: Player attributes to update
        
    Returns:
        bool: True if updated, False otherwise
    """
    try:
        player = Player.load(player_id)
        if not player:
            return False
        
        # Convert rating to int if provided
        if 'rating' in kwargs and kwargs['rating']:
            kwargs['rating'] = int(kwargs['rating'])
        
        player.update(**kwargs)
        return True
    except Exception as e:
        print(f"Error updating player: {e}")
        return False

def delete_player(player_id):
    """
    Delete a player
    
    Args:
        player_id (str): Player ID
        
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        player = Player.load(player_id)
        if not player:
            return False
        
        # Check if player is in any tournaments
        if player.tournaments:
            # Optional: implement logic to handle player in tournaments
            # For now, we'll allow deletion even if in tournaments
            pass
        
        return player.delete()
    except Exception as e:
        print(f"Error deleting player: {e}")
        return False

def search_players(query=None, federation=None, min_rating=None, max_rating=None):
    """
    Search for players
    
    Args:
        query (str, optional): Search query for name
        federation (str, optional): Filter by federation
        min_rating (int, optional): Minimum rating
        max_rating (int, optional): Maximum rating
        
    Returns:
        list: List of matching player dictionaries
    """
    try:
        all_players = Player.get_all()
        results = []
        
        for player in all_players:
            # Check query (name search)
            if query:
                full_name = f"{player.first_name} {player.last_name}".lower()
                if query.lower() not in full_name:
                    continue
            
            # Check federation
            if federation and (not player.federation or federation.lower() not in player.federation.lower()):
                continue
            
            # Check rating range
            if min_rating is not None and player.rating < int(min_rating):
                continue
            
            if max_rating is not None and player.rating > int(max_rating):
                continue
            
            # All filters passed
            results.append(player.to_dict())
        
        return results
    except Exception as e:
        print(f"Error searching players: {e}")
        return []

def get_player_tournaments(player_id):
    """
    Get tournaments a player is in
    
    Args:
        player_id (str): Player ID
        
    Returns:
        list: List of tournament summaries
    """
    try:
        player = Player.load(player_id)
        if not player:
            return []
        
        tournaments = []
        from models.tournament import Tournament
        
        for tournament_id in player.tournaments:
            tournament = Tournament.load(tournament_id)
            if tournament:
                tournaments.append({
                    'tournament_id': tournament.tournament_id,
                    'name': tournament.name,
                    'tournament_type': tournament.tournament_type.value,
                    'start_date': tournament.start_date,
                    'is_finished': tournament.is_finished
                })
        
        return tournaments
    except Exception as e:
        print(f"Error getting player tournaments: {e}")
        return [] 