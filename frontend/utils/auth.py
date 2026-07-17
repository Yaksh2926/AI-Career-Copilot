import os
import json
import re
import streamlit as st

USERS_DB_FILE = ".users_db.json"
SESSION_FILE = ".user_session.json"

# Pre-populate mock database
def init_mock_db():
    if not os.path.exists(USERS_DB_FILE):
        default_users = {
            "candidate@copilot.ai": {
                "name": "Yaksh Jindal",
                "email": "candidate@copilot.ai",
                "password": "Password123!", # In a real system, this is hashed
                "avatar": "https://api.dicebear.com/7.x/identicon/svg?seed=Yaksh"
            }
        }
        try:
            with open(USERS_DB_FILE, "w") as f:
                json.dump(default_users, f)
        except Exception:
            pass

def load_users():
    init_mock_db()
    try:
        with open(USERS_DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    try:
        with open(USERS_DB_FILE, "w") as f:
            json.dump(users, f)
    except Exception:
        pass

# Persistent Session Management ("Remember Me")
def save_persistent_session(user_data):
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(user_data, f)
    except Exception:
        pass

def load_persistent_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def clear_persistent_session():
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except Exception:
            pass

# User Actions
def login_user(email, password, remember_me=False) -> dict:
    users = load_users()
    email_clean = email.strip().lower()
    
    if email_clean in users:
        user_info = users[email_clean]
        if user_info["password"] == password:
            session_data = {
                "name": user_info["name"],
                "email": user_info["email"],
                "avatar": user_info.get("avatar", "https://api.dicebear.com/7.x/identicon/svg?seed=" + user_info["name"])
            }
            # Set session state
            st.session_state["user"] = session_data
            st.session_state["logged_in"] = True
            
            if remember_me:
                save_persistent_session(session_data)
            else:
                clear_persistent_session()
                
            return {"success": True, "message": "Login Successful", "user": session_data}
            
    return {"success": False, "message": "Invalid Credentials"}

def signup_user(name, email, password) -> dict:
    users = load_users()
    email_clean = email.strip().lower()
    
    if email_clean in users:
        return {"success": False, "message": "Account already exists with this email"}
        
    # Create new account
    avatar_seed = name.replace(" ", "")
    users[email_clean] = {
        "name": name.strip(),
        "email": email_clean,
        "password": password,
        "avatar": f"https://api.dicebear.com/7.x/identicon/svg?seed={avatar_seed}"
    }
    save_users(users)
    
    session_data = {
        "name": name.strip(),
        "email": email_clean,
        "avatar": f"https://api.dicebear.com/7.x/identicon/svg?seed={avatar_seed}"
    }
    st.session_state["user"] = session_data
    st.session_state["logged_in"] = True
    
    # Defaults to no remember me on signup
    clear_persistent_session()
    
    return {"success": True, "message": "Account Created Successfully", "user": session_data}

def forgot_password_request(email) -> dict:
    users = load_users()
    email_clean = email.strip().lower()
    
    if email_clean in users:
        # Simulate sending email
        return {"success": True, "message": "Password Reset Link Sent"}
    return {"success": False, "message": "Email address not found"}

def reset_user_password(email, new_password) -> dict:
    users = load_users()
    email_clean = email.strip().lower()
    
    if email_clean in users:
        users[email_clean]["password"] = new_password
        save_users(users)
        return {"success": True, "message": "Password Reset Successfully"}
    return {"success": False, "message": "Failed to reset password"}

def logout_user():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    clear_persistent_session()

# Validation Helpers
def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def calculate_password_strength(password: str) -> tuple:
    """
    Returns (score 0-4, text label, hex color)
    """
    if not password:
        return (0, "Empty", "#64748B")
        
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for char in password):
        score += 1
        
    if score == 0 or score == 1:
        return (score, "Weak", "#EF4444")
    elif score == 2 or score == 3:
        return (score, "Medium", "#F59E0B")
    else:
        return (score, "Strong", "#22C55E")
