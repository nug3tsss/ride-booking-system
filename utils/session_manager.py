import json
import os
import time

SESSION_FILE = "session.json"
SESSION_TIMEOUT_SECONDS = 60 * 60 * 24 * 7  # 7 days

def save_session(user_data, remember_me=False):
    data = {
        "user": user_data,
        "timestamp": time.time() if remember_me else 0
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None

    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)

        # If remember_me was False, timestamp is 0 (session ends after closing)
        if data.get("timestamp", 0) == 0:
            return None

        # Check for timeout
        if time.time() - data["timestamp"] > SESSION_TIMEOUT_SECONDS:
            clear_session()
            return None

        return data["user"]
    except:
        return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def update_session(new_user_data):
    """Update the session without changing the timestamp."""
    if not os.path.exists(SESSION_FILE):
        return

    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)

        # Update the user data while keeping the same timestamp
        data["user"] = new_user_data

        with open(SESSION_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass  # Optional: log error or warning

def get_logged_user():
    return load_session()