"""
Add AI Security, IoT Security, and Web3 Security domains to user profiles

This script adds three new skill columns to the users table for emerging
technology security domains:
- ai_security (AI/ML security)
- iot_security (IoT/ICS security)
- web3_security (Blockchain/Web3 security)
"""

import sqlite3
from pathlib import Path

def add_emerging_tech_domains(db_path: str = "cyberlearn.db"):
    """Add ai_security, iot_security, and web3_security columns to users table"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]

        domains_to_add = {
            'ai_security': 'AI Security',
            'iot_security': 'IoT Security',
            'web3_security': 'Web3 Security'
        }

        added_count = 0

        for column_name, display_name in domains_to_add.items():
            if column_name not in columns:
                print(f"Adding {display_name} domain...")
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} INTEGER DEFAULT 0")
                added_count += 1
                print(f"  ✓ Added {column_name} column")
            else:
                print(f"  ⊙ {display_name} domain already exists")

        conn.commit()

        if added_count > 0:
            print(f"\n✓ Successfully added {added_count} new domain(s)")
            print("\nNew domains available:")
            print("  - ai_security: AI/ML security, prompt injection, model security")
            print("  - iot_security: IoT/ICS security, embedded systems, OT networks")
            print("  - web3_security: Blockchain, smart contracts, DeFi security")
        else:
            print("\nAll domains already present in database")

        # Verify the changes
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"\nTotal skill domains in database: {len([c for c in columns if c not in ['user_id', 'username', 'email', 'created_at', 'last_login', 'total_xp', 'level', 'streak_days', 'longest_streak', 'badges', 'learning_preferences', 'total_lessons_completed', 'total_time_spent', 'diagnostic_completed', 'last_username', 'preferred_tag_filters']])}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"✗ Error adding domains: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    print("=== Adding Emerging Technology Security Domains ===\n")

    db_file = Path("cyberlearn.db")
    if not db_file.exists():
        print(f"✗ Database file not found: {db_file}")
        print("  Please run this script from the project root directory")
        exit(1)

    add_emerging_tech_domains(str(db_file))
    print("\n=== Migration Complete ===")
