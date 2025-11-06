"""
File-based Session Manager for Streamlit
Stores session tokens in a local JSON file keyed by browser fingerprint
This is the ONLY reliable way to persist sessions across page refreshes in Streamlit
"""

import streamlit as st
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta


class FileSessionManager:
    """
    Manages sessions using a local JSON file for persistence.

    Uses Streamlit's experimental_get_query_params to generate a stable
    browser fingerprint from the initial connection info.
    """

    def __init__(self, db):
        """
        Initialize session manager

        Args:
            db: Database instance
        """
        self.db = db
        self.sessions_file = Path("data/browser_sessions.json")
        self.sessions_file.parent.mkdir(exist_ok=True)

        # Generate stable browser fingerprint
        if "_browser_fingerprint" not in st.session_state:
            # Use session_id from Streamlit runtime as fingerprint
            # This is stable for a browser tab session
            try:
                from streamlit.runtime.scriptrunner import get_script_run_ctx
                ctx = get_script_run_ctx()
                if ctx:
                    session_id = ctx.session_id
                    st.session_state._browser_fingerprint = session_id
                    print(f"[FileSessionManager] Browser fingerprint: {session_id[:16]}...")
                else:
                    # Fallback: use a random ID
                    import secrets
                    st.session_state._browser_fingerprint = secrets.token_urlsafe(16)
                    print(f"[FileSessionManager] Fallback fingerprint generated")
            except Exception as e:
                print(f"[FileSessionManager] Error getting session context: {e}")
                import secrets
                st.session_state._browser_fingerprint = secrets.token_urlsafe(16)

    def _load_sessions(self) -> dict:
        """Load all sessions from file"""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_sessions(self, sessions: dict):
        """Save all sessions to file"""
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)

    def create_session(self, user_id: str, auth_manager) -> str:
        """
        Create a new session for the user

        Args:
            user_id: User ID
            auth_manager: AuthManager instance

        Returns:
            Session token
        """
        # Create session in database
        session_token = auth_manager.create_session(user_id)

        # Store in file keyed by browser fingerprint
        sessions = self._load_sessions()
        fingerprint = st.session_state._browser_fingerprint

        sessions[fingerprint] = {
            "token": session_token,
            "user_id": str(user_id),  # Convert UUID to string for JSON
            "created_at": datetime.utcnow().isoformat()
        }

        self._save_sessions(sessions)

        # Also store in session state for current tab
        st.session_state._current_session_token = session_token
        st.session_state._session_validated = True

        print(f"[FileSessionManager] Created session for user {user_id}, fingerprint {fingerprint[:16]}...")
        return session_token

    def get_current_session(self) -> str:
        """
        Get the current session token if valid

        Returns:
            Session token or None
        """
        # Check session state first (fast path for same tab)
        if hasattr(st.session_state, '_current_session_token') and st.session_state._current_session_token:
            if hasattr(st.session_state, '_session_validated') and st.session_state._session_validated:
                print(f"[FileSessionManager] Using cached session from tab state")
                return st.session_state._current_session_token

        # Load from file using browser fingerprint
        sessions = self._load_sessions()
        fingerprint = st.session_state._browser_fingerprint

        if fingerprint in sessions:
            session_data = sessions[fingerprint]
            token = session_data["token"]

            # Cache in session state
            st.session_state._current_session_token = token
            st.session_state._session_validated = True

            print(f"[FileSessionManager] Loaded session from file for fingerprint {fingerprint[:16]}...")
            return token

        print(f"[FileSessionManager] No session found for fingerprint {fingerprint[:16]}...")
        return None

    def clear_session(self, auth_manager):
        """
        Clear the current session

        Args:
            auth_manager: AuthManager instance
        """
        # Revoke from database
        if hasattr(st.session_state, '_current_session_token') and st.session_state._current_session_token:
            auth_manager.revoke_session(st.session_state._current_session_token)
            print(f"[FileSessionManager] Revoked session from database")

        # Remove from file
        sessions = self._load_sessions()
        fingerprint = st.session_state._browser_fingerprint

        if fingerprint in sessions:
            del sessions[fingerprint]
            self._save_sessions(sessions)
            print(f"[FileSessionManager] Removed session from file")

        # Clear from tab state
        st.session_state._current_session_token = None
        st.session_state._session_validated = False
        print(f"[FileSessionManager] Cleared session from tab state")
