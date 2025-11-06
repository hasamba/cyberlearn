"""
Session Manager for Streamlit using localStorage
Provides persistent browser-based authentication using localStorage via JavaScript
"""

import streamlit as st
from streamlit.components.v1 import html


class SessionManager:
    """Manages browser sessions using localStorage for persistence"""

    SESSION_KEY = "cyberlearn_session_token"

    def __init__(self):
        """Initialize session manager"""
        # Initialize storage for token
        if "_browser_session_token" not in st.session_state:
            st.session_state._browser_session_token = None

        # Check query params first (from JavaScript redirect)
        query_params = st.query_params
        if 'st' in query_params and not st.session_state._browser_session_token:
            # Token was passed via query param, store it
            st.session_state._browser_session_token = query_params['st']

    def get_browser_session(self) -> str:
        """
        Get session token from browser's localStorage

        Returns:
            Session token or None
        """
        # If we don't have a token yet, trigger JavaScript to load from localStorage
        if not st.session_state._browser_session_token:
            # This JavaScript will redirect with token in query param if found
            js_code = f"""
            <script>
            (function() {{
                const token = localStorage.getItem('{self.SESSION_KEY}');
                if (token) {{
                    // Redirect with token in query param
                    const url = new URL(window.location);
                    if (!url.searchParams.has('st')) {{
                        url.searchParams.set('st', token);
                        window.location.href = url.toString();
                    }}
                }}
            }})();
            </script>
            """
            html(js_code, height=0)

        return st.session_state._browser_session_token

    def set_browser_session(self, token: str):
        """
        Set session token in browser's localStorage

        Args:
            token: Session token to store
        """
        # Store in session state
        st.session_state._browser_session_token = token

        # Store in localStorage and redirect with token
        js_code = f"""
        <script>
        (function() {{
            // Store token in localStorage
            localStorage.setItem('{self.SESSION_KEY}', '{token}');

            // Redirect with token in query param for immediate use
            const url = new URL(window.location);
            url.searchParams.set('st', '{token}');
            window.location.href = url.toString();
        }})();
        </script>
        """
        html(js_code, height=0)

    def delete_browser_session(self):
        """Delete session token from browser's localStorage"""
        # Clear from session state
        st.session_state._browser_session_token = None

        # Remove from localStorage and clear query params
        js_code = f"""
        <script>
        (function() {{
            // Remove token from localStorage
            localStorage.removeItem('{self.SESSION_KEY}');

            // Clear query params
            const url = new URL(window.location);
            url.searchParams.delete('st');
            window.location.href = url.toString();
        }})();
        </script>
        """
        html(js_code, height=0)
