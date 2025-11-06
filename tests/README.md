# CyberLearn Testing Guide

## Setup

### Install Test Dependencies

On your VM where the app is running:

```bash
pip install -r requirements-dev.txt
playwright install chromium
```

## Running Tests

### Browser Back/Forward Navigation Tests

These tests verify that the browser back/forward buttons work correctly and trigger automatic page refresh.

**Prerequisites:**
- The Streamlit app must be running on `http://10.0.0.162:8501`
- At least one user account must exist (for quick login)
- At least one lesson must be available

**Run the tests:**

```bash
# Run all tests in verbose mode
pytest tests/test_browser_back_navigation.py -v

# Run a specific test
pytest tests/test_browser_back_navigation.py::test_browser_back_navigation_auto_refresh -v

# Run tests with browser visible (non-headless)
pytest tests/test_browser_back_navigation.py -v --headed

# Run tests and keep browser open after test
pytest tests/test_browser_back_navigation.py -v --headed --slowmo 1000
```

**What the tests verify:**

1. **test_browser_back_navigation_auto_refresh**:
   - User can login
   - User can navigate to a lesson
   - User can click through content blocks (Next button)
   - Pressing browser back button changes URL
   - Page auto-refreshes after back button (content updates)
   - URL parameters (block_index) are correctly synced
   - User can navigate back to learning page

2. **test_browser_forward_navigation**:
   - Browser forward button also works
   - Page auto-refreshes after forward button
   - Navigation state is correctly maintained

## Test Configuration

### Browser Settings

Default configuration in `conftest.py`:
- Browser: Chromium
- Headless: False (browser visible)
- Viewport: 1920x1080

To modify, edit `tests/conftest.py`.

### App URL

Tests currently hardcoded to `http://10.0.0.162:8501`. To change:
1. Edit the URL in test files
2. Or create a pytest fixture for configurable URLs

## Troubleshooting

### Test Fails: "Could not find lesson_id in URL"

**Cause**: No lessons are loaded in the database.

**Fix**: Load lessons into the database:
```bash
python load_all_lessons.py
```

### Test Fails: Quick Login button not found

**Cause**: No users exist in the database.

**Fix**: Create a user account:
1. Open the app in a browser
2. Create an account via the sidebar
3. Re-run tests

### Test Fails: Timeouts

**Cause**: App is slow to respond or network latency.

**Fix**: Increase sleep times in test file:
```python
time.sleep(2)  # Increase from 1 to 2 seconds
```

### Browser doesn't close after test

**Cause**: Test crashed or was interrupted.

**Fix**:
```bash
# Kill all chromium processes
pkill chromium
```

## Writing New Tests

Example test structure:

```python
def test_my_feature(page):
    """Test description"""

    # Navigate to app
    page.goto("http://10.0.0.162:8501")
    time.sleep(2)

    # Interact with elements
    page.click('button:has-text("My Button")')

    # Verify results
    assert "expected" in page.url

    # Check element visibility
    element = page.locator('text="My Text"')
    assert element.is_visible()
```

## CI/CD Integration

To run tests in CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    playwright install --with-deps chromium

- name: Start Streamlit app
  run: streamlit run app.py &

- name: Run tests
  run: pytest tests/ -v
```

## Related Documentation

- [Playwright Python Docs](https://playwright.dev/python/docs/intro)
- [pytest Documentation](https://docs.pytest.org/)
- [Streamlit Testing Guide](https://docs.streamlit.io/develop/api-reference/app-testing)
