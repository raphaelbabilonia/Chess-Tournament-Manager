"""
Command-line interface for Chess Tournament Manager
"""
import os
import sys
import time
from datetime import datetime
from tabulate import tabulate
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import controllers
from controllers.player import (
    create_player, get_player, get_all_players, update_player, delete_player,
    search_players, get_player_tournaments
)
from controllers.tournament import (
    create_tournament, update_tournament, start_tournament, finish_tournament,
    add_player_to_tournament, remove_player_from_tournament, start_next_round,
    update_result, get_tournament_report, delete_tournament
)
from controllers.pairing import generate_pairings
from models.tournament import TournamentType, Result

# Initialize Rich console
console = Console()

class ChessTournamentManagerCLI:
    """Command-line interface for the Chess Tournament Manager"""
    
    def __init__(self):
        """Initialize the CLI"""
        self.running = True
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a header with the given title"""
        console.print(Panel(f"[bold white]{title}[/bold white]", width=80, style="blue"))
        print()
    
    def print_success(self, message):
        """Print a success message"""
        console.print(f"[bold green]✓ {message}[/bold green]")
        print()
    
    def print_error(self, message):
        """Print an error message"""
        console.print(f"[bold red]✗ {message}[/bold red]")
        print()
    
    def print_info(self, message):
        """Print an info message"""
        console.print(f"[bold blue]ℹ {message}[/bold blue]")
        print()
    
    def print_table(self, headers, data):
        """Print a table with the given headers and data"""
        table = Table()
        
        for header in headers:
            table.add_column(header, style="bold")
        
        for row in data:
            table.add_row(*[str(item) for item in row])
        
        console.print(table)
        print()
    
    def input_required(self, prompt):
        """Get required input from the user"""
        while True:
            value = input(prompt)
            if value.strip():
                return value
            print("This field is required.")
    
    def input_optional(self, prompt):
        """Get optional input from the user"""
        return input(prompt)
    
    def input_number(self, prompt, min_value=None, max_value=None):
        """Get a number from the user"""
        while True:
            try:
                value = input(prompt)
                if not value.strip():
                    return None
                
                num = int(value)
                
                if min_value is not None and num < min_value:
                    print(f"Value must be at least {min_value}.")
                    continue
                
                if max_value is not None and num > max_value:
                    print(f"Value must be at most {max_value}.")
                    continue
                
                return num
            except ValueError:
                print("Please enter a valid number.")
    
    def input_date(self, prompt):
        """Get a date from the user (YYYY-MM-DD)"""
        while True:
            value = input(prompt)
            if not value.strip():
                return None
            
            try:
                date = datetime.strptime(value, "%Y-%m-%d")
                return date.isoformat()
            except ValueError:
                print("Please enter a valid date in format YYYY-MM-DD.")
    
    def input_menu_choice(self, options):
        """Get a menu choice from the user"""
        while True:
            try:
                choice = input("Enter your choice: ")
                choice = int(choice)
                
                if choice in options:
                    return choice
                
                print(f"Please enter a number between {min(options)} and {max(options)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def wait_for_user(self):
        """Wait for the user to press Enter"""
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the CLI application"""
        while self.running:
            self.show_main_menu()
    
    def show_main_menu(self):
        """Show the main menu"""
        self.clear_screen()
        self.print_header("CHESS TOURNAMENT MANAGER")
        
        console.print("[bold]Main Menu[/bold]")
        console.print("1. Player Management")
        console.print("2. Tournament Management")
        console.print("3. Exit")
        print()
        
        choice = self.input_menu_choice({1, 2, 3})
        
        if choice == 1:
            self.show_player_menu()
        elif choice == 2:
            self.show_tournament_menu()
        elif choice == 3:
            self.running = False
            console.print("[bold]Thank you for using Chess Tournament Manager![/bold]")
    
    def show_player_menu(self):
        """Show the player management menu"""
        while True:
            self.clear_screen()
            self.print_header("PLAYER MANAGEMENT")
            
            console.print("[bold]Player Menu[/bold]")
            console.print("1. Register New Player")
            console.print("2. View All Players")
            console.print("3. View Player Details")
            console.print("4. Edit Player")
            console.print("5. Delete Player")
            console.print("6. Search Players")
            console.print("7. Back to Main Menu")
            print()
            
            choice = self.input_menu_choice({1, 2, 3, 4, 5, 6, 7})
            
            if choice == 1:
                self.register_player()
            elif choice == 2:
                self.view_all_players()
            elif choice == 3:
                self.view_player_details()
            elif choice == 4:
                self.edit_player()
            elif choice == 5:
                self.delete_player()
            elif choice == 6:
                self.search_players()
            elif choice == 7:
                break
    
    def register_player(self):
        """Register a new player"""
        self.clear_screen()
        self.print_header("REGISTER NEW PLAYER")
        
        name = self.input_required("Player Name: ")
        rating = self.input_number("Rating (optional): ")
        federation = self.input_optional("Federation (e.g., FIDE, USCF) (optional): ")
        email = self.input_optional("Email (optional): ")
        phone = self.input_optional("Phone (optional): ")
        
        player_id = create_player(name, rating, federation, email, phone)
        
        if player_id:
            self.print_success(f"Player '{name}' registered successfully!")
        else:
            self.print_error("Failed to register player.")
        
        self.wait_for_user()
    
    def view_all_players(self):
        """View all registered players"""
        self.clear_screen()
        self.print_header("ALL PLAYERS")
        
        players = get_all_players()
        
        if not players:
            self.print_info("No players registered yet.")
        else:
            # Prepare data for tabulate
            headers = ["ID", "Name", "Rating", "Federation"]
            data = []
            
            for player in players:
                data.append([
                    player["player_id"][:8] + "...",  # Truncate ID for display
                    player["name"],
                    player["rating"] or "N/A",
                    player["federation"] or "N/A"
                ])
            
            self.print_table(headers, data)
        
        self.wait_for_user()
    
    def view_player_details(self):
        """View details of a specific player"""
        self.clear_screen()
        self.print_header("PLAYER DETAILS")
        
        player_id = self.input_required("Player ID: ")
        player = get_player(player_id)
        
        if not player:
            self.print_error("Player not found.")
        else:
            console.print(f"[bold]Name:[/bold] {player['name']}")
            console.print(f"[bold]ID:[/bold] {player['player_id']}")
            console.print(f"[bold]Rating:[/bold] {player['rating'] or 'N/A'}")
            console.print(f"[bold]Federation:[/bold] {player['federation'] or 'N/A'}")
            console.print(f"[bold]Email:[/bold] {player['email'] or 'N/A'}")
            console.print(f"[bold]Phone:[/bold] {player['phone'] or 'N/A'}")
            
            # Show tournaments
            tournaments = get_player_tournaments(player_id)
            
            if tournaments:
                print("\nTournament History:")
                headers = ["ID", "Name", "Type", "Status"]
                data = []
                
                for tournament in tournaments:
                    status = "Finished" if tournament["is_finished"] else "Active"
                    data.append([
                        tournament["tournament_id"][:8] + "...",
                        tournament["name"],
                        tournament["tournament_type"],
                        status
                    ])
                
                self.print_table(headers, data)
            else:
                print("\nNo tournament history.")
        
        self.wait_for_user()
    
    def edit_player(self):
        """Edit a player's details"""
        self.clear_screen()
        self.print_header("EDIT PLAYER")
        
        player_id = self.input_required("Player ID: ")
        player = get_player(player_id)
        
        if not player:
            self.print_error("Player not found.")
            self.wait_for_user()
            return
        
        console.print(f"Editing player: [bold]{player['name']}[/bold]")
        console.print("Leave fields blank to keep current values.")
        print()
        
        name = self.input_optional(f"Name [{player['name']}]: ")
        rating_str = self.input_optional(f"Rating [{player['rating']}]: ")
        federation = self.input_optional(f"Federation [{player['federation']}]: ")
        email = self.input_optional(f"Email [{player['email']}]: ")
        phone = self.input_optional(f"Phone [{player['phone']}]: ")
        
        # Prepare update data
        update_data = {}
        if name:
            update_data['name'] = name
        if rating_str:
            try:
                update_data['rating'] = int(rating_str)
            except ValueError:
                self.print_error("Invalid rating. This field will not be updated.")
        if federation:
            update_data['federation'] = federation
        if email:
            update_data['email'] = email
        if phone:
            update_data['phone'] = phone
        
        if update_data:
            if update_player(player_id, **update_data):
                self.print_success("Player updated successfully!")
            else:
                self.print_error("Failed to update player.")
        else:
            self.print_info("No changes were made.")
        
        self.wait_for_user()
    
    def delete_player(self):
        """Delete a player"""
        self.clear_screen()
        self.print_header("DELETE PLAYER")
        
        player_id = self.input_required("Player ID: ")
        player = get_player(player_id)
        
        if not player:
            self.print_error("Player not found.")
            self.wait_for_user()
            return
        
        console.print(f"Are you sure you want to delete player: [bold]{player['name']}[/bold]?")
        console.print("[bold red]Warning:[/bold red] This action cannot be undone.")
        confirmation = input("Type 'yes' to confirm: ")
        
        if confirmation.lower() == 'yes':
            if delete_player(player_id):
                self.print_success("Player deleted successfully!")
            else:
                self.print_error("Failed to delete player.")
        else:
            self.print_info("Deletion cancelled.")
        
        self.wait_for_user()
    
    def search_players(self):
        """Search for players"""
        self.clear_screen()
        self.print_header("SEARCH PLAYERS")
        
        console.print("Enter search criteria (leave blank to skip):")
        name_query = self.input_optional("Name contains: ")
        federation = self.input_optional("Federation: ")
        min_rating = self.input_number("Minimum rating: ")
        max_rating = self.input_number("Maximum rating: ")
        
        results = search_players(name_query, federation, min_rating, max_rating)
        
        if not results:
            self.print_info("No players found matching the criteria.")
        else:
            headers = ["ID", "Name", "Rating", "Federation"]
            data = []
            
            for player in results:
                data.append([
                    player["player_id"][:8] + "...",
                    player["name"],
                    player["rating"] or "N/A",
                    player["federation"] or "N/A"
                ])
            
            self.print_table(headers, data)
        
        self.wait_for_user()
    
    def show_tournament_menu(self):
        """Show the tournament management menu"""
        while True:
            self.clear_screen()
            self.print_header("TOURNAMENT MANAGEMENT")
            
            console.print("[bold]Tournament Menu[/bold]")
            console.print("1. Create New Tournament")
            console.print("2. View All Tournaments")
            console.print("3. View Tournament Details")
            console.print("4. Add Player to Tournament")
            console.print("5. Remove Player from Tournament")
            console.print("6. Start Tournament")
            console.print("7. Start Next Round")
            console.print("8. Update Game Result")
            console.print("9. View Tournament Standings")
            console.print("10. Finish Tournament")
            console.print("11. Delete Tournament")
            console.print("12. Back to Main Menu")
            print()
            
            choice = self.input_menu_choice(set(range(1, 13)))
            
            if choice == 1:
                self.create_tournament()
            elif choice == 2:
                self.view_all_tournaments()
            elif choice == 3:
                self.view_tournament_details()
            elif choice == 4:
                self.add_player_to_tournament()
            elif choice == 5:
                self.remove_player_from_tournament()
            elif choice == 6:
                self.start_tournament()
            elif choice == 7:
                self.start_next_round()
            elif choice == 8:
                self.update_game_result()
            elif choice == 9:
                self.view_tournament_standings()
            elif choice == 10:
                self.finish_tournament()
            elif choice == 11:
                self.delete_tournament()
            elif choice == 12:
                break
    
    def create_tournament(self):
        """Create a new tournament"""
        self.clear_screen()
        self.print_header("CREATE NEW TOURNAMENT")
        
        name = self.input_required("Tournament Name: ")
        
        # Tournament type selection
        console.print("\n[bold]Tournament Types:[/bold]")
        console.print("1. Swiss")
        console.print("2. Round Robin")
        console.print("3. Knockout")
        
        type_choice = self.input_menu_choice({1, 2, 3})
        tournament_type = ["Swiss", "Round Robin", "Knockout"][type_choice - 1]
        
        num_rounds = self.input_number("Number of Rounds: ", min_value=1)
        location = self.input_optional("Location (optional): ")
        start_date = self.input_date("Start Date (YYYY-MM-DD, optional): ")
        end_date = self.input_date("End Date (YYYY-MM-DD, optional): ")
        description = self.input_optional("Description (optional): ")
        
        tournament_id = create_tournament(
            name, tournament_type, num_rounds, location, start_date, end_date, description
        )
        
        if tournament_id:
            self.print_success(f"Tournament '{name}' created successfully!")
        else:
            self.print_error("Failed to create tournament.")
        
        self.wait_for_user()
    
    def view_all_tournaments(self):
        """View all tournaments"""
        self.clear_screen()
        self.print_header("ALL TOURNAMENTS")
        
        from models.tournament import Tournament
        tournaments = Tournament.get_all()
        
        if not tournaments:
            self.print_info("No tournaments created yet.")
        else:
            headers = ["ID", "Name", "Type", "Rounds", "Players", "Status"]
            data = []
            
            for tournament in tournaments:
                status = "Finished" if tournament.is_finished else (
                    f"Round {tournament.current_round}" if tournament.current_round > 0 else "Not Started"
                )
                
                data.append([
                    tournament.tournament_id[:8] + "...",
                    tournament.name,
                    tournament.tournament_type.value,
                    f"{tournament.current_round}/{tournament.num_rounds}",
                    len(tournament.players),
                    status
                ])
            
            self.print_table(headers, data)
        
        self.wait_for_user()
    
    def view_tournament_details(self):
        """View details of a specific tournament"""
        self.clear_screen()
        self.print_header("TOURNAMENT DETAILS")
        
        tournament_id = self.input_required("Tournament ID: ")
        report = get_tournament_report(tournament_id)
        
        if not report:
            self.print_error("Tournament not found.")
            self.wait_for_user()
            return
        
        # Tournament info
        tournament = report['tournament']
        console.print(f"[bold]Name:[/bold] {tournament['name']}")
        console.print(f"[bold]ID:[/bold] {tournament['id']}")
        console.print(f"[bold]Type:[/bold] {tournament['type']}")
        console.print(f"[bold]Rounds:[/bold] {tournament['current_round']}/{tournament['rounds']}")
        console.print(f"[bold]Location:[/bold] {tournament['location']}")
        console.print(f"[bold]Start Date:[/bold] {tournament['start_date'][:10]}")
        if tournament['end_date']:
            console.print(f"[bold]End Date:[/bold] {tournament['end_date'][:10]}")
        console.print(f"[bold]Status:[/bold] {'Finished' if tournament['is_finished'] else 'Active'}")
        console.print(f"[bold]Players:[/bold] {report['players']}")
        
        if tournament['description']:
            console.print(f"\n[bold]Description:[/bold]\n{tournament['description']}")
        
        # Show standings
        if report['standings']:
            print("\n[bold]Standings:[/bold]")
            headers = ["Rank", "Name", "Rating", "Score"]
            data = []
            
            for i, player in enumerate(report['standings']):
                data.append([
                    i + 1,
                    player['name'],
                    player['rating'] or "N/A",
                    player['score']
                ])
            
            self.print_table(headers, data)
        
        # Show rounds
        if report['rounds']:
            print("\n[bold]Rounds:[/bold]")
            for round_info in report['rounds']:
                console.print(f"Round {round_info['number']}")
                
                if round_info['pairings']:
                    headers = ["Board", "White", "Black", "Result"]
                    data = []
                    
                    for pairing in round_info['pairings']:
                        data.append([
                            pairing['board'],
                            pairing['white'],
                            pairing['black'],
                            pairing['result']
                        ])
                    
                    self.print_table(headers, data)
                else:
                    print("No pairings yet.")
        
        self.wait_for_user()
    
    def add_player_to_tournament(self):
        """Add a player to a tournament"""
        self.clear_screen()
        self.print_header("ADD PLAYER TO TOURNAMENT")
        
        tournament_id = self.input_required("Tournament ID: ")
        player_id = self.input_required("Player ID: ")
        
        if add_player_to_tournament(tournament_id, player_id):
            self.print_success("Player added to tournament successfully!")
        else:
            self.print_error("Failed to add player to tournament.")
            self.print_info("Note: Players cannot be added after a tournament has started.")
        
        self.wait_for_user()
    
    def remove_player_from_tournament(self):
        """Remove a player from a tournament"""
        self.clear_screen()
        self.print_header("REMOVE PLAYER FROM TOURNAMENT")
        
        tournament_id = self.input_required("Tournament ID: ")
        player_id = self.input_required("Player ID: ")
        
        if remove_player_from_tournament(tournament_id, player_id):
            self.print_success("Player removed from tournament successfully!")
        else:
            self.print_error("Failed to remove player from tournament.")
            self.print_info("Note: Players cannot be removed after a tournament has started.")
        
        self.wait_for_user()
    
    def start_tournament(self):
        """Start a tournament"""
        self.clear_screen()
        self.print_header("START TOURNAMENT")
        
        tournament_id = self.input_required("Tournament ID: ")
        
        if start_tournament(tournament_id):
            self.print_success("Tournament started successfully!")
        else:
            self.print_error("Failed to start tournament.")
        
        self.wait_for_user()
    
    def start_next_round(self):
        """Start the next round of a tournament"""
        self.clear_screen()
        self.print_header("START NEXT ROUND")
        
        tournament_id = self.input_required("Tournament ID: ")
        
        if start_next_round(tournament_id):
            self.print_success("Next round started successfully!")
        else:
            self.print_error("Failed to start next round.")
        
        self.wait_for_user()
    
    def update_game_result(self):
        """Update a game result"""
        self.clear_screen()
        self.print_header("UPDATE GAME RESULT")
        
        tournament_id = self.input_required("Tournament ID: ")
        round_number = self.input_number("Round Number: ", min_value=1)
        board_number = self.input_number("Board Number: ", min_value=1)
        
        console.print("\n[bold]Result Options:[/bold]")
        console.print("1. White Wins (1-0)")
        console.print("2. Black Wins (0-1)")
        console.print("3. Draw (1/2-1/2)")
        console.print("4. White Wins by Forfeit (1-0F)")
        console.print("5. Black Wins by Forfeit (0-1F)")
        console.print("6. Double Forfeit (0-0F)")
        console.print("7. Ongoing (*)")
        
        result_choice = self.input_menu_choice(set(range(1, 8)))
        
        result_map = {
            1: "1-0",
            2: "0-1",
            3: "1/2-1/2",
            4: "1-0F",
            5: "0-1F",
            6: "0-0F",
            7: "*"
        }
        
        result = result_map[result_choice]
        
        if update_result(tournament_id, round_number, board_number, result):
            self.print_success("Game result updated successfully!")
        else:
            self.print_error("Failed to update game result.")
        
        self.wait_for_user()
    
    def view_tournament_standings(self):
        """View tournament standings"""
        self.clear_screen()
        self.print_header("TOURNAMENT STANDINGS")
        
        tournament_id = self.input_required("Tournament ID: ")
        report = get_tournament_report(tournament_id)
        
        if not report:
            self.print_error("Tournament not found.")
            self.wait_for_user()
            return
        
        if not report['standings']:
            self.print_info("No standings available yet.")
        else:
            headers = ["Rank", "Name", "Rating", "Score"]
            data = []
            
            for i, player in enumerate(report['standings']):
                data.append([
                    i + 1,
                    player['name'],
                    player['rating'] or "N/A",
                    player['score']
                ])
            
            self.print_table(headers, data)
        
        self.wait_for_user()
    
    def finish_tournament(self):
        """Finish a tournament"""
        self.clear_screen()
        self.print_header("FINISH TOURNAMENT")
        
        tournament_id = self.input_required("Tournament ID: ")
        
        if finish_tournament(tournament_id):
            self.print_success("Tournament finished successfully!")
        else:
            self.print_error("Failed to finish tournament.")
        
        self.wait_for_user()
    
    def delete_tournament(self):
        """Delete a tournament"""
        self.clear_screen()
        self.print_header("DELETE TOURNAMENT")
        
        tournament_id = self.input_required("Tournament ID: ")
        
        from models.tournament import Tournament
        tournament = Tournament.load(tournament_id)
        
        if not tournament:
            self.print_error("Tournament not found.")
            self.wait_for_user()
            return
        
        console.print(f"Are you sure you want to delete tournament: [bold]{tournament.name}[/bold]?")
        console.print("[bold red]Warning:[/bold red] This action cannot be undone.")
        confirmation = input("Type 'yes' to confirm: ")
        
        if confirmation.lower() == 'yes':
            if delete_tournament(tournament_id):
                self.print_success("Tournament deleted successfully!")
            else:
                self.print_error("Failed to delete tournament.")
        else:
            self.print_info("Deletion cancelled.")
        
        self.wait_for_user()
