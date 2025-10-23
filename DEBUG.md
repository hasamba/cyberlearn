# Debug Mode Guide

CyberLearn includes a debug/verbose mode for troubleshooting and development.

## Enabling Debug Mode

### Using Start Scripts (Recommended)

**Linux/Mac:**
```bash
./start.sh -v
# or
./start.sh --debug
```

**Windows:**
```batch
start.bat -v
REM or
start.bat --debug
```

### Manual Start

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat # Windows

# Run with debug flag
streamlit run app.py -- -v
# or
streamlit run app.py -- --debug
```

**Note:** The `--` before the flag is required when using `streamlit run` directly.

## What Debug Mode Shows

### Terminal Output

When debug mode is enabled, you'll see:

```
[DEBUG] Application starting in DEBUG mode
[DEBUG] Python version: 3.12.0
[DEBUG] Streamlit version: 1.28.0
[DEBUG] Working directory: /home/user/cyberlearn
[DEBUG] Database connection initialized
[DEBUG] Session state initialized (no user)
```

### In-App Debug Panel

A debug info section appears in the sidebar showing:
- Current user ID
- Active page
- Database status
- Current lesson (if viewing one)

### Log Levels

Debug mode sets logging to `DEBUG` level, showing detailed information about:
- Database queries
- User state changes
- Navigation events
- Lesson loading
- Error details

Normal mode only shows `WARNING` and `ERROR` level messages.

## Common Debug Scenarios

### Database Issues

```bash
./start.sh -v
```

Look for:
- `[DEBUG] Database connection initialized`
- `[DEBUG] Lesson count: XX`
- Error messages about missing tables or corrupt data

### User Authentication Problems

Check debug output for:
- User ID values
- Session state initialization
- Login/logout events

### Lesson Loading Errors

Debug mode will show:
- Which lessons fail to load
- Validation errors in lesson JSON
- Missing prerequisites

### UI Navigation Issues

Monitor:
- Page transitions
- Button click events
- Session state updates

## Debug Configuration

The debug system is configured in `config.py`:

```python
from config import config

# Check if debug mode is active
if config.debug:
    print("Debug is enabled")

# Use logging
config.log_debug("This only shows in debug mode")
config.log_info("This always shows")
config.log_error("Error messages")
```

## Performance Impact

Debug mode has minimal performance impact:
- Extra console logging (~5% overhead)
- Debug panel in UI (negligible)
- More detailed error traces

It's safe to leave enabled during development.

## Disabling Debug Mode

Simply restart without the `-v` or `--debug` flag:

```bash
./start.sh  # Normal mode
```

## Troubleshooting with Debug Mode

### Issue: "No lessons found"

1. Enable debug mode: `./start.sh -v`
2. Look for database connection messages
3. Check lesson count in debug output
4. Verify `cyberlearn.db` exists

### Issue: "User not found"

1. Enable debug mode
2. Check user ID in sidebar debug panel
3. Verify database has users table
4. Check for authentication errors in logs

### Issue: Crashes or errors

1. Run with debug: `./start.sh -v`
2. Reproduce the error
3. Copy full error traceback from terminal
4. Check debug panel for state information

## Debug vs Production

| Feature | Normal Mode | Debug Mode |
|---------|-------------|------------|
| Logging Level | WARNING | DEBUG |
| Console Output | Minimal | Verbose |
| Debug Panel | Hidden | Visible |
| Error Details | Basic | Full traceback |
| Performance | 100% | ~95% |

## For Developers

### Adding Debug Logging

```python
from config import config, debug_print

# Quick debug print
debug_print("This shows in debug mode")

# Structured logging
config.log_debug("Detailed information")
config.log_info("General information")
config.log_warning("Warning message")
config.log_error("Error message")
```

### Conditional Debug Code

```python
if config.debug:
    # This only runs in debug mode
    st.sidebar.write("Debug info")
```

## Environment Variables

Currently, debug mode is controlled by command-line flags. Future versions may support:

```bash
export CYBERLEARN_DEBUG=1
streamlit run app.py
```

## Related Files

- `config.py` - Debug configuration
- `app.py` - Main app with debug integration
- `start.sh` / `start.bat` - Start scripts with debug support

---

**Last Updated**: 2025-10-23
