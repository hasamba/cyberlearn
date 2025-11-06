"""
Session Manager for Streamlit using localStorage
Provides persistent browser-based authentication using localStorage via JavaScript
"""

import streamlit as st
from streamlit.components.v1 import html
import time


class SessionManager:
    """Manages browser sessions using localStorage for persistence"""

    SESSION_KEY = "cyberlearn_session_token"

    def __init__(self):
        """Initialize session manager"""
        # Track if we've loaded from browser
        if "_session_loaded" not in st.session_state:
            st.session_state._session_loaded = False
            st.session_state._browser_session_token = None

    def get_browser_session(self) -> str:
        """
        Get session token from browser's localStorage

        Returns:
            Session token or None
        """
        if not st.session_state._session_loaded:
            # Load from localStorage using JavaScript
            js_code = f"""
            <script>
            // Get token from localStorage
            const token = localStorage.getItem('{self.SESSION_KEY}');

            // Send to Streamlit via query params (reliable method)
            if (token) {{
                const url = new URL(window.location);
                url.searchParams.set('session_token', token);
                // Use replace to avoid adding to history
                window.history.replaceState({{}}, '', url);
            }}
            </script>
            """
            html(js_code, height=0)
            st.session_state._session_loaded = True

            # Small delay to let JavaScript execute
            time.sleep(0.1)

        # Try to get from query params (set by JavaScript)
        query_params = st.query_params
        if 'session_token' in query_params:
            token = query_params['session_token']
            st.session_state._browser_session_token = token
            # Clear query param to avoid exposure in URL
            query_params_dict = dict(query_params)
            if 'session_token' in query_params_dict:
                del query_params_dict['session_token']
            st.query_params.update(query_params_dict)
            return token

        return st.session_state._browser_session_token

    def set_browser_session(self, token: str):
        """
        Set session token in browser's localStorage

        Args:
            token: Session token to store
        """
        js_code = f"""
        <script>
        // Store token in localStorage
        localStorage.setItem('{self.SESSION_KEY}', '{token}');

        // Also set in query params for immediate use
        const url = new URL(window.location);
        url.searchParams.set('session_token', '{token}');
        window.history.replaceState({{}}, '', url);
        </script>
        """
        html(js_code, height=0)
        st.session_state._browser_session_token = token

    def delete_browser_session(self):
        """Delete session token from browser's localStorage"""
        js_code = f"""
        <script>
        // Remove token from localStorage
        localStorage.removeItem('{self.SESSION_KEY}');

        // Clear query params
        const url = new URL(window.location);
        url.searchParams.delete('session_token');
        window.history.replaceState({{}}, '', url);
        </script>
        """
        html(js_code, height=0)
        st.session_state._browser_session_token = None
