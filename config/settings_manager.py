import json
import os

"""Settings manager for the ride booking system.
This module handles loading, saving, and resetting user settings."""

SETTINGS_FILE = "session.json"

DEFAULT_SETTINGS = {
    "theme_mode": "System",
}

# Ensure the settings file exists with default values if not present
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

# Save new settings to the settings file.
def save_settings(new_settings):
    # Ensure the file exists with default values if not present
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(DEFAULT_SETTINGS.copy(), file, indent=4)

    # Read existing settings (safe fallback)
    try:
        with open(SETTINGS_FILE, "r+") as file:
            try:
                settings = json.load(file)
            except json.JSONDecodeError:
                settings = DEFAULT_SETTINGS.copy()

            settings.update(new_settings)
            file.seek(0)
            json.dump(settings, file, indent=4)
            file.truncate()
    except Exception as e:
        print(f"Failed to save settings: {e}")

# Reset settings to default values.
def reset_settings():
    save_settings(DEFAULT_SETTINGS.copy())
