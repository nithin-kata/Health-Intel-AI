# db_handler.py - Secure Local SQLite Database Authentication

import sqlite3
import hashlib
import os

DB_PATH = "users.db"

def hash_password(password, salt=None):
    """
    Hashes a password using PBKDF2 HMAC with SHA-256 and a cryptographic salt.
    """
    if salt is None:
        # Generate a random 16-byte salt represented as a hex string
        salt = os.urandom(16).hex()
        
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000 # 100,000 iterations for safety
    ).hex()
    return pwd_hash, salt

def init_db():
    """
    Initializes the SQLite database and creates the users table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)
    conn.commit()
    
    # Seed default demo account if database is completely empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        pwd_hash, salt = hash_password("health123")
        cursor.execute(
            "INSERT INTO users (email, name, password_hash, salt) VALUES (?, ?, ?, ?)",
            ("patient@healthintel.ai", "Demo Patient", pwd_hash, salt)
        )
        conn.commit()
        
    conn.close()

def register_user(email, name, password):
    """
    Registers a new user in the local database.
    Checks if email is already registered.
    """
    email = email.strip().lower()
    name = name.strip()
    
    if not email or not name or not password:
        return False, "❌ All fields are required."
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return False, "❌ An account with this email address already exists."
        
    # Generate hash and salt
    pwd_hash, salt = hash_password(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (email, name, password_hash, salt) VALUES (?, ?, ?, ?)",
            (email, name, pwd_hash, salt)
        )
        conn.commit()
        success = True
        msg = "✅ Account successfully created!"
    except Exception as e:
        success = False
        msg = f"❌ Registration failed: {str(e)}"
        
    conn.close()
    return success, msg

def authenticate_user(email, password):
    """
    Verifies user credentials.
    Returns (success, message, user_name)
    """
    email = email.strip().lower()
    
    if not email or not password:
        return False, "❌ Email and password are required.", None
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, password_hash, salt FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return False, "❌ No account found matching this email.", None
        
    name, stored_hash, salt = row
    
    # Recompute hash using stored salt
    computed_hash, _ = hash_password(password, salt)
    
    if computed_hash == stored_hash:
        return True, "✅ Access granted!", name
    else:
        return False, "❌ Incorrect password. Please try again.", None

# Auto-initialize database on import
init_db()
