import json
import os

SETTINGS_FILE = "session.json"

DEFAULT_SETTINGS = {
    "theme_mode": "System",
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()

def save_settings(new_settings):
    with open("session.json", "r+") as file:
        settings = json.load(file)
        settings.update(new_settings)
        file.seek(0)
        json.dump(settings, file, indent=4)
        file.truncate()


def reset_settings():
    save_settings(DEFAULT_SETTINGS)
