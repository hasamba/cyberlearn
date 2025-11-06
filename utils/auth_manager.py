"""
Authentication Manager for CyberLearn
Handles browser-specific session management using cookies
"""

import streamlit as st
import hashlib
import secrets
from typing import Optional
from datetime import datetime, timedelta
from uuid import UUID


class AuthManager:
    """Manages user authentication and browser sessions using cookies"""

    COOKIE_NAME = "cyberlearn_session"
    COOKIE_EXPIRY_DAYS = 30

    def __init__(self, db):
        """Initialize auth manager with database connection"""
        self.db = db
        self._ensure_session_table()

    def _ensure_session_table(self):
        """Create sessions table if it doesn't exist"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                user_agent TEXT,
                ip_address TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        self.db.conn.commit()

    def _generate_session_token(self) -> str:
        """Generate a secure random session token"""
        return secrets.token_urlsafe(32)

    def _hash_token(self, token: str) -> str:
        """Hash token for secure storage"""
        return hashlib.sha256(token.encode()).hexdigest()

    def create_session(self, user_id: UUID, user_agent: str = None, ip_address: str = None) -> str:
        """
        Create a new session for a user
        Returns the session token to be stored in cookie
        """
        token = self._generate_session_token()
        hashed_token = self._hash_token(token)

        now = datetime.utcnow()
        expires_at = now + timedelta(days=self.COOKIE_EXPIRY_DAYS)

        cursor = self.db.conn.cursor()
        cursor.execute("""
            INSERT INTO user_sessions
            (session_token, user_id, created_at, expires_at, last_accessed, user_agent, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            hashed_token,
            str(user_id),
            now.isoformat(),
            expires_at.isoformat(),
            now.isoformat(),
            user_agent,
            ip_address
        ))
        self.db.conn.commit()

        return token  # Return unhashed token for cookie

    def validate_session(self, token: str) -> Optional[UUID]:
        """
        Validate a session token and return user_id if valid
        Returns None if session is invalid or expired
        """
        if not token:
            return None

        hashed_token = self._hash_token(token)

        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT user_id, expires_at
            FROM user_sessions
            WHERE session_token = ?
        """, (hashed_token,))

        row = cursor.fetchone()
        if not row:
            return None

        user_id, expires_at = row
        expires_dt = datetime.fromisoformat(expires_at)

        # Check if session expired
        if datetime.utcnow() > expires_dt:
            self.revoke_session(token)
            return None

        # Update last accessed time
        cursor.execute("""
            UPDATE user_sessions
            SET last_accessed = ?
            WHERE session_token = ?
        """, (datetime.utcnow().isoformat(), hashed_token))
        self.db.conn.commit()

        return UUID(user_id)

    def revoke_session(self, token: str):
        """Revoke/delete a session"""
        if not token:
            return

        hashed_token = self._hash_token(token)
        cursor = self.db.conn.cursor()
        cursor.execute("""
            DELETE FROM user_sessions
            WHERE session_token = ?
        """, (hashed_token,))
        self.db.conn.commit()

    def revoke_all_user_sessions(self, user_id: UUID):
        """Revoke all sessions for a user (e.g., on password change)"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            DELETE FROM user_sessions
            WHERE user_id = ?
        """, (str(user_id),))
        self.db.conn.commit()

    def cleanup_expired_sessions(self):
        """Remove expired sessions from database"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            DELETE FROM user_sessions
            WHERE expires_at < ?
        """, (datetime.utcnow().isoformat(),))
        self.db.conn.commit()

    def get_active_sessions_count(self, user_id: UUID) -> int:
        """Get number of active sessions for a user"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM user_sessions
            WHERE user_id = ? AND expires_at > ?
        """, (str(user_id), datetime.utcnow().isoformat()))
        return cursor.fetchone()[0]
