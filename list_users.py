#!/usr/bin/env python3
"""
List all users in the CyberLearn database
"""
from database import SessionLocal
from models.user import User

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()

        if not users:
            print("No users found in database.")
            return

        print(f"\nTotal Users: {len(users)}\n")
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Created At'}")
        print("-" * 80)

        for user in users:
            created = user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'N/A'
            print(f"{user.id:<5} {user.username:<20} {user.email:<30} {created}")

    finally:
        db.close()

if __name__ == "__main__":
    list_users()
