"""
Simple Session Manager for Streamlit
Uses browser fingerprinting + database storage for session persistence
No cookies, no localStorage, no JavaScript complexity
"""

import streamlit as st
import hashlib
import json


class SimpleSessionManager:
    """Manages sessions using browser fingerprint stored in query params"""

    def __init__(self):
        """Initialize session manager"""
        # Generate or retrieve browser fingerprint from query params
        if "_browser_id" not in st.session_state:
            # Check if we have a browser ID in query params
            query_params = st.query_params
            if 'bid' in query_params:
                # Use existing browser ID
                st.session_state._browser_id = query_params['bid']
            else:
                # Generate new browser ID (random)
                import secrets
                browser_id = secrets.token_urlsafe(16)
                st.session_state._browser_id = browser_id

                # Add to URL without redirect (just update query params)
                st.query_params['bid'] = browser_id

    def get_browser_id(self) -> str:
        """Get the current browser's unique ID"""
        return st.session_state._browser_id

    def get_session_token(self, db) -> str:
        """
        Get session token for this browser from database

        Args:
            db: Database instance

        Returns:
            Session token or None
        """
        browser_id = self.get_browser_id()

        # Query database for active session with this browser_id
        try:
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT session_token, user_id, expires_at
                FROM user_sessions
                WHERE user_agent = ?
                AND datetime(expires_at) > datetime('now')
                ORDER BY created_at DESC
                LIMIT 1
            """, (browser_id,))

            result = cursor.fetchone()
            conn.close()

            if result:
                return result[0]  # session_token
            return None

        except Exception as e:
            print(f"Error getting session token: {e}")
            return None

    def save_session_token(self, token: str, user_id: str, db):
        """
        Save session token for this browser

        Args:
            token: Session token
            user_id: User ID
            db: Database instance
        """
        # The token is already saved in database by AuthManager.create_session()
        # with user_agent = browser_id, so nothing to do here
        pass

    def clear_session(self, db):
        """
        Clear session for this browser

        Args:
            db: Database instance
        """
        browser_id = self.get_browser_id()

        try:
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()

            # Delete all sessions for this browser
            cursor.execute("""
                DELETE FROM user_sessions
                WHERE user_agent = ?
            """, (browser_id,))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error clearing session: {e}")
