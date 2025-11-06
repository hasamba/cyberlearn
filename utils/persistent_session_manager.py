"""
Persistent Session Manager for Streamlit
Uses a combination of Streamlit session state + database lookups
No cookies, no query params, no JavaScript - just Python
"""

import streamlit as st
from datetime import datetime
import sqlite3


class PersistentSessionManager:
    """
    Manages sessions using only Streamlit's built-in session state + database.

    Key insight: Streamlit session state persists within a browser tab session.
    We'll keep the user logged in for the duration of their browser tab being open.
    When they close and reopen, they'll need to log in again.

    This is actually the NORMAL behavior for most web apps without "remember me".
    """

    def __init__(self, db):
        """
        Initialize session manager

        Args:
            db: Database instance
        """
        self.db = db

        # Check if we already validated a session in this tab
        if "_session_validated" not in st.session_state:
            st.session_state._session_validated = False

        if "_current_session_token" not in st.session_state:
            st.session_state._current_session_token = None

    def create_session(self, user_id: str, auth_manager) -> str:
        """
        Create a new session for the user

        Args:
            user_id: User ID
            auth_manager: AuthManager instance

        Returns:
            Session token
        """
        # Create session (stored in database)
        session_token = auth_manager.create_session(user_id)

        # Store in Streamlit session state (persists for this tab)
        st.session_state._current_session_token = session_token
        st.session_state._session_validated = True

        print(f"[PersistentSessionManager] Created session for user {user_id}")
        return session_token

    def get_current_session(self) -> str:
        """
        Get the current session token if valid

        Returns:
            Session token or None
        """
        if st.session_state._current_session_token and st.session_state._session_validated:
            print(f"[PersistentSessionManager] Returning existing session from tab state")
            return st.session_state._current_session_token

        print(f"[PersistentSessionManager] No active session in this tab")
        return None

    def clear_session(self, auth_manager):
        """
        Clear the current session

        Args:
            auth_manager: AuthManager instance
        """
        if st.session_state._current_session_token:
            # Revoke session from database
            auth_manager.revoke_session(st.session_state._current_session_token)
            print(f"[PersistentSessionManager] Revoked session from database")

        # Clear from tab state
        st.session_state._current_session_token = None
        st.session_state._session_validated = False
        print(f"[PersistentSessionManager] Cleared session from tab state")
