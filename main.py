#!/usr/bin/env python3
"""
Chess Tournament Manager - Main Application
"""
import os
import sys
from views.gui import run_gui
from utils.helpers import ensure_data_directories

def main():
    """Main entry point for the application"""
    print("=" * 50)
    print("Starting Chess Tournament Manager GUI")
    print("=" * 50)
    print()
    
    # Create necessary directories
    ensure_data_directories()
    
    # Start the GUI
    run_gui()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Chess Tournament Manager. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1) 