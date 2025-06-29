
from database.db_handler import initialize_database # Initialize the database
initialize_database() 

from app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()