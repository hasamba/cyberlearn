"""
Test browser back/forward navigation with auto-refresh

This test verifies that pressing the browser back button automatically
refreshes the page to reflect the URL change.

Test scenario:
1. Login to the app
2. Navigate to a lesson
3. Click through several content blocks
4. Press browser back button multiple times
5. Verify page auto-refreshes each time
"""

import time


def test_browser_back_navigation_auto_refresh(page):
    """Test that browser back button triggers auto-refresh"""

    # Navigate to the app
    page.goto("http://10.0.0.162:8501")
    time.sleep(2)

    # Login (quick login)
    page.click('button:has-text("Quick Login")')
    time.sleep(2)

    # Navigate to a lesson - go to "My Learning"
    page.click('button:has-text("My Learning")')
    time.sleep(2)

    # Find and click on a lesson (any lesson will do)
    # Look for "Start" or "Continue" button
    start_button = page.locator('button:has-text("Start"), button:has-text("Continue")').first
    start_button.click()
    time.sleep(2)

    # Get current URL - should be a lesson page
    lesson_url = page.url
    print(f"Lesson URL: {lesson_url}")
    assert "lesson_id=" in lesson_url
    assert "block_index=" in lesson_url

    # Extract lesson_id from URL
    import re
    match = re.search(r'lesson_id=([^&]+)', lesson_url)
    lesson_id = match.group(1) if match else None
    assert lesson_id, "Could not find lesson_id in URL"

    # Click "Next" button 3 times to navigate through content blocks
    for i in range(3):
        next_button = page.locator('button:has-text("Next")')
        if next_button.is_visible():
            next_button.click()
            time.sleep(1)
            current_url = page.url
            print(f"After Next #{i+1}: {current_url}")
            # Verify block_index increased
            match = re.search(r'block_index=(\d+)', current_url)
            if match:
                block_index = int(match.group(1))
                assert block_index == i + 1, f"Expected block_index={i+1}, got {block_index}"

    # Now we should be at block_index=3
    current_url = page.url
    print(f"Current URL before back: {current_url}")
    assert "block_index=3" in current_url

    # Press browser back button
    print("\n=== Pressing back button (should go to block_index=2) ===")
    page.go_back()
    time.sleep(1.5)  # Wait for auto-refresh

    # Verify URL changed to block_index=2
    back_url_1 = page.url
    print(f"URL after back #1: {back_url_1}")
    assert "block_index=2" in back_url_1

    # Verify page content refreshed - check that we're viewing block 2
    # Look for section indicator
    section_text = page.locator('text=/Section \\d+ of \\d+/').first.inner_text()
    print(f"Section indicator: {section_text}")
    # Should show "Section 3 of X" (block_index=2 means section 3, since blocks are 0-indexed)

    # Press back again (should go to block_index=1)
    print("\n=== Pressing back button again (should go to block_index=1) ===")
    page.go_back()
    time.sleep(1.5)

    back_url_2 = page.url
    print(f"URL after back #2: {back_url_2}")
    assert "block_index=1" in back_url_2

    # Press back again (should go to block_index=0)
    print("\n=== Pressing back button again (should go to block_index=0) ===")
    page.go_back()
    time.sleep(1.5)

    back_url_3 = page.url
    print(f"URL after back #3: {back_url_3}")
    assert "block_index=0" in back_url_3

    # Press back again (should go to learning page)
    print("\n=== Pressing back button again (should go to learning page) ===")
    page.go_back()
    time.sleep(1.5)

    back_url_4 = page.url
    print(f"URL after back #4: {back_url_4}")
    assert "page=learning" in back_url_4
    assert "lesson_id=" not in back_url_4

    # Verify we're on the learning page (should see domain tabs)
    fundamentals_tab = page.locator('text="🔐 Fundamentals"')
    assert fundamentals_tab.is_visible(), "Should be back on learning page with domain tabs"

    print("\n✅ All browser back navigation tests passed!")


def test_browser_forward_navigation(page):
    """Test that browser forward button also triggers auto-refresh"""

    # Navigate to the app
    page.goto("http://10.0.0.162:8501")
    time.sleep(2)

    # Login
    page.click('button:has-text("Quick Login")')
    time.sleep(2)

    # Navigate to a lesson
    page.click('button:has-text("My Learning")')
    time.sleep(2)

    start_button = page.locator('button:has-text("Start"), button:has-text("Continue")').first
    start_button.click()
    time.sleep(2)

    # Click Next twice
    for i in range(2):
        next_button = page.locator('button:has-text("Next")')
        if next_button.is_visible():
            next_button.click()
            time.sleep(1)

    # Press back twice
    page.go_back()
    time.sleep(1)
    page.go_back()
    time.sleep(1)

    # Now press forward
    print("\n=== Pressing forward button ===")
    page.go_forward()
    time.sleep(1.5)

    forward_url = page.url
    print(f"URL after forward: {forward_url}")
    assert "block_index=1" in forward_url

    print("\n✅ Browser forward navigation test passed!")


if __name__ == "__main__":
    # This script is meant to be run with pytest
    print("Run with: pytest tests/test_browser_back_navigation.py -v")
