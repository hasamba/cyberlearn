#!/usr/bin/env python3
"""
List all users in the CyberLearn database using direct SQLite access
"""
import sqlite3
from datetime import datetime

def list_users():
    try:
        conn = sqlite3.connect('cyberlearn.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, username, email, created_at FROM users")
        users = cursor.fetchall()

        if not users:
            print("No users found in database.")
            return

        print(f"\nTotal Users: {len(users)}\n")
        print(f"{'User ID':<40} {'Username':<20} {'Email':<30} {'Created At'}")
        print("-" * 120)

        for user in users:
            user_id, username, email, created_at = user
            email_str = email if email else "N/A"
            print(f"{user_id:<40} {username:<20} {email_str:<30} {created_at}")

        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_users()
