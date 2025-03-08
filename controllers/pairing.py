"""
Pairing strategies for tournament types
"""
import random
from datetime import datetime
from models.tournament import Tournament, Round, Pairing, Result, TournamentType

class PairingStrategy:
    """Base class for pairing strategies"""
    
    @staticmethod
    def generate_pairings(tournament, round_number):
        """
        Generate pairings for a tournament round
        
        Args:
            tournament (Tournament): Tournament object
            round_number (int): Round number
            
        Returns:
            Round: Round object with generated pairings
        """
        raise NotImplementedError("Subclasses must implement this method")

class SwissPairingStrategy(PairingStrategy):
    """Swiss tournament pairing strategy"""
    
    @staticmethod
    def generate_pairings(tournament, round_number):
        """Generate pairings for a Swiss tournament round"""
        # Create a new round
        round_obj = Round(number=round_number, start_time=datetime.now().isoformat())
        
        # Get players and their scores
        player_scores = []
        for player_id in tournament.players:
            score = tournament.get_player_score(player_id)
            player_scores.append((player_id, score))
        
        # Sort players by score (highest first)
        player_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Extract just the player IDs in order
        players = [p[0] for p in player_scores]
        
        # Get previous opponents for each player
        previous_opponents = {}
        for player_id in players:
            previous_opponents[player_id] = tournament.get_player_opponents(player_id)
        
        # Create pairings
        pairings = []
        board_number = 1
        
        # Handle odd number of players - add a bye
        if len(players) % 2 != 0:
            # Find player with lowest score who hasn't had a bye yet
            bye_candidates = sorted(player_scores, key=lambda x: x[1])
            bye_player = None
            
            # Check previous rounds for byes
            players_with_byes = set()
            for r in tournament.rounds:
                for p in r.pairings:
                    if p.white_id and not p.black_id:
                        players_with_byes.add(p.white_id)
                    elif p.black_id and not p.white_id:
                        players_with_byes.add(p.black_id)
            
            for player_id, _ in bye_candidates:
                if player_id not in players_with_byes:
                    bye_player = player_id
                    break
            
            # If all players have had byes, give bye to lowest scoring player
            if not bye_player and bye_candidates:
                bye_player = bye_candidates[0][0]
            
            # Create the bye pairing (player vs None)
            if bye_player:
                pairings.append(Pairing(
                    white_id=bye_player,
                    black_id=None,
                    board_number=None,
                    result=Result.WHITE_WIN  # Bye counts as a win
                ))
                players.remove(bye_player)
        
        # Pair remaining players
        unpaired = players.copy()
        
        while len(unpaired) >= 2:
            current_player = unpaired.pop(0)
            best_opponent = None
            best_score_diff = float('inf')
            
            # Try to find best opponent who hasn't played this player before
            for potential_opponent in unpaired:
                if potential_opponent in previous_opponents[current_player]:
                    continue
                
                current_score = next((score for pid, score in player_scores if pid == current_player), 0)
                opponent_score = next((score for pid, score in player_scores if pid == potential_opponent), 0)
                score_diff = abs(current_score - opponent_score)
                
                if score_diff < best_score_diff:
                    best_opponent = potential_opponent
                    best_score_diff = score_diff
            
            # If no ideal opponent found, just take the first legal one
            if best_opponent is None:
                for potential_opponent in unpaired:
                    best_opponent = potential_opponent
                    break
            
            # If found an opponent, create the pairing
            if best_opponent:
                unpaired.remove(best_opponent)
                
                # Randomly determine colors, with higher-rated player slightly more likely to get White
                current_rating = 0
                opponent_rating = 0
                
                # Try to get player ratings
                from models.player import Player
                current_player_obj = Player.load(current_player)
                opponent_player_obj = Player.load(best_opponent)
                
                if current_player_obj and opponent_player_obj:
                    current_rating = current_player_obj.rating or 0
                    opponent_rating = opponent_player_obj.rating or 0
                
                # Determine who gets white - higher rated player gets slightly higher chance
                white_id, black_id = (current_player, best_opponent)
                if current_rating < opponent_rating:
                    # Give slight advantage to higher rated player for white
                    if random.random() < 0.55:
                        white_id, black_id = black_id, white_id
                else:
                    # Give slight advantage to higher rated player for white
                    if random.random() < 0.45:
                        white_id, black_id = black_id, white_id
                
                pairings.append(Pairing(
                    white_id=white_id,
                    black_id=black_id,
                    board_number=board_number,
                    result=Result.ONGOING
                ))
                board_number += 1
        
        # If any unpaired players remain (should be 0 or 1), give them a bye
        for player_id in unpaired:
            pairings.append(Pairing(
                white_id=player_id,
                black_id=None,
                board_number=None,
                result=Result.WHITE_WIN  # Bye counts as a win
            ))
        
        # Set board numbers for all pairings except byes
        board_pairings = [p for p in pairings if p.black_id is not None]
        for i, pairing in enumerate(board_pairings):
            pairing.board_number = i + 1
        
        # Add pairings to round
        round_obj.pairings = pairings
        
        return round_obj

class RoundRobinPairingStrategy(PairingStrategy):
    """Round Robin tournament pairing strategy"""
    
    @staticmethod
    def generate_pairings(tournament, round_number):
        """Generate pairings for a Round Robin tournament round"""
        # Create a new round
        round_obj = Round(number=round_number, start_time=datetime.now().isoformat())
        
        # For Round Robin tournaments, all pairings are pre-determined
        players = tournament.players.copy()
        
        # Handle odd number of players with a bye
        if len(players) % 2 != 0:
            players.append(None)  # Add a dummy player for byes
        
        n = len(players)
        
        # Using the "Circle Method" for round-robin tournament
        # Keep player 1 fixed, rotate others
        # https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method
        
        # Adjust round_number to be 0-indexed for calculation
        adjusted_round = round_number - 1
        
        pairings = []
        board_number = 1
        
        # Rotate players according to round number
        rotated_players = [players[0]]  # First player stays fixed
        
        # Calculate rotation for this round
        rotation = players[1:].copy()
        
        # Rotate the players the correct number of times for this round
        for _ in range(adjusted_round):
            rotation = [rotation[-1]] + rotation[:-1]
        
        rotated_players.extend(rotation)
        
        # Create pairings
        for i in range(n // 2):
            white_id = rotated_players[i]
            black_id = rotated_players[n - 1 - i]
            
            # Handle bye
            if white_id is None or black_id is None:
                real_player = white_id if white_id is not None else black_id
                pairings.append(Pairing(
                    white_id=real_player,
                    black_id=None,
                    board_number=None,
                    result=Result.WHITE_WIN  # Bye counts as a win
                ))
            else:
                # Alternate colors based on round and position
                if (i + adjusted_round) % 2 == 0:
                    white_id, black_id = black_id, white_id
                
                pairings.append(Pairing(
                    white_id=white_id,
                    black_id=black_id,
                    board_number=board_number,
                    result=Result.ONGOING
                ))
                board_number += 1
        
        # Set board numbers for all pairings except byes
        board_pairings = [p for p in pairings if p.black_id is not None]
        for i, pairing in enumerate(board_pairings):
            pairing.board_number = i + 1
        
        # Add pairings to round
        round_obj.pairings = pairings
        
        return round_obj

class KnockoutPairingStrategy(PairingStrategy):
    """Knockout tournament pairing strategy"""
    
    @staticmethod
    def generate_pairings(tournament, round_number):
        """Generate pairings for a Knockout tournament round"""
        # Create a new round
        round_obj = Round(number=round_number, start_time=datetime.now().isoformat())
        
        if round_number == 1:
            # First round - seed players by rating
            players = tournament.players.copy()
            
            # Sort players by rating
            player_ratings = []
            from models.player import Player
            for player_id in players:
                player = Player.load(player_id)
                rating = player.rating if player else 0
                player_ratings.append((player_id, rating))
            
            # Sort by rating (highest first)
            player_ratings.sort(key=lambda x: x[1], reverse=True)
            players = [p[0] for p in player_ratings]
            
            # Handle byes for uneven number of players
            while (len(players) & (len(players) - 1)) != 0:  # Check if not a power of 2
                players.append(None)  # Add byes
            
            # Create pairings (1 vs last, 2 vs second-last, etc.)
            pairings = []
            n = len(players)
            board_number = 1
            
            for i in range(n // 2):
                white_id = players[i]
                black_id = players[n - 1 - i]
                
                # Handle bye
                if white_id is None or black_id is None:
                    real_player = white_id if white_id is not None else black_id
                    pairings.append(Pairing(
                        white_id=real_player,
                        black_id=None,
                        board_number=None,
                        result=Result.WHITE_WIN  # Bye counts as a win
                    ))
                else:
                    # Randomly assign colors
                    if random.random() < 0.5:
                        white_id, black_id = black_id, white_id
                    
                    pairings.append(Pairing(
                        white_id=white_id,
                        black_id=black_id,
                        board_number=board_number,
                        result=Result.ONGOING
                    ))
                    board_number += 1
        else:
            # Subsequent rounds - pair winners from previous round
            previous_round = None
            for r in tournament.rounds:
                if r.number == round_number - 1:
                    previous_round = r
                    break
            
            if not previous_round:
                raise ValueError(f"Cannot find previous round {round_number - 1}")
            
            # Get winners from previous round
            winners = []
            for pairing in previous_round.pairings:
                if pairing.result == Result.WHITE_WIN or pairing.result == Result.FORFEIT_WHITE:
                    winners.append(pairing.white_id)
                elif pairing.result == Result.BLACK_WIN or pairing.result == Result.FORFEIT_BLACK:
                    winners.append(pairing.black_id)
                elif pairing.result == Result.DRAW:
                    # For knockout tournaments, need to resolve draws
                    # Here we'll just randomly pick a winner, but in practice
                    # you'd implement tiebreaks like Armageddon or rapid games
                    if random.random() < 0.5:
                        winners.append(pairing.white_id)
                    else:
                        winners.append(pairing.black_id)
            
            # Create pairings for this round
            pairings = []
            board_number = 1
            
            for i in range(0, len(winners), 2):
                # Check if we have enough players to pair
                if i + 1 < len(winners):
                    white_id = winners[i]
                    black_id = winners[i + 1]
                    
                    # Randomly assign colors
                    if random.random() < 0.5:
                        white_id, black_id = black_id, white_id
                    
                    pairings.append(Pairing(
                        white_id=white_id,
                        black_id=black_id,
                        board_number=board_number,
                        result=Result.ONGOING
                    ))
                    board_number += 1
                else:
                    # Odd number of winners (shouldn't happen in knockout, but handle it)
                    pairings.append(Pairing(
                        white_id=winners[i],
                        black_id=None,
                        board_number=None,
                        result=Result.WHITE_WIN
                    ))
        
        # Set board numbers for all pairings except byes
        board_pairings = [p for p in pairings if p.black_id is not None]
        for i, pairing in enumerate(board_pairings):
            pairing.board_number = i + 1
        
        # Add pairings to round
        round_obj.pairings = pairings
        
        return round_obj

def get_pairing_strategy(tournament_type):
    """
    Factory method to get appropriate pairing strategy
    
    Args:
        tournament_type (TournamentType): Type of tournament
        
    Returns:
        PairingStrategy: Appropriate pairing strategy
    """
    strategies = {
        TournamentType.SWISS: SwissPairingStrategy,
        TournamentType.ROUND_ROBIN: RoundRobinPairingStrategy,
        TournamentType.KNOCKOUT: KnockoutPairingStrategy
    }
    
    return strategies.get(tournament_type)

def generate_pairings(tournament_id, round_number=None):
    """
    Generate pairings for the next round of a tournament
    
    Args:
        tournament_id (str): Tournament ID
        round_number (int, optional): Round number. If None, use current round.
        
    Returns:
        bool: True if pairings were generated, False otherwise
    """
    tournament = Tournament.load(tournament_id)
    if not tournament:
        return False
    
    # If round_number not specified, use current round
    if round_number is None:
        round_number = tournament.current_round
    
    # Check if this round already has pairings
    for round_obj in tournament.rounds:
        if round_obj.number == round_number:
            return False  # Pairings already exist
    
    # Get appropriate pairing strategy
    strategy_class = get_pairing_strategy(tournament.tournament_type)
    if not strategy_class:
        return False
    
    # Generate pairings
    try:
        round_obj = strategy_class.generate_pairings(tournament, round_number)
        tournament.add_round(round_obj)
        return True
    except Exception as e:
        print(f"Error generating pairings: {e}")
        return False 