"""
Cookie Manager for Streamlit
Handles browser cookies for session persistence
"""

import streamlit as st
from streamlit.components.v1 import html
import json


class CookieManager:
    """Manages browser cookies for Streamlit applications"""

    def __init__(self):
        """Initialize cookie manager"""
        # Initialize cookies in session state if not present
        if "cookies" not in st.session_state:
            st.session_state.cookies = {}
            # Load cookies from browser on first run
            self._load_cookies_from_browser()

    def _load_cookies_from_browser(self):
        """Load cookies from browser using JavaScript"""
        # This component runs JavaScript to get all cookies
        js_code = """
        <script>
        // Function to parse cookies
        function getCookies() {
            const cookies = {};
            document.cookie.split(';').forEach(cookie => {
                const parts = cookie.trim().split('=');
                if (parts.length === 2) {
                    cookies[parts[0]] = decodeURIComponent(parts[1]);
                }
            });
            return cookies;
        }

        // Send cookies to Streamlit
        const cookies = getCookies();
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: cookies
        }, '*');
        </script>
        """

        # Use html component without key parameter for compatibility
        component_value = html(js_code, height=0)

        if component_value:
            st.session_state.cookies = component_value

    def set(self, name: str, value: str, max_age_days: int = 30):
        """
        Set a cookie

        Args:
            name: Cookie name
            value: Cookie value
            max_age_days: Cookie expiration in days
        """
        # Escape special characters
        safe_value = value.replace('"', '\\"')

        # Calculate max age in seconds
        max_age_seconds = max_age_days * 24 * 60 * 60

        # Set cookie using JavaScript
        js_code = f"""
        <script>
        document.cookie = "{name}={safe_value}; path=/; max-age={max_age_seconds}; SameSite=Lax";

        // Notify Streamlit that cookie was set
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: true
        }}, '*');
        </script>
        """

        html(js_code, height=0)

        # Update session state
        st.session_state.cookies[name] = value

    def get(self, name: str, default=None) -> str:
        """
        Get a cookie value

        Args:
            name: Cookie name
            default: Default value if cookie doesn't exist

        Returns:
            Cookie value or default
        """
        # Access the dictionary directly to avoid Streamlit API conflicts
        cookies_dict = dict(st.session_state.cookies)
        return cookies_dict.get(name, default)

    def delete(self, name: str):
        """
        Delete a cookie

        Args:
            name: Cookie name
        """
        # Set cookie with expired date
        js_code = f"""
        <script>
        document.cookie = "{name}=; path=/; max-age=0";

        // Notify Streamlit that cookie was deleted
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: true
        }}, '*');
        </script>
        """

        html(js_code, height=0)

        # Remove from session state
        if name in st.session_state.cookies:
            del st.session_state.cookies[name]

    def get_all(self) -> dict:
        """Get all cookies as a dictionary"""
        return dict(st.session_state.cookies)

    def clear_all(self):
        """Clear all cookies"""
        for name in list(st.session_state.cookies.keys()):
            self.delete(name)
