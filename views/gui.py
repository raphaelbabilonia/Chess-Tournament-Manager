"""
Chess Tournament Manager - GUI
A graphical user interface for the Chess Tournament Manager application using Tkinter.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import threading
import queue

# Import controllers
from controllers.player import (
    create_player, get_player, get_all_players, update_player, delete_player,
    search_players, get_player_tournaments
)
from controllers.tournament import (
    create_tournament, update_tournament, start_tournament, finish_tournament,
    add_player_to_tournament, remove_player_from_tournament, start_next_round,
    update_result, get_tournament_report, delete_tournament, get_all_tournaments,
    get_tournament
)
from controllers.pairing import generate_pairings
from models.tournament import TournamentType, Result

# Import utils
from utils.helpers import ensure_data_directories

class ChessTournamentManagerGUI:
    """Graphical User Interface for Chess Tournament Manager"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Chess Tournament Manager")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Ensure data directories exist
        ensure_data_directories()
        
        # Set theme and styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme
        
        # Configure styles
        self.style.configure("TNotebook", background="#f0f0f0")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10), background="#4a7abc", foreground="black")
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#4a7abc", foreground="white", padding=10)
        self.style.configure("Title.TLabel", font=("Arial", 24, "bold"), background="#f0f0f0", foreground="#333333")
        self.style.configure("Subtitle.TLabel", font=("Arial", 12), background="#f0f0f0", foreground="#555555")
        
        # Create status variable (initialized before other components)
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Create tabs
        self.tabs = ttk.Notebook(root)
        
        # Create frames
        self.home_frame = ttk.Frame(self.tabs)
        self.players_frame = ttk.Frame(self.tabs)
        self.tournaments_frame = ttk.Frame(self.tabs)
        
        # Initialize important variables
        self.player_search_var = tk.StringVar()
        self.player_tree = None
        self.player_context_menu = None
        self.tournament_tree = None
        self.tournament_context_menu = None
        
        # Setup tabs
        self.setup_home_tab()
        self.setup_players_tab()
        self.setup_tournaments_tab()
        
        # Add tabs to notebook
        self.tabs.add(self.home_frame, text="Home")
        self.tabs.add(self.players_frame, text="Players")
        self.tabs.add(self.tournaments_frame, text="Tournaments")
        
        self.tabs.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Status bar
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_home_tab(self):
        """Set up the home tab"""
        # Title frame
        title_frame = ttk.Frame(self.home_frame)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        # App title
        title = ttk.Label(title_frame, text="Chess Tournament Manager", style="Title.TLabel")
        title.pack(pady=10)
        
        subtitle = ttk.Label(title_frame, text="A comprehensive solution for managing chess tournaments", style="Subtitle.TLabel")
        subtitle.pack(pady=5)
        
        # Main content frame
        content_frame = ttk.Frame(self.home_frame)
        content_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Quick access buttons
        quick_access_frame = ttk.LabelFrame(content_frame, text="Quick Access")
        quick_access_frame.pack(fill="x", padx=10, pady=10)
        
        btn_frame = ttk.Frame(quick_access_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        # Quick access buttons - row 1
        btn_new_player = ttk.Button(btn_frame, text="New Player", command=self.show_add_player_dialog)
        btn_new_player.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        btn_new_tournament = ttk.Button(btn_frame, text="New Tournament", command=self.show_create_tournament_dialog)
        btn_new_tournament.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        btn_view_players = ttk.Button(btn_frame, text="View All Players", command=lambda: self.tabs.select(1))
        btn_view_players.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        btn_view_tournaments = ttk.Button(btn_frame, text="View All Tournaments", command=lambda: self.tabs.select(2))
        btn_view_tournaments.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Configure grid
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        
        # Help / About frame
        help_frame = ttk.LabelFrame(content_frame, text="About")
        help_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        about_text = "Chess Tournament Manager is a comprehensive application for managing chess tournaments.\n\n" \
                     "Features include:\n" \
                     "• Player registration and management\n" \
                     "• Tournament creation and configuration\n" \
                     "• Swiss-system pairing algorithm\n" \
                     "• Round management\n" \
                     "• Tournament statistics and reporting\n\n" \
                     "Version 1.0.0"
        
        about_label = ttk.Label(help_frame, text=about_text, wraplength=900, justify="left")
        about_label.pack(padx=10, pady=10, fill="both", expand=True)

    def setup_players_tab(self):
        """Set up the Players tab"""
        # Title and action buttons
        header_frame = ttk.Frame(self.players_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title = ttk.Label(header_frame, text="Player Management", style="Header.TLabel")
        title.pack(side=tk.LEFT, padx=10)
        
        # Action buttons frame
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT, padx=10)
        
        add_btn = ttk.Button(action_frame, text="Add Player", command=self.show_add_player_dialog)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(action_frame, text="Refresh", command=self.refresh_players)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(self.players_frame)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=5)
        
        self.player_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.player_search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_players)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Player list
        list_frame = ttk.Frame(self.players_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for players
        columns = ("ID", "First Name", "Last Name", "Rating", "Federation", "Email")
        self.player_tree = ttk.Treeview(list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.player_tree.heading("ID", text="ID")
        self.player_tree.heading("First Name", text="First Name")
        self.player_tree.heading("Last Name", text="Last Name")
        self.player_tree.heading("Rating", text="Rating")
        self.player_tree.heading("Federation", text="Federation")
        self.player_tree.heading("Email", text="Email")
        
        self.player_tree.column("ID", width=50, anchor="center")
        self.player_tree.column("First Name", width=100, anchor="w")
        self.player_tree.column("Last Name", width=100, anchor="w")
        self.player_tree.column("Rating", width=70, anchor="center")
        self.player_tree.column("Federation", width=80, anchor="center")
        self.player_tree.column("Email", width=150, anchor="w")
        
        self.player_tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.player_tree.yview)
        
        # Bind double-click event
        self.player_tree.bind("<Double-1>", self.on_player_double_click)
        
        # Bind right-click event
        self.player_tree.bind("<Button-3>", self.show_player_context_menu)
        
        # Create context menu
        self.player_context_menu = tk.Menu(self.player_tree, tearoff=0)
        self.player_context_menu.add_command(label="View Details", command=self.view_player_details)
        self.player_context_menu.add_command(label="Edit Player", command=self.edit_selected_player)
        self.player_context_menu.add_separator()
        self.player_context_menu.add_command(label="Delete Player", command=self.delete_selected_player)
        
        # Initial load
        self.refresh_players()
    
    def refresh_players(self):
        """Refresh player list"""
        # Clear existing items
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        
        # Get all players
        players = get_all_players()
        
        # Add to treeview
        for player in players:
            player_id = player.get("player_id", "")
            self.player_tree.insert("", "end", values=(
                player_id[:8] + "...",
                player.get("first_name", ""),
                player.get("last_name", ""),
                player.get("rating", "N/A"),
                player.get("federation", "N/A"),
                player.get("email", "N/A")
            ), tags=(player_id,))
        
        self.status_var.set(f"Loaded {len(players)} players")
    
    def search_players(self):
        """Search players"""
        query = self.player_search_var.get().strip()
        
        # Clear existing items
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        
        # Search players
        players = search_players(query)
        
        # Add to treeview
        for player in players:
            player_id = player.get("player_id", "")
            self.player_tree.insert("", "end", values=(
                player_id[:8] + "...",
                player.get("first_name", ""),
                player.get("last_name", ""),
                player.get("rating", "N/A"),
                player.get("federation", "N/A"),
                player.get("email", "N/A")
            ), tags=(player_id,))
        
        self.status_var.set(f"Found {len(players)} players matching '{query}'")
    
    def show_player_context_menu(self, event):
        """Show the player context menu on right-click"""
        # Select row under mouse
        iid = self.player_tree.identify_row(event.y)
        if iid:
            self.player_tree.selection_set(iid)
            self.player_context_menu.post(event.x_root, event.y_root)
    
    def get_selected_player_id(self):
        """Get the ID of the selected player"""
        selected_items = self.player_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a player first")
            return None
        
        # Get the full player ID from tags
        item_tags = self.player_tree.item(selected_items[0], "tags")
        if item_tags:
            return item_tags[0]
        else:
            # Fallback: try to get from the ID column
            values = self.player_tree.item(selected_items[0], "values")
            if values and len(values) > 0:
                # Extract the player ID from the display format
                display_id = values[0]
                # If it's truncated with "...", we can't reliably use it
                if "..." in display_id:
                    messagebox.showerror("Error", "Unable to determine player ID")
                    return None
                return display_id
            
            messagebox.showerror("Error", "Unable to determine player ID")
            return None
    
    def on_player_double_click(self, event):
        """Handle double-click on player"""
        self.view_player_details()
    
    def view_player_details(self):
        """View details of the selected player"""
        player_id = self.get_selected_player_id()
        if not player_id:
            return
        
        player = get_player(player_id)
        if not player:
            messagebox.showerror("Error", "Failed to retrieve player details")
            return
        
        # Create details dialog
        details_dialog = tk.Toplevel(self.root)
        details_dialog.title(f"Player Details: {player.get('first_name', '')} {player.get('last_name', '')}")
        details_dialog.geometry("600x400")
        details_dialog.transient(self.root)
        details_dialog.grab_set()
        
        main_frame = ttk.Frame(details_dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Player details
        details_frame = ttk.LabelFrame(main_frame, text="Player Information")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        details_grid = ttk.Frame(details_frame)
        details_grid.pack(fill="x", padx=10, pady=10)
        
        # First Name
        ttk.Label(details_grid, text="First Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=player.get("first_name", "")).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Last Name
        ttk.Label(details_grid, text="Last Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=player.get("last_name", "")).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Rating
        ttk.Label(details_grid, text="Rating:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=str(player.get("rating", "N/A"))).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Federation
        ttk.Label(details_grid, text="Federation:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=player.get("federation", "N/A")).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Email
        ttk.Label(details_grid, text="Email:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=player.get("email", "N/A")).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Phone
        ttk.Label(details_grid, text="Phone:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=player.get("phone", "N/A")).grid(row=5, column=1, sticky="w", padx=5, pady=5)
        
        # Player ID
        ttk.Label(details_grid, text="Player ID:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=player.get("player_id", "")).grid(row=6, column=1, sticky="w", padx=5, pady=5)
        
        # Tournaments
        tournaments_frame = ttk.LabelFrame(main_frame, text="Tournaments")
        tournaments_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Get tournaments for player
        player_tournaments = get_player_tournaments(player_id)
        
        if not player_tournaments:
            ttk.Label(tournaments_frame, text="Player has not participated in any tournaments").pack(padx=10, pady=10)
        else:
            # Tournament table
            tournaments_tree = ttk.Treeview(tournaments_frame, columns=("Name", "Date", "Status"), show="headings")
            
            tournaments_tree.heading("Name", text="Tournament Name")
            tournaments_tree.heading("Date", text="Date")
            tournaments_tree.heading("Status", text="Status")
            
            tournaments_tree.column("Name", width=200)
            tournaments_tree.column("Date", width=100)
            tournaments_tree.column("Status", width=100)
            
            # Add tournaments to the table
            for tournament in player_tournaments:
                status = "Active" if tournament.get("active", False) else "Finished"
                tournaments_tree.insert("", "end", values=(
                    tournament.get("name", ""),
                    tournament.get("start_date", ""),
                    status
                ))
            
            tournaments_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        edit_btn = ttk.Button(button_frame, text="Edit Player", command=lambda: [details_dialog.destroy(), self.edit_player(player_id)])
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(button_frame, text="Close", command=details_dialog.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def show_add_player_dialog(self):
        """Show dialog to add a new player"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Player")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Form title
        title = ttk.Label(main_frame, text="Register New Player", style="Header.TLabel")
        title.pack(pady=10)
        
        # Form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # First Name
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        first_name_var = tk.StringVar()
        first_name_entry = ttk.Entry(form_frame, textvariable=first_name_var, width=30)
        first_name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Last Name
        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        last_name_var = tk.StringVar()
        last_name_entry = ttk.Entry(form_frame, textvariable=last_name_var, width=30)
        last_name_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Rating
        ttk.Label(form_frame, text="Rating:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        rating_var = tk.StringVar()
        rating_entry = ttk.Entry(form_frame, textvariable=rating_var, width=30)
        rating_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Federation
        ttk.Label(form_frame, text="Federation:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        federation_var = tk.StringVar()
        federation_entry = ttk.Entry(form_frame, textvariable=federation_var, width=30)
        federation_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        email_var = tk.StringVar()
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        phone_var = tk.StringVar()
        phone_entry = ttk.Entry(form_frame, textvariable=phone_var, width=30)
        phone_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Function to handle save
        def save_player():
            first_name = first_name_var.get().strip()
            last_name = last_name_var.get().strip()
            
            if not first_name or not last_name:
                messagebox.showerror("Error", "Player first name and last name are required")
                return
            
            # Get rating
            rating = None
            if rating_var.get().strip():
                try:
                    rating = int(rating_var.get())
                except ValueError:
                    messagebox.showerror("Error", "Rating must be a number")
                    return
            
            # Create player
            player_id = create_player(
                first_name=first_name,
                last_name=last_name,
                rating=rating,
                federation=federation_var.get().strip() or None,
                email=email_var.get().strip() or None,
                phone=phone_var.get().strip() or None
            )
            
            if player_id:
                messagebox.showinfo("Success", f"Player '{first_name} {last_name}' registered successfully!")
                dialog.destroy()
                self.refresh_players()
            else:
                messagebox.showerror("Error", "Failed to register player")
        
        save_btn = ttk.Button(button_frame, text="Save", command=save_player)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Focus on name field
        first_name_entry.focus_set()
    
    def edit_selected_player(self):
        """Edit the selected player"""
        player_id = self.get_selected_player_id()
        if player_id:
            self.edit_player(player_id)
    
    def edit_player(self, player_id):
        """Show dialog to edit a player"""
        player = get_player(player_id)
        if not player:
            messagebox.showerror("Error", "Failed to retrieve player details")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Player: {player.get('first_name', '')} {player.get('last_name', '')}")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Form title
        title = ttk.Label(main_frame, text="Edit Player", style="Header.TLabel")
        title.pack(pady=10)
        
        # Form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # First Name
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        first_name_var = tk.StringVar(value=player.get("first_name", ""))
        first_name_entry = ttk.Entry(form_frame, textvariable=first_name_var, width=30)
        first_name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Last Name
        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        last_name_var = tk.StringVar(value=player.get("last_name", ""))
        last_name_entry = ttk.Entry(form_frame, textvariable=last_name_var, width=30)
        last_name_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Rating
        ttk.Label(form_frame, text="Rating:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        rating_var = tk.StringVar(value=str(player.get("rating", "")))
        rating_entry = ttk.Entry(form_frame, textvariable=rating_var, width=30)
        rating_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Federation
        ttk.Label(form_frame, text="Federation:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        federation_var = tk.StringVar(value=player.get("federation", ""))
        federation_entry = ttk.Entry(form_frame, textvariable=federation_var, width=30)
        federation_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        email_var = tk.StringVar(value=player.get("email", ""))
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        phone_var = tk.StringVar(value=player.get("phone", ""))
        phone_entry = ttk.Entry(form_frame, textvariable=phone_var, width=30)
        phone_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Function to handle update
        def update_player_details():
            first_name = first_name_var.get().strip()
            last_name = last_name_var.get().strip()
            
            if not first_name or not last_name:
                messagebox.showerror("Error", "Player first name and last name are required")
                return
            
            # Get rating
            rating = None
            if rating_var.get().strip():
                try:
                    rating = int(rating_var.get())
                except ValueError:
                    messagebox.showerror("Error", "Rating must be a number")
                    return
            
            # Update player
            success = update_player(
                player_id=player_id,
                first_name=first_name,
                last_name=last_name,
                rating=rating,
                federation=federation_var.get().strip() or None,
                email=email_var.get().strip() or None,
                phone=phone_var.get().strip() or None
            )
            
            if success:
                messagebox.showinfo("Success", f"Player '{first_name} {last_name}' updated successfully!")
                dialog.destroy()
                self.refresh_players()
            else:
                messagebox.showerror("Error", "Failed to update player")
        
        update_btn = ttk.Button(button_frame, text="Update", command=update_player_details)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def delete_selected_player(self):
        """Delete the selected player"""
        player_id = self.get_selected_player_id()
        if not player_id:
            return
        
        player = get_player(player_id)
        if not player:
            messagebox.showerror("Error", "Failed to retrieve player details")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete player '{player.get('first_name', '')} {player.get('last_name', '')}'?\n\n"
                              "This action cannot be undone."):
            # Delete player
            success = delete_player(player_id)
            
            if success:
                messagebox.showinfo("Success", "Player deleted successfully!")
                self.refresh_players()
            else:
                messagebox.showerror("Error", "Failed to delete player")

    def setup_tournaments_tab(self):
        """Set up the Tournaments tab"""
        # Title and action buttons
        header_frame = ttk.Frame(self.tournaments_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title = ttk.Label(header_frame, text="Tournament Management", style="Header.TLabel")
        title.pack(side=tk.LEFT, padx=10)
        
        # Action buttons frame
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT, padx=10)
        
        add_btn = ttk.Button(action_frame, text="Create Tournament", command=self.show_create_tournament_dialog)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(action_frame, text="Refresh", command=self.refresh_tournaments)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Tournament list
        list_frame = ttk.Frame(self.tournaments_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for tournaments
        columns = ("ID", "Name", "Type", "Location", "Status", "Players", "Rounds")
        self.tournament_tree = ttk.Treeview(list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.tournament_tree.heading("ID", text="ID")
        self.tournament_tree.heading("Name", text="Name")
        self.tournament_tree.heading("Type", text="Type")
        self.tournament_tree.heading("Location", text="Location")
        self.tournament_tree.heading("Status", text="Status")
        self.tournament_tree.heading("Players", text="Players")
        self.tournament_tree.heading("Rounds", text="Rounds")
        
        self.tournament_tree.column("ID", width=80, anchor="center")
        self.tournament_tree.column("Name", width=200, anchor="w")
        self.tournament_tree.column("Type", width=100, anchor="center")
        self.tournament_tree.column("Location", width=120, anchor="w")
        self.tournament_tree.column("Status", width=80, anchor="center")
        self.tournament_tree.column("Players", width=60, anchor="center")
        self.tournament_tree.column("Rounds", width=60, anchor="center")
        
        # Configure scrollbar
        scrollbar.config(command=self.tournament_tree.yview)
        
        # Pack the treeview
        self.tournament_tree.pack(fill="both", expand=True)
        
        # Bind double-click event
        self.tournament_tree.bind("<Double-1>", self.on_tournament_double_click)
        
        # Context menu
        self.tournament_context_menu = tk.Menu(self.tournament_tree, tearoff=0)
        self.tournament_context_menu.add_command(label="View Details", command=self.view_tournament_details)
        self.tournament_context_menu.add_command(label="Edit Tournament", command=self.edit_selected_tournament)
        self.tournament_context_menu.add_command(label="Delete Tournament", command=self.delete_selected_tournament)
        self.tournament_context_menu.add_separator()
        self.tournament_context_menu.add_command(label="Manage Players", command=self.manage_tournament_players)
        self.tournament_context_menu.add_command(label="Manage Rounds", command=self.manage_tournament_rounds)
        
        # Bind right-click event
        self.tournament_tree.bind("<Button-3>", self.show_tournament_context_menu)
        
        # Load tournaments
        self.refresh_tournaments()

    def refresh_tournaments(self):
        """Refresh the tournament list"""
        # Clear the treeview
        for item in self.tournament_tree.get_children():
            self.tournament_tree.delete(item)
        
        # Get all tournaments
        tournaments = get_all_tournaments()
        
        # Add tournaments to the treeview
        for tournament in tournaments:
            tournament_id = tournament.get("tournament_id", "")
            display_id = tournament_id[:8] + "..." if len(tournament_id) > 10 else tournament_id
            
            # Get tournament type
            tournament_type = tournament.get("tournament_type", "")
            if tournament_type == TournamentType.SWISS.value:
                type_display = "Swiss"
            elif tournament_type == TournamentType.ROUND_ROBIN.value:
                type_display = "Round Robin"
            elif tournament_type == TournamentType.KNOCKOUT.value:
                type_display = "Knockout"
            else:
                type_display = tournament_type
            
            # Get status
            status = "Active" if tournament.get("active", False) else "Finished"
            if not tournament.get("started", False):
                status = "Not Started"
            
            # Get player count
            player_count = len(tournament.get("players", []))
            
            # Get round count
            round_count = len(tournament.get("rounds", []))
            
            self.tournament_tree.insert("", "end", values=(
                display_id,
                tournament.get("name", ""),
                type_display,
                tournament.get("location", ""),
                status,
                player_count,
                round_count
            ), tags=(tournament_id,))
        
        self.status_var.set(f"Loaded {len(tournaments)} tournaments")
    
    def show_tournament_context_menu(self, event):
        """Show the tournament context menu on right-click"""
        # Select row under mouse
        iid = self.tournament_tree.identify_row(event.y)
        if iid:
            self.tournament_tree.selection_set(iid)
            self.tournament_context_menu.post(event.x_root, event.y_root)
    
    def get_selected_tournament_id(self):
        """Get the ID of the selected tournament"""
        selected_items = self.tournament_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a tournament first")
            return None
        
        # Get the full tournament ID from tags
        item_tags = self.tournament_tree.item(selected_items[0], "tags")
        if item_tags:
            return item_tags[0]
        return None
    
    def on_tournament_double_click(self, event):
        """Handle double-click on tournament"""
        self.view_tournament_details()

    def view_tournament_details(self):
        """View details of the selected tournament"""
        tournament_id = self.get_selected_tournament_id()
        if not tournament_id:
            return
        
        tournament = get_tournament(tournament_id)
        if not tournament:
            messagebox.showerror("Error", "Failed to retrieve tournament details")
            return
        
        # Create details dialog
        details_dialog = tk.Toplevel(self.root)
        details_dialog.title(f"Tournament Details: {tournament.get('name', '')}")
        details_dialog.geometry("800x600")
        details_dialog.transient(self.root)
        details_dialog.grab_set()
        
        main_frame = ttk.Frame(details_dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Tournament details
        details_frame = ttk.LabelFrame(main_frame, text="Tournament Information")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        details_grid = ttk.Frame(details_frame)
        details_grid.pack(fill="x", padx=10, pady=10)
        
        # Name
        ttk.Label(details_grid, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=tournament.get("name", "")).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Location
        ttk.Label(details_grid, text="Location:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=tournament.get("location", "N/A")).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Type
        ttk.Label(details_grid, text="Type:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tournament_type = tournament.get("tournament_type", "")
        if tournament_type == TournamentType.SWISS.value:
            type_display = "Swiss"
        elif tournament_type == TournamentType.ROUND_ROBIN.value:
            type_display = "Round Robin"
        elif tournament_type == TournamentType.KNOCKOUT.value:
            type_display = "Knockout"
        else:
            type_display = tournament_type
        ttk.Label(details_grid, text=type_display).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Rounds
        ttk.Label(details_grid, text="Rounds:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=str(tournament.get("total_rounds", 0))).grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        # Start Date
        ttk.Label(details_grid, text="Start Date:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=tournament.get("start_date", "N/A")).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # End Date
        ttk.Label(details_grid, text="End Date:").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=tournament.get("end_date", "N/A")).grid(row=2, column=3, sticky="w", padx=5, pady=5)
        
        # Status
        ttk.Label(details_grid, text="Status:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        status = "Active" if tournament.get("active", False) else "Finished"
        if not tournament.get("started", False):
            status = "Not Started"
        ttk.Label(details_grid, text=status).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Current Round
        ttk.Label(details_grid, text="Current Round:").grid(row=3, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(details_grid, text=str(tournament.get("current_round", 0))).grid(row=3, column=3, sticky="w", padx=5, pady=5)
        
        # Description
        ttk.Label(details_grid, text="Description:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        description_text = tournament.get("description", "N/A")
        description_label = ttk.Label(details_grid, text=description_text, wraplength=600)
        description_label.grid(row=4, column=1, columnspan=3, sticky="w", padx=5, pady=5)
        
        # Notebook for players and rounds
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Players tab
        players_frame = ttk.Frame(notebook)
        self.setup_tournament_players_tab(players_frame, tournament)
        
        # Rounds tab
        rounds_frame = ttk.Frame(notebook)
        self.setup_tournament_rounds_tab(rounds_frame, tournament)
        
        # Standings tab
        standings_frame = ttk.Frame(notebook)
        self.setup_tournament_standings_tab(standings_frame, tournament)
        
        notebook.add(players_frame, text="Players")
        notebook.add(rounds_frame, text="Rounds")
        notebook.add(standings_frame, text="Standings")
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Action buttons
        if not tournament.get("started", False):
            start_btn = ttk.Button(
                button_frame, 
                text="Start Tournament", 
                command=lambda: [
                    start_tournament(tournament_id),
                    details_dialog.destroy(),
                    self.refresh_tournaments(),
                    messagebox.showinfo("Success", "Tournament started")
                ]
            )
            start_btn.pack(side=tk.LEFT, padx=5)
            
            manage_players_btn = ttk.Button(
                button_frame, 
                text="Manage Players", 
                command=lambda: [
                    details_dialog.destroy(),
                    self.manage_tournament_players()
                ]
            )
            manage_players_btn.pack(side=tk.LEFT, padx=5)
            
        elif tournament.get("active", False):
            next_round_btn = ttk.Button(
                button_frame, 
                text="Start Next Round", 
                command=lambda: [
                    self.start_next_tournament_round(tournament_id),
                    details_dialog.destroy()
                ]
            )
            next_round_btn.pack(side=tk.LEFT, padx=5)
            
            finish_btn = ttk.Button(
                button_frame, 
                text="Finish Tournament", 
                command=lambda: [
                    finish_tournament(tournament_id),
                    details_dialog.destroy(),
                    self.refresh_tournaments(),
                    messagebox.showinfo("Success", "Tournament finished")
                ]
            )
            finish_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(
            button_frame, 
            text="Edit Tournament", 
            command=lambda: [
                details_dialog.destroy(),
                self.edit_tournament(tournament_id)
            ]
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(button_frame, text="Close", command=details_dialog.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def setup_tournament_players_tab(self, parent_frame, tournament):
        """Set up the players tab in tournament details"""
        # Title and info label
        title_frame = ttk.Frame(parent_frame)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        player_count = len(tournament.get("players", []))
        info_label = ttk.Label(title_frame, text=f"Total Players: {player_count}")
        info_label.pack(side=tk.LEFT, padx=5)
        
        # Player list
        list_frame = ttk.Frame(parent_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for players
        columns = ("ID", "First Name", "Last Name", "Rating", "Federation")
        players_tree = ttk.Treeview(list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Configure columns
        players_tree.heading("ID", text="ID")
        players_tree.heading("First Name", text="First Name")
        players_tree.heading("Last Name", text="Last Name")
        players_tree.heading("Rating", text="Rating")
        players_tree.heading("Federation", text="Federation")
        
        players_tree.column("ID", width=50, anchor="center")
        players_tree.column("First Name", width=100, anchor="w")
        players_tree.column("Last Name", width=100, anchor="w")
        players_tree.column("Rating", width=70, anchor="center")
        players_tree.column("Federation", width=80, anchor="center")
        
        players_tree.pack(fill="both", expand=True)
        scrollbar.config(command=players_tree.yview)
        
        # Get tournament players
        tournament_players = tournament.get("players", [])
        
        if not tournament_players:
            ttk.Label(parent_frame, text="No players in this tournament").pack(padx=10, pady=10)
            return
        
        # Add players to treeview
        for player_id in tournament_players:
            player = get_player(player_id)
            
            if player:
                players_tree.insert("", "end", values=(
                    player.get("player_id", "")[:8] + "...",
                    player.get("first_name", ""),
                    player.get("last_name", ""),
                    player.get("rating", "N/A"),
                    player.get("federation", "N/A")
                ), tags=(player_id,))
    
    def setup_tournament_rounds_tab(self, parent_frame, tournament):
        """Set up the rounds tab in tournament details"""
        # Rounds
        rounds = tournament.get("rounds", [])
        
        if not rounds:
            ttk.Label(parent_frame, text="No rounds played yet").pack(padx=10, pady=10)
            return
        
        # Create a notebook for rounds
        rounds_notebook = ttk.Notebook(parent_frame)
        rounds_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add a tab for each round
        for i, round_info in enumerate(rounds, 1):
            round_frame = ttk.Frame(rounds_notebook)
            
            # Round matches
            matches_list_frame = ttk.Frame(round_frame)
            matches_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(matches_list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Treeview for matches
            columns = ("Player1", "Player2", "Result")
            matches_tree = ttk.Treeview(matches_list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
            
            # Configure columns
            matches_tree.heading("Player1", text="Player 1")
            matches_tree.heading("Player2", text="Player 2")
            matches_tree.heading("Result", text="Result")
            
            matches_tree.column("Player1", width=200, anchor="w")
            matches_tree.column("Player2", width=200, anchor="w")
            matches_tree.column("Result", width=100, anchor="center")
            
            # Configure scrollbar
            scrollbar.config(command=matches_tree.yview)
            
            # Pack the treeview
            matches_tree.pack(fill="both", expand=True)
            
            # Add matches to treeview
            for match in round_info.get("matches", []):
                player1_id = match.get("player1", "")
                player2_id = match.get("player2", "")
                result = match.get("result", Result.NOT_PLAYED.value)
                
                player1 = get_player(player1_id)
                player2 = get_player(player2_id)
                
                player1_name = player1.get("name", "") if player1 else "Bye"
                player2_name = player2.get("name", "") if player2 else "Bye"
                
                # Format result
                if result == Result.PLAYER1_WIN.value:
                    result_text = "1 - 0"
                elif result == Result.PLAYER2_WIN.value:
                    result_text = "0 - 1"
                elif result == Result.DRAW.value:
                    result_text = "½ - ½"
                else:
                    result_text = "Not Played"
                
                matches_tree.insert("", "end", values=(
                    player1_name,
                    player2_name,
                    result_text
                ))
            
            rounds_notebook.add(round_frame, text=f"Round {i}")
        
        # Function to display match
        def display_match(match, parent):
            match_frame = ttk.Frame(parent)
            match_frame.pack(fill="x", padx=5, pady=5)
            
            player1_id = match.get("player1", "")
            player2_id = match.get("player2", "")
            result = match.get("result", Result.NOT_PLAYED.value)
            
            player1 = get_player(player1_id) if player1_id else None
            player2 = get_player(player2_id) if player2_id else None
            
            player1_name = f"{player1.get('first_name', '')} {player1.get('last_name', '')}" if player1 else "Bye"
            player2_name = f"{player2.get('first_name', '')} {player2.get('last_name', '')}" if player2 else "Bye"
            
            # Format result
            result_text = "vs"
            if result == Result.PLAYER1_WIN.value:
                result_text = "1-0"
            elif result == Result.PLAYER2_WIN.value:
                result_text = "0-1"
            elif result == Result.DRAW.value:
                result_text = "½-½"
                
            match_label = ttk.Label(
                match_frame, 
                text=f"{player1_name} {result_text} {player2_name}"
            )
            match_label.pack(side=tk.LEFT, padx=5)
            
            # Edit button (only if tournament is not finished)
            if not tournament.get("is_finished", False) and player1_id and player2_id:
                edit_btn = ttk.Button(
                    match_frame, 
                    text="Enter Result", 
                    command=lambda m=match: self.edit_match_result(tournament, m)
                )
                edit_btn.pack(side=tk.RIGHT, padx=5)
    
    def setup_tournament_standings_tab(self, parent_frame, tournament):
        """Set up the standings tab in tournament details"""
        # Get tournament report
        report = get_tournament_report(tournament.get("tournament_id", ""))
        
        if not report or not report.get("standings"):
            ttk.Label(parent_frame, text="No standings available").pack(padx=10, pady=10)
            return
        
        # Standings list
        standings_list_frame = ttk.Frame(parent_frame)
        standings_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(standings_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for standings
        columns = ("Rank", "Name", "Points", "Rating", "Federation")
        standings_tree = ttk.Treeview(standings_list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Configure columns
        standings_tree.heading("Rank", text="Rank")
        standings_tree.heading("Name", text="Name")
        standings_tree.heading("Points", text="Points")
        standings_tree.heading("Rating", text="Rating")
        standings_tree.heading("Federation", text="Federation")
        
        standings_tree.column("Rank", width=50, anchor="center")
        standings_tree.column("Name", width=200, anchor="w")
        standings_tree.column("Points", width=80, anchor="center")
        standings_tree.column("Rating", width=80, anchor="center")
        standings_tree.column("Federation", width=100, anchor="center")
        
        # Configure scrollbar
        scrollbar.config(command=standings_tree.yview)
        
        # Pack the treeview
        standings_tree.pack(fill="both", expand=True)
        
        # Add standings to treeview
        for i, standing in enumerate(report.get("standings", []), 1):
            player_id = standing.get("player_id", "")
            player = get_player(player_id)
            
            if player:
                standings_tree.insert("", "end", values=(
                    i,
                    f"{player.get('first_name', '')} {player.get('last_name', '')}",
                    standing.get("points", 0),
                    player.get("rating", "N/A"),
                    player.get("federation", "N/A")
                ))

    def show_create_tournament_dialog(self):
        """Show dialog to create a new tournament"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Tournament")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Form title
        title = ttk.Label(main_frame, text="Create New Tournament", style="Header.TLabel")
        title.pack(pady=10)
        
        # Form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=40)
        name_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        # Location
        ttk.Label(form_frame, text="Location:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        location_var = tk.StringVar()
        location_entry = ttk.Entry(form_frame, textvariable=location_var, width=40)
        location_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        # Start Date
        ttk.Label(form_frame, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        start_date_var = tk.StringVar()
        start_date_entry = ttk.Entry(form_frame, textvariable=start_date_var, width=40)
        start_date_entry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        # End Date
        ttk.Label(form_frame, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        end_date_var = tk.StringVar()
        end_date_entry = ttk.Entry(form_frame, textvariable=end_date_var, width=40)
        end_date_entry.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        # Tournament Type
        ttk.Label(form_frame, text="Tournament Type:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tournament_type_var = tk.StringVar(value=TournamentType.SWISS.value)
        tournament_type_frame = ttk.Frame(form_frame)
        tournament_type_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Radiobutton(tournament_type_frame, text="Swiss", variable=tournament_type_var, value=TournamentType.SWISS.value).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(tournament_type_frame, text="Round Robin", variable=tournament_type_var, value=TournamentType.ROUND_ROBIN.value).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(tournament_type_frame, text="Knockout", variable=tournament_type_var, value=TournamentType.KNOCKOUT.value).pack(side=tk.LEFT, padx=5)
        
        # Number of Rounds
        ttk.Label(form_frame, text="Number of Rounds:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        rounds_var = tk.StringVar(value="5")
        rounds_entry = ttk.Entry(form_frame, textvariable=rounds_var, width=40)
        rounds_entry.grid(row=5, column=1, sticky="we", padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        description_text = tk.Text(form_frame, width=40, height=5)
        description_text.grid(row=6, column=1, sticky="we", padx=5, pady=5)
        
        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Function to handle save
        def save_tournament():
            name = name_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Tournament name is required")
                return
            
            # Get dates
            start_date = start_date_var.get().strip()
            end_date = end_date_var.get().strip()
            
            if start_date:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Start date must be in format YYYY-MM-DD")
                    return
            
            if end_date:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "End date must be in format YYYY-MM-DD")
                    return
            
            # Get rounds
            rounds = 0
            if rounds_var.get().strip():
                try:
                    rounds = int(rounds_var.get())
                    if rounds <= 0:
                        messagebox.showerror("Error", "Number of rounds must be positive")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Number of rounds must be a number")
                    return
            
            # Get description
            description = description_text.get("1.0", tk.END).strip()
            
            # Create tournament
            tournament_id = create_tournament(
                name=name,
                location=location_var.get().strip() or None,
                start_date=start_date or None,
                end_date=end_date or None,
                tournament_type=tournament_type_var.get(),
                num_rounds=rounds,
                description=description or None
            )
            
            if tournament_id:
                messagebox.showinfo("Success", f"Tournament '{name}' created successfully!")
                dialog.destroy()
                self.refresh_tournaments()
            else:
                messagebox.showerror("Error", "Failed to create tournament")
        
        save_btn = ttk.Button(button_frame, text="Create Tournament", command=save_tournament)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Focus on name field
        name_entry.focus_set()

    def edit_selected_tournament(self):
        """Edit the selected tournament"""
        tournament_id = self.get_selected_tournament_id()
        if tournament_id:
            self.edit_tournament(tournament_id)
    
    def edit_tournament(self, tournament_id):
        """Show dialog to edit a tournament"""
        tournament = get_tournament(tournament_id)
        if not tournament:
            messagebox.showerror("Error", "Failed to retrieve tournament details")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Tournament: {tournament.get('name', '')}")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Form title
        title = ttk.Label(main_frame, text="Edit Tournament", style="Header.TLabel")
        title.pack(pady=10)
        
        # Form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        name_var = tk.StringVar(value=tournament.get("name", ""))
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=40)
        name_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        # Location
        ttk.Label(form_frame, text="Location:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        location_var = tk.StringVar(value=tournament.get("location", ""))
        location_entry = ttk.Entry(form_frame, textvariable=location_var, width=40)
        location_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        # Start Date
        ttk.Label(form_frame, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        start_date_var = tk.StringVar(value=tournament.get("start_date", ""))
        start_date_entry = ttk.Entry(form_frame, textvariable=start_date_var, width=40)
        start_date_entry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        # End Date
        ttk.Label(form_frame, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        end_date_var = tk.StringVar(value=tournament.get("end_date", ""))
        end_date_entry = ttk.Entry(form_frame, textvariable=end_date_var, width=40)
        end_date_entry.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        # Tournament Type
        ttk.Label(form_frame, text="Tournament Type:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tournament_type_var = tk.StringVar(value=tournament.get("tournament_type", TournamentType.SWISS.value))
        tournament_type_frame = ttk.Frame(form_frame)
        tournament_type_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Disable tournament type if the tournament has started
        tournament_type_state = "disabled" if tournament.get("started", False) else "normal"
        
        ttk.Radiobutton(tournament_type_frame, text="Swiss", variable=tournament_type_var, value=TournamentType.SWISS.value, state=tournament_type_state).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(tournament_type_frame, text="Round Robin", variable=tournament_type_var, value=TournamentType.ROUND_ROBIN.value, state=tournament_type_state).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(tournament_type_frame, text="Knockout", variable=tournament_type_var, value=TournamentType.KNOCKOUT.value, state=tournament_type_state).pack(side=tk.LEFT, padx=5)
        
        # Number of Rounds
        ttk.Label(form_frame, text="Number of Rounds:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        rounds_var = tk.StringVar(value=str(tournament.get("total_rounds", 0)))
        rounds_entry = ttk.Entry(form_frame, textvariable=rounds_var, width=40, state=tournament_type_state)
        rounds_entry.grid(row=5, column=1, sticky="we", padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        description_text = tk.Text(form_frame, width=40, height=5)
        description_text.grid(row=6, column=1, sticky="we", padx=5, pady=5)
        description_text.insert(tk.END, tournament.get("description", ""))
        
        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Function to handle update
        def update_tournament_details():
            name = name_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Tournament name is required")
                return
            
            # Get dates
            start_date = start_date_var.get().strip()
            end_date = end_date_var.get().strip()
            
            if start_date:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Start date must be in format YYYY-MM-DD")
                    return
            
            if end_date:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "End date must be in format YYYY-MM-DD")
                    return
            
            # Get rounds
            rounds = tournament.get("total_rounds", 0)
            if not tournament.get("started", False) and rounds_var.get().strip():
                try:
                    rounds = int(rounds_var.get())
                    if rounds <= 0:
                        messagebox.showerror("Error", "Number of rounds must be positive")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Number of rounds must be a number")
                    return
            
            # Get description
            description = description_text.get("1.0", tk.END).strip()
            
            # Update tournament
            success = update_tournament(
                tournament_id=tournament_id,
                name=name,
                location=location_var.get().strip() or None,
                start_date=start_date or None,
                end_date=end_date or None,
                tournament_type=tournament_type_var.get() if not tournament.get("started", False) else None,
                num_rounds=rounds if not tournament.get("started", False) else None,
                description=description or None
            )
            
            if success:
                messagebox.showinfo("Success", f"Tournament '{name}' updated successfully!")
                dialog.destroy()
                self.refresh_tournaments()
            else:
                messagebox.showerror("Error", "Failed to update tournament")
        
        update_btn = ttk.Button(button_frame, text="Update Tournament", command=update_tournament_details)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def delete_selected_tournament(self):
        """Delete the selected tournament"""
        tournament_id = self.get_selected_tournament_id()
        if not tournament_id:
            return
        
        tournament = get_tournament(tournament_id)
        if not tournament:
            messagebox.showerror("Error", "Failed to retrieve tournament details")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion", 
            f"Are you sure you want to delete tournament '{tournament.get('name', '')}'?\n\n"
            "This action cannot be undone."
        )
        
        if confirm:
            success = delete_tournament(tournament_id)
            
            if success:
                messagebox.showinfo("Success", "Tournament deleted successfully")
                self.refresh_tournaments()
            else:
                messagebox.showerror("Error", "Failed to delete tournament")
    
    def manage_tournament_players(self):
        """Manage players for the selected tournament"""
        tournament_id = self.get_selected_tournament_id()
        if not tournament_id:
            return
        
        tournament = get_tournament(tournament_id)
        if not tournament:
            messagebox.showerror("Error", "Failed to retrieve tournament details")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Manage Players: {tournament.get('name', '')}")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Dialog title
        title = ttk.Label(main_frame, text=f"Manage Players for {tournament.get('name', '')}", style="Header.TLabel")
        title.pack(pady=10)
        
        # Only allow adding/removing players if tournament hasn't started
        if tournament.get("started", False):
            ttk.Label(main_frame, text="Cannot modify players for a tournament that has already started.", foreground="red").pack(pady=10)
        
        # Split view with available players on left and tournament players on right
        split_frame = ttk.Frame(main_frame)
        split_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Available players frame
        available_frame = ttk.LabelFrame(split_frame, text="Available Players")
        available_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # Search frame for available players
        search_frame = ttk.Frame(available_frame)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)
        
        search_btn = ttk.Button(search_frame, text="Search", command=lambda: refresh_available_players(search_var.get()))
        search_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Available players list
        available_list_frame = ttk.Frame(available_frame)
        available_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        available_scrollbar = ttk.Scrollbar(available_list_frame)
        available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for available players
        available_tree = ttk.Treeview(available_list_frame, columns=("First Name", "Last Name", "Rating", "Federation"), show="headings", yscrollcommand=available_scrollbar.set)
        
        available_tree.heading("First Name", text="First Name")
        available_tree.heading("Last Name", text="Last Name")
        available_tree.heading("Rating", text="Rating")
        available_tree.heading("Federation", text="Federation")
        
        available_tree.column("First Name", width=100, anchor="w")
        available_tree.column("Last Name", width=100, anchor="w")
        available_tree.column("Rating", width=70, anchor="center")
        available_tree.column("Federation", width=80, anchor="center")
        
        # Configure scrollbar
        available_scrollbar.config(command=available_tree.yview)
        
        # Pack the treeview
        available_tree.pack(fill="both", expand=True)
        
        # Tournament players frame
        tournament_players_frame = ttk.LabelFrame(split_frame, text="Tournament Players")
        tournament_players_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)
        
        # Tournament players list
        tournament_players_list_frame = ttk.Frame(tournament_players_frame)
        tournament_players_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        tournament_players_scrollbar = ttk.Scrollbar(tournament_players_list_frame)
        tournament_players_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for tournament players
        tournament_players_tree = ttk.Treeview(tournament_players_list_frame, columns=("First Name", "Last Name", "Rating", "Federation"), show="headings", yscrollcommand=tournament_players_scrollbar.set)
        
        tournament_players_tree.heading("First Name", text="First Name")
        tournament_players_tree.heading("Last Name", text="Last Name")
        tournament_players_tree.heading("Rating", text="Rating")
        tournament_players_tree.heading("Federation", text="Federation")
        
        tournament_players_tree.column("First Name", width=100, anchor="w")
        tournament_players_tree.column("Last Name", width=100, anchor="w")
        tournament_players_tree.column("Rating", width=70, anchor="center")
        tournament_players_tree.column("Federation", width=80, anchor="center")
        
        # Configure scrollbar
        tournament_players_scrollbar.config(command=tournament_players_tree.yview)
        
        # Pack the treeview
        tournament_players_tree.pack(fill="both", expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(split_frame)
        buttons_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=10)
        
        add_btn = ttk.Button(
            buttons_frame, 
            text="Add >>", 
            command=lambda: add_player_to_tournament_action(),
            state="normal" if not tournament.get("started", False) else "disabled"
        )
        add_btn.pack(pady=10)
        
        remove_btn = ttk.Button(
            buttons_frame, 
            text="<< Remove", 
            command=lambda: remove_player_from_tournament_action(),
            state="normal" if not tournament.get("started", False) else "disabled"
        )
        remove_btn.pack(pady=10)
        
        # Bottom buttons
        bottom_buttons_frame = ttk.Frame(main_frame)
        bottom_buttons_frame.pack(fill="x", padx=10, pady=10)
        
        close_btn = ttk.Button(bottom_buttons_frame, text="Close", command=dialog.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Function to refresh available players
        def refresh_available_players(search_term=""):
            # Clear the treeview
            for item in available_tree.get_children():
                available_tree.delete(item)
            
            # Get all players
            if search_term:
                players = search_players(search_term)
            else:
                players = get_all_players()
            
            # Get tournament players
            tournament_players = tournament.get("players", [])
            
            # Add players to the treeview if they are not in the tournament
            for player in players:
                player_id = player.get("player_id", "")
                
                if player_id not in tournament_players:
                    available_tree.insert("", "end", values=(
                        player.get("first_name", ""),
                        player.get("last_name", ""),
                        player.get("rating", "N/A"),
                        player.get("federation", "N/A")
                    ), tags=(player_id,))
        
        # Function to refresh tournament players
        def refresh_tournament_players():
            # Clear the treeview
            for item in tournament_players_tree.get_children():
                tournament_players_tree.delete(item)
            
            # Get tournament players
            tournament_player_ids = tournament.get("players", [])
            
            # Add players to the treeview
            for player_id in tournament_player_ids:
                player = get_player(player_id)
                
                if player:
                    tournament_players_tree.insert("", "end", values=(
                        player.get("first_name", ""),
                        player.get("last_name", ""),
                        player.get("rating", "N/A"),
                        player.get("federation", "N/A")
                    ), tags=(player_id,))
        
        # Function to add player to tournament
        def add_player_to_tournament_action():
            selected_items = available_tree.selection()
            if not selected_items:
                messagebox.showinfo("Info", "Please select a player to add")
                return
            
            # Get the player ID
            item_tags = available_tree.item(selected_items[0], "tags")
            if not item_tags:
                return
            
            player_id = item_tags[0]
            player = get_player(player_id)
            
            if not player:
                messagebox.showerror("Error", "Failed to retrieve player details")
                return
            
            # Add player to tournament
            success = add_player_to_tournament(tournament_id, player_id)
            
            if success:
                # Update the tournament object
                tournament["players"] = tournament.get("players", []) + [player_id]
                
                # Refresh both trees
                refresh_available_players(search_var.get())
                refresh_tournament_players()
            else:
                messagebox.showerror("Error", "Failed to add player to tournament")
        
        # Function to remove player from tournament
        def remove_player_from_tournament_action():
            selected_items = tournament_players_tree.selection()
            if not selected_items:
                messagebox.showinfo("Info", "Please select a player to remove")
                return
            
            # Get the player ID
            item_tags = tournament_players_tree.item(selected_items[0], "tags")
            if not item_tags:
                return
            
            player_id = item_tags[0]
            player = get_player(player_id)
            
            if not player:
                messagebox.showerror("Error", "Failed to retrieve player details")
                return
            
            # Remove player from tournament
            success = remove_player_from_tournament(tournament_id, player_id)
            
            if success:
                # Update the tournament object
                tournament["players"] = [p for p in tournament.get("players", []) if p != player_id]
                
                # Refresh both trees
                refresh_available_players(search_var.get())
                refresh_tournament_players()
            else:
                messagebox.showerror("Error", "Failed to remove player from tournament")
        
        # Initial load
        refresh_available_players()
        refresh_tournament_players()
    
    def manage_tournament_rounds(self):
        """Manage rounds for the selected tournament"""
        tournament_id = self.get_selected_tournament_id()
        if not tournament_id:
            return
        
        tournament = get_tournament(tournament_id)
        if not tournament:
            messagebox.showerror("Error", "Failed to retrieve tournament details")
            return
        
        # Check if tournament has started
        if not tournament.get("started", False):
            messagebox.showinfo("Info", "Tournament has not started yet")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Manage Rounds: {tournament.get('name', '')}")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Dialog title
        title = ttk.Label(main_frame, text=f"Manage Rounds for {tournament.get('name', '')}", style="Header.TLabel")
        title.pack(pady=10)
        
        # Status information
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        # Status
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        status = "Active" if tournament.get("active", False) else "Finished"
        ttk.Label(status_frame, text=status).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Current Round
        ttk.Label(status_frame, text="Current Round:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(status_frame, text=str(tournament.get("current_round", 0))).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Total Rounds
        ttk.Label(status_frame, text="Total Rounds:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        ttk.Label(status_frame, text=str(tournament.get("total_rounds", 0))).grid(row=0, column=5, sticky="w", padx=5, pady=5)
        
        # Rounds frame
        rounds_frame = ttk.Frame(main_frame)
        rounds_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Rounds notebook
        rounds_notebook = ttk.Notebook(rounds_frame)
        rounds_notebook.pack(fill="both", expand=True)
        
        # Get rounds
        rounds = tournament.get("rounds", [])
        
        if not rounds:
            ttk.Label(rounds_frame, text="No rounds played yet").pack(pady=20)
        else:
            # Add a tab for each round
            for i, round_info in enumerate(rounds, 1):
                round_frame = ttk.Frame(rounds_notebook)
                
                # Round matches
                matches_list_frame = ttk.Frame(round_frame)
                matches_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
                
                # Scrollbar
                scrollbar = ttk.Scrollbar(matches_list_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Treeview for matches
                columns = ("Player1", "Player2", "Result")
                matches_tree = ttk.Treeview(matches_list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
                
                # Configure columns
                matches_tree.heading("Player1", text="Player 1")
                matches_tree.heading("Player2", text="Player 2")
                matches_tree.heading("Result", text="Result")
                
                matches_tree.column("Player1", width=200, anchor="w")
                matches_tree.column("Player2", width=200, anchor="w")
                matches_tree.column("Result", width=100, anchor="center")
                
                # Configure scrollbar
                scrollbar.config(command=matches_tree.yview)
                
                # Pack the treeview
                matches_tree.pack(fill="both", expand=True)
                
                # Add matches to treeview
                for j, match in enumerate(round_info.get("matches", [])):
                    player1_id = match.get("player1", "")
                    player2_id = match.get("player2", "")
                    result = match.get("result", Result.NOT_PLAYED.value)
                    
                    player1 = get_player(player1_id)
                    player2 = get_player(player2_id)
                    
                    player1_name = player1.get("name", "") if player1 else "Bye"
                    player2_name = player2.get("name", "") if player2 else "Bye"
                    
                    # Format result
                    if result == Result.PLAYER1_WIN.value:
                        result_text = "1 - 0"
                    elif result == Result.PLAYER2_WIN.value:
                        result_text = "0 - 1"
                    elif result == Result.DRAW.value:
                        result_text = "½ - ½"
                    else:
                        result_text = "Not Played"
                    
                    matches_tree.insert("", "end", values=(
                        player1_name,
                        player2_name,
                        result_text
                    ), tags=(f"{i}:{j}",))  # Tag with round:match index
                
                # Double-click handler for updating match results
                def on_match_double_click(event, tree=matches_tree, round_idx=i-1):
                    item = tree.identify_row(event.y)
                    if not item:
                        return
                    
                    # Get the match index from tags
                    tags = tree.item(item, "tags")
                    if not tags:
                        return
                    
                    try:
                        round_idx, match_idx = map(int, tags[0].split(":"))
                        round_idx -= 1  # Convert to 0-indexed
                        
                        if round_idx < len(rounds):
                            round_data = rounds[round_idx]
                            if match_idx < len(round_data.get("matches", [])):
                                match = round_data["matches"][match_idx]
                                self.update_match_result(tournament_id, round_idx, match_idx, match)
                    except (ValueError, IndexError):
                        pass
                
                matches_tree.bind("<Double-1>", lambda e, t=matches_tree, r=i-1: on_match_double_click(e, t, r))
                
                rounds_notebook.add(round_frame, text=f"Round {i}")
        
        # Bottom buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Only show "Start Next Round" button if tournament is active and not all rounds are completed
        if tournament.get("active", False) and tournament.get("current_round", 0) < tournament.get("total_rounds", 0):
            next_round_btn = ttk.Button(
                buttons_frame, 
                text="Start Next Round", 
                command=lambda: [
                    self.start_next_tournament_round(tournament_id),
                    dialog.destroy()
                ]
            )
            next_round_btn.pack(side=tk.LEFT, padx=5)
        
        # Only show "Finish Tournament" button if tournament is active
        if tournament.get("active", False):
            finish_btn = ttk.Button(
                buttons_frame, 
                text="Finish Tournament", 
                command=lambda: [
                    finish_tournament(tournament_id),
                    dialog.destroy(),
                    self.refresh_tournaments(),
                    messagebox.showinfo("Success", "Tournament finished")
                ]
            )
            finish_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            buttons_frame, 
            text="Refresh", 
            command=lambda: [
                dialog.destroy(),
                self.manage_tournament_rounds()
            ]
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(buttons_frame, text="Close", command=dialog.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_match_result(self, tournament_id, round_idx, match_idx, match):
        """Update the result of a match"""
        player1_id = match.get("player1", "")
        player2_id = match.get("player2", "")
        
        player1 = get_player(player1_id)
        player2 = get_player(player2_id)
        
        if not player1 or not player2:
            # One player is a bye
            return
        
        player1_name = player1.get("name", "")
        player2_name = player2.get("name", "")
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Match Result")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Dialog title
        title = ttk.Label(main_frame, text="Update Match Result", style="Header.TLabel")
        title.pack(pady=10)
        
        # Match info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=10)
        
        ttk.Label(info_frame, text=f"{player1_name} vs {player2_name}", font=("Arial", 12, "bold")).pack()
        
        # Result options
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill="x", pady=10)
        
        result_var = tk.StringVar(value=match.get("result", Result.NOT_PLAYED.value))
        
        ttk.Radiobutton(result_frame, text=f"{player1_name} wins (1-0)", variable=result_var, value=Result.PLAYER1_WIN.value).pack(anchor="w", pady=2)
        ttk.Radiobutton(result_frame, text=f"{player2_name} wins (0-1)", variable=result_var, value=Result.PLAYER2_WIN.value).pack(anchor="w", pady=2)
        ttk.Radiobutton(result_frame, text="Draw (½-½)", variable=result_var, value=Result.DRAW.value).pack(anchor="w", pady=2)
        ttk.Radiobutton(result_frame, text="Not Played", variable=result_var, value=Result.NOT_PLAYED.value).pack(anchor="w", pady=2)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        def save_result():
            result = result_var.get()
            success = update_result(tournament_id, round_idx, match_idx, result)
            
            if success:
                messagebox.showinfo("Success", "Match result updated successfully")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to update match result")
        
        save_btn = ttk.Button(button_frame, text="Save Result", command=save_result)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def start_next_tournament_round(self, tournament_id):
        """Start the next round of a tournament"""
        tournament = get_tournament(tournament_id)
        if not tournament:
            messagebox.showerror("Error", "Failed to retrieve tournament details")
            return
        
        # Check if tournament is active
        if not tournament.get("active", False):
            messagebox.showinfo("Info", "Tournament is not active")
            return
        
        # Check if all rounds are completed
        if tournament.get("current_round", 0) >= tournament.get("total_rounds", 0):
            messagebox.showinfo("Info", "All rounds have been completed")
            return
        
        # Start next round
        success = start_next_round(tournament_id)
        
        if success:
            messagebox.showinfo("Success", "Next round started successfully")
            self.refresh_tournaments()
        else:
            messagebox.showerror("Error", "Failed to start next round")

    def edit_match_result(self, tournament, match):
        """Edit match result"""
        player1_id = match.get("player1", "")
        player2_id = match.get("player2", "")
        
        player1 = get_player(player1_id)
        player2 = get_player(player2_id)
        
        if not player1 or not player2:
            messagebox.showerror("Error", "Unable to retrieve player information")
            return
        
        player1_name = f"{player1.get('first_name', '')} {player1.get('last_name', '')}"
        player2_name = f"{player2.get('first_name', '')} {player2.get('last_name', '')}"
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Match Result")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Info frame
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Tournament and round info
        tournament_name = tournament.get("name", "Unknown Tournament")
        round_number = match.get("round_number", 0)
        
        ttk.Label(info_frame, text=f"{tournament_name} - Round {round_number}", font=("Arial", 10)).pack()
        ttk.Label(info_frame, text=f"{player1_name} vs {player2_name}", font=("Arial", 12, "bold")).pack()
        
        # Result frame
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill="x", padx=10, pady=10)
        
        result_var = tk.StringVar(value=match.get("result", Result.NOT_PLAYED.value))
        
        ttk.Radiobutton(result_frame, text=f"{player1_name} wins (1-0)", variable=result_var, value=Result.PLAYER1_WIN.value).pack(anchor="w", pady=2)
        ttk.Radiobutton(result_frame, text=f"{player2_name} wins (0-1)", variable=result_var, value=Result.PLAYER2_WIN.value).pack(anchor="w", pady=2)
        ttk.Radiobutton(result_frame, text="Draw (½-½)", variable=result_var, value=Result.DRAW.value).pack(anchor="w", pady=2)
        ttk.Radiobutton(result_frame, text="Not played", variable=result_var, value=Result.NOT_PLAYED.value).pack(anchor="w", pady=2)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        def save_result():
            result = result_var.get()
            success = update_result(tournament.get("tournament_id", ""), round_number, match.get("match_number", 0), result)
            
            if success:
                messagebox.showinfo("Success", "Match result updated successfully")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to update match result")
        
        save_btn = ttk.Button(button_frame, text="Save Result", command=save_result)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

def run_gui():
    """Run the GUI application"""
    root = tk.Tk()
    app = ChessTournamentManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
