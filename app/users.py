import streamlit as st
import json
import os
import bcrypt

# Path to the user database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, 'data', 'users.json')

def hash_password(password):
    """Securely hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    """Check if a plain text password matches a hashed bcrypt password."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def load_users():
    """Load users from the JSON file or return defaults if file doesn't exist."""
    if not os.path.exists(USERS_FILE):
        defaults = {
            "admin": {"password": hash_password("admin123"), "role": "admin"},
            "sachin": {"password": hash_password("1234"), "role": "user"}
        }
        save_users(defaults)
        return defaults
    
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save the users dictionary to the JSON file."""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def verify_user(username, password):
    """Verify if a user exists and the bcrypt password matches."""
    users = load_users()
    if username in users:
        hashed = users[username]["password"]
        if hashed == password or check_password(password, hashed):
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            return True
    return False

def register_user(username, password, role="user"):
    """Register a new user with a hashed password."""
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    
    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    save_users(users)
    return True, "Registration successful!"

def change_password(username, new_password):
    """Update a user's password."""
    users = load_users()
    if username in users:
        users[username]["password"] = hash_password(new_password)
        save_users(users)
        return True, "Password updated successfully."
    return False, "User not found."

def delete_user(username):
    """Remove a user from the database."""
    users = load_users()
    if username in users:
        if username == "admin":
            return False, "Cannot delete primary admin account!"
        del users[username]
        save_users(users)
        return True, f"User '{username}' deleted successfully."
    return False, "User not found."