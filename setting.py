import streamlit as st
import os
import json

SETTINGS_FILE = "settings.json"
SOUND_FOLDER = "alarm_sounds"

def load_settings():
    """Load settings from a JSON file."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"alarm_enabled": True, "alarm_sound": "default.wav"}

def save_settings(settings):
    """Save settings to a JSON file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def settings():
    """Settings UI in Streamlit."""
    st.title("")
    settings = load_settings()

    # Toggle for enabling/disabling alarm
    alarm_enabled = st.checkbox("Enable Alarm", value=settings["alarm_enabled"])

    # Select or upload custom alarm sound
    sound_files = [f for f in os.listdir(SOUND_FOLDER) if f.endswith((".wav", ".mp3"))]
    selected_sound = st.selectbox("Select Alarm Sound", sound_files, index=sound_files.index(settings["alarm_sound"]) if settings["alarm_sound"] in sound_files else 0)

    uploaded_file = st.file_uploader("Upload Custom Alarm Sound", type=["wav", "mp3"])
    if uploaded_file:
        sound_path = os.path.join(SOUND_FOLDER, uploaded_file.name)
        with open(sound_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name}")
        sound_files.append(uploaded_file.name)
        selected_sound = uploaded_file.name

    # Save settings
    if st.button("Save Settings"):
        settings["alarm_enabled"] = alarm_enabled
        settings["alarm_sound"] = selected_sound
        save_settings(settings)
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    settings()
