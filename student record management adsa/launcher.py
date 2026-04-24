#!/usr/bin/env python3
"""
Student Management System Launcher
Double-click this file to run the application
"""

import os
import sys
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the main application
    app_path = os.path.join(script_dir, "complete_dashboard.py")
    
    try:
        # Change to the application directory
        os.chdir(script_dir)
        
        # Run the application
        subprocess.run([sys.executable, app_path], check=True)
        
    except FileNotFoundError:
        print("Error: Python not found or application file missing!")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Error running application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()