from database.db_handler import get_connection

class Message:
    """Model for handling messages from contact page."""
    
    @staticmethod
    def save(name, email, message):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages (name, email, message)
            VALUES (?, ?, ?)
            """,
            (name, email, message)
        )

        conn.commit()
        conn.close()
