from setup.loading_screen import LoadingScreen
from app import App
from utils.console_message import print_launch_message

# Main entry point for the Gethub application
# This script initializes the virtual environment, installs dependencies,
def start_app():
    print_launch_message() # Print the launch message with ASCII art and project details
    app = App()
    app.mainloop()

if __name__ == "__main__":
    loader = LoadingScreen(start_app) # Initialize the loading screen with the callback to start the app
    loader.mainloop() # Start the loading screen which will eventually launch the main app after loading is complete
