"""
Controllers package for Chess Tournament Manager
"""

from controllers.player import (
    create_player,
    get_player,
    get_all_players,
    update_player,
    delete_player,
    search_players,
    get_player_tournaments
)

from controllers.tournament import (
    create_tournament,
    update_tournament,
    start_tournament,
    finish_tournament,
    add_player_to_tournament,
    remove_player_from_tournament,
    start_next_round,
    update_result,
    get_tournament_report,
    delete_tournament
)

from controllers.pairing import (
    generate_pairings
)

__all__ = [
    # Player controllers
    'create_player',
    'get_player',
    'get_all_players',
    'update_player',
    'delete_player',
    'search_players',
    'get_player_tournaments',
    
    # Tournament controllers
    'create_tournament',
    'update_tournament',
    'start_tournament',
    'finish_tournament',
    'add_player_to_tournament',
    'remove_player_from_tournament',
    'start_next_round',
    'update_result',
    'get_tournament_report',
    'delete_tournament',
    
    # Pairing controllers
    'generate_pairings'
] 