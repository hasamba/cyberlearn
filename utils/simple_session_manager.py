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
        # ALWAYS check query params first, as they persist across refreshes
        query_params = st.query_params
        url_browser_id = query_params.get('bid', None)

        # If we have a browser_id in URL, use it (takes priority)
        if url_browser_id:
            if "_browser_id" not in st.session_state:
                print(f"[SessionManager] Retrieved browser_id from URL: {url_browser_id[:8]}...")
                st.session_state._browser_id = url_browser_id
            elif st.session_state._browser_id != url_browser_id:
                # URL has different ID than session - URL wins
                print(f"[SessionManager] URL browser_id differs, using URL: {url_browser_id[:8]}...")
                st.session_state._browser_id = url_browser_id
            else:
                print(f"[SessionManager] Using existing browser_id: {url_browser_id[:8]}...")
        else:
            # No browser_id in URL
            if "_browser_id" not in st.session_state:
                # Generate new browser ID
                import secrets
                browser_id = secrets.token_urlsafe(16)
                print(f"[SessionManager] Generated new browser_id: {browser_id[:8]}...")
                st.session_state._browser_id = browser_id

                # Add to URL (this should persist)
                st.query_params['bid'] = browser_id
                print(f"[SessionManager] Added browser_id to URL: {browser_id}")
            else:
                # Have session ID but not in URL - re-add to URL
                print(f"[SessionManager] Re-adding browser_id to URL: {st.session_state._browser_id[:8]}...")
                st.query_params['bid'] = st.session_state._browser_id

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
            from datetime import datetime

            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()

            # Get current time for comparison
            now = datetime.utcnow().isoformat()

            cursor.execute("""
                SELECT session_token, user_id, expires_at
                FROM user_sessions
                WHERE user_agent = ?
                AND expires_at > ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (browser_id, now))

            result = cursor.fetchone()
            conn.close()

            if result:
                print(f"[SessionManager] Found session for browser {browser_id[:8]}...")
                return result[0]  # session_token
            else:
                print(f"[SessionManager] No active session for browser {browser_id[:8]}...")
            return None

        except Exception as e:
            print(f"[SessionManager] Error getting session token: {e}")
            import traceback
            traceback.print_exc()
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
