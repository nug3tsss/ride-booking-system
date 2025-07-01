# It connects to the SQLite database and Initialize the database if it does not exist.

import sqlite3
import os

def get_connection():
    """
    Return a sqlite3 Connection to the rides.db file,
    with row_factory set to sqlite3.Row for dictionary data type access.
    """
    try: # Handle any errors that may occur during the connection process
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Determine path to project root
    
        db_path = os.path.join(base_dir, 'database', 'rides.db')  # Build path to the database file

        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) # Connect (creates the file if it doesn't exist)

        conn.row_factory = sqlite3.Row   # Return rows as sqlite3.Row for attribute or key access
       
        return conn

    except sqlite3.Error as e:
        print(f"[Database ERROR] It failed to connect to the database: {e}")
        return None 