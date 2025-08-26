# bot/memory.py
from config import MAX_HISTORY

# Short-term chat history
chat_history = {}

# Long-term user profiles
user_profiles = {}

def store_message(chat_id: int, user_id: int, text: str):
    # Store short-term chat history
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    chat_history[chat_id].append(f"{user_id}: {text}")
    if len(chat_history[chat_id]) > MAX_HISTORY:
        chat_history[chat_id] = chat_history[chat_id][-MAX_HISTORY:]
    
    # Initialize user profile if not exist
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            "name": None,
            "tone": "friendly",
            "notes": [],
            "last_message": ""
        }
    # Update last message
    user_profiles[user_id]["last_message"] = text

def get_history(chat_id: int):
    return chat_history.get(chat_id, [])

def get_user_profile(user_id: int):
    return user_profiles.get(user_id, None)

def set_user_tone(user_id: int, tone: str):
    if user_id in user_profiles:
        user_profiles[user_id]["tone"] = tone

def add_user_note(user_id: int, note: str):
    if user_id in user_profiles:
        user_profiles[user_id]["notes"].append(note)
