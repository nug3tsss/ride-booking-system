# It connects to the SQLite database and Initialize the database if it does not exist.
import sqlite3
import os
import sys

# This module provides a function to establish a connection to the rides.db SQLite database.
def get_connection():
    """
    Establish and return a connection to the rides.db SQLite database.
    
    The connection uses sqlite3.Row for dictionary-like access to rows.
    Returns:
        sqlite3.Connection: Database connection object, or None if connection fails.
    """
    try:
        
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Determine the absolute path to the project's root directory
        
        db_dir = os.path.join(base_dir, 'database') # Ensure 'database' directory exists (safeguard)
        os.makedirs(db_dir, exist_ok=True)

        db_path = os.path.join(db_dir, 'rides.db') # Build the full path to the database file
        
        # Establish the connection with proper parsing of declared types
        conn = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row

        return conn

    except sqlite3.Error as e:
        print(f"[Database ERROR] Failed to connect to the database: {e}", file=sys.stderr)
        return None
