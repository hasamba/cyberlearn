# Cookie-Based Authentication System

## Overview

CyberLearn uses a secure, cookie-based authentication system to manage user sessions across different browsers and devices. This ensures that each browser maintains its own independent login state.

## Problem Solved

**Previous Issue**: The old system used global auto-login that looked up the last user who logged in from the database. This caused a critical security flaw:
- User A logs in on Browser 1
- User B opens the app on Browser 2
- User B would automatically be logged in as User A!

**Solution**: Cookie-based per-browser sessions ensure each browser maintains its own authentication state independently.

## Architecture

### Components

1. **AuthManager** (`utils/auth_manager.py`)
   - Manages user sessions and authentication tokens
   - Creates, validates, and revokes session tokens
   - Handles session expiration and cleanup

2. **CookieManager** (`utils/cookie_manager.py`)
   - Handles browser cookie operations
   - Stores and retrieves session tokens
   - Integrates with Streamlit using JavaScript

3. **Database Table: `user_sessions`**
   ```sql
   CREATE TABLE user_sessions (
       session_token TEXT PRIMARY KEY,    -- Hashed session token
       user_id TEXT NOT NULL,            -- User ID (FK)
       created_at TEXT NOT NULL,          -- Session creation timestamp
       expires_at TEXT NOT NULL,          -- Session expiration timestamp
       last_accessed TEXT NOT NULL,       -- Last access timestamp
       user_agent TEXT,                   -- Browser user agent (optional)
       ip_address TEXT,                   -- IP address (optional)
       FOREIGN KEY (user_id) REFERENCES users (user_id)
   )
   ```

### Security Features

1. **Token Hashing**
   - Session tokens are hashed (SHA-256) before storage in database
   - Only hashed tokens are stored, raw tokens never persisted
   - Tokens are 32-byte URL-safe random strings

2. **Session Expiration**
   - Default expiration: 30 days
   - Configurable via `AuthManager.COOKIE_EXPIRY_DAYS`
   - Expired sessions are automatically cleaned up

3. **Per-Browser Isolation**
   - Each browser gets its own unique session token
   - Sessions are stored in browser cookies
   - No cross-browser authentication leakage

4. **Secure Cookie Settings**
   - `SameSite=Lax`: CSRF protection
   - `path=/`: Available across entire application
   - `max-age`: Automatic expiration

## Authentication Flow

### Login Flow

1. User enters username and submits login form
2. `login_user(user)` is called:
   - Updates user's `last_login` and streak
   - Saves user to database
   - Creates new session via `auth_manager.create_session(user_id)`
   - Generates secure random session token
   - Hashes and stores token in `user_sessions` table
   - Returns unhashed token
3. Token is stored in browser cookie via `cookie_manager.set()`
4. User is authenticated

### Session Validation Flow

1. On page load, `initialize_session_state()` is called
2. Retrieves session token from cookie
3. Validates token via `auth_manager.validate_session(token)`:
   - Hashes the token
   - Looks up hashed token in database
   - Checks if session is expired
   - Updates `last_accessed` timestamp
   - Returns user_id if valid, None otherwise
4. If valid, loads user from database
5. If invalid/expired, deletes cookie and shows login page

### Logout Flow

1. User clicks "Logout" button
2. Retrieves session token from cookie
3. Revokes session via `auth_manager.revoke_session(token)`:
   - Deletes session record from database
4. Deletes cookie via `cookie_manager.delete()`
5. Clears `st.session_state.current_user`
6. Redirects to welcome page

## API Reference

### AuthManager

```python
# Initialize
auth_manager = AuthManager(db)

# Create session (returns token for cookie)
token = auth_manager.create_session(
    user_id,
    user_agent="Mozilla/5.0...",  # Optional
    ip_address="192.168.1.1"       # Optional
)

# Validate session (returns user_id or None)
user_id = auth_manager.validate_session(token)

# Revoke session
auth_manager.revoke_session(token)

# Revoke all user sessions
auth_manager.revoke_all_user_sessions(user_id)

# Cleanup expired sessions
auth_manager.cleanup_expired_sessions()

# Get active session count
count = auth_manager.get_active_sessions_count(user_id)
```

### CookieManager

```python
# Initialize
cookie_manager = CookieManager()

# Set cookie
cookie_manager.set(
    name="session_token",
    value="abc123...",
    max_age_days=30
)

# Get cookie
value = cookie_manager.get("session_token", default=None)

# Delete cookie
cookie_manager.delete("session_token")

# Get all cookies
cookies = cookie_manager.get_all()

# Clear all cookies
cookie_manager.clear_all()
```

### Helper Functions (app.py)

```python
# Login user and create session
login_user(user: UserProfile)
```

## Database Migration

To add the `user_sessions` table to an existing database:

```bash
python scripts/migrate_add_sessions_table.py
```

This script:
- Adds `user_sessions` table if it doesn't exist
- Creates indexes for efficient lookups
- Migrates both working and template databases

## Configuration

### Session Expiration

Modify in `utils/auth_manager.py`:

```python
class AuthManager:
    COOKIE_NAME = "cyberlearn_session"
    COOKIE_EXPIRY_DAYS = 30  # Change this value
```

## Testing

### Multi-Browser Testing

1. **Browser 1**: Login as User A
   - Should show User A's dashboard
   - Cookie should be set for User A's session

2. **Browser 2** (incognito/different browser): Login as User B
   - Should show login page (NOT auto-login as User A)
   - After login, should show User B's dashboard
   - Cookie should be set for User B's session

3. **Browser 1**: Refresh
   - Should still show User A's dashboard
   - User A's session should remain active

4. **Browser 2**: Refresh
   - Should still show User B's dashboard
   - User B's session should remain active

### Session Expiration Testing

1. Login and note the session token
2. Manually expire the session in database:
   ```sql
   UPDATE user_sessions
   SET expires_at = '2020-01-01T00:00:00'
   WHERE session_token = '<hashed_token>'
   ```
3. Refresh page
4. Should redirect to login page
5. Cookie should be deleted

## Troubleshooting

### Issue: User stays logged in after logout
**Cause**: Cookie not properly deleted
**Fix**: Check browser dev tools → Application → Cookies → Verify cookie is removed

### Issue: User gets logged out on every page refresh
**Cause**: Cookies not being stored/retrieved
**Fix**:
- Check browser cookie settings
- Ensure JavaScript is enabled
- Check cookie_manager component is loading

### Issue: Multiple browsers share the same session
**Cause**: Cookies are shared between browsers (shouldn't happen)
**Fix**:
- Clear all browser cookies
- Verify each browser has unique session token
- Check `user_sessions` table for multiple entries

### Issue: Session expired but user still logged in
**Cause**: Validation not running or bypassed
**Fix**:
- Verify `initialize_session_state()` is called on every page load
- Check `cleanup_expired_sessions()` is running
- Manually clean up: `DELETE FROM user_sessions WHERE expires_at < datetime('now')`

## Best Practices

1. **Never store raw tokens in database** - Always hash tokens before storage
2. **Set reasonable expiration** - Balance security vs user convenience
3. **Clean up expired sessions** - Run cleanup regularly to prevent database bloat
4. **Log authentication events** - Use debug mode to track login/logout/validation
5. **Handle edge cases** - User deleted, database unavailable, cookie disabled

## Security Considerations

1. **Token Generation**: Uses `secrets.token_urlsafe(32)` for cryptographically secure random tokens
2. **Token Storage**: Tokens are hashed with SHA-256 before storage
3. **Transport Security**: Use HTTPS in production to prevent token interception
4. **CSRF Protection**: `SameSite=Lax` cookie attribute
5. **Session Cleanup**: Expired sessions are automatically purged

## Future Enhancements

- [ ] Add "Remember Me" option with longer expiration
- [ ] Add IP address and user agent validation for additional security
- [ ] Implement session activity logging
- [ ] Add "Active Sessions" page where users can see and revoke sessions
- [ ] Add email/password authentication (currently username-only)
- [ ] Implement 2FA (Two-Factor Authentication)
- [ ] Add OAuth integration (Google, GitHub, etc.)

## References

- Streamlit Components Documentation
- OWASP Session Management Cheat Sheet
- RFC 6265 (HTTP State Management Mechanism)
